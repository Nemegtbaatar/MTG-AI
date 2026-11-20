# Changelog

This file records what changed in the pilot and the tournament rules, and why. The pilot file is `pilot.md` from version 4.4 and was `pilot.txt` before that. The card-specific examples that used to sit in the pilot file are kept here.

## Version 7.0

Rules now live in one place, matches are computed from profiles, and the pilot uses its judgment wherever a setting was arbitrary.

- **One place for every rule.** Every rule about how a deck is played and scored is in `pilot.md`: the decklist rules (1.1), the turn 5 rule and the opponent (1.2), the baseline and match win (1.3), and the compute limits (1.5). `tournament.md` keeps only how the event is run, and its Settings table keeps only event logistics. The "[rules]" markers and the back-and-forth references are gone.
- **No adaptation to opponents.** Every deck optimizes against opponent A only. A match between two decks is computed from their baseline profiles (1.3), with no further games. Profiles now record losses by the deck's own actions on each turn, which the computation needs. Per-pairing mulligan bars, games per match, the draw band, match points, Swiss rounds and tiebreak settings are removed. Every deck is paired with every other (a round robin costs nothing), and standings are by average match win, with ties broken by match win against opponent A.
- **Compute limits apply to the baseline games only** (1.5): 50,000 lines per game after the keep on average, caches of 100,000 positions, and mulligan play-outs of at most 64 per kept hand, 160 per bottoming choice and 200 per game on average. Discovery, the budget check, calibration, bars, the check of mulligan decisions and audits are the pilot's judgment, with their cost reported. Bar games play the baseline's mulligan policy.
- **Removed fixed counts:** the minimum games per mulligan bar (300 and 150; the 0.02 standard error remains), the number of discovery games and of audited positions. Each is the pilot's judgment, with what has served noted.
- **Code reuse** (Part 3, step 3): the pilot writes the code for each run. Shared tools in the repository may be used (today only `tools/wincredit.py`); any other existing code, including code from earlier runs, only with the player's permission, asked first, and listed in the report.
- **Report format** (`instructions.md`): rebuilt to match what `pilot.md` says is reported. That means the list of choices on the card sheet, the budget check, discovery and win routes, the full mulligan method (bars, allocation, replacement model, decision check), the checks and fixes, play-outs and lines per baseline game against the limits, preparation compute, and code reused. The home-test settings table is gone, since every setting is now in `pilot.md`.
- **Player guidance:** removed advice that no longer holds. That covers asking for fewer baseline games to save time (the time is now in the mulligan preparation), asking for three example games (the report has ten), and treating a missing recipe as proof the pilot missed the deck's win.

Why: the settings in `tournament.md` and `instructions.md` had drifted from the pilot. Values were said to be "fixed in pilot.md" when `pilot.md` sent the reader back to `tournament.md`. Bar minimums predated 6.2. Nothing said which play-outs counted toward the cap. Per-pairing adaptation would have needed a full mulligan preparation for every match under 6.2 to 6.4. In the Cosmogoyf runs, the play-out cap, applied everywhere, forced approximations that the line limits did not.

## Version 6.4

