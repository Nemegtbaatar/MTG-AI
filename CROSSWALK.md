# Crosswalk: pilot.md 5.0 to 6.0

6.0 keeps a short fixed core of rules and turns the rest into principles, a default workflow and examples. Each 5.0 section, and where it went. Earlier crosswalks are in `versions/`.

| 5.0 | 6.0 | Status |
|---|---|---|
| Intro principles | Intro; principles 2 and 7 | Kept; "exact where affordable" now governs every method, not just the win check |
| 1 What the pilot receives | 1.1 | Kept |
| 2 Objective and turn values | 1.2 | Kept |
| 3 Baseline and match values | 1.3 | Kept |
| 4 Legal play and information | 1.4; principles 3 and 5 | Rules kept in the core (legality, no peeking); land drop timing, targets and losing moved to principles |
| 5 Compute budget | 1.5 | Kept: lines, same limits, flags, limits set once. Dropped: "full or basic pilot" as fixed levels; a deck fits the limits by its own measured approximations (principle 2) |
| 6 Seeds and parallel runs | 1.6 | Kept, condensed |
| 7 Logging | 1.7 | Kept, condensed |
| 8 Win credit and analyses | 1.7 | Kept |
| 9 Card sheet | Part 3, step 1 | Kept |
| 10 Deck analysis and deck-specific judgment | Principle 1; Part 3, step 2 | Kept; judgment is now how the whole file works, so its separate limits became principle 7 and the core |
| 11 Build and test positions | Principle 4; Part 3, step 3 | Kept (same-turn test kept as a lesson) |
| 12 Budget check | Part 3, step 4; principle 2 | Changed: it measures the exact methods first and uses them if they fit; the sampled lookahead is no longer imposed (it cost the pump deck about a point) |
| 13 Reading the deck | Part 3, step 5 | Kept, condensed |
| 14 Audit | Principle 4; Part 3, step 6 | Kept |
| 15 Mulligans | Part 3, step 7; settings | Kept; "three bottom candidates" became "the few least useful kinds" |
| 16 Baseline, checks, report | Part 3, steps 8 to 10; 1.8 | Kept |
| 17 Turn decision procedure | Part 4 (a default turn) | Changed from rule to example; shortlist-from-all-candidates kept as principle 3 |
| 18 Exact search | Part 4 (shortcuts); principle 6 | Changed to examples; the fixed-payment color-conflict test is covered by "a test position for each interaction" |
| 19 Random actions | Principle 5 | Kept as principle, including the risk formula |
| 20 Turns that chain draws | Principle 5; Part 4 | Kept as principle and example |
| 21 Mana engines and repeated actions | Part 4 | Example |
| 22 Cheap policy and speed | Principle 6 | Kept as principle |
| 23 Methods by kind of deck | Part 4 table | Kept; pump decks now list the exact lookahead |
| 24 Checks | Principle 4; Part 3, step 9 | Kept |
| 25 Review | 1.8 | Kept |
| 26 Changes | 1.8 | Kept |
| Settings: lookahead counts, shortlist size, simulations per policy decision | Removed from Settings | Methods, not fairness; compute fairness is kept by the line limits |

## 6.0 to 6.1

| 6.0 | 6.1 | Status |
|---|---|---|
| Principle 6: "the policy that plays them stays cheap: a win check, then the best progress, with no nested evaluation" | Principle 6; Part 3, step 7 | Changed: the pilot chooses the play-out policy and measures its cost |
| Part 3, step 7: play-outs, bars, three least useful kinds as bottom candidates, land minimum, mulligan replacements | Part 3, step 7 | Rewritten: honest bars, every bottom on shared libraries, fresh play-outs with expected-loss stopping, replacement value adjusted to the library, measured allocation, decision check; the land minimum is dropped |
| Settings: mulligan play-outs 16 to 64 per hand | Settings | Replaced by limits per decision and per game |

## 6.1 to 6.2

| 6.1 | 6.2 | Status |
|---|---|---|
| Part 3, step 7, Value | Part 3, step 7, Value | Added: hand values and bars are compared in full-pilot units |
| (none) | Part 3, step 7, Calibration | New: cheap values are converted to full-pilot units with a fit measured before the bars; may be skipped with a stated reason |
| Part 3, step 7, Bars | Part 3, step 7, Bars | Changed: the kept hand is valued by the full pilot (one play-out per bar game is enough) |
| Part 3, step 7, Check | Part 3, step 7, Check | Added: the calibration sample measures the play-out policy's effect on keeps |
| Settings: 10,000 lines per bar game and per measured game | Settings | Raised to 50,000 |

## 6.2 to 6.3

| 6.2 | 6.3 | Status |
|---|---|---|
| (none) | Part 3, Trigger windows | New: check for an instant-speed win before a losing trigger resolves; Pact on a non-lethal turn stays a candidate |

## 6.3 to 6.4

| 6.3 | 6.4 | Status |
|---|---|---|
| Part 3, step 1, Card sheet | Part 3, step 1 | Added: list every choice in the card texts and how each is handled |
| Principle 3 | Principle 3 | Added: choices inside an effect, including declining an optional one, are candidates |
| Part 3, step 7, Calibration lesson (four-color pump list) | Part 5 | Moved |
| Part 4, Trigger windows (named Summoner's Pact) | Part 4, Trigger windows; Part 5 | Made generic; adds that upkeep triggers resolve before the draw step; the Pact example moved to Part 5 |
| (none) | Part 5, lessons from specific decks | New: every lesson that names a card or deck, removable as a block |

## 6.4 to 7.0

| 6.4 | 7.0 | Status |
|---|---|---|
| tournament.md, What is legal | pilot.md 1.1 | Moved |
| tournament.md, The opponent; The turn 5 rule | pilot.md 1.2 | Moved |
| pilot.md 1.2, pairing values in a match | (none) | Removed: every deck optimizes against opponent A only |
| pilot.md 1.3, pairing values and per-match bars; same deal in every match | pilot.md 1.3, Baseline profile and match win | Replaced: 1,000 baseline games; profile includes own-action losses by turn; game win and match win computed from two profiles |
| tournament.md, How a match is played; Match result; Tournament structure | tournament.md, Matches and standings | Replaced: round robin computed from profiles; standings by average match win |
| tournament.md Settings: discovery games, baseline games, bar games, play-outs, lines, caches, audits, games per match, draw band, match points, Swiss rounds, tiebreaks, compute limits | pilot.md 1.3 and 1.5, or the pilot's judgment | Moved or removed |
| pilot.md 1.5, limits [rules], set after submissions close | pilot.md 1.5 | Fixed values, for baseline games only; everything else is judgment |
| pilot.md principle 4, audit count [rules] | principle 4 | The pilot's judgment (ten has served) |
| pilot.md Part 3, step 3, shared tools | Part 3, step 3 | Added: other code only with the player's permission, listed in the report |
| pilot.md Part 3, step 5, discovery games [rules] | Part 3, step 5 | The pilot's judgment (two rounds of 200 have served) |
| pilot.md Part 3, step 7, results reused against other opponents | (none) | Removed |
| instructions.md, Settings for a home test | (none) | Removed: settings are in pilot.md |
| instructions.md, Ground rules | instructions.md, Home-test rules | Duplicates of pilot.md replaced by references |
| instructions.md, Report format (10 items) | Report format (12 items) | Rebuilt to match pilot.md |
| instructions.md, Match win | pilot.md 1.3 | Moved |
