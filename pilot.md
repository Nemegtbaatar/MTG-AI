# Pilot: how every deck is played in the tournament

Version 7.0

The AI pilot receives a Modern decklist and nothing else. It reads the cards, works out how the deck wins, builds what it needs to play the deck, and plays it alone many times against an opponent that does nothing. A match between two decks is computed from how fast each one wins (1.3).

This file has five parts:

- **Part 1, the fixed core:** what must be the same for every deck so results are fair and comparable. These are rules.
- **Part 2, principles:** how the pilot decides everything else. They are not procedures; the pilot applies them with judgment and reports how. Each carries, in its wording, a lesson that cost something to learn (`CHANGELOG.md` has the stories).
- **Part 3, the default workflow:** the order of work that has served well. The pilot may adapt it with a stated reason.
- **Part 4, method examples:** ways of playing turns that have worked, for the pilot to choose among or improve on.
- **Part 5, lessons from specific decks:** the lessons that name cards or decks, kept in one place so the rest of the file stays generic. Parts 1 to 4 do not depend on it; removing it changes no rule.

Where a principle and an example disagree, the principle wins. Where the core and anything else disagree, the core wins. Every rule about how a deck is played and scored is in this file; `tournament.md` covers only how the event is run. Anything this file does not fix is the pilot's judgment, stated in the report. Time targets, as guidance: about 30 minutes from decklist to report for a simple deck, two to three hours for the most complex.

# Part 1. The fixed core

## 1.1 Input

- The pilot receives card names and counts only. It takes no advice on how to play a deck, before or after submission; strategy notes in a submission are not passed to it.
- A legal decklist has 60 cards or more, no more than four copies of any card other than basic lands, and only cards legal in Modern on the legality date (`tournament.md`; for a home test, the day of the test), checked card by card on Scryfall. Sideboards are ignored. The pilot checks the list before anything else and stops on a problem.

## 1.2 The game, the opponent and turn values

- **The turn 5 rule** (a tournament rule, not a rule of Magic): the deck on the play loses at the end of its turn 5 if it has not won. A deck therefore plays 5 turns on the play and 4 on the draw.
- **The opponent never acts.** It starts at 20 life with a 7-card hand and a 53-card library, draws a card each turn, plays no cards, controls no permanents and makes no choices. A deck wins in any way the rules of Magic allow: the opponent at 0 life, 10 poison counters, the opponent drawing from an empty library, or a card that says so.
- **The objective is a table of turn values:** what a win on each turn is worth. A win is worth the chance that the opponent has not already won: on the play, that the opponent does not win before its own turn t; on the draw, that it does not win by its own turn t. Every deck optimizes against **opponent A**, the same generic opponent for every deck, which wins on turn 2 in 25% of games, turn 3 in 50% and turn 4 in 25%, and never loses by its own actions:

| Win on turn | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| On the play | 1.00 | 1.00 | 0.75 | 0.25 | 0.00 |
| On the draw | 1.00 | 0.75 | 0.25 | 0.00 | none |

- One table is used for every decision in a run, mulligans included. A deck does not adapt to the decks it is paired with.
- A game not won, or lost by the deck's own actions, is worth nothing.
- Every game is played until the deck wins, loses or runs out of turns, even when the remaining turns are worth nothing. Among lines of equal value, the earliest win is taken.

## 1.3 Baseline profile and match win

- **Baseline:** every deck plays 1,000 baseline games against opponent A, 500 on the play and 500 on the draw, each deal seeded separately (1.6). Its **profile** is, for each seat, the share of games won on each turn, the share lost by its own actions on each turn, and the share not won. The profile is published and fixed for the event.
- **Game win between two decks.** Each deck's game ends at its first event: a win, or a loss by its own actions. For deck X, let w(t) and l(t) be its profile's shares of games won and lost by its own actions on its turn t in the seat it is in, and let S(t) = 1 − the sum of w(k) + l(k) over k ≤ t (with S(0) = 1). Turns alternate, starting with the deck on the play.
  - X on the play against Y on the draw (turns X1, Y1, X2, …, Y4, X5):
    P = Σ over t = 1…5 of w_X(t) · S_Y(t − 1) + Σ over t = 1…4 of l_Y(t) · S_X(t).
  - X on the draw against Y on the play (turns Y1, X1, …, X4, Y5):
    P = Σ over t = 1…4 of w_X(t) · S_Y(t) + Σ over t = 1…5 of l_Y(t) · S_X(t − 1) + S_Y(5) · S_X(4), the last term being the turn 5 rule.
  - Against opponent A these give exactly the turn values in 1.2, applied to the deck's own profile.
