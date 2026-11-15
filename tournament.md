# Tournament rules

This file covers how the event is run: how decks are submitted, how two decks' results become a match, and how standings are decided. How a single deck is played is in `pilot.md`.

Every value the organizer has to choose is in the Settings table at the end. Suggested values there are proposals until the organizer confirms them.

## The format in brief

- Players submit Modern decklists. An AI pilot plays every deck.
- There is no interaction between players. Each deck is played alone against an opponent that does nothing, and a game goes to the deck that wins first.
- Every deck is played by the same procedure (`pilot.md`), from its decklist alone.

## Decklists

### What is legal

- 60 cards or more, with no more than four copies of any card other than basic lands.
- Every card must be legal in Modern on the legality date (Settings). Legality is checked card by card on Scryfall.
- Sideboards are not used. Any sideboard in a submission is ignored.

### How to submit

Submit by the deadline (Settings) in one of three ways:

- as text in a Reddit post;
- as a link to a decklist;
- by direct message to the organizer, for a list that should stay private.

### Decklist only

The pilot is given card names and counts and nothing else. Strategy notes, combos and mulligan advice in a submission are not passed to the pilot.

### Private lists

- A private list stays private until the publication date (Settings).
- Its card sheet, deck plan and game logs are published when the list is.
- Its baseline profile is published with everyone else's, because opponents need it.

### Cards the pilot cannot model

- The card sheet lists every clause the pilot could not model (`pilot.md`, section 1).
- A deck with unmodeled clauses is flagged to its submitter during review. The submitter may keep the deck with those clauses ignored, replace it, or withdraw it.

## The opponent

Each deck plays alone against an opponent that never acts:

- It starts at 20 life with a 7-card hand and a 53-card library, and draws a card each turn.
- It plays no cards, controls no permanents and makes no choices.
- A deck wins in any way the rules of Magic allow: the opponent at 0 life, 10 poison counters, the opponent drawing from an empty library, or a card that says so.

## Baseline profiles

Before any match, every deck plays a baseline run against opponent A, a generic opponent that wins on turn 2 in 25% of games, turn 3 in 50% and turn 4 in 25% (`pilot.md`, sections 2 and 3). The result is the deck's baseline profile: how often it wins on each turn, on the play and on the draw.

- Every deck plays the same number of baseline games (Settings).
- Profiles are published before round 1 and stay fixed for the whole event.
- A profile is the only information a deck has about its opponent.

## The turn 5 rule

This is a tournament rule, not a rule of Magic.

**The deck on the play loses the game at the end of its turn 5 if it has not won.**

The rule keeps games short and limits the compute needed to simulate them. Its consequences:

- The deck on the play has 5 turns. The deck on the draw has 4, because its turn 5 would come after the game has ended.
- The deck on the draw wins any game in which the deck on the play does not win in time. It does not need to win by itself.
- No game is drawn.

## How a match is played

### Preparation

For a match between X and Y, each deck adjusts to the other's baseline profile (`pilot.md`, sections 2 and 3):

- X's turn values are built from Y's profile, and Y's from X's.
- Each deck measures its mulligan bars against those values and uses them for its play.
- This is done once. Neither deck sees how the other adjusts to it.

### Games

A match is a fixed number of games (Settings), half with each deck on the play. In each game both decks are played alone, and the game is decided by the first of these to happen, in turn order:

- **A deck wins.** If both would win on the same turn, the deck on the play wins, because it takes that turn first.
- **A deck loses by its own actions,** such as life payments or an empty library. The other deck wins.
- **The deck on the play ends its turn 5 without a win.** The deck on the draw wins.

A deck's deal in game number n is the same in every match it plays.

### Match result

- The deck with more game wins takes the match.
- A match is drawn if the leading deck's share of games is inside the draw band (Settings).

## Tournament structure

- **Fewer than 8 decks:** full round robin. Every deck plays every other deck once.
- **8 decks or more:** Swiss pairings. Each round, decks with the same match points are paired, and no pair meets twice.
- Match points and tiebreaks are in Settings.

## Schedule

The event runs in this order. Dates are in Settings.

1. **Submissions close.**
2. **Card sheets and deck reading.** The pilot writes each deck's card sheet, test positions and deck plan (`pilot.md`, sections 1, 8 and 14).
3. **Compute limits published.** The same limits for every deck (`pilot.md`, section 11).
4. **Review window.** Card sheets, deck plans and trial-game logs are open to challenge.
5. **Freeze.** After the review window closes, nothing changes: no decklist, card model, pilot version or setting.
6. **Baseline runs.** Profiles are published.
7. **Rounds.** Pairings and results are posted on Reddit after each round.
8. **Results.** Final standings, seeds, logs and the standard analyses (`pilot.md`, section 15) are published.

## Review and rulings

- During the review window, anyone may challenge a card model or a rules error by pointing to a card sheet entry or a logged game.
- Challenges are made in the place named in Settings.
- The organizer rules on each challenge. Every ruling is recorded in `rulings.md`.
- Strategy is not open to challenge. The pilot accepts no advice on how to play a deck, before or after submission.
- A deck flagged for unmodeled clauses or for reaching compute limits may be kept, replaced or withdrawn by its submitter before the freeze. A replacement goes through the same steps.

## What is published

- For every deck: decklist, card sheet, deck plan, baseline profile, test positions and report.
- For the event: pairings, match results, standings, seeds, game logs and rulings.
- The versions of `pilot.md` and of this file that the event used.

## Settings

| Setting | Value | Suggested |
|---|---|---|
| Submission deadline | To be set | |
| Legality date | To be set | The submission deadline |
| Decks per player | To be set | 1 |
| Publication date for private lists | To be set | When round 1 results are posted |
| Review window | To be set | 7 days |
| Where challenges are made | To be set | Issues on the repository |
| Turns per game | 5 on the play, 4 on the draw | Fixed by the turn 5 rule |
| Discovery games | To be set | 200 per round, 2 rounds |
| Baseline games per deck | To be set | 1,000 (500 in each seat) |
| Games per mulligan bar | 300 | Fixed in `pilot.md`, section 9 |
| Games per match | To be set | 1,000 (500 in each seat) |
| Draw band | To be set | Drawn if the leading deck has under 53% of games |
| Match points | To be set | Win 3, draw 1, loss 0 |
| Swiss rounds | To be set | 3 for 8 decks, 4 for 9 to 16, 5 for 17 to 32 |
| Tiebreaks | To be set | Share of all games won, then score against opponent A |
| Compute limits | Set after submissions close | See `pilot.md`, section 11 |
| Event seed | Published with results | |

Why a 53% draw band: with 1,000 games, chance alone moves a deck's share of games by about 1.6 points, so a lead under 3 points is not reliable evidence that one deck is faster.
