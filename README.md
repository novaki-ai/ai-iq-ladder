# Same Test, 60 Years of AI

The questions, the answer key and every system's raw answers from the Novaki video **https://youtu.be/LLGYXMpPL80**.

One test, given to sixteen systems: from a one-rule thermostat and ELIZA (1966) to the models released this month.
You can take the test yourself in [`TEST.md`](TEST.md) (answers at the bottom), then compare with the machines in [`answers/`](answers/).

## The test

- **42 text puzzles on 7 rungs**, newly generated with the puzzle generators of Webb, Holyoak & Lu (2023, *Nature Human Behaviour*).
  Rungs 1, 2, 3 and 5 are digit matrices in the style of Raven's matrices; rungs 4, 6 and 7 are letter-string analogies with one, two and three twists.
- **The ladder is set by people.** Each rung is one puzzle type, ordered by how many UCLA students got that type right in the paper's released data
  (85% on rung 1, 28% on rung 7). A system climbs a rung if it does at least as well as the students did, and it can't skip a rung.
- **This is not an IQ test.** The students never saw these exact puzzles; it is a student baseline on the same kinds of puzzle, not a population norm.
- **One chess puzzle** (mate in two, Lichess, CC0) is added for systems that can only read chess. It is not part of the ladder or the 42-point total.
- The questions, the answer key and the scoring rules were locked with SHA-256 before the scored runs.

## Results

| System | Year | Effort | Correct (of 42) | Rungs climbed (of 7) | Chess | Time | Est. cost |
|---|---|---|---:|---:|:---:|---:|---:|
| Thermostat rule | 1880s idea |  | 0 | 0 | · |  |  |
| ELIZA (DOCTOR script) | 1966 |  | 0 | 0 | · |  |  |
| Stockfish 19 at 2850 (Deep Blue-strength stand-in) | 1997 |  | 0 | 0 | ✓ |  |  |
| GPT-2 XL 1.5B | 2019 |  | 11 | 0 | · |  |  |
| TinyLlama 1.1B Chat | 2023 |  | 1 | 0 | · |  |  |
| Qwen2.5 0.5B Instruct | 2024 |  | 3 | 0 | · |  |  |
| Claude Haiku 4.5 | 2025 | high | 36 | 7 | · | 7.8 min | $0.35 |
| Claude Sonnet 5.5 | 2026 | high | 33 | 7 | ✓ | 1.8 min | $0.12 |
| GPT-6.1 Sol | 2026 | high | 36 | 7 | ✓ | 2.5 min | $0.08 |
| Claude Haiku 5.5 | 2026 | high | 37 | 7 | ✓ | 2.9 min | $0.02 |
| GPT-6 Luna | 2026 | high | 37 | 7 | ✓ | 1.7 min | under 1¢ |
| Claude Opus 5.5 | 2026 | low | 37 | 7 | · | 1.7 min | $0.14 |
| Kimi K3.1 Pro | 2026 | max | 38 | 7 | ✓ | 42.5 min | $0.74 |
| Claude Opus 5.5 | 2026 | max | 39 | 7 | ✓ | 7.1 min | $0.91 |
| Gemini 4 Argon | 2026 | high | 42 | 7 | ✓ | 6.3 min | $0.43 |
| GPT-6 Astra | 2026 | max | 42 | 7 | ✓ | 6.4 min | $0.77 |

GPT-3's published result on the paper's own puzzles (not our run) is in [`results/gpt3-2022-published.json`](results/gpt3-2022-published.json):
it beat the students on six of the seven rungs and fell on the last one (24% against 28%).

## How each system was run

- **Today's models** answered through their own official tools (Claude Code, Codex CLI, Antigravity CLI, Kimi Code) with no tools allowed:
  one page of six puzzles per call, then the chess puzzle as a separate call. Effort level is in the table. Time and cost are per model for the whole test;
  cost is an estimate at API list prices.
- **GPT-2** only continues text, so it got each grid with the last cell left open, the way Webb et al. tested GPT-3.
- **TinyLlama** and **Qwen 2.5** got one puzzle at a time in their own chat template; **ELIZA** one puzzle per fresh session.
- **The thermostat** and **Stockfish** answer with what they can read; everything else stays blank.
- The exact prompts are in [`prompts/`](prompts/).

## Re-score it yourself

```
pip install chess
python3 score.py --check
```

`score.py` reads the raw replies in `answers/`, applies the fixed rules and compares the result with [`results/scores.json`](results/scores.json).

One puzzle worth arguing about: on rung 7, if `q r s t` becomes `q r s u`, what does `j x k x l x m x` become?
The key says `j x k x l x n x` (the x's are spacers). Seven of the ten runs of today's models said `j x k x l x m y`. Which would you give?

## Licenses

Questions, answers, results and text: [CC BY 4.0](LICENSE). Code (`score.py`): [MIT](LICENSE-CODE). Credits and third-party notes: [NOTICE](NOTICE).

Channel: [youtube.com/@Novaki_ai](https://www.youtube.com/@Novaki_ai) · [novaki.lol](https://novaki.lol)