- **Match win** is best of three: the first deck to win two games wins the match; the seat in game 1 is decided at random, and the loser of each game is on the play in the next. With p and q the deck's game win on the play and on the draw, and a = q + (1 − q) · p, match win = ½ · [p · a + (1 − p) · p · q] + ½ · [q · a + (1 − q) · p · q]. Check: p = 0.750 and q = 0.495 give 0.684.
- The chance error of p and q is the standard error of the 500 games in each seat; the match win's error follows from them.

## 1.4 Legal play and information

- Every play is legal under the rules of Magic and the cards' official text and rulings. An approximation may leave legal lines out; it may never make an illegal one.
- The pilot never looks at the library order, except cards it legitimately knows (put on the top or bottom, or exiled by a mulligan replacement).

## 1.5 Compute fairness

- Compute is measured in lines, counted by the engine, not in seconds: one candidate turn checked, one position expanded by a search, or one action simulated. A bound counts as one line; a result reused from memory costs nothing. Line counts are the same on any machine.
- **Limits apply to the baseline games**, the same for every deck:
  - the play of each game after the keep: 50,000 lines on average over the baseline, with caches of at most 100,000 positions (a full cache is cleared);
  - mulligan play-outs: at most 64 to value a kept hand, at most 160 to choose what to bottom, and at most 200 per game on average across all of a game's mulligan decisions.
- Everything else (discovery, the budget check, calibration, bars, the check of mulligan decisions, audits) is the pilot's judgment: enough to trust the result, with its cost reported. Bar games play the same mulligan policy as the baseline, so a bar measures the policy actually used.
- How a deck fits the limits is the pilot's judgment (Part 2); that it fits them is a rule. The pilot may set its own per-decision or per-game guards; reaching one never stops a game: the pilot takes the best line found so far and logs the decision. A deck reaching its guards in over 5% of decisions, or over a limit above, is flagged.

## 1.6 Reproducibility

- Every seed (deal, play-out, sampled draw, simulation) is derived from integers: the event seed, the deck, the game and position numbers. Never from text hashing, a shared random stream, or the order work finishes in. Each deal is seeded separately from the pilot's own random numbers.
- Line counts used for a decision start from empty caches. Work may run in parallel; results are collected in game order and must be identical on any number of workers, checked once before the event.
- Every game count is stated before running.

## 1.7 Logging and win credit

