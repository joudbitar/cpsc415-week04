"""Shared code for the indexer and the asker: OpenRouter calls, chunking, ranking."""
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "https://openrouter.ai/api/v1"
INDEX_FILE = Path(__file__).with_name("index.json")
MAX_CHARS = 1200
TOP_K = 5
REFUSAL = "I can't find that in the course documents."


def load_dotenv(path=Path(__file__).with_name(".env")):
    """Read KEY=value lines from .env (gitignored) without overriding the shell."""
    if path.exists():
        for line in path.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("\"'"))


def settings(env=os.environ):
    load_dotenv()
    key = env.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("missing environment variable: OPENROUTER_API_KEY")
    return {
        "key": key,
        "chat_model": env.get("CHAT_MODEL", "minimax/minimax-m3"),
        "embed_model": env.get("EMBED_MODEL", "openai/text-embedding-3-small"),
    }


def post(path, body, key):
    req = urllib.request.Request(
        BASE_URL + path,
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        sys.exit(f"HTTP {err.code} from {path}: {err.read().decode()[:300]}")
    except (urllib.error.URLError, TimeoutError) as err:
        sys.exit(f"request to {path} failed: {err}")


def embed(texts, cfg):
    data = post("/embeddings", {"model": cfg["embed_model"], "input": texts}, cfg["key"])
    return [item["embedding"] for item in sorted(data["data"], key=lambda d: d["index"])]


def chat(system, user, cfg):
    data = post("/chat/completions", {
        "model": cfg["chat_model"],
        "max_tokens": 800,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
    }, cfg["key"])
    return (data["choices"][0]["message"].get("content") or "").strip() or "(empty reply)"


def chunk_page(path, text):
    """Split one Markdown page at headings, then at paragraphs past MAX_CHARS.
    Each chunk starts with the page title and heading so short chunks still match."""
    title = next((l.lstrip("# ").strip() for l in text.splitlines() if l.startswith("# ")), path)
    sections, heading, lines = [], title, []
    for line in text.splitlines():
        if re.match(r"#{1,4} ", line):
            if lines:
                sections.append((heading, "\n".join(lines).strip()))
            heading, lines = line.lstrip("# ").strip(), []
        else:
            lines.append(line)
    if lines:
        sections.append((heading, "\n".join(lines).strip()))

    for heading, body in sections:
        chunks = []
        if not body:
            continue
        piece = ""
        for para in body.split("\n\n"):
            if piece and len(piece) + len(para) > MAX_CHARS:
                chunks.append(piece)
                piece = ""
            piece = f"{piece}\n\n{para}" if piece else para
        if piece:
            chunks.append(piece)
        for c in chunks:
            yield {"file": path, "heading": heading, "text": f"{title} > {heading}\n{c}"}


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def top_chunks(question_vec, index, k=TOP_K):
    """Rank every chunk by cosine similarity to the question; keep the best k."""
    scored = [(cosine(question_vec, c["vector"]), c) for c in index]
    return sorted(scored, key=lambda s: s[0], reverse=True)[:k]
