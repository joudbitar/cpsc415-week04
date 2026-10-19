"""Five-question eval. Usage: python3 eval.py [--no-retrieval]"""
import argparse
import json

import rag
from ask import answer

parser = argparse.ArgumentParser()
parser.add_argument("--no-retrieval", action="store_true")
args = parser.parse_args()
cfg = rag.settings()

questions = json.load(open("questions.json"))
passed = 0
for q in questions:
    reply, hits = answer(q["question"], cfg, retrieval=not args.no_retrieval, show=False)
    ok = all(p.lower() in reply.lower() for p in q["expect"])
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  {q['id']}  {q['question']}")
    print(f"      reply: {' '.join(reply.split())[:240]}")
    if hits:
        print("      chunks: " + ", ".join(f"{s:.3f} {c['file']}" for s, c in hits))
mode = "without retrieval" if args.no_retrieval else "with retrieval"
print(f"\n{passed}/{len(questions)} passed {mode} ({cfg['chat_model']}, {cfg['embed_model']})")