- Enough is logged to rebuild any board without rerunning the game: the deal and every mulligan decision; each turn's starting board; every card reaching the hand, exiled or discarded, with its cause; every random action's revealed cards and choices; each end-of-turn position; each decision that reached a limit; and the winning position and line.
- Every card has an instance id kept through every zone and change of face; tokens record their maker; damage and life gained are recorded by source.
- **Win credit:** each winning board is split among its pieces by a Shapley split (exact when small, sampled with integer seeds when large; each win's shares add to exactly 1), weighted by the win's turn value, so credits add up exactly to the score. One table by card (tokens credited to their maker), one passed back to what put each piece there. For decks whose wins are long chains, an equal split over the pieces used in the winning line is allowed and named. `tools/wincredit.py` implements all of this for any deck.
- Also published after the event: opening-hand value, draw value, and bottlenecks (the smallest additions that would have won a turn not won). A claim about a card's role is made only when the logs record it.

## 1.8 Report, review and changes

- The report follows the format in `instructions.md`. It states the methods chosen, every approximation with its measured or argued cost, every check and its result, every reuse of code (Part 3, step 3) and the time each stage took.
- Card models and rules errors can be challenged during review (`tournament.md`). Strategy, including the methods and judgment the pilot chose, is not open to challenge, except where it makes an illegal play.
- This file changes only by the organizer, with a new version in `CHANGELOG.md`. Every deck in an event uses the same version; nothing changes after review closes.

# Part 2. Principles

**1. Understand how the deck wins before building anything.**
Write a short analysis from the card texts first: the deck's routes to a win and their likely turns; which turns are puzzles over known cards and which depend on cards drawn during the turn; and the interactions most likely to be modeled wrong. Choose methods from that analysis, and afterwards compare the routes predicted with the wins the games find; a disagreement points at a modeling error. *Lesson: the design a deck needs (an exact search, a mana solver, a policy with simulation) is visible from its cards in minutes, and invisible from a default engine until much later.*

**2. Exact where it is affordable; approximate where it is not; measure what any approximation costs.**
This applies everywhere: the win check, the turn's candidate lines, the lookahead, mulligans. Use the exact method whenever it fits the compute limits. When it does not, choose the approximation, state it, and measure its cost on the same deals when that is affordable, or argue it when not. Never impose an approximation on a deck that can afford the exact method. *Lesson: a lookahead fixed to sampling for every deck cost a cheap deck about a point on the play, against a deck that could easily afford exact; sampling cost a costlier deck under a point, within noise.*

**3. Every legal line is a candidate.**
A line is left out only with a reason showing it cannot win or improve the deck's chances, and the reason is stated. A shortlist is cut from all the candidates by a stated score, never from a cheaper subset of them. Turns happen in time: the land drop can come before or after anything else, and a card put into hand mid-turn (drawn, tutored, returned) can be played that turn, including as the land drop. Each instance and copy of a spell may choose its own target. Names, the legend rule, double faces, and when each cost is paid are read from the text. Choices inside an effect are candidates too, including declining an optional action. *Lessons: a shortlist built from cheap lines hid the best line for a whole run; an engine that chose the land drop before casting a tutor missed a turn-1 kill.*

**4. Check against independent evidence.**
Write a test position for each card and interaction before any game, including, for every card that puts a card into hand, one whose only win uses that card the same turn. Audit real positions from the deck's own games by reasoning from the card texts: positions where a win looked possible but none was found, and wins found, checked for legality. How many is the pilot's judgment (ten, seven misses and three wins, has served). An optimistic bound must never be below the true best. Every simplification is listed with its reason. A check that shares the engine's assumptions proves nothing. *Lesson: a brute-force reference built on the engine's own move list agreed with the engine on 900 positions while both missed the same kill; reasoning about one real hand found it.*

**5. Play well under uncertainty.**
Resolve random effects with the real cards and re-plan with what they show. Value an uncertain action by its effect on the turn values, counting outs exactly where possible and including the chance of losing: an action that can win now or lose is worth taking when P(win now) × the value of winning now exceeds (P(win now) + P(lose)) × the value of not taking it; there are no fixed thresholds. Use information before committing: draw and selection effects before the land drop when mana allows. Count every known card, and never dig past a card the deck needs without counting that loss. When a turn chains many unknown draws, play it with a stated policy, decide whether to go ahead by simulating it from the real library, and guard against drawing from an empty library. Losing is an outcome, not a prohibition; every loss is recorded.

**6. Be fast where the time goes, without changing decisions unknowingly.**
Mulligan play-outs dominate the run time, so the policy that plays them is chosen with its cost in mind (Part 3, step 7). Prefer exact formulas to sampling, reuse results that cannot change a decision, prune with bounds that never underestimate, rank candidates and evaluate the best first. A speedup that should not change decisions is used only after a fixed sample of games reproduces exactly; one that may change them is an approximation (principle 2). Profile before optimizing.

**7. Never tune to results, and take no advice.**
Methods and judgment are settled before the mulligan bars are measured. A change after the baseline reruns every stage it affects. The deck's results never steer its own pilot.

# Part 3. The default workflow

1. **Card sheet.** Check the list (1.1). Fetch every card's official text and rulings before modeling it; never model from memory. For every clause, say how it is modeled or why it is ignored, with attention to timing, what moves where, conditions (including the legend rule by name), copies and costs. List every choice the text gives the player: "may" (including declining), "up to" and "any number", modes, X, targets, names, the order of triggers, and which cards to keep, put back or exile. For each, state whether the engine searches it, settles it by a stated dominance argument, or fixes it, which is an approximation (principle 2). List unmodeled clauses. Published.
2. **Deck analysis** (principle 1), published with the card sheet: routes, kinds of turn, risky interactions, methods, tier and expected time.
3. **Build and test positions** (principles 3 and 4). Write the code for this run. The repository's shared tools may be used where they fit (today only `tools/wincredit.py`). Any other existing code, including code written for an earlier run or another deck, is reused only with the player's permission, asked before it is used, and every reuse is listed in the report.
4. **Budget check.** Right after the build, play a small sample of measured deals with empty caches and count lines (principle 2). Use the exact methods if they fit the limits (1.5); otherwise choose and state approximations, and measure their cost on the same deals where affordable.
5. **Reading the deck.** Play discovery games (how many is the pilot's judgment; two rounds of 200 have served) with a generic progress score (progress toward any way of winning, mana, cards seen). Reduce each win to a recipe, the smallest set of pieces the win still needs, and use the recipes, weighted by how often and how early they win, as the deck plan: the progress score becomes the distance to the nearest recipe, and the plan decides what tutors name and what to discard. Repeat for the set number of rounds. For a deck whose wins do not repeat as small recipes, the analysis may set the progress score instead. Compare with the analysis.
6. **Audit** (principle 4). A confirmed miss or illegal line is fixed, the reading redone, and a fresh set audited.
7. **Mulligans.**
   - **Value.** A hand's value is the average turn value of play-outs of that hand. The pilot chooses the policy that plays them, which may be the full pilot or a cheaper one, and states it. A policy other than the full pilot is an approximation (principle 2); its effect on mulligan decisions is measured. Play-outs keep known cards known: bottomed cards stay at the bottom, and cards exiled by a mulligan replacement are out of the library. Hand values and bars are compared in full-pilot units (Calibration).
   - **Calibration.** A cheaper play-out policy does not undervalue every hand by the same amount: it undervalues weak hands, which need careful setup turns, more than strong ones, so its errors do not cancel between a hand and its bar. Before the bars, the pilot plays a sample of hands for each seat and hand size both ways on the same libraries, and fits the full pilot's value as a function of the cheap value (a straight line has served). A kept hand's cheap estimate is converted with the fit before it is compared with a threshold; bottoming candidates are compared on cheap values, since a rising fit keeps their order. The fit, its correlation and its cost are reported. If the fit would cost more than it can gain, the pilot may skip it and state the bias.
   - **Bars.** The bar for a hand of size n is V(n−1): the value of going down one card and playing the actual mulligan policy from there, against opponent A in this seat. A bar is measured honestly, by making each decision with one set of play-outs and valuing the hand kept with separate ones, played by the full pilot (one per bar game is enough; the standard error sets the number of games). It is never estimated as the average of max(estimated value, threshold), which is biased upward by about ½·f(t)·σ²(t). Each bar is measured to a standard error of 0.02 or less, in a first pass and then a second pass that uses the first pass's bars.
   - **Bottoming.** Every distinct choice of cards to bottom is a candidate when affordable. Candidates are played against the same shuffled libraries, since they draw from the same library. They are compared by successive halving: the budget is spent evenly over about log₂(number of candidates) rounds, dropping the worse half after each round. A shortcut that leaves candidates out is an approximation (principle 2), stated, with its cost measured.
   - **Keep.** The best candidate is valued with fresh play-outs, never with the play-outs that selected it. Play-outs are added in batches until the expected loss of deciding now, σ·ψ((estimate − threshold)/σ), falls below a set level, within the play-out limits (1.5). The hand is kept if its value is at least the threshold. Here ψ(d) = φ(d) − |d|·Φ(−|d|), and σ is the standard error of the estimate.
   - **Mulligan replacements.** Exiling the hand and redrawing at the same size is one more option in the comparison. Its value is V(n), adjusted to the library that will remain once the hand is exiled. The adjustment is measured or modeled from the library's composition, and checked against direct play-outs on a sample. The threshold is the larger of V(n−1) and that adjusted V(n). Cards exiled stay known.
   - **Budget.** The play-outs per game (1.5) are allocated where they reduce expected loss the most, comparing bottoming and keep decisions at the same marginal value per play-out. The allocation is measured on a sample of hands before the bars, and reported.
   - **Check.** Before the bars, a random sample of mulligan decisions (keep, bottom, replacement) is compared with decisions made from many play-outs per option, and the average loss is reported. The calibration sample also shows the play-out policy's effect on keep decisions, so it serves as that measurement.
8. **Baseline run** (1.3) with full logging (1.7).
9. **Checks:** tests pass; every winning board rebuilds; credits add up; nothing untraced; at least three games reviewed turn by turn for rules errors; analysis compared with the wins found.
10. **Report.**

# Part 4. Method examples

Not rules: ways that have worked, for the pilot to choose among or improve on.

- **A default turn:** win now if the win check finds a line; else look for a certain win next turn by testing the best lines with a blank next draw (a win with a blank wins with any draw, once a check shows no card hurts when drawn), and keep it certain; else value the candidate end-of-turn positions by a two-turn lookahead, exact over the next two draws if affordable, otherwise over sampled draws on a shortlist, counting kills. Keep the shortlist diverse: include the best line that keeps mana open for an instant-speed card in hand, and the best line that skips a random action. Value a line with the instant-speed plays it leaves open.
- **Trigger windows:** delayed and upkeep triggers open moments to act. Before a trigger that would lose the game resolves (such as a delayed payment that cannot or will not be made), check for a win with instant-speed actions and the mana untapped at that moment (no land drop, no sorcery-speed spells or abilities, no combat). Upkeep triggers resolve before the draw step, so cards drawn that turn cannot be used. A spell whose delayed payment the deck never intends to make is then free, so lines that cast it on a turn that is not lethal stay candidates.
- **Exact search shortcuts that cannot miss a win:** identical creatures are interchangeable; added power goes to the creature that multiplies it most, after the other effects are assigned and separately for each way to win (ruled out by any condition on power); triggers that count spells depend on the number of instances, not their targets; no more optional costs than the mana left can pay.
- **Counting outs** for draw and selection effects, with hypergeometric odds, in place of sampled play-outs.
- **A mana solver** for decks whose mana comes from untap effects, lands that return lands, or extra land drops, with pieces of the same role grouped.
- **Grouped actions** for repeated identical sequences, such as recasting the same artifact.
- **A stated policy with simulation** for turns that chain draws, with a decking guard.

| Kind of deck | Methods that have fit |
|---|---|
| Creatures and pump spells | Exact search with the power shortcut, exact two-turn lookahead |
| Cantrip aggro | Exact search, counting outs |
| Unusual engines over known cards | Exact search with stated fixed orders, many test positions, full audit |
| Mana engines, tutors for several cards | Mana solver, grouping by role |
| Long chains of spells that draw | Stated policy with simulation, decking guard, equal credit split |

# Part 5. Lessons from specific decks

Each lesson names the rule it belongs to. Nothing in Parts 1 to 4 refers to this part.

- **Mulligan calibration** (Part 3, step 7). On the four-color pump list, the cheap play-outs sent borderline 6-card hands to 5 that the full pilot keeps (26 decisions against 1). Mulligans made with full-pilot play-outs scored about a point of match win more.
- **Trigger windows** (Part 4). Summoner's Pact asks for {2}{G}{G} in the next upkeep. A deck with an instant-speed kill (Fling on Cosmogoyf) can let the payment trigger go on the stack and win in response, so Pact is a free tutor on the turn before the kill. One engine resolved the trigger after the draw step, which let a card drawn that turn answer it.
- **Choices on the card sheet** (Part 3, step 1; principle 3). Devourer of Destiny says "you may put one of those cards back on top of your library. Exile the rest." A card sheet that read it as "put one back" never considered exiling all four, one more card in exile for a deck that counts exiled cards. On the Cosmogoyf list it cost under 0.1 point of match win, but the same misreading of "may" can hide a win.
