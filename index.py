"""Indexer: chunk the course pages, embed them, save index.json.
Usage: python3 index.py [--course ../ai-integration-course]"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import rag

parser = argparse.ArgumentParser()
parser.add_argument("--course", default="../ai-integration-course")
args = parser.parse_args()
cfg = rag.settings()

root = Path(args.course).resolve()
if not (root / "syllabus.md").exists():
    sys.exit(f"course folder not found: {root}")
pages = [root / "syllabus.md", *sorted((root / "assignments").glob("*.md"))]
for week in ("01", "02", "03"):
    pages += sorted((root / "weeks" / week).glob("*.md"))
# The course as it stood before this lab: skip assignment sheets for week 4 and later.
pages = [p for p in pages if not p.name.startswith(("week04", "week05", "week06"))]

chunks = []
for page in pages:
    chunks += rag.chunk_page(str(page.relative_to(root)), page.read_text())
if len(chunks) < 20:
    sys.exit(f"only {len(chunks)} chunks: wrong course folder?")

for start in range(0, len(chunks), 64):
    batch = chunks[start:start + 64]
    for chunk, vec in zip(batch, rag.embed([c["text"] for c in batch], cfg)):
        chunk["vector"] = vec

rag.INDEX_FILE.write_text(json.dumps({"embed_model": cfg["embed_model"], "chunks": chunks}))
for file, n in Counter(c["file"] for c in chunks).items():
    print(f"{n:4d}  {file}")
print(f"{len(chunks)} chunks from {len(pages)} pages -> {rag.INDEX_FILE.name}")
