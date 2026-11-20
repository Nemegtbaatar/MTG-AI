# Modern Goldfish Tournament

A Magic: The Gathering tournament in which players submit Modern decklists and an AI plays them. There is no interaction between players: each deck is played alone, and matches are decided by which deck wins faster.

**Status:** not yet open. Dates will be posted here and on Reddit.

## How it works

1. You submit a decklist. Nothing else is needed, and nothing else is used.
2. The AI pilot reads the deck, works out how it wins, and plays it 1,000 times against the same generic opponent to measure how fast it is: its baseline profile.
3. Every deck is paired with every other. Each match result is computed from the two decks' profiles, and standings are by average match win.
4. One special rule keeps games short: the deck on the play loses at the end of its turn 5 if it has not won.

## Take part

- **Submit a deck:** post it as text on Reddit, share a link to the list, or send it to the organizer by direct message to keep it private. Details are in [tournament.md](tournament.md).
- **Test your deck first:** [instructions.md](instructions.md) shows how to run the same test at home with your own AI.
- **Reddit thread:** link to be added.

## Files

| File | What it covers |
|---|---|
| [tournament.md](tournament.md) | How the event is run: submissions, review, schedule, standings and settings |
| [pilot.md](pilot.md) | Every rule for playing and scoring a deck: the turn 5 rule, the opponent, the baseline, match win, compute limits, and how the AI plays |
| [instructions.md](instructions.md) | Testing a deck with your own AI |
| [rulings.md](rulings.md) | Challenges raised in review and the organizer's rulings |
| [CHANGELOG.md](CHANGELOG.md) | Version history of the pilot and the rules |
| `decks/` | One folder per deck: decklist, card sheet, deck plan, baseline profile, test positions, report |
| `tools/` | Shared code the pilot may use: `wincredit.py` |
| `results/` | The match table, standings, seeds and game logs |

The `decks/` and `results/` folders are filled in as the event runs.

## Notice

This is an unofficial fan project. It is not affiliated with, approved or endorsed by Wizards of the Coast. Magic: The Gathering and its card names and text are property of Wizards of the Coast LLC. Card text is taken from Scryfall.
