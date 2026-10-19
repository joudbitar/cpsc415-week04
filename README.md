# cpsc415-week04: ask the course

Answers questions about CPSC 415 from the course's own Markdown pages, prints the chunks it retrieved with their scores, cites the pages it used, and replies "I can't find that in the course documents." when the pages don't say.

The artifact chain is in [`intent/ask-the-course.md`](intent/ask-the-course.md), [`spec.md`](spec.md) and [`plan.md`](plan.md). The plan was approved and committed before the first code commit.

## run it

Python 3.9 or later, standard library only. Clone the course repo next to this one as `../ai-integration-course`.

```bash
export OPENROUTER_API_KEY=...        # or put OPENROUTER_API_KEY=... in .env (gitignored)
python3 index.py                     # builds index.json from the course pages
python3 ask.py "When is Team Project 1 due?"
python3 eval.py                      # five questions with retrieval
python3 eval.py --no-retrieval       # same questions, no excerpts
```

Optional: `CHAT_MODEL` (default `minimax/minimax-m3`), `EMBED_MODEL` (default `openai/text-embedding-3-small`). `index.json` is gitignored. Rebuild it with `python3 index.py`.

## the five questions

In [`questions.json`](questions.json):

1. When is Team Project 1 due? Checks a date that sits in one place.
2. What percentage of the grade is the Individual Portfolio? Checks a number from the grading table.
3. In the Week 3 lab, which variable do you change to run a second model? Checks a step inside one lab handout.
4. When is Team Project 1 due, and how many late days does each student get? The answer needs two pages, the project sheet and the syllabus.
5. Where should CPSC 415 students park? The pages don't say, so the right answer is the refusal. This catches a model that makes things up.

## results

Pending. The eval did not run before the deadline because both of my OpenRouter keys were dead (expired, and an account that no longer exists). The chunker ran offline: 148 chunks from 15 pages, with nothing from Week 4. Details and the empty result tables are in [`CHECKS.md`](CHECKS.md).

## stale page

`weeks/01/setup.md` says the fallback is `xiaomi/mimo-v2.5`. `weeks/03/lab.md` uses `xiaomi/mimo-v2.6-flash`. What the program answers is pending the eval run. The fix I'd try: tag each chunk with its file's last commit date and tell the model to trust the newest excerpt when two disagree.

## one line I can explain

`rag.py:106`

```python
scored = [(cosine(question_vec, c["vector"]), c) for c in index]
```

This is where chunks get ranked. Every chunk's vector is compared with the question's vector by cosine similarity, the cosine of the angle between them. 1.0 means they point the same way (same meaning), and near 0 means unrelated. The next line sorts by that score and keeps the top 5. Those 5 are the only text the model sees.
