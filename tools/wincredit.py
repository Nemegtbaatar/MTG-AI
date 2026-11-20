"""wincredit.py: reusable provenance logging and win credit (pilot.md section 15) for any deck.

The engine keeps a Ledger during each logged game and calls it as it applies its chosen lines. At the winning moment it
hands the Ledger's snapshot and a win function to Credit, which splits the win among the pieces on the board and passes
each share back to whatever put that piece there. Nothing here knows any card's rules.

What stays deck-specific (a few lines per action, and one function):
  1. calling the Ledger as actions happen (a card moves, a tutor finds a card, a token is made, damage or life is gained);
  2. win_fn(counts) -> bool: does the winning position, cut down to these piece counts, still win this turn?

---------------------------------------------------------------- the Ledger
    L = Ledger()
    L.deal(hand_names, library_names, origin='opening hand')   # origin: 'opening hand', 'Serum Powder redeal', ...
    i = L.draw()                                  # top card to hand, origin 'draw step' (or L.draw(origin=...))
    L.move(i, 'battlefield')                      # any zone name; the card keeps its origin
    j = L.fetch("Disciple of Freyalise", by=pact_id, to='hand')    # a tutor: origin is the tutor card
    t = L.token('Goblin token', by=forge_id)      # tokens are credited to the card that made them
    L.resource('damage', 3, by=dross_id)          # running totals: damage, life gain, poison, mana, ...
    L.pick('hand', 'Fortifying Draught')          # the id of a card of that name in that zone (oldest first)
    L.rename(i, 'Garden of Freyalise')            # a back face or transformed side: its own player key, credit to its card
    tr = L.trace(players)                         # a small picklable Trace (card and source per piece) for the log

Every piece is a player key (zone, name), e.g. ('hand', 'Fortifying Draught') or ('battlefield', 'Goblin token').
Running totals are players too, e.g. ('earlier', 'damage'), split among their contributors in proportion.

---------------------------------------------------------------- Credit
    C = Credit(values)                            # values[seat][turn] = turn value against the opponent
    players = L.snapshot(['hand', 'battlefield'], resources=['damage'])
    C.add_win(seat, turn, players, win_fn, ledger=L)    # Shapley split: exact, or sampled when large
    C.add_win_line(seat, turn, used_ids, ledger=L)      # cheaper: equal split among the cards used in the winning line
    C.add_game(seat)                              # count every game, won or not
    C.report()                                    # by card and by source, with the check that credits add up to the score

Shapley values are exact when the number of piece subsets is at most EXACT_LIMIT; otherwise they are sampled over
SAMPLES random orders, seeded from integers. Either way each win's shares add up to exactly 1, so credits always add up
to the score. A win whose full board does not win, or an empty board that wins, is reported as a problem.
"""
import itertools, math, random, zlib
from collections import defaultdict

EXACT_LIMIT = 4096
SAMPLES = 400


def _fdict(): return defaultdict(float)


class Trace:
    """what Credit needs from a game, small enough to save in its log: each piece's card and source"""
    def __init__(self, card, source): self.card = card; self.source = source
    def card_of(self, i): return self.card.get(i, i)
    def source_of(self, i): return self.source.get(i, 'untraced')


