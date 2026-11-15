# Pilot: how every deck is played in the tournament

Version 4.5

This file explains how the AI pilot plays a submitted Modern deck. Every deck is played by the same procedure. The pilot receives the decklist and nothing else, and works out by itself how the deck wins (section 8).

The pilot plays each deck alone: the opponent has no blockers, no responses and no disruption, and the opponent's cards never matter. A match compares how fast two decks win.

The pilot is written to be accurate first and fast second.

This file covers how one deck is played. How decks are submitted, how two decks' results become a match, and how the event is run are in `tournament.md`.

Values marked [rules] are set in the Settings table of `tournament.md`. Card-specific examples and the history behind each rule are in `CHANGELOG.md`.

## What the pilot receives

- The pilot is given a decklist: card names and counts. It is given nothing else about the deck.
- How decklists are submitted, and how private lists are handled, is in `tournament.md`.

## 1. Card sheet before any code

- Every card's official text is fetched from Scryfall before the card is modeled. No card is modeled from memory.
- Each card's own Modern legality is checked, not only the ban list. A card can be illegal without being banned, because it was never printed in a Modern-legal set.
- For every clause of every card, the sheet says how the clause is modeled or why it is ignored. Four things get particular attention:
  - **Timing:** whose upkeep a trigger uses, opening-hand effects, and instant-speed windows.
  - **What moves where:** exile, graveyard or library, and whether the library is shuffled.
  - **Conditions:** the legendary rule, "if you are not the starting player", metalcraft, life payments.
  - **Interactions:** copies, responses to triggers, and cards that replace themselves.
- The pilot writes the card sheet itself, from the card text alone. A clause it cannot model is listed as unmodeled, with the reason.
- Card sheets are published and open to review (section 14).

## 2. Objective and turn values

The pilot's objective is a table of turn values: what a win on each turn is worth, on the play and on the draw. A win is worth the chance that the opponent has not already won:

- On the play, a win on turn t is worth the chance that the opponent does not win before its own turn t.
- On the draw, a win on turn t is worth the chance that the opponent does not win by its own turn t.

### Opponent A

Opponent A is a generic opponent, the same for every deck. It wins on turn 2 in 25% of games, on turn 3 in 50% and on turn 4 in 25%. That gives these values:

| Win on turn | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| On the play | 1.00 | 1.00 | 0.75 | 0.25 | 0.00 |
| On the draw | 1.00 | 0.75 | 0.25 | 0.00 | none |

The deck on the draw has no turn 5 (the turn 5 rule, `tournament.md`).

### Pairing values

In a match, the table is built the same way from the real opponent's baseline profile (section 3). That profile is the only information a deck has about its opponent.

### Where each table is used

- The baseline run uses opponent A's values for every decision.
- A match uses the pairing values for every decision, mulligans included. Opponent A's values end at turn 4, so they cannot guide play against a slower opponent.
- Within a run, the same table is used in every evaluation: mulligans, lookahead, risk and the analyses.

### Games without a win

Under the turn 5 rule (`tournament.md`), a game the deck does not win can still be won:

- On the draw, it is worth the chance that the opponent does not win by its turn 5.
- On the play, it is worth only the chance that the opponent loses by its own actions first.
- Against opponent A it is worth nothing in either seat, because opponent A always wins by turn 4.
- A game the deck loses by its own actions is worth nothing in either seat.

### Late turns

Every game is played until the deck wins or runs out of turns (5 on the play, 4 on the draw), even when the remaining turns are worth nothing. Among lines of equal value, the pilot takes the earliest win. This keeps each baseline profile complete for decks slower than opponent A.

## 3. Baseline profile and match values

### Baseline profile

Before the tournament, every deck plays the same number of solo games [rules], half on the play and half on the draw, with its mulligans and play optimized against opponent A. The deck's baseline profile is the share of games won on each turn, the share not won, and the share lost by its own actions, on the play and on the draw. It is published, measured once, and fixed for the whole event.

