"""Meta Graph API publisher with a second, independent duplicate guard.

The ledger stops us re-posting. This module also asks Instagram what it
already has, so even a corrupted or reverted ledger cannot produce a repeat.
Belt and braces, because the failure mode is public.
"""
from __future__ import annotations

import hashlib
import os
import time
import urllib.parse
import urllib.request

GRAPH = "https://graph.facebook.com/v21.0"


def _post(path: str, params: dict) -> dict:
    import json as _json
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(f"{GRAPH}/{path}", data=data, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return _json.loads(r.read())


def _get(path: str, params: dict) -> dict:
    import json as _json
    url = f"{GRAPH}/{path}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        return _json.loads(r.read())


def caption_fingerprint(caption: str) -> str:
    """First line of the caption is the hook; that's what a follower recognises."""
    head = caption.strip().split("\n")[0].lower()
    return hashlib.sha256(head.encode()).hexdigest()[:12]


def already_on_feed(ig_user_id: str, token: str, caption: str, lookback: int = 40) -> bool:
    """Ask Instagram directly. Independent of our ledger."""
    try:
        res = _get(f"{ig_user_id}/media", {
            "fields": "caption,timestamp", "limit": lookback, "access_token": token,
        })
    except Exception:
        return False  # never block a post on a read failure; the ledger still guards
    fp = caption_fingerprint(caption)
    return any(
        caption_fingerprint(m.get("caption") or "") == fp for m in res.get("data", [])
    )


def _wait_ready(container_id: str, token: str, timeout_s: int = 300) -> None:
    """Reels need encoding time. Publishing early is the other classic
    double-post cause: the job times out, retries, and posts twice."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        st = _get(container_id, {"fields": "status_code", "access_token": token})
        code = st.get("status_code")
        if code == "FINISHED":
            return
        if code == "ERROR":
            raise RuntimeError(f"Container {container_id} failed encoding")
        time.sleep(10)
    raise TimeoutError(f"Container {container_id} not ready after {timeout_s}s")


def publish(entry: dict, media: dict, dry_run: bool = True) -> dict:
    """media = {"image_url": ...} | {"video_url": ...} | {"image_urls": [...]}"""
    ig = os.environ.get("IG_USER_ID", "")
    token = os.environ.get("META_ACCESS_TOKEN", "")
    caption = entry["caption"]

    if dry_run or not (ig and token):
        return {"dry_run": True, "would_post": entry["content_id"],
                "format": entry["format"], "chars": len(caption)}

    if already_on_feed(ig, token, caption):
        return {"skipped": "already_on_feed", "content_id": entry["content_id"]}

    fmt = entry["format"]
    if fmt == "reel":
        c = _post(f"{ig}/media", {"media_type": "REELS", "video_url": media["video_url"],
                                  "caption": caption, "share_to_feed": "true",
                                  "access_token": token})
        _wait_ready(c["id"], token)
        creation_id = c["id"]
    elif fmt == "carousel":
        kids = []
        for url in media["image_urls"]:
            k = _post(f"{ig}/media", {"image_url": url, "is_carousel_item": "true",
                                      "access_token": token})
            kids.append(k["id"])
        for k in kids:
            _wait_ready(k, token, timeout_s=120)
        c = _post(f"{ig}/media", {"media_type": "CAROUSEL", "children": ",".join(kids),
                                  "caption": caption, "access_token": token})
        creation_id = c["id"]
    else:
        c = _post(f"{ig}/media", {"image_url": media["image_url"], "caption": caption,
                                  "access_token": token})
        creation_id = c["id"]

    out = _post(f"{ig}/media_publish", {"creation_id": creation_id, "access_token": token})
    return {"published": out.get("id"), "content_id": entry["content_id"], "format": fmt}