class Ledger:
    def __init__(self):
        self.name = {}       # id -> card or token name
        self.origin = {}     # id -> a label ('opening hand', 'draw step', ...) or the id of the card that caused it
        self.zone = {}       # id -> zone
        self.order = defaultdict(list)   # zone -> ids, oldest first
        self.library = []    # ids, top first
        self.res = defaultdict(_fdict)   # resource -> id -> amount
        self.face = {}       # id -> the name it currently goes by (a transformed or back face), if not its card name
        self.events = []
        self.tokens = set()
        self._n = 0

    # ---- making and moving pieces
    def _new(self, name, zone, origin):
        self._n += 1
        i = '%s#%d' % (name, self._n)
        self.name[i] = name; self.origin[i] = origin; self._put(i, zone)
        return i

    def _put(self, i, zone):
        old = self.zone.get(i)
        if old is not None and i in self.order[old]: self.order[old].remove(i)
        self.zone[i] = zone; self.order[zone].append(i)

    def deal(self, hand_names, library_names, origin='opening hand'):
        """a fresh deal: earlier ids are forgotten (a mulligan's redeal starts again with its own origin label)"""
        self.__init__()
        ids = [self._new(n, 'hand', origin) for n in hand_names]
        for n in library_names:
            i = self._new(n, 'library', None); self.order['library'].remove(i); self.library.append(i)
        return ids

    def bottom(self, i):
        """a card put from hand on the bottom of the library (London mulligan)"""
        self.order[self.zone[i]].remove(i); self.zone[i] = 'library'; self.origin[i] = None; self.library.append(i)

    def draw(self, origin='draw step', to='hand'):
        i = self.library.pop(0)
        self.origin[i] = origin; self.zone[i] = to; self.order[to].append(i)
        self.events.append(('draw', i, origin))
        return i

    def fetch(self, name, by, to='hand'):
        """a tutor or effect takes a card of this name from the library; the card's origin becomes `by`"""
        i = next((x for x in self.library if self.name[x] == name), None)
        if i is None: raise ValueError('no %s in library' % name)
        self.library.remove(i); self.origin[i] = by; self.zone[i] = to; self.order[to].append(i)
        self.events.append(('fetch', i, by))
        return i

    def move(self, i, zone, by=None):
        """move a piece; `by` (optional) is recorded as the cause of the move but does not change its origin"""
        self._put(i, zone); self.events.append(('move', i, zone, by))

    def token(self, name, by, zone='battlefield'):
        i = self._new(name, zone, by); self.tokens.add(i); self.events.append(('token', i, by))
        return i

    def resource(self, kind, amount, by):
        if amount: self.res[kind][by] += amount; self.events.append(('resource', kind, amount, by))

    def pick(self, zone, name):
        """the oldest id of this name (or current face) in the zone"""
        for i in self.order[zone]:
            if self.face.get(i, self.name[i]) == name: return i
        raise ValueError('no %s in %s' % (name, zone))

    def rename(self, i, face):
        """the piece now goes by another name (transformed, or a land played from a double-faced card); credit still goes
        to its card"""
        self.face[i] = face; self.events.append(('rename', i, face))

    def reorder_library(self, names):
        """the library was shuffled or reordered: match ids to the new order of names"""
        pool = defaultdict(list)
        for i in self.library: pool[self.name[i]].append(i)
        self.library = [pool[n].pop(0) for n in names]

    # ---- tracing
    def card_of(self, i):
        """the card behind a piece: itself, or for a token the card that made it"""
        seen = set()
        while i in self.tokens and i not in seen:
            seen.add(i); o = self.origin[i]
            if o in self.name: i = o
            else: break
        return self.name.get(i, i)

    def source_of(self, i):
        """what put the piece where it is: an origin label, or the name of the card that caused it"""
        o = self.origin.get(i)
        if o is None: return 'untraced'
        return self.name[o] if o in self.name else o

    def snapshot(self, zones, resources=(), resource_label='earlier'):
        """players at the winning moment: (zone, name) -> ids, and (label, kind) -> {id: amount}"""
        out = {}
        for z in zones:
            for i in self.order[z]: out.setdefault((z, self.face.get(i, self.name[i])), []).append(i)
        for k in resources:
            if any(self.res[k].values()): out[(resource_label, k)] = dict(self.res[k])
        return out

    def trace(self, players):
        """a Trace for the pieces in a snapshot, to save with the game's log"""
        ids = set()
        for x in players.values(): ids.update(x.keys() if isinstance(x, dict) else x)
        return Trace({i: self.card_of(i) for i in ids}, {i: self.source_of(i) for i in ids})

    def check(self, players, expected):
        """compare the ledger with the engine's own counts {(zone, name): n}; returns the mismatches (untraced pieces)"""
        bad = []
        for k, n in expected.items():
            got = len(players.get(k, [])) if not isinstance(players.get(k), dict) else 1
            if got != n: bad.append('%s %s: ledger %d, engine %d' % (k[0], k[1], got, n))
        return bad


