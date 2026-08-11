"""
Mentorsy - media hosting

Meta fetches media itself from a public HTTPS URL; it will not take an upload.
So the files have to be somewhere on the open internet at publish time.

This pushes them into the existing public repo through the GitHub contents
API, then hands back raw.githubusercontent.com URLs pinned to the commit SHA
rather than to main. The pin matters: raw.githubusercontent is aggressively
CDN-cached, and a URL on `main` can serve a previous version of a file for
several minutes. A SHA-pinned URL is immutable, so what Meta downloads is
always exactly what was pushed.
"""

import base64
import os
import time

import requests

REPO = os.environ.get("MENTORSY_REPO", "Mentorsy/mentorsy-reels")
BRANCH = "main"
API = "https://api.github.com"
RAW = "https://raw.githubusercontent.com"
PREFIX = "publish"


def _headers(token):
    return {"Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"}


def _put(path, blob, token, message):
    url = f"{API}/repos/{REPO}/contents/{path}"
    body = {"message": message, "branch": BRANCH,
            "content": base64.b64encode(blob).decode()}

    existing = requests.get(url, headers=_headers(token),
                            params={"ref": BRANCH}, timeout=30)
    if existing.status_code == 200:
        body["sha"] = existing.json()["sha"]

    r = requests.put(url, headers=_headers(token), json=body, timeout=120)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"GitHub rejected {path}: "
                           f"{r.json().get('message', r.status_code)}")
    return r.json()["content"]["sha"], r.json()["commit"]["sha"]


def _reachable(url, tries=12, gap=5):
    for _ in range(tries):
        try:
            if requests.head(url, timeout=20, allow_redirects=True).status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(gap)
    return False


def push(files, key, env):
    """
    files: local paths. key: '9 August/8-30pm_2reel'.
    Returns public URLs in the same order.
    """
    # Running inside GitHub Actions the files are already in the repo, checked
    # out at a known commit. Nothing needs uploading - the raw host is serving
    # them at that SHA already, and pinning to the SHA rather than to main
    # means the CDN cannot hand Meta a stale version.
    sha = os.environ.get("GITHUB_SHA")
    if sha and os.environ.get("GITHUB_ACTIONS"):
        root = os.environ.get("GITHUB_WORKSPACE", os.getcwd())
        urls = []
        for f in files:
            rel = os.path.relpath(os.path.abspath(f), root).replace(os.sep, "/")
            urls.append(f"{RAW}/{REPO}/{sha}/"
                        + "/".join(requests.utils.quote(p) for p in rel.split("/")))
        return urls

    token = env.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError(
            "GITHUB_TOKEN is not set. Meta fetches media from a public URL, "
            "so the files need pushing somewhere public first.")

    safe = key.replace(" ", "_").replace("/", "__")
    urls = []
    for f in files:
        with open(f, "rb") as fh:
            blob = fh.read()
        path = f"{PREFIX}/{safe}/{os.path.basename(f)}"
        _, commit = _put(path, blob, token, f"publish: {key}")
        urls.append(f"{RAW}/{REPO}/{commit}/{path}")

    for u in urls:
        if not _reachable(u):
            raise RuntimeError(f"Pushed but not yet reachable: {u}")
    return urls