### Match values

For a match between X and Y, X's pairing values are built from Y's baseline profile, and Y's from X's. Each deck then measures its mulligan bars against its pairing values. This is done once. Neither deck sees how the other adjusts to it.

### Turns available

Under the turn 5 rule in `tournament.md`, the deck on the play loses at the end of its turn 5 if it has not won. The pilot therefore plays 5 turns on the play and 4 on the draw.

### Deals

A deck's deal in game number n is the same in every match it plays. Differences between a deck's matches therefore come only from its own decisions and from the opponent.

How games and matches are decided, and how the tournament is structured, is in `tournament.md`.

## 4. Rules engine and exact win check

- Each turn, before doing anything else, the pilot searches every legal order of main-phase actions with an exact, cached win check.
- The search includes instant-speed windows: the opponent's end step, upkeep, and responses to triggers.
- The state is kept in a canonical form (sorted zones), so identical positions share cache entries.
- If mana is paid by a fixed rule and not by trying every assignment, the test positions cover color conflicts. Colorless and painless sources are spent on generic costs first.
- The pilot never looks at the library order, except for cards it legitimately knows (sections 6 and 7).

## 5. Turn decision procedure

Each turn the pilot works through these steps in order.

1. **Win now**, if the exact check finds a line.
2. **Look for a certain win next turn.** The best few lines are tested with a blank next draw. A position that wins with a blank wins with any draw, so one search replaces one search per card in the library. This needs a check, made once per deck from the card sheet, that no card hurts the deck when drawn. When a certain win exists, the pilot keeps it certain and spends leftover resources only on actions that cannot break it.
3. **Otherwise, shortlist end-of-turn positions** by the progress score (section 8). The best few are valued with a two-turn lookahead: exact over the next draws, with the cheap policy in between.
4. **Keep the shortlist diverse.** It always includes:
   - the best line that leaves open the mana each instant-speed card in hand needs (an end-step tutor, surveil, flashback);
   - the best line that skips any random action, such as a draw or a reveal.
5. **Value a line with its options.** A line's value is the larger of its lookahead value and the value of each instant-speed play it leaves open at the opponent's end step.

## 6. Losing and risk

- Losing the game is an outcome, not a prohibition. A deck can lose by its own actions, such as life payments or an empty library. Such a game is lost and is worth nothing. On the draw this is worse than not winning, which can still win the game under the turn 5 rule (section 2).
- Risky actions are chosen by their effect on the objective, including the chance of losing. That chance is computed exactly whenever possible. No loss goes unrecorded.
- Every known card is used in risk and value. The pilot counts the cards it knows are on the bottom (from mulligans) or on top (from look-and-keep effects and surveil). It never reveals, exiles or draws past a card it needs without counting that loss.
- A risky action is compared with every alternative that uses the same resources this turn, including cheaper ways to dig.

## 7. Random actions inside a turn

- **Resolve for real, then re-plan.** When the pilot casts a draw, loot, surveil or reveal, the effect resolves with the real cards at that moment. The rest of the turn is planned with what it showed. The pilot does not plan through unknown cards by sampling them.
- **Blanks for the win check only.** To find guaranteed wins through such an action, unknown cards are treated as blanks. A win found with blanks is a real win.
- **The decision to cast is made by counting outs.**
  - An out is a kind of card that would turn the position into a win this turn or a certain win next turn. Finding each out costs one search.
  - Using hypergeometric odds over the cards the action shows, the pilot compares casting with not casting, weighted by the turn values.
  - This replaces sampled play-outs whenever counting is enough.
- **Information first.** When mana allows, draw and selection effects are cast before the land drop or other choices are committed.
- **Cards that replace themselves** (free cycling, free cantrips) count as "draw the next card" in the lookahead and are not modeled further. They are used as soon as waiting cannot improve the information, for example after a look-at-the-top trigger.
- **Choices made after seeing cards** (discards, surveil, what to keep on top): each option is first tried with the exact win check. If none wins, the deck plan decides (section 8).

