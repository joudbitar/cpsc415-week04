# Checks

## status at submission (October 19, 1:30 PM)

The eval has not run yet. Both OpenRouter keys I had on disk were dead when I got to the run: one returned `401 API key expired`, the other `401 User not found`. The code, the questions and the plan were done. I'll make a new key, run the eval both ways and fill in the tables below in a follow-up commit.

## offline check (no API calls)

The chunker ran without the embedding step: 15 pages, 148 chunks, the longest 2,311 characters (one long paragraph that has no break to split on). The pages are `syllabus.md`, `assignments/portfolio.md`, `assignments/team-project-1.md`, the Week 1 to 3 assignment sheets, and the README, lab and setup pages for weeks 01 to 03. No `weeks/04` file and no Week 4 or later assignment sheet is in the list. This passes plan proof step 1 for the file list and chunk count. The embedding half still has to run.

## five-question eval

| Run | Passed | Failures and the chunks they cited |
|---|---|---|
| With retrieval (`python3 eval.py`) | pending | pending |
| Without retrieval (`python3 eval.py --no-retrieval`) | pending | pending |

## stale page

Question: "Which Xiaomi MiMo model does this course use as the fallback or second model?"

Two indexed pages disagree. `weeks/01/setup.md` names `xiaomi/mimo-v2.5` as the instructor fallback. `weeks/03/lab.md` has students switch `CHAT_MODEL` to `xiaomi/mimo-v2.6-flash`. I found these by searching the pages, not by running the program, so what the program answers and which chunks it cites are still pending.

One way to prefer the current page: store each file's last git commit date on its chunks, put the date in each excerpt header, and tell the model that when excerpts disagree, the newest one wins.
