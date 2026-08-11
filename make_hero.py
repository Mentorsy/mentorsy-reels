"""
Build one hero reel.

    python3 make_hero.py --slug hero_2026_09
    python3 make_hero.py --slug hero_2026_09 --date 2026-09-15 --time 8:30pm

Reads the script from heroes.py, picks up whatever clips are sitting in
presenter/ under that slug, and writes the finished reel into the dated folder
alongside a caption - same shape as everything else, so it uploads the same way.
"""

import argparse
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import deliver
import hero
from heroes import HEROES

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    os.pardir))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--date", help="YYYY-MM-DD, defaults to the script's own")
    ap.add_argument("--time", default="8:30pm")
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--out", help="write the mp4 here instead of a dated folder")
    a = ap.parse_args()

    spec = HEROES.get(a.slug)
    if not spec:
        print(f"No script called {a.slug}. Known: {', '.join(sorted(HEROES))}")
        return 1
    spec = dict(spec, slug=a.slug)

    have_face = hero.find_presenter(a.slug)
    brolls = [i for i in range(1, len(spec.get("broll", [])) + 1)
              if hero.find_broll(a.slug, i)]
    print("presenter clip: " +
          ("yes" if have_face else "none - using the designed cold open"))
    print(f"b-roll clips:   {len(brolls)} of {len(spec.get('broll', []))}")

    if a.out:
        out = os.path.abspath(a.out)
        os.makedirs(os.path.dirname(out), exist_ok=True)
    else:
        date = (dt.date.fromisoformat(a.date) if a.date
                else dt.date.fromisoformat(spec["date"]))
        folder = os.path.join(a.root, deliver.day_folder(date),
                              deliver.slot_folder(a.time, 2, "reel"))
        os.makedirs(folder, exist_ok=True)
        out = os.path.join(folder, "reel.mp4")
        with open(os.path.join(folder, "caption.txt"), "w",
                  encoding="utf-8") as f:
            f.write(deliver._caption_text(dict(spec, kind="reel")))

    print("rendering...")
    print(hero.render(spec, out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
