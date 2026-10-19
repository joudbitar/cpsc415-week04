# Spec

## Intent
Implements `intent/ask-the-course.md`.

## Components

### indexer
- **What it does:** reads the course pages, splits each page into chunks at Markdown headings (long sections split again at paragraph breaks, about 1,200 characters at most), embeds every chunk, and saves `index.json` with the source file, heading, text and vector of each chunk.
- **Language:** Python 3.9+, standard library only. **Why:** Weeks 2 and 3 already make the OpenRouter HTTP call with `urllib`, and the JSON index needs only the `json` module. Java was the alternative; it needs a JSON library and more code for the same thing.
- **Model:** `openai/text-embedding-3-small` through OpenRouter's embeddings endpoint. **Why:** cheap ($0.02 per million tokens, the whole course is about 30k tokens, so a full index costs under a tenth of a cent) and widely used. The alternative is `openai/text-embedding-3-large`: better on fine distinctions, 6.5 times the price, not needed for a few hundred chunks of plain English.
- **Interfaces:** `python3 index.py [--course ../ai-integration-course]` writes `index.json` and prints the chunk count per file and in total.
- **Dependencies:** none beyond the Python standard library.

### asker
- **What it does:** embeds the question with the same embedding model, ranks every chunk by cosine similarity, takes the top 5, prints them with their scores and sources, and asks a chat model to answer only from those excerpts with citations.
- **Language:** Python 3.9+, standard library only. **Why:** same as the indexer; both share one `rag.py` module.
- **Model:** `minimax/minimax-m3` (`CHAT_MODEL`). **Why:** the class model; in Week 3 it matched `xiaomi/mimo-v2.6-flash` on the five cases at about $0.0003 a call. The eval also runs once without retrieval to show what the model says from its own knowledge.
- **Interfaces:**
  - `python3 ask.py "<question>"` prints the retrieved chunks (rank, score, file, heading), then the answer with cited files.
  - `python3 ask.py --no-retrieval "<question>"` sends the question with no excerpts.
  - `python3 eval.py [--no-retrieval]` runs `questions.json` and prints PASS or FAIL per question plus a summary.
  - Environment: `OPENROUTER_API_KEY` (required), `CHAT_MODEL` (default `minimax/minimax-m3`), `EMBED_MODEL` (default `openai/text-embedding-3-small`).
- **Dependencies:** none beyond the Python standard library.

## Behavior
1. The indexer reads only `syllabus.md`, `assignments/*.md` and `weeks/01`–`weeks/03`, and prints the chunk count.
2. Every answer prints the top 5 chunks with score (cosine similarity, 3 decimals), file path and heading, before the answer.
3. The answer cites the file path of each page it used.
4. When the excerpts do not contain the answer, the reply is exactly "I can't find that in the course documents."
5. The chat model is told to use only the excerpts and never its own knowledge.
6. `--no-retrieval` sends no excerpts, so the eval can compare.
7. `eval.py` checks each answer against the expected key phrase in `questions.json` (case-insensitive) and prints PASS or FAIL.

## Failure handling
- **Missing key:** names `OPENROUTER_API_KEY` and exits before any call.
- **Missing `index.json`:** tells the user to run `index.py` first.
- **Course folder not found or fewer than 20 chunks:** the indexer exits with an error (the wrong-folder mistake the lab warns about).
- **HTTP error or 60-second timeout:** prints the status and exits non-zero; the eval marks that question FAIL and continues.
- **Empty model reply:** printed as `(empty reply)`; counts as FAIL. `max_tokens` is 800 because MiniMax M3 spends part of it on hidden reasoning.

## Cost estimate
Indexing: about 30k tokens once, under $0.001. Per question: one embedding call (about 20 tokens) plus about 2,000 tokens in and 300 out on the chat model, roughly $0.001. A semester of 200 questions is about $0.20.

## Out of scope
Carried over from the intent. Also ruled out: a vector database (a JSON file and a linear scan over a few hundred vectors is enough) and a RAG framework (the lab requires printing chunks and scores, which is easier by hand).
