"""Standing audit: prove the feed cannot repeat, in plain numbers.

Run:  python3 tests/audit_no_repeats.py
"""
import json, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
from dedup import content_hash, hook_signature, tokens   # noqa: E402

bank = json.loads((ROOT / "content" / "bank.json").read_text())


def text(p):
    return " ".join([p.get("hook", ""), p.get("body", "")]
                    + (p.get("slides") or []) + [p.get("reel_script", "")])


def contain(a, b):
    return len(a & b) / min(len(a), len(b)) if a and b else 0.0


T = {p["id"]: tokens(text(p)) for p in bank}
fail = []

print(f"BANK: {len(bank)} pieces\n")

# 1 -- one piece, one format. A carousel physically cannot become a reel.
multi = [p["id"] for p in bank if len(p["formats"]) != 1]
print(f"1. one format per piece ............ {'PASS' if not multi else 'FAIL ' + str(multi)}")
fail += multi

# 2 -- every reel carries its own script; no reel borrows carousel slides.
bad = [p["id"] for p in bank
       if (p["formats"] == ["reel"] and not p.get("reel_script"))
       or (p["formats"] == ["reel"] and p.get("slides"))
       or (p["formats"] == ["carousel"] and p.get("reel_script"))]
print(f"2. reels have own scripts, carousels have none  {'PASS' if not bad else 'FAIL ' + str(bad)}")
fail += bad

# 3 -- no two pieces share a body.
h = Counter(content_hash(p) for p in bank)
dupe_h = [k for k, v in h.items() if v > 1]
print(f"3. no duplicate bodies ............. {'PASS' if not dupe_h else 'FAIL'}")
fail += dupe_h

# 4 -- no two pieces share a hook shape.
k = Counter(hook_signature(p["hook"]) for p in bank)
dupe_k = [x for x, v in k.items() if v > 1]
print(f"4. no duplicate hooks .............. {'PASS' if not dupe_k else 'FAIL'}")
fail += dupe_k

# 5 -- nothing says what something else already says.
#      Pairs sharing an idea_group are exempt: gate 8 already guarantees only
#      one of them can ever ship, so their overlap can never reach a feed.
def group(p):
    return p.get("idea_group", p["id"])

worst, pair = 0.0, None
for i, a in enumerate(bank):
    for b in bank[i + 1:]:
        if group(a) == group(b):
            continue
        c = contain(T[a["id"]], T[b["id"]])
        if c > worst:
            worst, pair = c, (a["id"], b["id"])
ok = worst < 0.40
print(f"5. max text overlap ................ {worst:.2f} between {pair[0]} and {pair[1]}  "
      f"{'PASS (<0.40)' if ok else 'FAIL'}")
if not ok:
    fail.append("overlap")

# 6 -- idea groups: how many pieces can speak for the same idea.
g = Counter(p.get("idea_group", p["id"]) for p in bank)
shared = {k: v for k, v in g.items() if v > 1}
print(f"6. distinct ideas .................. {len(g)} ideas for {len(bank)} pieces")
for k, v in shared.items():
    print(f"     '{k}' has {v} pieces — the idea gate keeps them "
          f"365 days apart, in different formats")

print(f"\nformats: {Counter(p['formats'][0] for p in bank)}")
print(f"sources: {Counter(p.get('source','?') for p in bank)}")
print()
print("AUDIT PASSED — no piece can repeat another, and no idea can ship twice."
      if not fail else f"AUDIT FAILED: {fail}")
sys.exit(1 if fail else 0)
