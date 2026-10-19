# Plan

## Files to create or change
| File | Purpose |
|---|---|
| `rag.py` | Shared code: settings from the environment, OpenRouter embeddings and chat calls, chunking, cosine similarity, top-k ranking. |
| `index.py` | Indexer CLI: walk the allowed course pages, chunk, embed in batches, write `index.json`. |
| `ask.py` | Asker CLI: embed the question, rank chunks, print them, ask the chat model. `--no-retrieval` flag. |
| `questions.json` | Five eval questions with an expected key phrase each. |
| `eval.py` | Runs the five questions with or without retrieval, prints PASS/FAIL. |
| `CHECKS.md` | Eval results both ways, the stale-page finding. |
| `README.md` | How to run, the questions, results, finding, one line explained. |
| `.gitignore` | Add `index.json` (rebuildable, large). |

## Order of work
1. `rag.py` + `index.py`. Build the index.
2. `ask.py`. Ask one question with a known answer.
3. `questions.json` + `eval.py`. Run with retrieval, then `--no-retrieval`.
4. Ask the stale-page question, record it.
5. `CHECKS.md`, `README.md`, commit, tag `week04-submitted`, push.

## Risks
- **Wrong folder or wrong glob:** the index is tiny or includes `weeks/04`. Noticed by the per-file chunk counts printed in step 1.
- **OpenRouter embeddings endpoint or model name not available:** step 1 fails on the first batch. Fallback: another embedding model slug via `EMBED_MODEL`.
- **Chunks too large or too small:** too large dilutes the score, too small splits a date from its heading. Each chunk keeps its heading text so a short chunk still says what it is about.
- **The model answers from its own knowledge instead of refusing:** the unanswerable question in the eval catches it.
- **Two pages disagree (old and new model):** the asker shows both chunks and the model may pick the wrong one. Recorded in step 4, not fixed.
- Blast radius is small: the program only reads the course clone and writes `index.json` here.

## Proof
1. `python3 index.py` prints per-file chunk counts; total is over 20 and no `weeks/04` file appears.
2. `python3 ask.py "When is Team Project 1 due?"` prints 5 chunks with scores, and the answer says November 2 and cites `assignments/team-project-1.md` or `syllabus.md`.
3. **The five-question eval:** `python3 eval.py` and `python3 eval.py --no-retrieval`. Expected: with retrieval at least 4 of 5 pass, including "I can't find that" on the unanswerable question; without retrieval, fewer pass. Both runs go in `CHECKS.md`.
4. The stale-page question prints the cited chunks; the finding goes in `CHECKS.md`.

## Questions asked of this plan
- **"How big is one chunk, and why that size?"** One Markdown section, split again past about 1,200 characters (roughly 300 tokens). A section is the unit the author wrote about one topic, and 300 tokens keeps a due date next to its heading. Changed in the plan: each chunk now carries its page title and heading so short chunks still match.
- **"What does the proof step actually run, and what output means it worked?"** The eval runs `eval.py` both ways and prints PASS/FAIL per question against an expected key phrase. Changed in the plan: Proof now names the pass threshold (4 of 5 with retrieval) and requires the refusal on question 5.

## Subagents and parallel work
None. Five small files in one order; parallel work would cost more than it saves.

**Approved by:** Joud Bitar, 2026-10-19
