"""
Mentorsy - build a month of content into dated folders.

    python3 build.py                  # 30 days starting tomorrow
    python3 build.py --start 2026-09-07
    python3 build.py --days 30 --skip-existing

Every run writes into Desktop/Mentorsy Instagram/<D Month>/, and skips any day
folder that already exists unless told otherwise. That is what makes the daily
schedule additive: run it today and you get the next 30 days, run it tomorrow
and you get the 30 after that, without ever rewriting a day you have already
looked at.

The content bank holds 30 days. Beyond that the builder cycles it while
rotating which subject leads, so month two is not a replay - the pieces recur
in a different order against different dates. A month is the right horizon for
Claude to write fresh copy into anyway; the cycling is a floor, not the plan.
"""

import argparse
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import deliver
from carousels import CAROUSEL_POINTS
from content_a import DAYS_A
from content_b import DAYS_B
from content_2026_09 import DAYS_C

BANK = DAYS_A + DAYS_B + DAYS_C

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    os.pardir))
LEDGER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ledger.json")

# 09:00 IST is 07:30 in Dubai - the school run.
# 20:30 IST is 19:00 Dubai, 16:00 London, 11:00 New York.
SLOTS = ["9:00am", "8:30pm"]


def load_ledger():
    if os.path.exists(LEDGER):
        with open(LEDGER, encoding="utf-8") as f:
            return json.load(f)
    return {"written": [], "cursor": 0}


def save_ledger(led):
    with open(LEDGER, "w", encoding="utf-8") as f:
        json.dump(led, f, indent=1)


def pieces_for(idx):
    """Return [(time, spec), ...] for the idx-th day of the run."""
    entry = BANK[idx] if idx < len(BANK) else sys.exit(f"Content bank exhausted: day {idx} of {len(BANK)}. Add pieces before building further. Refusing to wrap and repeat.")
    post = dict(entry["post"])
    reel = dict(entry["reel"])

    # Six days a month, the feed post gets the swipe treatment instead.
    pts = CAROUSEL_POINTS.get(reel["slug"])
    if pts:
        post["kind"] = "carousel"
        post["points"] = pts

    return [(SLOTS[0], post), (SLOTS[1], reel)]


def build_heroes(root, first, last, force=False):
    """
    Render any hero reel whose date falls inside the window.

    A hero replaces the evening reel for that day rather than adding a third
    piece, because the point of a hero is that it is the thing you notice, and
    it cannot be that if it is competing with another reel an hour later.
    """
    import hero
    from heroes import HEROES

    made = 0
    for slug, spec in HEROES.items():
        try:
            date = dt.date.fromisoformat(spec["date"])
        except (KeyError, ValueError):
            continue
        if not (first <= date <= last):
            continue

        folder = os.path.join(root, deliver.day_folder(date),
                              deliver.slot_folder(SLOTS[1], 2, "reel"))
        out = os.path.join(folder, "reel.mp4")
        marker = os.path.join(folder, ".hero")

        # The rotation will already have written an ordinary reel into this
        # slot, so a hero always overwrites rather than skipping. The marker
        # is what stops it re-rendering on every subsequent build.
        if os.path.exists(marker) and not force:
            continue

        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "caption.txt"), "w",
                  encoding="utf-8") as f:
            f.write(deliver._caption_text(dict(spec, kind="reel")))
        face = "with presenter" if hero.find_presenter(slug) else "cold open"
        hero.render(dict(spec, slug=slug), out)
        open(marker, "w").close()
        print(f"  {deliver.day_folder(date):<14} HERO ({face})")
        made += 1
    return made


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", help="YYYY-MM-DD, defaults to tomorrow")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--force", action="store_true",
                    help="rewrite day folders that already exist")
    a = ap.parse_args()

    start = (dt.date.fromisoformat(a.start) if a.start
             else dt.date.today() + dt.timedelta(days=1))

    led = load_ledger()
    written = set(led["written"])
    cursor = led["cursor"]

    made = skipped = 0
    for i in range(a.days):
        date = start + dt.timedelta(days=i)
        key = date.isoformat()
        folder = os.path.join(a.root, deliver.day_folder(date))

        # Folder presence is the source of truth, not the ledger. A run that
        # dies halfway leaves finished days on disk but an unsaved ledger, and
        # resuming should trust the disk.
        if os.path.isdir(folder) and not a.force:
            skipped += 1
            written.add(key)
            cursor += 1
            continue

        deliver.write_day(a.root, date, pieces_for(cursor))
        cursor += 1
        written.add(key)
        made += 1
        print(f"  {deliver.day_folder(date):<14} 2 pieces")

    # Hero reels are dated in heroes.py rather than positioned in the rotation,
    # because they are events - one a month, tied to a moment worth spending a
    # face on. Building them here means they arrive on the calendar by
    # themselves, with or without a presenter clip sitting in presenter/.
    made += build_heroes(a.root, start, start + dt.timedelta(days=a.days - 1),
                         a.force)

    led["written"] = sorted(written)
    led["cursor"] = cursor
    save_ledger(led)

    print(f"\n{made} days written, {skipped} already present.")
    if made:
        print(f"Covers {start} to {start + dt.timedelta(days=a.days - 1)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
