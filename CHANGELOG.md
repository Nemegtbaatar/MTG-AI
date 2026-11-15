# Changelog

This file records what changed in the pilot and the tournament rules, and why. The pilot file is `pilot.md` from version 4.4 and was `pilot.txt` before that. The card-specific examples that used to sit in the pilot file are kept here.

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
