# Intent: ask the course

## Goal
A command-line program that answers a question about CPSC 415 using only the course's own Markdown pages, names the pages it used, and replies "I can't find that in the course documents" when the pages do not contain the answer.

## Who it is for
A student in the course. Today they search the syllabus, assignment sheets and lab handouts by hand, or ask a chat model that has never seen the pages and makes up dates.

## Constraints
- Documents: `../ai-integration-course`: `syllabus.md`, `assignments/`, `weeks/01` to `weeks/03`. Skip `weeks/04` and later. Read from the clone, never copy pages into this repo.
- Models through OpenRouter, key in `OPENROUTER_API_KEY`. No key in the repo.
- Every answer prints the retrieved chunks and their scores.
- Cost: under one cent per question.
- Deadline: October 19, 2026, 1:30 PM.

## Not in scope
- A web interface.
- Updating the index automatically when the course repo changes.
- Fixing stale pages (we record the problem only).

**Approved by:** Joud Bitar, 2026-10-19
