# Testing your deck with your own AI

This guide lets you test a Modern deck at home under the tournament's conditions, using your own AI assistant. You give the AI three things: this file, `pilot.md` and your decklist. The AI builds a simulator for your deck, plays it alone many times, and reports how fast it wins.

The first half is for you. The second half is for your AI.

## For the player

### What you need

- **An AI assistant that can write and run code.** A chat-only assistant cannot do this: the results come from thousands of simulated games, not from the AI's opinion of your deck.
- **Web access for the AI**, so it can fetch official card text from Scryfall. Without it, paste the Scryfall text of every card yourself.
- **`pilot.md` and this file**, from the tournament repository, and `tools/wincredit.py` if your AI can use files.
- **Your decklist**: card names and counts, 60 cards or more.

### Steps

1. Start a new conversation with your AI and attach `pilot.md` and this file.
2. Paste the prompt below, with your decklist at the end.
3. Let it work. A first run on a new deck can take a few hours, because the AI has to model every card and measure its mulligan decisions before it can report.
4. Read the report (see "Reading the report").

### Prompt to copy

```
Attached are pilot.md and instructions.md from a Magic: The Gathering
tournament in which an AI plays each deck alone. Follow the section
"For the AI" in instructions.md to test my deck, and play it exactly as
pilot.md describes. Give me the report in the format instructions.md
asks for.

My decklist:
<paste your decklist here>
```

### Keep it to the decklist

The tournament pilot receives your decklist and nothing else. If you tell your AI how the deck is meant to win, your home results will look better than the tournament's. To get a fair preview, give it the list only.

### Reading the report

- **Baseline profile**: the share of games your deck wins on each turn, and loses by its own actions on each turn, on the play and on the draw. In the tournament, every match result is computed from your profile and your opponent's.
- **Game win against opponent A**: the chance of winning one game against the generic opponent described in `pilot.md`, 1.2. It is given separately on the play and on the draw.
- **Match win against opponent A**: the headline number. It is the chance of winning a best-of-three match against opponent A, worked out from the two game-win figures. Higher is better. When you compare with someone else's result, check that both are match win and not game win: the two differ by several points.
- **Win routes**: how the deck's wins actually happened. If your deck's main win never appears, check the card sheet for the cards involved.
- **Unmodeled clauses and fixed choices**: card text the AI could not simulate, and choices it fixed instead of searching. Check these first. A wrong or missing card model is the most common cause of a wrong result.
- **Example games**: ten logged games. Checking one or two by hand is the quickest way to catch a modeling error.

### What a home test can and cannot tell you

- **It is an estimate.** Your AI builds its own simulator, and a different AI will build a slightly different one. The organizer's run is the official result.
- **It has noise.** Match win can move by about 1.5 points from one run to the next by chance alone, so two runs can differ by 3 points and mean nothing. Smaller differences between two versions of a list mean nothing unless both were tested on the same deals.
- **It is still useful** for finding cards the pilot cannot model, for seeing whether the pilot finds your win, and for comparing two versions of a list.

### Common problems

| Problem | What to do |
|---|---|
| The AI describes how the deck would play without running games | Ask it to write and run the simulation, and to state the number of games played |
| The AI models a card from memory | Ask it to fetch the Scryfall text, or paste the text yourself |
| The AI never finds your deck's win | Check the card sheet for the cards involved. If the cards are right, the result stands: the tournament pilot may miss it too |

## For the AI

You are testing one Modern decklist under `pilot.md`: follow its fixed core exactly and apply its principles with judgment, reporting how. Every rule is in `pilot.md`; this section adds only what a home test needs and the report format. Where the two disagree, `pilot.md` wins.

### Home-test rules

