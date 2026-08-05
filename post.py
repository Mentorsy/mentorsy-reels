"""
Mentorsy — Instagram + Facebook auto-poster

Publishes finished Reels through the Instagram Graph API. Two-step: create a
media container, poll until Instagram has finished ingesting the video, then
publish. Also cross-posts to the linked Facebook Page if configured.

    python post.py --due          # post everything scheduled for today
    python post.py --slug NAME    # post one specific reel
    python post.py --dry-run      # show what would post, touch nothing

Instagram must be able to DOWNLOAD the mp4 over public HTTPS, so each file
needs a public URL. See SETUP_GUIDE.md — Cloudflare R2's free tier covers
this at zero cost.
"""

import argparse
import csv
import datetime
import json
import os
import time

import requests

import config as C

GRAPH = "https://graph.facebook.com/v21.0"
LOG = os.path.join(C.BASE_DIR, "posted_log.csv")


# ── logging ────────────────────────────────────────────────────────────

def audience_now():
    """
    GitHub Actions runners are UTC; the posting slots are Gulf time.
    TZ_OFFSET_HOURS shifts the clock so a 07:30 slot fires at 07:30 GST
    wherever this actually runs. Locally it defaults to your own clock.
    """
    off = os.environ.get("TZ_OFFSET_HOURS")
    if off is None:
        return datetime.datetime.now()
    return datetime.datetime.utcnow() + datetime.timedelta(hours=float(off))



def _log_rows():
    if not os.path.exists(LOG):
        return []
    return list(csv.DictReader(open(LOG, encoding="utf-8")))


def already_posted(slug):
    return any(r["slug"] == slug and r["status"] == "published" for r in _log_rows())


def posted_today():
    today = audience_now().date().isoformat()
    return sum(1 for r in _log_rows()
               if r["status"] == "published" and r["posted_at"].startswith(today))


def write_log(slug, status, media_id="", note=""):
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["posted_at", "slug", "status", "media_id", "note"])
        w.writerow([datetime.datetime.now().isoformat(timespec="seconds"),
                    slug, status, media_id, note])


# ── publishing ─────────────────────────────────────────────────────────

def build_caption(meta):
    tags = " ".join(meta["hashtags"][:5])   # Instagram caps hashtags at 5
    return f"{meta['caption']}\n\n{tags}"


def publish_reel(video_url, caption, dry_run=False):
    if dry_run:
        print(f"    [dry run] would publish {video_url}")
        return "DRY_RUN_ID"

    r = requests.post(
        f"{GRAPH}/{C.IG_USER_ID}/media",
        data={"media_type": "REELS", "video_url": video_url,
              "caption": caption, "share_to_feed": "true",
              "access_token": C.IG_ACCESS_TOKEN},
        timeout=90,
    )
    r.raise_for_status()
    container = r.json()["id"]
    print(f"    container {container} — waiting for Instagram to ingest…")

    # Instagram must finish downloading and transcoding before we can publish
    for attempt in range(60):
        time.sleep(5)
        s = requests.get(f"{GRAPH}/{container}",
                         params={"fields": "status_code,status",
                                 "access_token": C.IG_ACCESS_TOKEN},
                         timeout=30).json()
        code = s.get("status_code")
        if code == "FINISHED":
            break
        if code == "ERROR":
            raise RuntimeError(f"ingest failed: {s.get('status')}")
        if attempt % 6 == 5:
            print(f"    still {code}… ({(attempt + 1) * 5}s)")
    else:
        raise RuntimeError("timed out waiting for Instagram to ingest the video")

    p = requests.post(f"{GRAPH}/{C.IG_USER_ID}/media_publish",
                      data={"creation_id": container,
                            "access_token": C.IG_ACCESS_TOKEN}, timeout=90)
    p.raise_for_status()
    return p.json()["id"]


def cross_post_facebook(video_url, caption, dry_run=False):
    page_id = os.environ.get("FB_PAGE_ID", "")
    page_token = os.environ.get("FB_PAGE_TOKEN", "")
    if not page_id or not page_token:
        return None
    if dry_run:
        print("    [dry run] would cross-post to Facebook")
        return "DRY_RUN_FB"
    try:
        r = requests.post(f"{GRAPH}/{page_id}/videos",
                          data={"file_url": video_url, "description": caption,
                                "access_token": page_token}, timeout=120)
        r.raise_for_status()
        return r.json().get("id")
    except Exception as e:
        print(f"    facebook cross-post failed (instagram still went out): {e}")
        return None


# ── orchestration ──────────────────────────────────────────────────────

def load_meta(slug):
    p = os.path.join(C.OUTPUT_DIR, f"{slug}.json")
    if not os.path.exists(p):
        return None
    return json.load(open(p, encoding="utf-8"))


def due_today():
    cal = os.path.join(C.BASE_DIR, "calendar_60.csv")
    if not os.path.exists(cal):
        return []
    stamp = audience_now()
    today = stamp.date().isoformat()
    now = stamp.strftime("%H:%M")
    out = []
    for r in csv.DictReader(open(cal, encoding="utf-8")):
        if r["date"] != today:
            continue
        if r["slot"] > now:          # not yet time for this slot
            continue
        if already_posted(r["slug"]):
            continue
        out.append(r)
    return out


def post_one(slug, dry_run=False):
    meta = load_meta(slug)
    if not meta:
        print(f"    no rendered video for {slug} — run render.py first")
        write_log(slug, "skipped", note="not rendered")
        return False

    if not C.PUBLIC_VIDEO_BASE_URL and not dry_run:
        print("    PUBLIC_VIDEO_BASE_URL is not set — see SETUP_GUIDE.md")
        return False

    base = C.PUBLIC_VIDEO_BASE_URL.rstrip("/") or "https://EXAMPLE-NOT-SET"
    video_url = f"{base}/{slug}.mp4"
    caption = build_caption(meta)

    try:
        media_id = publish_reel(video_url, caption, dry_run)
        cross_post_facebook(video_url, caption, dry_run)
        write_log(slug, "published" if not dry_run else "dry_run", media_id)
        print(f"    ✓ published {media_id}")
        return True
    except Exception as e:
        print(f"    ✗ {e}")
        write_log(slug, "failed", note=str(e)[:180])
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--due", action="store_true", help="post everything due today")
    ap.add_argument("--slug")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.slug:
        post_one(a.slug, a.dry_run)
        return

    if not a.due:
        ap.print_help()
        return

    rows = due_today()
    if not rows:
        print("Nothing due right now.")
        return

    budget = C.MAX_POSTS_PER_DAY - posted_today()
    if budget <= 0:
        print(f"Daily cap of {C.MAX_POSTS_PER_DAY} already reached.")
        return

    for r in rows[:budget]:
        print(f"▸ {r['slot']} · {r['topic'][:56]}")
        post_one(r["slug"], a.dry_run)
        time.sleep(8)   # keep well clear of the publishing rate limit


if __name__ == "__main__":
    main()
