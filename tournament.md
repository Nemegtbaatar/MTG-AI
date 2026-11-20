# Tournament rules

This file covers how the event is run: submissions, review, the schedule, how match results become standings, and what is published. Every rule about how a deck is played and scored, including the turn 5 rule, the opponent, the baseline, match win and compute limits, is in `pilot.md`, and is not repeated here.

The few values the organizer has to choose are in the Settings table at the end. Suggested values there are proposals until the organizer confirms them.

## The format in brief

- Players submit Modern decklists. An AI pilot plays every deck under `pilot.md`, from its decklist alone.
- There is no interaction between players. Each deck plays a baseline run alone against a generic opponent, opponent A, and every deck is optimized against that same opponent.
- Matches are not played as separate games. The result of every pairing is computed from the two decks' baseline profiles (`pilot.md`, 1.3).

## Decklists

### What is legal

A decklist is legal as `pilot.md`, 1.1 sets out, on the legality date (Settings). Any sideboard in a submission is ignored.

### How to submit

Submit by the deadline (Settings) in one of three ways:

- as text in a Reddit post;
- as a link to a decklist;
- by direct message to the organizer, for a list that should stay private.

### Decklist only

The pilot is given card names and counts and nothing else (`pilot.md`, 1.1). Strategy notes, combos and mulligan advice in a submission are not passed to it.

### Private lists

- A private list stays private until the publication date (Settings).
- Its card sheet, deck plan and game logs are published when the list is.
- Its baseline profile is published with everyone else's, because match results are computed from it.

### Cards the pilot cannot model

- The card sheet lists every clause the pilot could not model and every choice it fixed instead of searching (`pilot.md`, Part 3).
- A deck with unmodeled clauses is flagged to its submitter during review. The submitter may keep the deck with those clauses ignored, replace it, or withdraw it.

## Matches and standings

- **Every deck is paired with every other deck.** Because results are computed from profiles, a full round robin costs nothing extra.
- **A match result** is each deck's match win against the other (`pilot.md`, 1.3). The two add up to 100%.
- **Standings** are by average match win against all other decks. Ties are broken by match win against opponent A.

## Schedule

The event runs in this order. Dates are in Settings.

1. **Submissions close.**
2. **Card sheets and deck reading.** For each deck the pilot checks the list, writes the card sheet and deck analysis, builds and tests the engine, reads the deck in discovery games and audits it (`pilot.md`, Part 3, steps 1 to 6).
3. **Review window.** Card sheets, deck plans, test positions, discovery logs and audits are open to challenge.
4. **Freeze.** After the review window closes, nothing changes: no decklist, card model, pilot version or setting.
5. **Baseline runs** (`pilot.md`, Part 3, steps 7 to 10). Profiles and reports are published.
6. **Results.** The match table, standings, seeds and logs are posted on Reddit and in the repository.

## Review and rulings

- During the review window, anyone may challenge a card model or a rules error by pointing to a card sheet entry or a logged game.
- Challenges are made in the place named in Settings.
- The organizer rules on each challenge. Every ruling is recorded in `rulings.md`.
- Strategy, including the methods and judgment the pilot chose, is not open to challenge (`pilot.md`, 1.8).
- A deck flagged for unmodeled clauses or for compute (`pilot.md`, 1.5) may be kept, replaced or withdrawn by its submitter before the freeze. A replacement goes through the same steps.

## What is published

- For every deck: decklist, card sheet, deck analysis, deck plan, test positions, baseline profile and report.
- For the event: the match table, standings, seeds, game logs and rulings.
- The versions of `pilot.md` and of this file that the event used.

## Settings

| Setting | Value | Suggested |
|---|---|---|
| Submission deadline | To be set | |
| Legality date | To be set | The submission deadline |
| Decks per player | To be set | 1 |
| Publication date for private lists | To be set | When results are posted |
| Review window | To be set | 7 days |
| Where challenges are made | To be set | Issues on the repository |
| Event seed | Published with results | |