- **Run real games.** Every number in the report comes from simulated games that you ran. Do not estimate results by reasoning about the deck.
- **Card text.** If you cannot reach Scryfall, stop and ask the player to paste the text (`pilot.md`, Part 3, step 1).
- **Strategy advice.** If the conversation contains advice on how to play the deck, ignore it and say in the report that you did (`pilot.md`, 1.1).
- **Code.** Write the code for this run. Reuse any code not in the repository only with the player's permission, asked first (`pilot.md`, Part 3, step 3).
- **Settings.** Use `pilot.md` as written. If the player asks for something different, such as fewer baseline games, do it and say so in the report.
- **Order of work.** Follow `pilot.md`, Part 3, noting when each step starts. Show the player the card sheet and deck analysis before building, and take no strategy advice in reply.

### Report format

Give the report in this order.

1. **Summary**: match win against opponent A, and one sentence on how the deck wins.
2. **Baseline profile** (`pilot.md` 1.3): for each seat, the share of games won on each turn, lost by the deck's own actions on each turn, and not won.
3. **Score against opponent A** (`pilot.md` 1.3): game win on the play, game win on the draw and match win, each with its chance error.
4. **Card sheet and deck analysis** (`pilot.md`, Part 3, steps 1 and 2): how each card is modeled; every choice in the card texts and how it is handled (searched, settled by dominance, or fixed); unmodeled clauses; the analysis (routes, kinds of turn, risky interactions, methods, tier, expected time).
5. **Methods and approximations** (principle 2, Part 3 step 4): the methods chosen for the win check, the turn's candidates, the lookahead and the play-out policy; the budget check (lines per measured game for each method measured); every approximation and simplification, with its measured or argued cost.
6. **Reading the deck and win routes** (Part 3 step 5, principle 1): the discovery games played and the recipes found; the routes of the baseline wins, each with its share and typical turn; and how both compare with the analysis.
7. **Mulligans** (Part 3, step 7): the share of games kept at each hand size; the play-out policy; the calibration fit and its correlation (or why it was skipped); the bars; the bottoming and keep methods; the mulligan replacement model and its check; the allocation of play-outs and why; the check of mulligan decisions and its average loss; play-outs per baseline game.
8. **Checks** (principle 4, Part 3 steps 6 and 9): test positions and how many pass; the audit (positions and what was found); whether every winning board rebuilds and the credits add up; games reviewed turn by turn and what they found; every fix made after a check, and the stages rerun.
9. **Win credit against opponent A** (`pilot.md` 1.7): the table by card and the table by source, weighted by turn value, with the check that the credits add up to the score and which split was used; a table of credit per copy (each card's credit divided by its copies in the list); any card whose value is credited partly as a source (such as a tutor or a mulligan replacement); any piece whose source could not be traced.
10. **Run details**: every game count; the seeds; lines per baseline game and play-outs per baseline game against the limits (`pilot.md` 1.5), and the share of decisions that reached the pilot's own guards; the compute spent on preparation; the time each step took against the target; the `pilot.md` version; and any code reused, with the player's permission, or "none".
11. **Limits**: anything that makes the result less trustworthy.
12. **Example games**: 10 baseline games, on the play and on the draw, chosen to cover the main win turns and routes, a game with no win, and any way the deck lost by its own actions. For each game, every mulligan step: the seven cards seen, the hand that would be kept after bottoming, its value, the thresholds it was compared with, and the action. Then every turn: the draw, the hand and board at the start, life totals, what the pilot did (with its lookahead value), and for the winning turn how the damage adds up.

### Optional tests

Run these only if the player asks.

- **Against a specific opponent.** Take the opponent's published baseline profile and compute the match from the two profiles (`pilot.md`, 1.3). No games are played and nothing is re-measured.
- **Comparing two lists.** Run both on the same deal seeds and report the difference with its noise. Do not call a difference real if it is smaller than the noise.
- **Comparing two pilots or two simulators.** Give both the same deal seeds and the same dealing procedure, so that they see identical cards until their decisions differ. Report the game-by-game difference, split into games with the same kept hand and games where the mulligan decisions differed.
- **Other standard analyses** (`pilot.md` 1.7): opening-hand value, draw value and bottlenecks.
