"""Asker: answer a question from the course pages, printing the chunks it used.
Usage: python3 ask.py [--no-retrieval] "<question>" """
import argparse
import json
import sys

import rag

SYSTEM = (
    "You answer questions about the course CPSC 415 using ONLY the excerpts given. "
    "Do not use your own knowledge. Cite the file path of every excerpt you used, "
    f"like (syllabus.md). If the excerpts do not contain the answer, reply exactly: {rag.REFUSAL}"
)
SYSTEM_NO_RETRIEVAL = "You answer questions about the course CPSC 415 at Trinity College. Be brief."


def answer(question, cfg, retrieval=True, show=True):
    if not retrieval:
        return rag.chat(SYSTEM_NO_RETRIEVAL, question, cfg), []
    if not rag.INDEX_FILE.exists():
        sys.exit("index.json not found: run python3 index.py first")
    index = json.loads(rag.INDEX_FILE.read_text())["chunks"]
    hits = rag.top_chunks(rag.embed([question], cfg)[0], index)
    if show:
        print("Retrieved chunks:")
        for rank, (score, c) in enumerate(hits, 1):
            print(f"  {rank}. {score:.3f}  {c['file']}  > {c['heading']}")
    excerpts = "\n\n".join(f"[{c['file']}]\n{c['text']}" for _, c in hits)
    reply = rag.chat(SYSTEM, f"Excerpts:\n\n{excerpts}\n\nQuestion: {question}", cfg)
    return reply, hits


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--no-retrieval", action="store_true")
    args = parser.parse_args()
    reply, _ = answer(args.question, rag.settings(), retrieval=not args.no_retrieval)
    print("\nAnswer:\n" + reply)
