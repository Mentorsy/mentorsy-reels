"""Merge the migrated legacy pieces with the new bank and remove every
cross-bank near-duplicate. Nothing survives that says what another piece
already says, in any format."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from migrate_legacy import toks, jac, containment

NEW = json.load(open(os.path.join(HERE, "..", "content", "bank.json")))
LEG = json.load(open(os.path.join(HERE, "..", "content", "_legacy_pieces.json")))

for p in NEW:                       # every authored piece is its own idea
    p.setdefault("idea_group", f"NEW-{p['id']}")
    p.setdefault("source", "authored 2026-08")

def text(p):
    return " ".join([p.get("hook", ""), p.get("body", "")]
                    + (p.get("slides") or []) + [p.get("reel_script", "")])

ALL = NEW + LEG
T = {p["id"]: toks(text(p)) for p in ALL}

CONTAIN_LIMIT = 0.40     # how much of the shorter piece may already exist elsewhere
JACCARD_LIMIT = 0.30

# Text similarity cannot see a CONCEPTUAL twin: two pieces that share no
# vocabulary but make the same point. These were found by reading the closest
# pairs by hand. Giving them one idea_group lets the scheduler's idea gate keep
# them months apart instead of in the same week.
CONCEPT_TWINS = {
    "ASK-BETTER-QUESTIONS": ["P1-10", "L22R"],
    "AI-AND-HOMEWORK":      ["L12C", "L40C"],
    "CHOOSING-A-SCHOOL":    ["L11R", "L21R"],
    "ESSAY-ARCHITECTURE":   ["P2-07", "P2-13"],
    "WHAT-A-SESSION-IS":    ["L28C", "L38C"],
}

collisions, drop = [], set()
for i, a in enumerate(ALL):
    if a["id"] in drop:
        continue
    for b in ALL[i + 1:]:
        if b["id"] in drop:
            continue
        c, j = containment(T[a["id"]], T[b["id"]]), jac(T[a["id"]], T[b["id"]])
        if c >= CONTAIN_LIMIT or j >= JACCARD_LIMIT:
            # Keep the richer piece: prefer a real reel script or real slides,
            # then the longer body.
            def weight(p):
                return (bool(p.get("reel_script")) + bool(p.get("slides")),
                        len(p.get("body", "")))
            loser = b if weight(a) >= weight(b) else a
            winner = a if loser is b else b
            drop.add(loser["id"])
            collisions.append((winner["id"], loser["id"], round(c, 2), round(j, 2),
                               loser["hook"][:64]))
            if loser is a:
                break

KEPT = [p for p in ALL if p["id"] not in drop]

# Apply the hand-found conceptual groupings to whatever survived.
by_id = {p["id"]: p for p in KEPT}
merged_groups = 0
for group, ids in CONCEPT_TWINS.items():
    present = [i for i in ids if i in by_id]
    if len(present) > 1:
        for i in present:
            by_id[i]["idea_group"] = group
        merged_groups += 1
json.dump(KEPT, open(os.path.join(HERE, "..", "content", "bank_legacy.json"), "w"), indent=1, ensure_ascii=False)

from collections import Counter
print(f"in : {len(NEW)} authored + {len(LEG)} migrated legacy = {len(ALL)}")
print(f"dropped as near-duplicates: {len(drop)}")
print(f"final bank: {len(KEPT)} pieces")
print()
print("formats  :", Counter(f for p in KEPT for f in p["formats"]))
print("pillars  :", Counter(p["pillar"] for p in KEPT))
print("subjects :", Counter(p.get("subject") for p in KEPT))
print("sources  :", Counter(p["source"] for p in KEPT))
print(f"concept-twin groups applied: {merged_groups}")
gc = Counter(p["idea_group"] for p in KEPT)
print(f"distinct ideas: {len(gc)} across {len(KEPT)} pieces "
      f"({sum(1 for v in gc.values() if v > 1)} ideas carry more than one piece)")
print()
if collisions:
    print(f"collisions removed ({len(collisions)}):")
    for w, l, c, j, hook in collisions:
        print(f"  kept {w:8} dropped {l:8} contain={c} jac={j}  | {hook}")
