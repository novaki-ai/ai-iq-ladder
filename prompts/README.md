# Prompts, word for word

- **Today's models** got one page of six puzzles per call (7 pages), plus the chess puzzle as its own call, each starting with the same note. `todays-models-page-R1.txt` is page 1 exactly as sent; the other pages swap in the other rung's six puzzles. `todays-models-chess.txt` is the chess call.
- **TinyLlama and Qwen 2.5** got one puzzle per call (`chatbots-one-question-R1-2.txt`), inside their own chat template.
- **GPT-2** only continues text, so it got the grid with the last cell left open (`gpt2-completion-R1-2.txt`), the way Webb et al. tested GPT-3. Letter puzzles start with `Let's try to complete the pattern:` and a blank line; the chess puzzle ends with `The winning move is 1.`
- **ELIZA** got each puzzle flattened to one line in a fresh session. **The thermostat** and **Stockfish** read nothing but what they can read.
