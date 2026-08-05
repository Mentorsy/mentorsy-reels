"""
Mentorsy — one command for the whole thing.

    python run_all.py --build          # calendar + 120 scripts + 120 videos
    python run_all.py --build --days 7 # just the first week, to sanity-check
    python run_all.py --daily          # what the scheduler runs each day
    python run_all.py --status         # where everything stands

--build is the two-month batch. Run it once, leave it going. It is resumable:
if it stops, run it again and it picks up where it left off.

--daily renders anything still missing for the next few days and posts
whatever is due. This is what Windows Task Scheduler should call.
"""

import argparse
import csv
import datetime
import os
import subprocess
import sys

import config as C

PY = sys.executable


def sh(args, desc):
    print(f"\n─── {desc} " + "─" * max(0, 52 - len(desc)))
    return subprocess.run([PY] + args, cwd=C.BASE_DIR).returncode


def calendar_rows():
    p = os.path.join(C.BASE_DIR, "calendar_60.csv")
    if not os.path.exists(p):
        return []
    return list(csv.DictReader(open(p, encoding="utf-8")))


def status():
    rows = calendar_rows()
    if not rows:
        print("No calendar yet. Run:  python run_all.py --build")
        return

    scripts = {f[:-5] for f in os.listdir(C.SCRIPTS_DIR) if f.endswith(".json")}
    videos = {f[:-4] for f in os.listdir(C.OUTPUT_DIR) if f.endswith(".mp4")}

    posted = set()
    log = os.path.join(C.BASE_DIR, "posted_log.csv")
    if os.path.exists(log):
        posted = {r["slug"] for r in csv.DictReader(open(log, encoding="utf-8"))
                  if r["status"] == "published"}

    n = len(rows)
    today = datetime.date.today().isoformat()
    upcoming = [r for r in rows if r["date"] >= today]

    def bar(k, total, label):
        pct = k / total if total else 0
        fill = int(pct * 34)
        print(f"  {label:<10} [{'█' * fill}{'░' * (34 - fill)}] {k:>3}/{total}")

    print(f"\nMentorsy Reel Factory — {rows[0]['date']} → {rows[-1]['date']}\n")
    bar(len(scripts & {r['slug'] for r in rows}), n, "scripts")
    bar(len(videos & {r['slug'] for r in rows}), n, "videos")
    bar(len(posted & {r['slug'] for r in rows}), n, "posted")
    print(f"\n  {len(upcoming)} posts still ahead of you\n")

    nxt = [r for r in upcoming if r["slug"] not in posted][:5]
    if nxt:
        print("  Next up:")
        for r in nxt:
            mark = "✓" if r["slug"] in videos else "·"
            print(f"    {mark} {r['date']} {r['slot']}  {r['topic'][:54]}")
        print()


def build(days, start, limit_render):
    if not os.path.exists(os.path.join(C.BASE_DIR, "calendar_60.csv")):
        args = ["calendar_60.py", "--days", str(days)]
        if start:
            args += ["--start", start]
        sh(args, "planning the calendar")
    else:
        print("─── calendar already exists, keeping it ───")

    sh(["scriptgen.py"], "writing scripts (free Gemini tier)")

    rows = calendar_rows()
    todo = [r for r in rows
            if os.path.exists(os.path.join(C.SCRIPTS_DIR, f"{r['slug']}.json"))
            and not os.path.exists(os.path.join(C.OUTPUT_DIR, f"{r['slug']}.mp4"))]
    if limit_render:
        todo = todo[:limit_render]

    print(f"\n─── rendering {len(todo)} videos " + "─" * 26)
    for i, r in enumerate(todo, 1):
        print(f"\n[{i}/{len(todo)}]")
        subprocess.run([PY, "render.py",
                        os.path.join(C.SCRIPTS_DIR, f"{r['slug']}.json")],
                       cwd=C.BASE_DIR)

    status()


def daily():
    """Runs every day. Keeps a rolling buffer rendered, then posts what's due."""
    rows = calendar_rows()
    today = datetime.date.today()
    horizon = (today + datetime.timedelta(days=5)).isoformat()

    todo = [r for r in rows
            if today.isoformat() <= r["date"] <= horizon
            and not os.path.exists(os.path.join(C.OUTPUT_DIR, f"{r['slug']}.mp4"))]

    for r in todo:
        sp = os.path.join(C.SCRIPTS_DIR, f"{r['slug']}.json")
        if not os.path.exists(sp):
            subprocess.run([PY, "scriptgen.py", "--limit", "0"], cwd=C.BASE_DIR)
            continue
        subprocess.run([PY, "render.py", sp], cwd=C.BASE_DIR)

    sh(["post.py", "--due"], "posting what's due")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--daily", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--days", type=int, default=60)
    ap.add_argument("--start", default=None)
    ap.add_argument("--limit-render", type=int, default=None)
    a = ap.parse_args()

    if a.build:
        build(a.days, a.start, a.limit_render)
    elif a.daily:
        daily()
    elif a.status:
        status()
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
