"""Runs sample texts through the analyzer and reports validity and claim coverage."""
import json

from llm_client import analyze

with open("samples/samples.json", encoding="utf-8") as f:
    samples = json.load(f)

passed = 0
for s in samples:
    try:
        result = analyze(s["text"])
    except Exception as e:
        print(f"[FAIL] {s['name']}: {e}")
        continue
    found = " ".join(c.claim.lower() for c in result.claims)
    enough = len(result.claims) >= s["min_claims"]
    keywords_ok = all(k.lower() in found for k in s["keywords"])
    ok = enough and keywords_ok
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] {s['name']}: {len(result.claims)} claims, keywords_ok={keywords_ok}")

print(f"\n{passed}/{len(samples)} samples passed")