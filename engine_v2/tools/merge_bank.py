"""Merge content/bank_*.json into content/bank.json and validate the schema."""
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ("id", "pillar", "formats", "hook", "body", "idea_group")

bank, errors = [], []
for f in sorted(glob.glob(str(ROOT / "content" / "bank_p*.json"))
                + glob.glob(str(ROOT / "content" / "bank_legacy.json"))):
    bank += json.loads(Path(f).read_text())

seen = set()
cfg = json.loads((ROOT / "content" / "pillars.json").read_text())
pillar_ids = {p["id"] for p in cfg["pillars"]}
banned = [b.lower() for b in cfg["brand"]["banned_phrases"]]

for p in bank:
    for k in REQUIRED:
        if not p.get(k):
            errors.append(f"{p.get('id','?')}: missing {k}")
    if p["id"] in seen:
        errors.append(f"{p['id']}: duplicate id")
    seen.add(p["id"])
    if p["pillar"] not in pillar_ids:
        errors.append(f"{p['id']}: unknown pillar {p['pillar']}")
    if "reel" in p["formats"] and not p.get("reel_script"):
        errors.append(f"{p['id']}: reel format with no reel_script "
                      f"(this is the carousel-posted-as-a-reel bug)")
    if "carousel" in p["formats"] and not p.get("slides"):
        errors.append(f"{p['id']}: carousel format with no slides")
    if p.get("keyword") and p["keyword"] not in cfg["lead_magnets"]:
        errors.append(f"{p['id']}: keyword {p['keyword']} has no lead magnet")
    blob = json.dumps(p).lower()
    for b in banned:
        if b in blob:
            errors.append(f"{p['id']}: banned phrase '{b}'")
    if len(p["formats"]) != 1:
        errors.append(f"{p['id']}: a piece must declare exactly ONE format "
                      f"(got {p['formats']}) — multi-format pieces are how the "
                      f"same idea ends up as both a carousel and a reel")
    if len(p["hook"]) > 140:
        errors.append(f"{p['id']}: hook is {len(p['hook'])} chars — trim to <140")

if errors:
    print("VALIDATION FAILED")
    for e in errors:
        print("  -", e)
    sys.exit(1)

(ROOT / "content" / "bank.json").write_text(json.dumps(bank, indent=1, ensure_ascii=False))
print(f"OK — {len(bank)} pieces merged into content/bank.json")
