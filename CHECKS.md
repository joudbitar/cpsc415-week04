# Checks

## timeline

The code, questions, intent, spec and plan were tagged `week04-submitted` at 1:17 PM on October 19, before the eval ran. Both OpenRouter keys I had were dead (one `401 API key expired`, the other `401 User not found`). I made a new key after class and ran everything below that evening. These results come in a commit after the tag.

## index

`python3 index.py` read 15 pages and wrote 148 chunks: 40 from `syllabus.md`, 4 to 8 from each assignment sheet, and 5 to 18 from each weeks/01 to 03 page. No `weeks/04` file and no Week 4 or later assignment sheet is in the list. Embedding model `openai/text-embedding-3-small`.

## five-question eval

Chat model `minimax/minimax-m3`, top 5 chunks.

| Question | With retrieval | Top chunk score | Without retrieval |
|---|---|---|---|
| due-date: When is Team Project 1 due? | PASS, November 2, cites `assignments/team-project-1.md` | 0.612 | FAIL, says it has no access to the syllabus |
| grade-weight: Portfolio share of the grade? | PASS, 25%, cites `syllabus.md` and `assignments/portfolio.md` | 0.630 | FAIL, no number |
| lab-step: Week 3 variable for a second model? | PASS, `CHAT_MODEL`, cites `weeks/03/lab.md` | 0.544 | FAIL, guesses `MODEL_NAME` or `MODEL_ID` |
| spread: TP1 due date and late days | PASS, November 2 and 3 late days, from two pages | 0.601 | FAIL, no facts |
| unanswerable: Where do students park? | PASS, exact refusal | 0.392 | FAIL, no exact refusal phrase, points to Moodle and the department |

With retrieval: 5/5. Without retrieval: 0/5.

Without excerpts the model mostly said it didn't know, which is honest but useless. The one place it made something up was the lab step, where it guessed variable names that aren't in the lab. The parking question fails without retrieval only on the exact phrase: it didn't invent a parking lot, it just didn't use the refusal sentence it was never told about.

The unanswerable question's best chunk scored 0.392. Every answerable question's best chunk scored 0.544 or higher. A score cutoff around 0.45 would let the program refuse without calling the chat model at all. I didn't add one; the refusal comes from the prompt.

## stale page

Question: "Which Xiaomi MiMo model does this course use as the fallback or second model?"

Retrieved chunks:

```
1. 0.423  weeks/03/lab.md    > 4. The second model (5 minutes)
2. 0.385  weeks/01/setup.md  > 1. Accounts and a small budget
3. 0.377  syllabus.md        > Computing Resources
4. 0.361  weeks/02/setup.md  > 3. Optional: a local model
5. 0.359  weeks/01/setup.md  > 1. Accounts and a small budget
```

The program didn't pick one. It reported both: `xiaomi/mimo-v2.5` as the instructor fallback, citing `weeks/01/setup.md`, and `xiaomi/mimo-v2.6-flash` as the Week 3 second model, citing `weeks/03/lab.md`. Those are the only two chunks in the index that mention MiMo, and both were retrieved. Nothing in the answer says which one is current. A student would have to guess, and the Week 1 page is the one that was never updated after the September 28 change.

One way to prefer the current page: store each file's last git commit date on its chunks, put that date in each excerpt's header, and tell the model that when excerpts disagree, the newest one wins and the older one gets flagged as possibly stale.