- **Choices on the card sheet** (Part 3, step 1). The card sheet lists every choice each card's text gives the player ("may", including declining; "up to"; modes; X; targets; names; trigger order; which cards to keep, put back or exile) and says whether the engine searches it, settles it by a stated dominance argument, or fixes it as an approximation.
- **Principle 3:** choices inside an effect are candidates too, including declining an optional action.
- **Trigger windows** (Part 4): now generic. It no longer names Summoner's Pact, and it states that upkeep triggers resolve before the draw step.
- **Part 5, lessons from specific decks:** the lessons that name cards or decks (the four-color pump calibration, Summoner's Pact and Fling, Devourer of Destiny) moved into one part, so Parts 1 to 4 are generic and Part 5 can be removed without changing any rule.

Why: the Cosmogoyf test modeled Devourer of Destiny's "you may put one of those cards back on top" as always putting one back, so exiling all four was never considered. The card sheet listed which card was kept as a simplification, but not whether one was kept, so nothing flagged the missing choice. A bound on the baseline games put the cost under 0.1 point of match win. The same run's turn-by-turn review also found an engine resolving the Pact upkeep trigger after the draw step.

## Version 6.3

- **Trigger windows** (Part 3, default turn). Before a trigger that would lose the game resolves, the pilot checks for a win with instant-speed actions and the untapped mana; lines that cast Summoner's Pact on a turn that is not lethal stay candidates when the next turn can win in response to the payment trigger.

- **Report format** (`instructions.md`): win credit per copy added to item 7; a new item 10, ten example games with every mulligan step and every turn.

Why: the engines modeled each turn as a main phase and an end step, so a debt that could not be paid ended the game at once, and a win in the upkeep, with the trigger on the stack, was never searched. On the Resonance Draught list this matters only for extort drains from instants (combat and Sorin's loyalty abilities are sorcery speed), but for a deck with an instant-speed kill it turns Pact into a free tutor.

## Version 6.2

- **Mulligan calibration** (Part 3, step 7). When the play-out policy is cheaper than the full pilot, a sample of hands for each seat and size is played both ways on the same libraries, and the full pilot's value is fitted as a function of the cheap value. Kept-hand estimates are converted with the fit before they meet a threshold. Bars value the kept hand with the full pilot (one play-out per bar game is enough). The pilot may skip the calibration if it costs more than it can gain, and says so.
- **Settings:** lines per bar game and per measured game raised from 10,000 to 50,000 on average.

Why: on the four-color pump list, cheap play-outs undervalued weak hands more than strong ones (by 6 points for bad 7-card hands on the play, 0 for strong ones). Near the keep line of 6-card hands the gap exceeded the bar's, so the cheap policy mulliganed hands the full pilot keeps: 26 decisions against 1 in a sample of 1,500 hands. Mulligans made with full-pilot play-outs and twice the play-outs scored +1.04 ± 0.34 points of match win on 600 paired deals. On the Devoted Druid list, the lean version (calibration about 2.5 minutes, full-pilot bars under a minute more) ran in about 35 minutes in all. There a cheap play-out costs about 89 lines, so the 10,000-line limit forced a sampled, shortlisted lookahead (−0.6 ± 0.5 points against exact) and only 32 play-outs per bottoming choice (2.6 points lost per decision). Exact lookahead averaged about 20,000 lines per game, inside the new limit.

## Version 6.1

- **Mulligans rewritten** (Part 3, step 7). The pilot chooses and states the play-out policy, measuring its effect if it is not the full pilot. Play-outs keep bottomed and exiled cards known. Bars are honest values of the actual policy one size down, measured to a standard error of 0.02. Every distinct bottom is a candidate, compared on shared shuffled libraries by successive halving. The kept hand is valued with fresh play-outs and expected-loss stopping. A mulligan replacement's value is adjusted to the library left after the exile. Play-outs are allocated where they reduce expected loss most, measured before the bars, and a sample of decisions is checked against decisions from many play-outs.
- **Principle 6** no longer prescribes the play-out policy. The unnamed "cheap" policy description is removed; the choice is the pilot's (principle 2).
- **Settings:** play-outs per decision (64 to value a kept hand, 160 to choose a bottom), play-outs per game (200 on average), bars measured until their standard error is at most 0.02.

Why: in the from-scratch 6.0 test of the four-color pump list, bottoming among only the three "least useful" kinds of card lost 3.5 points per decision when keeping 6 and 11 when keeping 5. Trying every candidate on shared libraries cut that to under 1 point at a similar budget per game. Valuing a redraw after Serum Powder from the full deck understated it by 2.8 ± 0.8 points, and play-outs reshuffled bottomed cards into the library. The 6.0 build kept weaker hands and scored about 3 points below the 5.0 port, although its turn play was better.

## Version 6.0

A rewrite around principles, with 5.0 as the reference (`versions/pilot_5.0.md`; `CROSSWALK.md` maps every section).

- **Part 1, the fixed core:** only what must be the same for every deck: input, turn values, baseline and matches, legal play and information, compute fairness (line limits), reproducibility, logging and win credit, report and review.
- **Part 2, seven principles**, each carrying its most costly lesson in its wording: understand the deck first; exact where affordable, approximate where not, and measure the cost; every legal line is a candidate (shortlists from all candidates; turns happen in time); check against independent evidence; play well under uncertainty; be fast without unknowingly changing decisions; never tune to results.
- **Part 3, a default workflow** the pilot may adapt with a stated reason. **Part 4, method examples**, not rules.
- **Dropped as rules:** the full and basic pilot levels, the fixed sampled lookahead, the shortlist size and sample counts in Settings, and the fixed turn procedure (now an example).
- **Length:** about 2,850 words, under half of 5.0.

Why: 5.0's fixed sampled lookahead overrode its own principle and cost the four-color pump deck about a point on the play (paired, −0.95 ± 0.27), though that deck could easily afford the exact lookahead. The goal is a pilot governed by principles, not patched for each case, keeping the lessons that mattered in how the principles are written.

## Version 5.0

A rewrite, with version 4.12 as the reference (`versions/pilot_4.12.md`). `CROSSWALK.md` lists every 4.12 rule and where it went.

- **Structure.** Part A, fixed rules for every deck (objective, turn values, legal play and information, compute budget, seeds, logging, win credit). Part B, the workflow every deck follows. Part C, methods the pilot chooses among. Part D, checks, review and changes.
- **Deck analysis before the build** (section 10): how the deck wins, the kinds of turn, a checklist of risky interactions, the methods chosen, and the deck's tier and expected time. The wins found in discovery are compared with it afterwards.
- **Deck-specific judgment is central** (section 10) and covers a separate mana solver, grouped actions and a stated policy with simulation for turns that chain draws (sections 20 and 21). Its limits are unchanged: Part A stays as written, decisions come before the bars, each is listed with its reason, and no advice is taken.
- **Exact search becomes the default method** (section 18), not a requirement for every turn.
- **One budget check** (section 12) replaces the bar test and the measured-game test: taken right after the build, it settles the full or basic pilot before any deck reading, so nothing is redone. The lookahead is always the sampled shortlist; a deck over the measured-game limit is flagged.
- **A line also counts one action simulated by a policy** (section 5).
- **Win credit** may be sampled (seeded, still adding up exactly) on large boards, or split equally over the winning line for long chains; the report names the split (section 8). `tools/wincredit.py` implements provenance and credit for any deck.
- **Time targets:** about 30 minutes for a simple deck, two to three hours for the most complex; the report gives the time taken by each step.

Why: the goal is a pilot that, from this file alone, handles decks that chain dozens of spells, mana engines with tutors for several cards, and unusual lists like the Fortifying Draught deck, while staying fast for simple decks. 4.12 assumed one design, an exact engine checking every legal order each turn, throughout sections 4, 5, 10, 11 and 14; patching it again would have left contradictions every deck pays for in reading time.

Length: 5.0 is about 6,000 words, the same as 4.12, while covering the new methods and the deck analysis. The suggested 3,500 to 4,000 words was not reached without dropping rules.

## Version 4.12

- **The independent reference check is removed** (section 14). In its place, the pilot **audits 10 positions** drawn from the discovery games before the bars: 7 where the bound allows a win but none was found, and 3 found wins, checked step by step for legality. A confirmed miss or illegal line is fixed and a fresh set is audited. Simplifications in the win check are listed on the card sheet, each with a one-line reason.
- **Kept from 4.11:** the land drop is an action in the order (section 4), and the same-turn test position for each card that puts a card into hand (section 14).
- **Cache size** (section 10): each cache holds at most 100,000 positions [rules] and is cleared when full. Clearing never changes a decision, only the lines it costs.
- **Deck-specific judgment** (section 8): the pilot may change how a deck is searched and played where that makes sense for the deck (shortcuts, fixed orders, setup lines left out, tutor and discard rules, pruning, cache sizes). The objective, turn values, settings, game counts, seeds, logging and the legality of every play stay as written; changes are decided before the bars, listed on the card sheet with reasons, and taken without advice from the player.

Why: the goal is about 30 minutes from decklist to report. On the Providence list the reference took about 20 minutes to build and debug; the lines only it found were worth under half a point, inside the noise. The miss that mattered, Summoner's Pact for a Garden played that turn, was found by reasoning about one real hand, and the same-turn test position now covers it. Trade-offs accepted: shortcuts now rest on reasoning, and ten audits catch a line that matters in 7% of positions about half the time; deck-specific judgment means decks can be searched with different care.

## Version 4.11

- **The land drop is an action in the order** (section 4). It can come before or after any other action, and a card put into hand during the turn can be played or cast later that turn, including as the land drop.
- **The reference check is independent** (section 14). It is written separately from the win check, shares none of its move lists or ordering rules, and takes each action, the land drop included, from the hand as it stands at that moment.
- **Same-turn test positions** (section 14). Each card that puts a card into hand during a turn gets a test position whose only win uses that card the same turn.

Why: the Providence / Chancellor / Leyline / Sorin list's engine chose the land drop before casting any spell, so a Summoner's Pact could never fetch Disciple of Freyalise to be played as Garden of Freyalise that turn. Its reference check chose the land the same way and reported 0 disagreements in 900 positions. The hand Providence, Leyline of Resonance, Leyline of Hope, Summoner's Pact, Chancellor of the Forge, Fortifying Draught wins on turn 1 on the play every time with that line (Goblin for 26); the engine found no turn-1 win and no win at all in 55% of games. The 4.10 wording already required every legal order and every land drop; both programs read "every land drop" as the lands in hand at the start of the turn. These clarifications close that reading, and the independent reference is what would have caught it.

- **Effect on that list.** The independent reference found four more kinds of line the engine missed: a Garden paid for with life gained earlier in the turn, a Sorin cast while a Sorin planeswalker is out (the faces have different names, so both stay, and each spell is extorted twice), spells cast only to trigger extort (Serum Powder, a second Quicksilver), and the planeswalker's +2 Food eaten on the kill turn. With all of them fixed (600 random and 600 targeted positions, 0 disagreements), the list's match win rose from 24.0% to 28.2% (same 1,000 deals: +4.0 ± 1.0 points on the play, +2.7 ± 0.8 on the draw). Pact for a Garden was in 11% of the winning turns; the other lines were used a handful of times. The new lines took the bar test to 10,237 lines; two exact speedups (no more extorts than the mana left, Sorin always attacking on the kill check), with every decision reproduced on 48 bar games and 16 measured games, brought it to 9,507.

## Version 4.10

- **The line replaces the node** as the unit of compute (section 11): one full candidate turn checked, or one position expanded by a step-by-step search. Bounds count as one line; reused results cost nothing.
- **Bar test** (section 11), taken while the bars are measured: if the first 10 games of each bar's first pass average at most 10,000 lines per bar game over seats and hand sizes, the deck uses the full pilot (4.9's targets, every legal line, reference check). Otherwise it uses the basic pilot (4.7's rules: copies take the original's target, the card sheet's lines, test positions), and its deck reading and bars are redone.
- **Measured-game test** (section 11) replaces the 3× lookahead test: on 20 deals per seat, the deck uses the first lookahead option that averages at most 10,000 lines per game after the keep: every position exact, the shortlist of six exact, or the shortlist of six sampled. A deck over the limit even when sampled uses the sampled option and is flagged.
- **Sampled lookahead** (section 5, step 3): 8 sampled next draws, then 8 sampled draws for the turn after, counting kills only. Samples are seeded only from the position's numbers.
- **Reuse within a turn or a game** (section 10) is allowed when it can never change a decision, checked by reproducing a fixed sample of bar games and measured games exactly.
- `tournament.md` (Settings) and `instructions.md` (home defaults, order of work, report item 8) updated to match.

Why: the 4.8 and 4.9 improvements made some decks slow to simulate. Measured on this workspace's hardware (single core), the goals were about 0.5 s per bar game and 1 s per measured game.

- **Lines per bar game, each test game with empty caches:** four-color pump 541, infect 759, Devoted Druid 2,097, Cori-Steel Cutter 3,306, the Leyline of Hope Sorin list about 381,000 (3.1 s per bar game). The Sorin lists move to the basic pilot; the old Leyline of Resonance engine, built to 4.7, ran 0.30 s per bar game.
- **Cutter's measured games:** after the keep, the exact shortlist costs about 93,000 lines and every position about 258,000; the sampled lookahead about 5,100. Whole games, mulligans included, took 2.9 s, 7.5 s and 0.53 s.
- **Paired test on Cutter**, 1,000 deals against the exact shortlist (match win 10.6%):

| Measured-game lookahead | Seconds per game | Match win | Change |
|---|---|---|---|
| Sampled, 8 draws then 8 | 0.53 | 9.7% | −0.8 ± 0.5 |
| Sampled, 16 then 16 | 0.80 | 9.5% | −1.1 ± 0.5 |
| Sampled, 6 then 6 | 0.50 | 9.0% | −1.6 ± 0.5 |
| Second turn: certain wins only | 0.71 | 7.5% | −3.1 ± 0.5 |
| Progress score, sampled cantrips | 0.25 | 7.2% | −3.4 ± 0.6 |
| Progress score after 8 sampled draws | 0.32 | 7.6% | −3.0 ± 0.6 |

  Eight samples is the only option tested that is both under 1 s per game and within two standard errors of the exact lookahead. The options that drop the exact kill check on the turn after next lose about 3 points, because Cutter's setup lines mostly lead to a probable, not certain, kill two turns out.
- **Reuse within a turn** on Cutter's engine (each spell set's best casting order worked out once per turn, deck-plan scores and hand rankings remembered): bar games 0.22 → 0.12 s, measured games with the sampled lookahead 0.47 → 0.32 s, with every decision identical on a fixed sample of 48 bar games and 16 measured games.
- **Not adopted:** caching hand values (about 0.5% of mulligan hands repeat in 1,000 games); pruning play-out win checks to the 12 best affordable plans and counting only outs for tutors in play-outs (on the Hope list they cut bar games from 3.4 to 0.73 s with no loss in play-out value, but each needs a definition per engine and the list would still be over the bar limit); choosing the cards to bottom by rule, or capping close mulligan calls at 32 play-outs (untested).
- During this work, sampled games were briefly seeded with a hash that Python randomizes per process. The rule now requires seeds from the position's numbers only; repeat runs were confirmed identical.

## Version 4.9

- **Targets are choices** (section 4). Every legal target of every spell instance is searched, including each copy's new target. A target may be fixed by a rule only if the reference check shows the rule never misses a win.
- **Copy effects on the card sheet** (section 1): which spells are copied, whether a copy counts as cast, and whether it may choose new targets.
- **Exact shortcuts for targets** (section 10): identical creatures in a fixed order; added power to the creature with the largest multiplier, after enumerating every other effect; spell-counting triggers depend on the count only.
- **Setup lines** (section 5, step 3) choose a target for each spell instance.
- **Validation** (section 14): a split test for each copy effect or set of keyword-granting spells; a brute-force reference check on at least 500 random positions before any run; every win-check simplification listed and either passing the check or fixed.
- `instructions.md` (order of work, report items 6 and 8) updated to match.

Why: on a four-color Glistener Elf / Leyline of Resonance / Tainted Strike list, the pilot gave every Leyline copy to the creature that received the original spell. It missed kills that need copies on different creatures, such as one Tainted Strike giving infect to two Cacophony Scamps on turn 3. Searching every target raised match win from 87.2% to 87.8% (+0.6 ± 0.3, paired). A brute-force check would have caught the simplification before any games were run.

## Version 4.8

- **Lookahead test** (section 11). Before its baseline, each deck plays 20 deals per seat twice on the same seeds: once valuing a shortlist of six end-of-turn positions, once valuing every position. If every position costs at most 3 times the nodes of the shortlist, including mulligan play-outs, the deck values every position in its measured games. Mulligan play-outs and bars still use the cheap policy.
- **Every legal line is a candidate** (section 5, step 3). Setup turns include lines such as spending cards now for damage or not playing a land. A line may be left out only if the card sheet shows it can never help, with the reason stated.
- Section 11 no longer requires the same shortlist size for every deck; the test applies one rule to all.
- `instructions.md` (home defaults, run details) and `tournament.md` (Settings) updated to match.

Why: on a Glistener Elf / Leyline of Resonance list, valuing every setup line, including pump spells cast early and a land held for landfall, raised match win against opponent A from 82.0% to 83.8% (+1.8 ± 0.4 on 1,000 paired deals). Measured cost: the infect list 1.8 times the nodes, Devoted Druid 1.4 times. The Shoal / Spoils of the Vault list measured 1.0 times, but its pilot offered no Fortifying Draught, Shoal or Pact lines on setup turns, so that figure understates the cost of a complete set of lines.

## Version 4.7

- **Fewer games for most mulligan bars** (section 9). The 7-card bar keeps 300 games per seat; the 4-, 5- and 6-card bars use 150. This trades steadiness for time: a 150-game bar has a chance error of about ±0.037 against ±0.026 at 300, still smaller than the ±0.06 one win moves a 16-playout hand estimate. The 7-card bar keeps 300 because it decides the most common choice, whether to keep the first hand.
- Tested on the Swiftspear / Leyline of Resonance list: bar measurement fell from about 10 to 7 minutes.
- `instructions.md` (home defaults) and `tournament.md` (Settings) updated to match.

## Version 4.6

- **Random actions have no fixed thresholds** (section 7). An action that can win now but can also lose the game is cast when P(win now) × the value of a win this turn exceeds (P(win now) + P(lose)) × the value of not casting. The bar moves with the opponent and the turn.
- **Win credit is weighted by turn value against the opponent** (section 15), so credits add up to the score against opponent A or the real opponent. It is published as two tables: by card, and passed back to sources.
- **Logging** (section 13): a hand dealt after a mulligan-replacement effect is its own source, and earlier damage is logged per attacking card.
- `instructions.md`: win credit against opponent A is now part of the report, and measured games must log card identities.

Why: in a test of a Spoils of the Vault deck, the main-phase rule used fixed cut-offs (at least 15% to win, at most 5% to die). Against opponent A the right cut-off depends on the turn and on what holding is worth. The first win-credit analysis could not pass credit to Spoils of the Vault or Serum Powder because the logs had no card identities.

## Version 4.5

- Split the event rules out of `pilot.md` into a new `tournament.md`. `pilot.md` now covers only how one deck is played.
- Moved to `tournament.md`: decklist submission and private lists, the turn 5 rule, how games and matches are decided, the tournament structure and the review procedure.
- `pilot.md` keeps what the pilot needs for its decisions: turn values, baseline profiles, match values and the number of turns available. Its section numbers are unchanged.
- Added to `tournament.md`: deck legality, the do-nothing opponent, the handling of cards the pilot cannot model, the schedule, and a Settings table that holds every value marked [rules].
- Added `README.md` and `rulings.md`.
- This file is now Markdown, `CHANGELOG.md`.

## Version 4.4

- The pilot file is now Markdown, `pilot.md`, to match `instructions.md`. The wording and section numbers are unchanged.
- Added parallel runs to section 11: where work may be split, the order that must be kept, and the seeding, cache and node-count rules that make results the same on any number of workers.
- Added a check that a sample of games gives identical logs with different numbers of workers (section 11).

## Version 4.3

The turn 5 rule:

- Added a tournament rule: the deck on the play loses at the end of its turn 5 if it has not won. It keeps games short and limits compute.
- The turn limit is no longer a setting. It is 5 turns on the play and 4 on the draw.
- No game is drawn. The deck on the draw wins any game the deck on the play does not win in time.
- A game without a win now has a value: on the draw, the chance that the opponent does not win by its turn 5 (section 2).
- A loss by the deck's own actions is worth nothing, which on the draw is now worse than not winning (section 6).
- The baseline profile records games not won and games lost by the deck's own actions separately (section 3).

## Version 4.2

Opponent A:

- Added opponent A, a generic opponent that wins on turn 2 in 25% of games, turn 3 in 50% and turn 4 in 25%. Its turn values replace the old example table (section 2).
- A deck's baseline profile is now its win distribution by turn with its mulligans optimized against opponent A. It is the only information an opponent gets (sections 2 and 3).
- In a match, every decision uses the pairing values, not only mulligans. Opponent A's values end at turn 4 and cannot guide play against a slower deck (section 2).
- Games are played to the last available turn even when the remaining turns are worth nothing, so that slow decks have complete profiles (section 2).

Decklist only:

- Added how decklists are submitted on Reddit, and that the pilot gets card names and counts only.
- Removed the missing-piece list and the submitter's note. The pilot now reads the deck itself: roles from card text, discovery games, win recipes and a deck plan (section 8).
- The pilot writes the card sheet itself (section 1).
- The keep-value rule and the land minimum now come from the deck plan (sections 8 and 9).
- Reading the deck has the same compute budget for every deck (section 11).
- Review covers card models and rules errors only. Strategy is not open to challenge (section 14).
- Private lists: card sheet, deck plan and logs are published when the list is.

## Version 4.1 (public edition)

Rewritten for tournament use:

- Removed the approval notes and the kept / changed / new tags.
- Moved every reference to a specific card into this file. The pilot file now describes effects by what they do.
- Renumbered the sections from 1. The old section 0 is now section 1.

New rules:

- Mulligans are decided against the specific opponent, using pairing values built from the opponent's baseline profile (sections 2, 3 and 9).
- Added how a match is played and decided (section 3).
- Added the tournament structure: full round robin with fewer than 8 decks, Swiss pairings with 8 or more (section 3).
- Added a proposed compute budget counted in nodes (section 11).
- Added the review window and the rule for changing the file (sections 14 and 16).
- The cheap policy may not use turn values, so play-outs can be re-scored for each opponent (sections 9 and 10).

## Version 4.0

Each entry gives the rule, then the error that led to it.

### Card sheet (section 1)

- Rule: fetch official card text and check each card's own legality.
- Most errors in the project came from card text modeled from memory:
  - Elvish Spirit Guide was treated as legal. It is not banned, but it was never printed in a Modern-legal set.
  - Spoils of the Vault was modeled with a shuffle it does not have.
  - Serum Powder's exile was not treated as lasting for the game.
- "First upkeep" can be the opponent's upkeep.

### Turn decision procedure (section 5)

- Rule: the shortlist always includes a line that leaves instant-speed mana open, and a line is valued with its options.
- The cheap progress score ranked "tap out" lines first. The pilot never kept {B} open for Spoils of the Vault or {U} open for Otherworldly Gaze, even when that was the better line.

### Losing and risk (section 6)

- Rule: use every known card, and compare a risky action with every alternative that uses the same resources.
- Spoils of the Vault exiled a Goryo's Vengeance that Devourer of Destiny had just placed on top.
- Its death risk ignored the two cards known to be on the bottom.
- It was chosen over a free Otherworldly Gaze costing the same mana.

### Random actions inside a turn (section 7)

- Rule: resolve for real, then re-plan, and decide by counting outs.
- Sampling Faithless Looting's draws inside the lookahead cost most of a 90-minute run and still chose discards blind. Resolving for real made the same decisions better, in milliseconds.

### Missing-piece model (section 8; replaced by "Reading the deck" in 4.2)

- Example list for a reanimation deck: a lethal target in the graveyard, the reanimation spell, a big card in exile, and two mana including black.
- The pre-game choice the model first covered was Gemstone Caverns' exile.

### Mulligans (section 9)

- Rule: when bottoming, keep lands up to the deck's minimum.
- When every candidate scored 0, the tie went to bottoming a second land, which left a one-land 5-card hand.
- The mulligan-replacement effect the rule was written for is Serum Powder.

### Efficiency (section 10)

What changed in the Ulamog pilot:

| Measure | Before | After |
|---|---|---|
| Looting decision | 4 sampled reveals × lookahead | Outs counting, about 8 ms |
| Cheap pilot on 12 fixed positions | 486 ms | 48 ms |
| Hands holding Spoils of the Vault | 101–336 ms | 3–27 ms |
| 2,000-game run | About 90 min | About 9 min |

### Logging and seeds (section 12)

- Rule: log the opening hand and every mulligan decision.
- Without opening-hand logs, it was not possible to tell whether Chancellor of the Dross was needed in a win. It was claimed not to be when it was.

### Logging for win credit (section 13)

- The first credit analysis had to guess how Ulamog reached the graveyard and what exiled the Emrakul, for 14–21% of wins. With traces, every win rebuilt and nothing was guessed.
- Cards behind the general wording in this section:
  - **Instance ids:** for example Goryo's Vengeance #3.
  - **Tokens:** Chancellor of the Forge's Goblin, a Construct, a Food.
  - **Reaching the hand:** a cycler, a loot, Spoils of the Vault, Labyrinth's return.
  - **Top or bottom:** Devourer of Destiny, surveil.
  - **Graveyard:** loot, Cookbook, surveil, cycling.
  - **Exile:** Serum Powder, Gemstone Caverns, Devourer of Destiny, Spoils of the Vault, a Labyrinth imprint, flashback, delve. Returns from exile: Pull from Eternity, Labyrinth.
  - **Battlefield from the opening hand:** Leylines, Quicksilver.
  - **Battlefield by another card:** Stoneforge, a reanimation spell.
  - **Attachments:** an equip cost, Sigarda's Aid, Puresteel Paladin.
  - **Life gained this turn:** Fortifying Draught scales with it.
