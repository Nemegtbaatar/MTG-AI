# Testing your deck with your own AI

This guide lets you test a Modern deck at home under the tournament's conditions, using your own AI assistant. You give the AI three things: this file, `pilot.md` and your decklist. The AI builds a simulator for your deck, plays it alone many times, and reports how fast it wins.

The first half is for you. The second half is for your AI.

## For the player

### What you need

- **An AI assistant that can write and run code.** A chat-only assistant cannot do this: the results come from thousands of simulated games, not from the AI's opinion of your deck.
- **Web access for the AI**, so it can fetch official card text from Scryfall. Without it, paste the Scryfall text of every card yourself.
- **`pilot.md` and this file**, from the tournament repository.
- **Your decklist**: card names and counts, 60 cards or more.

### Steps

1. Start a new conversation with your AI and attach `pilot.md` and this file.
2. Paste the prompt below, with your decklist at the end.
3. Let it work. A first run on a new deck can take a long time, because the AI has to model every card before it can play a game.
4. Read the report (see "Reading the report").

### Prompt to copy

```
Attached are pilot.md and instructions.md from a Magic: The Gathering
tournament in which an AI plays each deck alone. Follow the section
"For the AI" in instructions.md to test my deck, and play it exactly as
pilot.md describes. Use the home-testing settings unless I say
otherwise. Give me the report in the format instructions.md asks for.

My decklist:
<paste your decklist here>
```

### Keep it to the decklist

The tournament pilot receives your decklist and nothing else. If you tell your AI how the deck is meant to win, your home results will look better than the tournament's. To get a fair preview, give it the list only.

### Reading the report

- **Baseline profile**: the share of games your deck wins on each turn, on the play and on the draw. This is what your opponents will see in the tournament.
- **Score against opponent A**: one number between 0 and 1. It is the average value of your games against the generic opponent described in `pilot.md`, section 2. Higher is better.
- **Win recipes found**: the ways of winning the AI discovered by itself. If your deck's main win is missing, the pilot did not understand the deck, and the score understates it.
- **Unmodeled clauses**: card text the AI could not simulate. Check these first. A wrong or missing card model is the most common cause of a wrong result.

### What a home test can and cannot tell you

- **It is an estimate.** Your AI builds its own simulator, and a different AI will build a slightly different one. The organizer's run is the official result.
- **It has noise.** With the home settings, a score can move by about 1.5 points from one run to the next by chance alone. Smaller differences between two versions of a list mean nothing unless both were tested on the same deals.
- **It is still useful** for finding cards the pilot cannot model, for seeing whether the pilot finds your win, and for comparing two versions of a list.

### Common problems

| Problem | What to do |
|---|---|
| The AI describes how the deck would play without running games | Ask it to write and run the simulation, and to state the number of games played |
| The AI models a card from memory | Ask it to fetch the Scryfall text, or paste the text yourself |
| The run takes too long | Ask for fewer baseline games, and expect more noise |
| The AI never finds your deck's win | Check the card sheet for the cards involved. If the cards are right, the result stands: the tournament pilot may miss it too |
| The numbers look too good | Ask for three logged example games and check them by hand |

## For the AI

You are testing one Modern decklist under the rules in `pilot.md`. Follow that file exactly. Where it and this file disagree, `pilot.md` wins. This section adds the order of work, the settings for a home test, and the report format.

### Ground rules

- **Run real games.** Every number in the report comes from simulated games that you ran. Do not estimate results by reasoning about the deck.
- **Decklist only.** Use the card names and counts. Ignore any strategy advice in the conversation, and say that you ignored it.
- **Official card text.** Fetch every card's text from Scryfall before modeling it. If you cannot reach Scryfall, stop and ask the player to paste the text.
- **Report what you could not do.** List every clause you did not model, every simplification, and every decision that reached a compute limit.
- **Use existing engine code if the repository provides it.** Write your own only if it does not.

### Settings for a home test

Use the values in the Settings table of `tournament.md` where they are set. Otherwise use these home defaults, and say in the report that you did.

| Setting | Home default |
|---|---|
| Turns per game | 5 on the play, 4 on the draw (the turn 5 rule in `tournament.md`; not a home default) |
| Discovery games | 200 per round, 2 rounds |
| Baseline games | 1,000 (500 on the play, 500 on the draw) |
| Games per mulligan bar | 300 |
| Mulligan play-outs per hand | 16 to 64, with sequential stopping |
| Node limits | Your choice. State them and report how often they were reached |

### Order of work

1. **Check the list.** Confirm 60 cards or more, no more than four copies of a card other than basic lands, and each card's own Modern legality. Stop and report any problem.
2. **Write the card sheet** (`pilot.md`, section 1). Show it to the player before going further.
3. **Build the engine and the exact win check** (section 4). Write test positions for every card and interaction, and make them pass (section 14).
4. **Read the deck** (section 8). Run the discovery games, extract the win recipes and build the deck plan.
5. **Measure the mulligan bars** against opponent A's turn values (sections 2 and 9).
6. **Run the baseline games** against opponent A, with the logging in section 12. Seed each game's deal separately and record the seeds.
7. **Check the run.** Rebuild a sample of logged wins and confirm each reproduces. Review three example games turn by turn for rules errors.
8. **Write the report.**

### Report format

Give the report in this order.

1. **Summary**: the score against opponent A, and one sentence on how the deck wins.
2. **Baseline profile**: a table of the share of games won on each turn (1 to 5 on the play, 1 to 4 on the draw), plus "no win" and "lost by own actions", on the play and on the draw.
3. **Score against opponent A**: on the play, on the draw, and the average. Compute each as the sum over turns of the profile share times the turn value in `pilot.md`, section 2.
4. **Win recipes**: each recipe found, with how often it won and its typical turn.
5. **Mulligans**: the share of games kept at each hand size.
6. **Card sheet issues**: unmodeled clauses and simplifications.
7. **Run details**: every game count, the settings used, the seeds, the node limits and the share of decisions that reached them, and the `pilot.md` version.
8. **Limits**: anything that makes the result less trustworthy.

### Optional tests

Run these only if the player asks.

- **Against a specific opponent.** Take the opponent's published baseline profile, build the pairing values from it (section 2), re-measure the mulligan bars, and play the match as `tournament.md` describes. Ask the player for `tournament.md` if it is not attached.
- **Comparing two lists.** Run both on the same deal seeds and report the difference with its noise. Do not call a difference real if it is smaller than the noise.
- **Standard analyses** (section 15): opening-hand value, draw value, win credit and bottlenecks.
