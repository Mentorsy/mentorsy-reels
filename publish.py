"""
Mentorsy - auto-publisher

Reads a slot folder written by build.py and publishes it to Instagram, and
optionally to the linked Facebook Page, through the Meta Graph API.

    python3 publish.py --due            # anything scheduled up to now
    python3 publish.py --slot "9 August/9-00am_1carousel"
    python3 publish.py --due --dry-run  # show what would go out

## How the media gets to Meta

Meta will not accept a file upload for content publishing. It fetches the
media itself from a public HTTPS URL, which means every image and video has to
be reachable on the open internet at publish time. The repo at
github.com/Mentorsy/mentorsy-reels is already public and already serving
artwork over raw.githubusercontent.com, so that is the host: the publisher
pushes the day's files there, waits for them to be reachable, and hands Meta
the URLs.

That does mean anything published is briefly public before it is posted, which
for marketing artwork is not a concern - it is about to be public anyway.

## Credentials

Never in this file, never in the repo, never in a chat window. The publisher
reads them from the environment, or from a `.env` file sitting next to it that
is excluded from git:

    META_IG_USER_ID=17841400000000000
    META_PAGE_ID=100000000000000
    META_ACCESS_TOKEN=EAA...
    GITHUB_TOKEN=ghp_...            # only needed for the media push

`python3 publish.py --check` verifies all four without printing any of them.

## Rate limits

Instagram allows 50 published posts per rolling 24 hours per account. At two a
day there is no risk, but the publisher checks the quota before each run and
stops rather than burning a retry on a rejection.
"""

import argparse
import datetime as dt
import json
import os
import sys
import time

import requests

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, os.pardir))
GRAPH = "https://graph.facebook.com/v21.0"
LOG = os.path.join(BASE, "published.json")

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


# -- config --------------------------------------------------------------

