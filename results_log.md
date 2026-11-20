# Results log

One row per home test, newest first. Match win, p and q are against opponent A (`pilot.md` 1.3). Every chance error is one standard error. Add a row after each test.

**Read before comparing rows:**
- Every run from 6.1 to 6.4 reused mulligan and measurement code from earlier runs without saying so. The deck engines were new each time. So a difference between pilot versions measures the pilot text together with carried-over code, not the text alone.
- Every run stopped mulligans at 4 cards, a limit in the code, not the rules. That matters most for Serum Powder decks.
- Every run derived seeds from SHA-256 of text labels. `pilot.md` 1.6 says seeds come from integers, never text hashing.
- No two runs below used the same deals. Every comparison between rows is unpaired.

## Runs with full reports

| Date | Run | Deck | Pilot | Match win | p (play) | q (draw) | Time | Code reused | Known problems found later |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-19 | `cg64` | Cosmogoyf, revised: Hierarch, Tangle, Sell-Sword, Starting Town (list below) | 6.4 | 55.6% ± 1.5 | 61.50% ± 1.5 | 45.90% ± 1.4 | 2 h 50 min | Mulligan and measurement code from `gf63`; engine design followed `gf63`. Disclosed in the corrected report | 4-card floor (77 draw and 38 play games kept a 4-card hand valued under 0.10). The win credit cannot see setup mana, so Tangle and Hierarch are undervalued there |
| 2026-11-19 | `gf63` | Cosmogoyf / Thud / Serum Powder, original (list below) | 6.3 | 34.2% ± 1.4 | 49.85% ± 1.5 | 29.10% ± 1.3 | 2 h 10 min | Mulligan and measurement code from `rs62`. Not disclosed | **End-step Plunge lookahead error:** the library after Plunge was rebuilt by rounding each card's share, usually 2 to 6 cards too few, so end-step Plunge lines were undervalued. Devourer of Destiny always kept a card (never exiled all four). 4-card floor. The result is probably somewhat low |
| — | `rs62` | Swiftspear / Leyline of Resonance / Fortifying Draught | 6.2 | 48.8% ± 1.9 | 57.15% ± 1.8 | 41.30% ± 1.6 | about 2 h | Mulligan code "as in the Druid run" (stated in its code, not its report) | 4-card floor |
| — | `dr61` | Devoted Druid | 6.1 | 68.0% ± 1.3 | 74.15% ± 1.0 | 49.80% ± 1.4 | about 35 min | Not recorded in the report. The extent of reuse was not checked | 4-card floor |
| — | `ts61` | Four-color Tainted Strike pump (with Starting Town) | 6.1 | 88.5% ± 0.8 | 89.75% ± 1.08 | 66.50% ± 0.96 | about 22 min | Not recorded in the report. The extent of reuse was not checked | 4-card floor |

The dates of the 6.1 and 6.2 runs are not in their reports.

## Earlier results, as quoted in later reports

These have no report in the current format. They are listed only because later reports compare against them.

| Run | Deck | Pilot | Match win | p | q |
|---|---|---|---|---|---|
| `ts60` | Four-color Tainted Strike pump | 6.0 | 85.55% | 86.95% | 63.95% |
| Druid run of Nov 15 | Devoted Druid | older | 65.0% | 72.65% | 47.2% |
| `dz` | Swiftspear / Leyline of Resonance / Fortifying Draught | 4.5 engine | 50.2% | 56.8% | 43.4% |

## Decklists of the Cosmogoyf runs

**`gf63` (original):** 4 Cosmogoyf, 2 Fling, 2 Providence, 4 Thud, 4 Serum Powder, 4 Chancellor of the Dross, 4 Plunge into Darkness, 4 Devourer of Destiny, 4 Spoils of the Vault, 4 Summoner's Pact; 4 Gemstone Caverns, 1 Swamp, 1 Blightstep Pathway, 4 Blackcleave Cliffs, 4 Blooming Marsh, 2 Cavern of Souls, 1 Darkbore Pathway, 4 Gemstone Mine, 1 Boseiju, Who Endures, 2 Copperline Gorge.

**`cg64` (revised):** 4 Cosmogoyf, 4 Thud, 2 Callous Sell-Sword, 4 Ignoble Hierarch, 4 Chancellor of the Tangle, 4 Serum Powder, 4 Plunge into Darkness, 4 Spoils of the Vault, 4 Summoner's Pact, 2 Devourer of Destiny; 4 Gemstone Caverns, 4 Gemstone Mine, 4 Blackcleave Cliffs, 4 Blooming Marsh, 4 Copperline Gorge, 2 Starting Town, 1 Blightstep Pathway, 1 Darkbore Pathway.

## Open items

- **Mulligan floor:** whether to let mulligans go below 4 cards, and what `pilot.md` should say about it. Undecided.
- **Fair Cosmogoyf comparison:** rerun the original list under the current pilot on the same deals as the revised list, adding one change at a time (mana, Tangle, Hierarch). Not yet approved.
- **Earlier reports:** whether to add the code-reuse caveat to the `ts61`, `dr61`, `rs62` and `gf63` reports. Undecided.
- **Seeds:** derive them from integers, as `pilot.md` 1.6 requires, starting with the next run's new code.
