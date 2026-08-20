"""Workflow entrypoint. One slot, one run, never twice."""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from publish import publish                                   # noqa: E402
from schedule import LEDGER, NothingToPost, choose, load, runway_report  # noqa: E402
from slots import BY_ID, slots_for_weekday                    # noqa: E402


def resolve_slot(now_ist: datetime) -> str | None:
    """Map the current IST time to exactly one slot, within a 300-minute window.

    Cron drift on GitHub Actions is routine (runs can be 5-20 minutes late and
    occasionally skipped). A window absorbs that WITHOUT ever matching two
    slots, because no two slots on the same weekday are less than 3 hours apart.
    """
    mins = now_ist.hour * 60 + now_ist.minute
    best, best_gap = None, 10 ** 9
    for s in slots_for_weekday(now_ist.weekday()):
        h, m = (int(x) for x in s.hhmm_ist.split(":"))
        gap = mins - (h * 60 + m)
        if 0 <= gap <= 300 and gap < best_gap:
            best, best_gap = s.id, gap
    return best

IST = timezone(timedelta(minutes=330))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slot", default="auto",
                    help='slot id, or "auto" to resolve from the current IST time')
    ap.add_argument("--date", default=None, help="YYYY-MM-DD in IST; defaults to today")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    today = (
        datetime.fromisoformat(a.date).date() if a.date
        else datetime.now(IST).date()
    )
    slot_id = a.slot
    if slot_id == "auto":
        slot_id = resolve_slot(datetime.now(IST))
        if slot_id is None:
            print("::notice::no slot due right now — exiting without posting")
            return 0
        print(f"::notice::resolved slot -> {slot_id}")
    if slot_id not in BY_ID:
        print(f"::error::unknown slot {slot_id}")
        return 1

    cfg, bank, ledger = load()

    try:
        entry, note = choose(slot_id, today, cfg, bank, ledger)
    except NothingToPost as e:
        print(f"::error::{e}")
        print(f"::notice::runway {runway_report(cfg, bank, ledger, today)}")
        return 78  # neutral: alert, do not fail the repo red

    if entry is None:
        print(f"::notice::{note}")
        return 0

    media = (bank_media(entry) or {})
    result = publish(entry, media, dry_run=a.dry_run or not os.environ.get("META_ACCESS_TOKEN"))
    print(json.dumps(result, indent=2))

    if not result.get("dry_run"):
        entry["publish_result"] = result
        ledger.append(entry)
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        LEDGER.write_text(json.dumps(ledger, indent=1, ensure_ascii=False))
        print(f"::notice::ledger updated — {len(ledger)} posts recorded")

    runway = runway_report(cfg, bank, ledger, today)
    print(f"::notice::runway {runway}")
    if min(runway.values()) < cfg["rules"]["min_bank_runway_posts"]:
        print("::warning::Content bank running low. Refill before it starves.")
        Path("RUNWAY_LOW").write_text(json.dumps(runway))
    return 0


def bank_media(entry: dict) -> dict:
    """Where the rendered asset URLs come from. Point this at your Canva /
    R2 / S3 exports keyed by content_id + format."""
    manifest = Path(__file__).resolve().parent.parent / "content" / "media.json"
    if not manifest.exists():
        return {}
    m = json.loads(manifest.read_text())
    return m.get(f"{entry['content_id']}:{entry['format']}", {})


if __name__ == "__main__":
    raise SystemExit(main())
