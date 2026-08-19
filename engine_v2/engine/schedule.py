"""Decide what publishes into one slot. Deterministic, auditable, refuses to repeat."""
from __future__ import annotations

import json
import random
from datetime import date
from pathlib import Path

from dedup import Deduper, content_hash, hook_signature, tokens
from render import render_caption
from slots import BY_ID, slot_key

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "content" / "bank.json"
PILLARS = ROOT / "content" / "pillars.json"
LEDGER = ROOT / "state" / "ledger.json"


def load():
    cfg = json.loads(PILLARS.read_text())
    bank = json.loads(BANK.read_text())
    ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else []
    return cfg, bank, ledger


class NothingToPost(Exception):
    """Raised instead of recycling. Silence beats a fourth repost."""


def choose(slot_id: str, today: date, cfg: dict, bank: list[dict], ledger: list[dict]):
    slot = BY_ID[slot_id]
    key = slot_key(today.isoformat(), slot_id)
    ded = Deduper(ledger, cfg["rules"])

    if ded.slot_already_fired(key):
        return None, f"slot {key} already published — exiting clean (idempotent)"

    pool = ded.eligible(bank, slot.fmt, today)
    if not pool:
        raise NothingToPost(
            f"No eligible {slot.fmt} for {key}. Bank is dry or fully cooled down. "
            f"Refusing to recycle."
        )

    pillar_of = {p["id"]: p for p in cfg["pillars"]}

    # CTA pacing: demote a hard/mid ask once the weekly quota is spent, so the
    # feed never turns into a wall of "book now".
    hard_used = ded.hard_ctas_this_week(today)
    mid_used = ded.mid_ctas_this_week(today)

    def strength_for(p):
        s = pillar_of[p["pillar"]]["cta_strength"]
        if s == "hard" and hard_used >= cfg["cta_ladder"]["hard"]["max_per_week"]:
            s = "mid"
        if s == "mid" and mid_used >= cfg["cta_ladder"]["mid"]["max_per_week"]:
            s = "soft"
        return s

    def keyword_for(p):
        """Every mid-strength post must carry a DM trigger — that comment is the
        lead. Fall back to the subject's default magnet rather than silently
        demoting the post to a soft CTA and losing the capture."""
        if p.get("keyword"):
            return p["keyword"]
        k = cfg["subject_default_keyword"].get(p.get("subject", "General"), "EXAM")
        if isinstance(k, list):          # rotate deterministically, never random
            k = k[sum(ord(c) for c in p["id"]) % len(k)]
        return k

    # Rank: honour pillar target share, break ties with the oldest-unused piece,
    # then a date-seeded shuffle so two identical scores don't always resolve
    # the same way.
    posted_ids = {e["content_id"] for e in ledger}
    counts = {p["id"]: 0 for p in cfg["pillars"]}
    for e in ledger[-40:]:
        counts[e["pillar"]] = counts.get(e["pillar"], 0) + 1
    total = max(1, sum(counts.values()))

    rng = random.Random(f"{today.isoformat()}:{slot_id}")

    def score(p):
        want = pillar_of[p["pillar"]]["target_share"]
        have = counts.get(p["pillar"], 0) / total
        deficit = want - have                      # under-served pillars first
        never_posted = 0 if p["id"] in posted_ids else 1
        return (never_posted, round(deficit, 4), rng.random())

    pick = max(pool, key=score)
    strength = strength_for(pick)
    if strength == "mid":
        pick = {**pick, "keyword": keyword_for(pick)}
    seed = abs(hash(f"{today}{slot_id}{pick['id']}")) % 10**6
    caption = render_caption(pick, strength, cfg, seed)

    entry = {
        "slot_key": key,
        "posted_on": today.isoformat(),
        "slot_id": slot_id,
        "format": slot.fmt,
        "content_id": pick["id"],
        "pillar": pick["pillar"],
        "idea_group": pick.get("idea_group") or pick["id"],
        "subject": pick.get("subject"),
        "cta_strength": strength,
        "keyword": pick.get("keyword"),
        "content_hash": content_hash(pick),
        "hook_sig": hook_signature(pick["hook"]),
        "tokens": sorted(tokens(pick["hook"] + " " + pick.get("body", ""))),
        "caption": caption,
        "runway_after": len(pool) - 1,
    }
    return entry, None


def runway_report(cfg, bank, ledger, today: date) -> dict:
    ded = Deduper(ledger, cfg["rules"])
    return {f: len(ded.eligible(bank, f, today)) for f in ("reel", "carousel", "single")}