def shapley(players, win_fn, seed=0):
    """Shapley value of each player type for a win (value 1). players: {key: count}. win_fn(counts dict) -> bool.
    Exact over all sub-multisets when small, otherwise sampled over random orders. Returns ({key: value}, method)."""
    keys = [k for k, n in players.items() if n]
    n = [players[k] for k in keys]
    memo = {}
    def v(c):
        c = tuple(c)
        if c not in memo: memo[c] = 1 if win_fn(dict(zip(keys, c))) else 0
        return memo[c]
    if v(n) != 1: raise ValueError('the full board does not win')
    if v([0] * len(n)) != 0: raise ValueError('the empty board wins')
    N = sum(n); phi = defaultdict(float)
    if math.prod(x + 1 for x in n) <= EXACT_LIMIT:
        fN = math.factorial(N)
        for combo in itertools.product(*[range(x + 1) for x in n]):
            s = sum(combo)
            if s == N: continue
            w = math.factorial(s) * math.factorial(N - s - 1) / fN
            base = v(combo)
            for p in range(len(n)):
                if combo[p] < n[p]:
                    up = list(combo); up[p] += 1; d = v(up) - base
                    if not d: continue
                    mult = 1
                    for q in range(len(n)): mult *= math.comb(n[q] - (1 if q == p else 0), combo[q])
                    phi[keys[p]] += w * mult * d * n[p]
        return dict(phi), 'exact'
    rng = random.Random(seed)
    seq = [p for p in range(len(n)) for _ in range(n[p])]
    for _ in range(SAMPLES):
        rng.shuffle(seq); c = [0] * len(n); prev = 0
        for p in seq:
            c[p] += 1; cur = v(c)
            if cur != prev: phi[keys[p]] += (cur - prev) / SAMPLES
            prev = cur
    return dict(phi), 'sampled'


class Credit:
    def __init__(self, values):
        self.values = values
        self.by_card = defaultdict(lambda: defaultdict(float)); self.by_source = defaultdict(lambda: defaultdict(float))
        self.total = defaultdict(float); self.games = defaultdict(int); self.problems = []; self.methods = defaultdict(int)

    def add_game(self, seat): self.games[seat] += 1

    def _give(self, seat, share, ids, ledger, source_label=None):
        if isinstance(ids, dict):                        # a running total: split in proportion to the amounts
            tot = sum(ids.values())
            for i, a in ids.items():
                self.by_card[seat][ledger.card_of(i)] += share * a / tot
                self.by_source[seat][source_label or ledger.source_of(i)] += share * a / tot
            return
        for i in ids:
            self.by_card[seat][ledger.card_of(i)] += share / len(ids)
            self.by_source[seat][source_label or ledger.source_of(i)] += share / len(ids)

    def add_win(self, seat, turn, players, win_fn, ledger, source_labels=None, game=None):
        """players: {key: list of ids, or {id: amount} for a running total}; win_fn takes {key: count}"""
        wt = self.values[seat][turn]; self.total[seat] += wt
        counts = {k: (1 if isinstance(x, dict) else len(x)) for k, x in players.items()}
        try:
            phi, method = shapley(counts, win_fn, seed=zlib.crc32(('%s:%s' % (seat, game)).encode()))   # integers only
        except ValueError as e:
            self.problems.append((seat, game, str(e))); self.by_source[seat]['untraced'] += wt; self.by_card[seat]['(untraced)'] += wt
            return
        self.methods[method] += 1
        for k, share in phi.items():
            self._give(seat, share * wt, players[k], ledger, (source_labels or {}).get(k))

    def add_win_line(self, seat, turn, used_ids, ledger, game=None):
        """cheaper credit: an equal split among the pieces used in the winning line (no win function needed)"""
        wt = self.values[seat][turn]; self.total[seat] += wt
        if not used_ids:
            self.problems.append((seat, game, 'no pieces logged')); self.by_source[seat]['untraced'] += wt; return
        self.methods['line'] += 1
        self._give(seat, wt, list(used_ids), ledger)

    def check(self):
        """credits add up to the score in each seat"""
        out = {}
        for seat in self.games:
            got = sum(self.by_card[seat].values()); out[seat] = (got / max(1, self.games[seat]), self.total[seat] / max(1, self.games[seat]))
        return out

    def report(self, title='Win credit', file=None):
        lines = []
        seats = sorted(self.games)
        for name, table in (('by card', self.by_card), ('by source', self.by_source)):
            keys = sorted({k for s in table for k in table[s]}, key=lambda k: -sum(table[s].get(k, 0) for s in table))
            lines.append('%s %s (points of game win)' % (title, name))
            lines.append('%-40s' % '' + ''.join('%12s' % s for s in seats))
            for k in keys:
                lines.append('%-40s' % str(k)[:40] + ''.join('%12.2f' % (100 * table[s].get(k, 0) / max(1, self.games[s])) for s in seats))
        for s, (got, score) in self.check().items():
            lines.append('check %s: credits %.4f = score %.4f' % (s, got, score))
        lines.append('methods %s; problems %d' % (dict(self.methods), len(self.problems)))
        text = '\n'.join(lines)
        print(text, file=file)
        return text
