"""Port the 60 legacy Mentorsy entries into the new one-idea-one-piece schema.

The legacy bank pairs a post and a reel inside every entry, and measurement
shows 85% of those pairs are the same argument told twice (median token
similarity 0.49, max 0.88). That pairing is the "reels made from carousels"
complaint, so the migration's job is to collapse each pair to ONE piece unless
the two halves are genuinely different.
"""
import json, os, re, sys

# Point this at a checkout of github.com/Mentorsy/mentorsy-reels.
LEGACY_REPO = os.environ.get("LEGACY_REPO", "../mentorsy-reels")
sys.path.insert(0, LEGACY_REPO)

from content_a import DAYS_A
from content_b import DAYS_B
from content_2026_09 import DAYS_C

BANK = DAYS_A + DAYS_B + DAYS_C

PILLAR_MAP = {
    "Parent Scripts": "P1",       # naming what a grade actually means
    "Confidence": "P1",
    "Inside the Method": "P3",    # how we teach / proof
    "Curriculum Decoded": "P4",
    "School Choice": "P4",
    "Future Skills": "P2",        # teaches something
}
SUBJECT_MAP = {
    "Mathematics": "Mathematics", "Science": "Science", "French": "French",
    "Coding": "Coding", "Public Speaking": "Public Speaking",
    "AI": "Coding",               # folded in: same hashtag pool, same parent question
    "Mentorsy": "General",
}

STOP = set("a an the and or but if of to in on for with is are was were be been it its this that these those you your they them their we our i my at as by from not no do does did so than then there here what how why when".split())


def toks(t):
    t = re.sub(r"[^a-z0-9\s]", " ", str(t).lower())
    return {w for w in t.split() if w not in STOP and len(w) > 2}


def jac(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0


def containment(a, b):
    """|A n B| / min(|A|,|B|).

    Jaccard hides this failure: when the reel is a short restatement of a long
    post, the union is dominated by the post's extra words and the score looks
    safe. Containment asks the honest question -- how much of the SHORTER piece
    is already inside the longer one. Median across the legacy bank: 0.84.
    """
    return len(a & b) / min(len(a), len(b)) if a and b else 0.0


def points_of(d):
    out = []
    for p in d.get("points", []) or []:
        if isinstance(p, dict):
            h = p.get("heading", "")
            b = p.get("body", "") or p.get("detail", "")
            out.append(f"{h} — {b}".strip(" —") if b else h)
        else:
            out.append(str(p))
    return [x for x in out if x]


def blob(d):
    return " ".join([d.get("hook", ""), d.get("caption", "")] + points_of(d)
                    + list(d.get("beats", []) or []))


def script_from_beats(hook, beats, cta):
    """A reel script written from the reel's own beats — never from slides."""
    lines = [f"HOOK (0-4s): {hook}"]
    t = 4
    for b in beats:
        nxt = t + max(5, min(9, len(b) // 6))
        lines.append(f"BEAT ({t}-{nxt}s): {b}")
        t = nxt
    lines.append(f"CTA ({t}-{t+5}s): {cta}")
    return "\n".join(lines)


def as_reel(e, i):
    r = e["reel"]
    return {
        "id": f"L{i:02d}R",
        "idea_group": f"LEG{i:02d}",
        "pillar": PILLAR_MAP.get(r.get("pillar"), "P1"),
        "subject": SUBJECT_MAP.get(r.get("subject"), "General"),
        "formats": ["reel"],
        "hook": r.get("hook", "").strip(),
        "body": (r.get("caption", "") or "").strip(),
        "reel_script": script_from_beats(r.get("hook", ""),
                                         list(r.get("beats", []) or []),
                                         r.get("cta", "Link in bio.")),
        "source": "legacy reel",
    }


def as_carousel(e, i):
    p = e["post"]
    pts = points_of(p)
    return {
        "id": f"L{i:02d}C",
        "idea_group": f"LEG{i:02d}",
        "pillar": PILLAR_MAP.get(p.get("pillar"), "P1"),
        "subject": SUBJECT_MAP.get(p.get("subject"), "General"),
        "formats": ["carousel"],
        "hook": p.get("hook", "").strip(),
        "body": (p.get("caption", "") or "").strip(),
        "slides": [p.get("hook", "").strip()] + pts + [p.get("cta", "").strip()],
        "source": "legacy post",
    }


def as_single(e, i):
    p = e["post"]
    return {
        "id": f"L{i:02d}S",
        "idea_group": f"LEG{i:02d}",
        "pillar": PILLAR_MAP.get(p.get("pillar"), "P1"),
        "subject": SUBJECT_MAP.get(p.get("subject"), "General"),
        "formats": ["single"],
        "hook": p.get("hook", "").strip(),
        "body": (p.get("caption", "") or "").strip(),
        "source": "legacy post",
    }


# Measured across all 60 legacy entries: containment median 0.84, and 87% of
# pairs score >= 0.70 -- literally the same post twice. Not one pair came in
# under 0.30. So no entry keeps both halves; every one collapses to a single
# piece. This is the structural fix for "reels made from carousels".
KEEP_BOTH_BELOW = 0.0

def migrate():
    pieces, log = [], []
    # Target mix mirrors the slot mix: 5 reels / 3 carousels / 2 singles a week.
    carousel_budget = 22
    for i, e in enumerate(BANK):
        p, r = e["post"], e["reel"]
        sim = containment(toks(blob(p)), toks(blob(r)))
        pts = points_of(p)

        if sim < KEEP_BOTH_BELOW:
            pieces += [as_reel(e, i), as_carousel(e, i) if len(pts) >= 3 else as_single(e, i)]
            log.append((i, round(sim, 2), "kept BOTH (genuinely different angles)"))
            continue

        # One survivor. Prefer carousel while budget lasts and there is real
        # slide material; otherwise the reel, because reels are the scarce slot.
        if len(pts) >= 4 and carousel_budget > 0:
            pieces.append(as_carousel(e, i)); carousel_budget -= 1
            log.append((i, round(sim, 2), "collapsed -> carousel (reel twin dropped)"))
        elif r.get("beats"):
            pieces.append(as_reel(e, i))
            log.append((i, round(sim, 2), "collapsed -> reel (post twin dropped)"))
        else:
            pieces.append(as_single(e, i))
            log.append((i, round(sim, 2), "collapsed -> single (reel twin dropped)"))
    return pieces, log


if __name__ == "__main__":
    pieces, log = migrate()
    json.dump(pieces, open(os.path.join(os.path.dirname(__file__), "..", "content", "_legacy_pieces.json"), "w"),
              indent=1, ensure_ascii=False)
    from collections import Counter
    print(f"legacy entries in : {len(BANK)}  (=> {len(BANK)*2} raw post/reel halves)")
    print(f"unique pieces out : {len(pieces)}")
    print(f"halves discarded  : {len(BANK)*2 - len(pieces)} duplicate twins removed")
    print()
    print("formats:", Counter(p["formats"][0] for p in pieces))
    print("pillars:", Counter(p["pillar"] for p in pieces))
    print("subjects:", Counter(p["subject"] for p in pieces))
    print()
    print("decisions (first 12):")
    for i, s, d in log[:12]:
        print(f"  #{i:2}  sim={s:<5} {d}")
    both = [l for l in log if "BOTH" in l[2]]
    print(f"\nentries that kept both halves: {len(both)} -> {[b[0] for b in both]}")
