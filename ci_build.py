"""
CI entry point — renders reels due inside a rolling horizon.

Called by .github/workflows/build.yml. Keeps each run inside the free
GitHub Actions allowance by only rendering what's about to be needed,
rather than the whole calendar every night.
"""

import csv
import datetime
import os
import subprocess
import sys

import config as C

HORIZON = int(os.environ.get("HORIZON_DAYS", "10"))
FORCE_ALL = os.environ.get("FORCE_ALL", "false").lower() == "true"

# Leave headroom in the 2,000 min/month free allowance.
MAX_PER_RUN = int(os.environ.get("MAX_RENDERS_PER_RUN", "12"))


def main():
    cal = os.path.join(C.BASE_DIR, "calendar_60.csv")
    if not os.path.exists(cal):
        print("No calendar_60.csv — nothing to build.")
        return 0

    rows = list(csv.DictReader(open(cal, encoding="utf-8")))
    today = datetime.date.today()
    limit = (today + datetime.timedelta(days=HORIZON)).isoformat()

    todo = []
    for r in rows:
        if not FORCE_ALL and not (today.isoformat() <= r["date"] <= limit):
            continue
        if os.path.exists(os.path.join(C.OUTPUT_DIR, f"{r['slug']}.mp4")):
            continue
        if not os.path.exists(os.path.join(C.SCRIPTS_DIR, f"{r['slug']}.json")):
            print(f"  no script yet for {r['slug']} — skipping")
            continue
        todo.append(r)

    if not FORCE_ALL:
        todo = todo[:MAX_PER_RUN]

    if not todo:
        print("Everything inside the horizon is already rendered.")
        return 0

    print(f"Rendering {len(todo)} reels (horizon {HORIZON} days)\n")
    failures = 0
    for i, r in enumerate(todo, 1):
        print(f"[{i}/{len(todo)}] {r['date']} · {r['topic'][:52]}")
        rc = subprocess.run(
            [sys.executable, "render.py",
             os.path.join(C.SCRIPTS_DIR, f"{r['slug']}.json")],
            cwd=C.BASE_DIR,
        ).returncode
        if rc != 0:
            print(f"  ! render failed for {r['slug']} — will retry tomorrow")
            failures += 1

    print(f"\nDone. {len(todo) - failures} rendered, {failures} failed.")
    # Never fail the workflow for a single bad render — tomorrow's run retries.
    return 0


if __name__ == "__main__":
    sys.exit(main())
