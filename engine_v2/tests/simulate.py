"""Dry-run the scheduler forward N days and PROVE the feed cannot repeat.

Run:  python3 tests/simulate.py 90
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))

from dedup import Deduper                      # noqa: E402
from schedule import NothingToPost, choose, runway_report   # noqa: E402
from slots import slots_for_weekday            # noqa: E402


def run(days: int, start: date):
    cfg = json.loads((ROOT / "content" / "pillars.json").read_text())
    bank = json.loads((ROOT / "content" / "bank.json").read_text())
    ledger: list[dict] = []
    starved: list[str] = []

    for i in range(days):
        d = start + timedelta(days=i)
        for slot in slots_for_weekday(d.weekday()):
            try:
                entry, note = choose(slot.id, d, cfg, bank, ledger)
            except NothingToPost as e:
                starved.append(f"{d} {slot.id} ({slot.fmt}): {e}")
                continue
            if entry:
                ledger.append(entry)

    return cfg, bank, ledger, starved


def assertions(cfg, bank, ledger):
    r = cfg["rules"]
    fails = []

    # 1. slot idempotency
    keys = [e["slot_key"] for e in ledger]
    if len(keys) != len(set(keys)):
        fails.append(f"SLOT COLLISION: {len(keys)-len(set(keys))} duplicate slot keys")

    # 2. format lock -- a reel must come from a piece with a real reel script
    by_id = {b["id"]: b for b in bank}
    for e in ledger:
        piece = by_id[e["content_id"]]
        if e["format"] not in piece["formats"]:
            fails.append(f"FORMAT LEAK: {e['content_id']} posted as {e['format']}")
        if e["format"] == "reel" and not piece.get("reel_script"):
            fails.append(f"CAROUSEL-AS-REEL: {e['content_id']} had no reel script")

    # 3. content cooldown
    seen: dict[str, str] = {}
    for e in ledger:
        prev = seen.get(e["content_id"])
        if prev and (date.fromisoformat(e["posted_on"]) - date.fromisoformat(prev)).days <= r["content_cooldown_days"]:
            fails.append(f"REPEAT: {e['content_id']} on {prev} and again on {e['posted_on']}")
        seen[e["content_id"]] = e["posted_on"]

    # 4. identical body
    hseen: dict[str, str] = {}
    for e in ledger:
        prev = hseen.get(e["content_hash"])
        if prev and (date.fromisoformat(e["posted_on"]) - date.fromisoformat(prev)).days <= r["content_cooldown_days"]:
            fails.append(f"DUPLICATE BODY: hash {e['content_hash']} on {prev} and {e['posted_on']}")
        hseen[e["content_hash"]] = e["posted_on"]

    # 5. hook cooldown
    kseen: dict[str, str] = {}
    for e in ledger:
        prev = kseen.get(e["hook_sig"])
        if prev and (date.fromisoformat(e["posted_on"]) - date.fromisoformat(prev)).days <= r["hook_cooldown_days"]:
            fails.append(f"HOOK REUSE: {e['content_id']} reuses a hook from {prev}")
        kseen[e["hook_sig"]] = e["posted_on"]

    # 6. pillar spacing
    for i in range(1, len(ledger)):
        w = ledger[max(0, i - r["pillar_no_repeat_within_posts"]):i]
        if any(x["pillar"] == ledger[i]["pillar"] for x in w):
            fails.append(f"PILLAR CLUSTER at {ledger[i]['posted_on']} {ledger[i]['pillar']}")

    # 6b. THE IDEA GATE -- one idea must never ship twice, in any format.
    #     This is the assertion that answers "not even the reels from carousels".
    iseen = {}
    for e in ledger:
        g = e.get("idea_group")
        prev = iseen.get(g)
        if prev:
            days = (date.fromisoformat(e["posted_on"]) - date.fromisoformat(prev[0])).days
            if days <= r.get("idea_cooldown_days", 365):
                fails.append(
                    f"IDEA REPEAT: '{g}' shipped as {prev[1]} on {prev[0]} "
                    f"and again as {e['format']} on {e['posted_on']} ({days}d apart)")
        iseen[g] = (e["posted_on"], e["format"])

    # 6c. no piece may even be ELIGIBLE for more than one format
    for e in ledger:
        if len(by_id[e["content_id"]]["formats"]) != 1:
            fails.append(f"MULTI-FORMAT: {e['content_id']} can render as more than one format")

    # 7. no fabricated proof reached the feed
    for e in ledger:
        if Deduper.unfilled_placeholders(by_id[e["content_id"]]):
            fails.append(f"TEMPLATE PUBLISHED: {e['content_id']} still had placeholders")

    # 8. CTA pacing
    weeks: dict[date, Counter] = {}
    for e in ledger:
        d = date.fromisoformat(e["posted_on"])
        weeks.setdefault(d - timedelta(days=d.weekday()), Counter())[e["cta_strength"]] += 1
    for wk, c in weeks.items():
        if c["hard"] > cfg["cta_ladder"]["hard"]["max_per_week"]:
            fails.append(f"CTA OVERLOAD week of {wk}: {c['hard']} hard asks")
    return fails, weeks


if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 90
    start = date(2026, 8, 24)  # a Monday
    cfg, bank, ledger, starved = run(days, start)
    fails, weeks = assertions(cfg, bank, ledger)

    print(f"Simulated {days} days from {start}")
    print(f"Published: {len(ledger)} posts | unique pieces: {len({e['content_id'] for e in ledger})}")
    print(f"Format mix: {Counter(e['format'] for e in ledger)}")
    print(f"Pillar mix: {Counter(e['pillar'] for e in ledger)}")
    print(f"CTA mix:    {Counter(e['cta_strength'] for e in ledger)}")
    print()
    if starved:
        print(f"BANK RAN DRY on {len(starved)} slots. First: {starved[0]}")
        print(f"Last full posting day: {ledger[-1]['posted_on']}")
    else:
        print("Bank never ran dry.")
    print()
    print(f"Runway left today: {runway_report(cfg, bank, [], start)}")
    print()
    if fails:
        print(f"FAILED {len(fails)} assertion(s):")
        for f in fails[:20]:
            print("  -", f)
        sys.exit(1)
    print("ALL REPETITION ASSERTIONS PASSED — zero repeats, zero format leaks, zero fabricated proof.")