def load_env():
    """
    Environment first, then a .env on disk. Never printed.

    The .env lives OUTSIDE _engine, in a sibling .mentorsy-secrets folder.
    That is deliberate: the repo is public, and GitHub's web uploader ignores
    .gitignore entirely, so a secret sitting inside the folder you drag would
    go straight into a public repo. Keeping it one level up makes that
    mistake impossible rather than merely discouraged.

    In GitHub Actions there is no file at all - the values arrive as encrypted
    secrets through the environment.
    """
    env = {}
    for path in (os.path.join(ROOT, ".mentorsy-secrets", ".env"),
                 os.path.join(BASE, ".env")):
        if not os.path.exists(path):
            continue
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
        break
    for k in ("META_IG_USER_ID", "META_PAGE_ID", "META_ACCESS_TOKEN",
              "GITHUB_TOKEN", "MEDIA_BASE_URL"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def check(env):
    need = ["META_IG_USER_ID", "META_ACCESS_TOKEN"]
    missing = [k for k in need if not env.get(k)]
    if missing:
        print("Missing: " + ", ".join(missing))
        return False
    r = requests.get(f"{GRAPH}/{env['META_IG_USER_ID']}",
                     params={"fields": "username,followers_count",
                             "access_token": env["META_ACCESS_TOKEN"]},
                     timeout=30)
    if r.status_code != 200:
        print(f"Token rejected: {r.json().get('error', {}).get('message')}")
        return False
    d = r.json()
    print(f"Connected to @{d.get('username')} "
          f"({d.get('followers_count', '?')} followers)")
    if env.get("META_PAGE_ID"):
        print("Facebook Page: configured")
    return True


def quota_left(env):
    r = requests.get(f"{GRAPH}/{env['META_IG_USER_ID']}/content_publishing_limit",
                     params={"access_token": env["META_ACCESS_TOKEN"]},
                     timeout=30)
    try:
        used = r.json()["data"][0]["quota_usage"]
        return 50 - int(used)
    except Exception:
        return 50


# -- slot discovery ------------------------------------------------------

def parse_slot(day_name, slot_name):
    """('9 August', '8-30pm_2reel') -> (datetime, kind)"""
    try:
        d_str, m_str = day_name.split(None, 1)
        month = MONTHS.index(m_str.strip()) + 1
        day = int(d_str)
    except (ValueError, IndexError):
        return None, None

    clock, _, rest = slot_name.partition("_")
    kind = "".join(c for c in rest if c.isalpha()) or "post"
    ampm = clock[-2:].lower()
    hm = clock[:-2].split("-")
    hour = int(hm[0]) % 12
    minute = int(hm[1]) if len(hm) > 1 else 0
    if ampm == "pm":
        hour += 12

    today = dt.date.today()
    year = today.year
    # A month far behind us belongs to next year, not this one.
    if month < today.month - 6:
        year += 1
    return dt.datetime(year, month, day, hour, minute), kind


def slots(root):
    out = []
    for day in sorted(os.listdir(root)):
        p = os.path.join(root, day)
        if day.startswith("_") or not os.path.isdir(p):
            continue
        for slot in sorted(os.listdir(p)):
            sp = os.path.join(p, slot)
            if not os.path.isdir(sp):
                continue
            when, kind = parse_slot(day, slot)
            if when:
                out.append({"when": when, "kind": kind, "path": sp,
                            "key": f"{day}/{slot}"})
    return sorted(out, key=lambda s: s["when"])


def already_done():
    if os.path.exists(LOG):
        return json.load(open(LOG, encoding="utf-8"))
    return {}


def record(key, result):
    log = already_done()
    log[key] = {"at": dt.datetime.now().isoformat(timespec="seconds"),
                **result}
    with open(LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=1)


# -- caption -------------------------------------------------------------

def caption_of(path):
    """The audience part only - everything above the instruction rule."""
    raw = open(os.path.join(path, "caption.txt"), encoding="utf-8").read()
    return raw.split("-" * 46)[0].strip()


def media_files(path, kind):
    if kind == "reel":
        return [os.path.join(path, "reel.mp4")]
    if kind == "carousel":
        return [os.path.join(path, f) for f in sorted(os.listdir(path))
                if f.lower().endswith(".png")]
    return [os.path.join(path, "post.png")]


# -- publishing ----------------------------------------------------------

def _wait_ready(container_id, env, timeout=300):
    """Video containers are transcoded asynchronously; publishing early fails."""
    start = time.time()
    while time.time() - start < timeout:
        r = requests.get(f"{GRAPH}/{container_id}",
                         params={"fields": "status_code,status",
                                 "access_token": env["META_ACCESS_TOKEN"]},
                         timeout=30).json()
        code = r.get("status_code")
        if code == "FINISHED":
            return True
        if code == "ERROR":
            raise RuntimeError(f"Container failed: {r.get('status')}")
        time.sleep(6)
    raise RuntimeError("Container never finished processing")


def _container(env, params):
    r = requests.post(f"{GRAPH}/{env['META_IG_USER_ID']}/media",
                      data={**params, "access_token": env["META_ACCESS_TOKEN"]},
                      timeout=60)
    j = r.json()
    if "id" not in j:
        raise RuntimeError(j.get("error", {}).get("message", str(j)))
    return j["id"]


def publish_instagram(env, kind, urls, caption):
    if kind == "reel":
        cid = _container(env, {"media_type": "REELS", "video_url": urls[0],
                               "caption": caption, "share_to_feed": "true"})
        _wait_ready(cid, env)
    elif kind == "carousel":
        children = []
        for u in urls[:10]:
            children.append(_container(env, {"image_url": u,
                                             "is_carousel_item": "true"}))
        cid = _container(env, {"media_type": "CAROUSEL",
                               "children": ",".join(children),
                               "caption": caption})
    else:
        cid = _container(env, {"image_url": urls[0], "caption": caption})

    r = requests.post(f"{GRAPH}/{env['META_IG_USER_ID']}/media_publish",
                      data={"creation_id": cid,
                            "access_token": env["META_ACCESS_TOKEN"]},
                      timeout=60)
    j = r.json()
    if "id" not in j:
        raise RuntimeError(j.get("error", {}).get("message", str(j)))
    return j["id"]


def publish_facebook(env, kind, urls, caption):
    """Best effort. A Facebook failure never fails the Instagram post."""
    page, token = env.get("META_PAGE_ID"), env.get("META_ACCESS_TOKEN")
    if not page:
        return None
    try:
        if kind == "reel":
            return None  # Page reels use a different upload flow entirely
        r = requests.post(f"{GRAPH}/{page}/photos",
                          data={"url": urls[0], "caption": caption,
                                "access_token": token}, timeout=60)
        return r.json().get("post_id") or r.json().get("id")
    except Exception as e:
        print(f"    facebook: {e}")
        return None


# -- main ----------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--due", action="store_true",
                    help="publish everything scheduled up to now")
    ap.add_argument("--slot", help="publish one slot, e.g. '9 August/8-30pm_2reel'")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--facebook", action="store_true",
                    help="also post to the linked Page")
    a = ap.parse_args()

    env = load_env()
    if a.check:
        return 0 if check(env) else 1

    if not a.dry_run and not env.get("META_ACCESS_TOKEN"):
        print("No credentials. Run --check, or see the header of this file.")
        return 1

    done = already_done()
    now = dt.datetime.now()
    todo = []
    for s in slots(a.root):
        if s["key"] in done:
            continue
        if a.slot and s["key"] != a.slot:
            continue
        if a.due and not (0 <= (now - s["when"]).total_seconds() <= 10800):
            continue
        todo.append(s)

    if not todo:
        print("Nothing due.")
        return 0

    if not a.dry_run:
        left = quota_left(env)
        if left < len(todo):
            print(f"Only {left} posts left in the 24h quota; "
                  f"{len(todo)} are due. Stopping.")
            return 1

    from media_host import push  # local import: only needed when publishing

    for s in todo:
        files = media_files(s["path"], s["kind"])
        cap = caption_of(s["path"])
        print(f"{s['key']}  {s['kind']}  {len(files)} file(s)")
        if a.dry_run:
            print(f"    {cap.splitlines()[0][:70]}...")
            continue
        try:
            urls = push(files, s["key"], env)
            ig = publish_instagram(env, s["kind"], urls, cap)
            fb = publish_facebook(env, s["kind"], urls, cap) if a.facebook else None
            record(s["key"], {"instagram": ig, "facebook": fb})
            print(f"    published {ig}")
        except Exception as e:
            print(f"    FAILED: {e}")
            record(s["key"], {"error": str(e)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