## 8. Reading the deck

The pilot is given no description of the deck. It works out the deck's plan from the card sheet and from its own games, by the same procedure for every deck. Nothing is written by hand for a single deck.

1. **Roles from the text.** From each card's modeled text, the pilot records what the card can do: make mana, draw or select cards, find a named card, move cards between zones, put permanents into play, deal damage or advance another way of winning. A card can have several roles.
2. **Discovery games.** Before the baseline run, the pilot plays a fixed number of solo games [rules] with the exact win check and a generic progress score. The generic score counts progress toward any way the game can be won (the opponent's life, poison, library), the mana available and the cards seen.
3. **Win recipes.** Each win found is reduced to a recipe: the smallest set of cards, by zone, and mana that the win still needs. The pilot finds it by removing pieces from the winning position until the win check fails. Recipes of the same shape are merged and counted.
4. **Deck plan.** The recipes, weighted by how often and how early they win, are the deck plan. The progress score becomes the distance to the nearest recipe: a position scores higher with fewer pieces missing, and with missing pieces that are easier to find. The generic score remains the fallback for positions far from every recipe.
5. **Repeat.** Steps 2 to 4 are repeated for a fixed number of rounds [rules], each using the plan from the round before, because better play finds more recipes.

The deck plan decides:

- what a tutor names: only cards that complete a recipe;
- what to discard, surveil away or exile, and any pre-game choices;
- the keep-value rule and the land minimum used in mulligans (section 9);
- fallback decisions when no win is in reach.

### Limits and checks

- A deck whose win the discovery games never find is played by the generic score alone. The number of recipes found is reported for every deck.
- The plan is checked against the bottleneck analysis (section 15). If games keep failing on a piece that no recipe contains, this is reported as a limit of the pilot for that deck.
- Each deck's plan is published with its card sheet.

## 9. Mulligans

Mulligan decisions are made for the specific opponent: opponent A in the baseline run, the real opponent in a match.

- **Play-outs.** A hand is valued by playing it out with the cheap policy (section 10) and recording the turn of the win, if any. The cheap policy does not use turn values, so one play-out result can be scored against any opponent.
- **Hand value.** A hand's value is the average turn value of its play-out results, for this opponent and this seat (play or draw).
- **Bars.** A hand is kept if its value beats the bar for its size: the measured value of going down one card against this opponent, in this seat. Each bar is measured over 300 games.
- **Stopping.** Play-outs use sequential stopping: at least 16, at most 64, stopping as soon as the comparison with the bar is clear.
- **Bottoming.** The hand is ranked by the keep-value rule and only the three least useful kinds of card are play-tested as candidates for the bottom. Ties are broken by the rule, and lands are kept up to the deck's land minimum (section 8).
- **Mulligan-replacement effects** (exile the hand and redraw) are allowed at every hand size, including the smallest. Cards exiled this way stay exiled for the game and count as known.
- **Noise.** At 16 play-outs, one win moves a hand's value by about 0.06. Closer calls are coin flips and are not treated as evidence about the deck.

## 10. Efficiency

### Pruning

- Prune before searching. Any position whose optimistic bound cannot reach a win is skipped. Bounds must never underestimate, and the test positions confirm it.
- When an action chooses among many targets or names, only those that change the win check or the progress score are considered. Among equivalent choices, the one with the least risk is taken.
- The order of actions is fixed wherever a fixed order cannot make a line worse.
- Rank, then evaluate the best few. Outcomes that lead to the same result, such as equivalent draws, are grouped and evaluated once. End-of-turn options are fully evaluated in progress order, stopping when no remaining option's optimistic value can beat the best found.
- Play-outs are spent only on live choices: when an option's optimistic value could beat the best alternative. They stop as soon as the difference is clear.
- The cheap policy stays cheap: exact win check, then highest progress, with no nested evaluation and no use of turn values.
- Every pruning change is validated. The test positions must still pass, and on a fixed set of logged decisions the pruned pilot must agree with the full pilot. The disagreement rate and the cost of each disagreement are reported.

### Speed

- Profile before optimizing, on fixed test positions and not on new games. Each kind of decision is timed separately.
- Mulligans dominate. A game typically runs 150 to 300 cheap play-outs before it starts, so the cheap policy's cost sets the run time.
- Each decision in the cheap policy costs a constant handful of searches. Any exact evaluation inside it, such as a win chance for every card a tutor could name, is replaced by a rule.
- Exact formulas are preferred to sampling: hypergeometric odds, exact survival chances, and tests like the blank draw. They are faster and have no noise.
- Evaluations are kept cache-friendly. Lookahead results are keyed by library composition, and the pilot avoids creating many slightly different libraries.
- Play-out results are stored as winning turns, so the same play-outs are re-scored for each opponent and not replayed.
- For once-per-game choices, such as pre-game choices, play-outs use rules and the recorded game uses exact checks.

## 11. Compute budget and parallel runs

### Compute budget (proposed)

- The unit is the node: one position expanded by the win check or the lookahead, counted by the engine. Budgets are not measured in seconds. A node count is the same on any machine, so any run can be reproduced and checked.
- Every deck has the same limits [rules]: nodes per decision and nodes per game, including mulligan play-outs. Play-out counts, shortlist sizes and lookahead depth are also the same for every deck.
- The turn 5 rule (section 3) caps every game at 5 turns on the play and 4 on the draw, which bounds the cost of a game for every deck.
- Reading the deck (section 8) has the same budget for every deck: the same number of discovery games, rounds and nodes.
- Reaching a limit never stops a game. The pilot takes the best line it has found so far for that decision. If it has valued none, it takes the cheap policy's choice. Every such decision is logged.
- Each deck's report shows the nodes it used and the share of its decisions that reached a limit. A deck above 5% is flagged to its submitter during review. The submitter may keep, replace or withdraw the deck.
- The limits are set once. After submissions close, every deck is timed on its fixed test positions and a short trial. The limits are chosen so that the whole event fits the available hardware, and they are published before review opens. No limit is changed for a single deck.
- Speedups that apply to one deck are allowed only if the pilot derives them itself, they pass the validation in section 10, and they are published. They may save nodes. They may not change decisions.
- Every deck plays the same number of baseline games and the same number of games per match. Later rounds get no larger budget than earlier ones.

### Parallel runs

Every deck is played alone and every game has its own seed, so games do not depend on each other and can run at the same time.

**Where work may be split**

- Across decks: card sheets, deck reading and baseline runs.
- Across the games of one deck's run.
- Across the mulligan play-outs of one game.
- Across the matches of one round.

**Order that must be kept**

- A deck's reading is finished before its baseline run starts, and its discovery rounds run one after another.
- Every baseline run is finished before any match starts.
- Each Swiss round is finished before the next round is paired.

**Same results on any number of workers**

- The seed of every game and every play-out is derived from the event seed, the deck, the game number and the play-out number. It never comes from a shared random stream or from the order in which work finishes.
- Results are collected in game-number order, not in finishing order.
- Each worker has its own cache, or all workers read one cache that was built beforehand. No cache is written by several workers at once.
- A decision's node count must not depend on which other games ran before it. Either each game starts with an empty cache, or a cached result is charged the nodes it first cost.

**Check**

- Before the event, a sample of games is run twice with different numbers of workers. The two sets of logs must be identical. The check and its result are reported.

## 12. Logging and seeds

Enough is logged to rebuild any board without rerunning the game:

- the first 7 cards, every mulligan decision with its estimate and bar, each mulligan-replacement effect with the cards it exiled, the kept hand and the bottomed cards;
- the board at the start of every turn;
- every card reaching the hand, with its source (draw step, cycling, loot, tutor, a look-at-the-top effect);
- every exile and discard, with its cause;
- every random action's revealed cards and choices;
- each end-of-turn position, and the exact winning position and line;
- every decision that reached a compute limit.

Each game's deal is seeded separately from the pilot's own random numbers, so two lists or two pilot versions can be compared on the same deals. Seeds are published with the results.

## 13. Logging for win credit

The win credit analysis (section 15) rebuilds each winning board, then re-runs the exact win check with cards removed. It then passes each card's share back to whatever put the card there. For that, every recorded game logs the following. Play-outs log only their winning turn.

### Card identity

- Every card gets an instance id when it is dealt and keeps it through every zone change, including exile during mulligans and the bottom of the library.
- Tokens get their own ids, plus the id of the card that made them.

### Provenance events

One event per change, with turn, step (pre-game, upkeep, draw, main, combat, end step), card id, source card id, from-zone and to-zone:

- **Reaching the hand:** opening hand, draw step, or the card that drew, tutored or returned it.
- **Placed on top or bottom:** by a look-and-keep effect or by mulligan bottoming.
- **Graveyard:** discarded, milled, surveiled or cast, with the card or cost that put it there.
- **Exile:** with its cause, and any return from exile.
- **Battlefield:** how each permanent arrived. It was cast, played as a land, put into play from the opening hand, or put into play by another card.
- **Attachments and counters:** which card attached what to which permanent, and which card added or removed counters.

### Damage and life

- Every life change for either player, with its source card id: damage, drain, land costs, life payments, life gain.
- Damage dealt on earlier turns is its own resource in the credit split, credited to its sources.
- Life gained this turn is tracked by source, because some effects scale with it.

### The winning moment

- A full snapshot of the position where the winning line starts, at the exact point the win check succeeds. This can be mid-turn, after a loot or tutor has resolved. It includes:
  - hand;
  - permanents, with tapped state, counters, imprints and attachments;
  - graveyard and exile;
  - mana pool, land drop used, life totals, life gained this turn;
  - library composition and any known cards in it.
- The winning line, as the ordered list of actions with card ids.
- The snapshot uses the engine's own state format, so the win check runs on it directly and on any copy with cards removed.

### Checks

- Rebuilding a logged winning snapshot must reproduce the win. Every win that fails to rebuild is reported. The target is none.
- Credits must add up to the game-win rate exactly.
- Any resource whose source cannot be traced is reported, not guessed.

## 14. Validation and review

- Test positions are written for every new card and interaction before any run. When a test fails, the report says whether the pilot or the test was wrong.
- Every game count is stated before running: discovery games, baseline games, bar games, match games, timing games and paired reruns. Work on fixed test positions is allowed and reported. Mulligan play-outs are part of each game's decisions, and their count is reported.
- Lists or pilot versions are compared on the same deals whenever the expected difference is smaller than the unpaired noise. With 500 games per side, that noise is about 3 points of game-win rate.
- Audit loop: test positions, trace review of example games, the bound gap, a usage report, and reproducing any disagreement between versions.
- **Review.** Card models and rules errors can be challenged during the review window, as `tournament.md` describes.
- **Strategy is not open to challenge.** The pilot accepts no advice on how to play a deck, before or after submission.

## 15. Standard analyses

Published for every deck after the event:

- **Opening-hand value:** regression of game value on the first 7 cards dealt.
- **Draw value:** game value after drawing each card, compared with an average draw that turn.
- **Win credit:** each winning board is rebuilt from the trace (section 13), the win is split among the cards present with an exact Shapley split, and each share is passed back to what put that card there.
- **Bottlenecks:** for games that did not win, the smallest set of added pieces that would have made each turn a win.

A claim about a card's role is made only when the logs record it.

## 16. Changes to this file

- Changes are made by the organizer and recorded in `CHANGELOG.md` with a new version number.
- Every deck in an event is played under the same version.
- No change is made after the review window closes.
