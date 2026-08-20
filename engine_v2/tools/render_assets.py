"""Render every piece in the v2 bank into artwork the Graph API can fetch.

The engine decides WHAT and WHEN. Until now nothing decided what the post
actually looks like, so `content/media.json` did not exist and a live run
would have thrown a KeyError instead of publishing.

This bridges the v2 bank into the renderers that already exist at the repo
root (reels.py, cards.py, brand.py) and writes the media manifest.

    python3 engine_v2/tools/render_assets.py            # everything missing
    python3 engine_v2/tools/render_assets.py --limit 6  # a sample, to eyeball
"""
from __future__ import annotations

import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_V2 = os.path.dirname(HERE)
REPO = os.path.dirname(ENGINE_V2)
sys.path.insert(0, REPO)          # brand.py / reels.py / cards.py live here

import cards                       # noqa: E402
import reels                       # noqa: E402

BANK = os.path.join(ENGINE_V2, "content", "bank.json")
PILLARS = os.path.join(ENGINE_V2, "content", "pillars.json")
MEDIA_DIR = os.path.join(ENGINE_V2, "media")
MANIFEST = os.path.join(ENGINE_V2, "content", "media.json")

RAW = "https://raw.githubusercontent.com/Mentorsy/mentorsy-reels/main/engine_v2/media"

# The renderer's palette is keyed on the legacy vocabulary. Map ours onto it
# so every piece gets a colour rather than the muted fallback.
SUBJECT_MAP = {
    "Mathematics": "Mathematics", "Science": "Science", "French": "French",
    "Coding": "Coding", "Public Speaking": "Public Speaking",
    "English": "Mentorsy", "General": "Mentorsy",
}
PILLAR_MAP = {
    "P1": "Parent Scripts", "P2": "Future Skills", "P3": "Inside the Method",
    "P4": "Curriculum Decoded", "P5": "Inside the Method", "P6": "School Choice",
}

BEAT = re.compile(r"^\s*[A-Z][A-Z0-9 /]*\s*\(\s*\d+\s*-\s*\d+\s*s\s*\)\s*:\s*", re.I)


QUOTE_CHARS = "'‘’“”\""


def _spoken(line):
    """A script line is often a stage direction wrapped around speech:

        DEMO (3-15s): Write 3 _ 2 on a board. 'Split the digits. Add them.'

    On a static card the direction is noise. Take what sits between the first
    and last quote mark; keep the whole line when there is no quoted speech.
    """
    idx = [i for i, c in enumerate(line) if c in QUOTE_CHARS]
    if len(idx) >= 2 and idx[-1] - idx[0] > 12:
        line = line[idx[0] + 1:idx[-1]]
    return line.strip().strip(QUOTE_CHARS).strip()


def beats_from_script(script):
    """Turn a shooting script into card text.

    If these are ever filmed, the script in the bank stays the source of
    truth -- this only affects the artwork.
    """
    out = []
    for raw in (script or "").splitlines():
        line = BEAT.sub("", raw).strip()
        if not line:
            continue
        line = re.sub(r"^On screen[,:]?\s*", "", line, flags=re.I)
        line = _spoken(line)
        if len(line) > 4:
            out.append(line if len(line) <= 130 else line[:127].rstrip() + "…")
    return out[1:] or out          # first line is the hook; the cover shows it


def _split_slide(text: str) -> dict:
    """cards._point() wants a heading and a body. Our slides are one string,
    usually 'LABEL - detail' or 'N. detail', so split on the first dash."""
    for sep in (" \u2014 ", " - ", ": "):
        if sep in text:
            head, _, rest = text.partition(sep)
            if 3 < len(head) <= 60:
                return {"heading": head.strip(), "body": rest.strip()}
    # No separator: keep the sentence whole. Splitting on a character count
    # cuts mid-clause ("...than you were last" / "year?") and looks broken.
    return {"heading": text, "body": ""}


def spec_for(piece: dict, cta: str) -> dict:
    base = {
        "hook": piece["hook"],
        "subject": SUBJECT_MAP.get(piece.get("subject", "General"), "Mentorsy"),
        "pillar": PILLAR_MAP.get(piece["pillar"], "Curriculum Decoded"),
        "cta": cta,
    }
    fmt = piece["formats"][0]
    if fmt == "reel":
        base["beats"] = beats_from_script(piece.get("reel_script", ""))[:8]
    elif fmt == "carousel":
        slides = [s.strip() for s in (piece.get("slides") or []) if s.strip()]
        # Slide 1 repeats the hook (already the cover) and the last is the CTA.
        body = slides[1:-1][:8] or slides[:6]
        base["points"] = [_split_slide(s) for s in body]
        base["kind"] = "list"
    else:
        base["kind"] = "statement"
        base["sub"] = (piece.get("body") or "").split("\n")[0][:160]
    return base


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    bank = json.load(open(BANK, encoding="utf-8"))
    cfg = json.load(open(PILLARS, encoding="utf-8"))
    soft = cfg["cta_ladder"]["soft"]["lines"][0]
    os.makedirs(MEDIA_DIR, exist_ok=True)
    manifest = json.load(open(MANIFEST, encoding="utf-8")) if os.path.exists(MANIFEST) else {}

    made = skipped = failed = 0
    for piece in (bank[:a.limit] if a.limit else bank):
        pid, fmt = piece["id"], piece["formats"][0]
        key = f"{pid}:{fmt}"
        if key in manifest and not a.force:
            skipped += 1
            continue
        spec = spec_for(piece, soft)
        try:
            if fmt == "reel":
                out = os.path.join(MEDIA_DIR, f"{pid}.mp4")
                if reels.render(spec, out) is None:
                    raise RuntimeError("ffmpeg unavailable")
                manifest[key] = {"video_url": f"{RAW}/{pid}.mp4"}
            elif fmt == "carousel":
                urls = []
                # cards.carousel() gives cover + points + close; cards.render()
                # collapses a list into ONE page, which is not a carousel.
                for i, page in enumerate(cards.carousel(spec), 1):
                    p = os.path.join(MEDIA_DIR, f"{pid}-{i}.jpg")
                    page.convert("RGB").save(p, quality=88)
                    urls.append(f"{RAW}/{pid}-{i}.jpg")
                manifest[key] = {"image_urls": urls}
            else:
                page = cards.render(spec)[0]
                p = os.path.join(MEDIA_DIR, f"{pid}.jpg")
                page.convert("RGB").save(p, quality=88)
                manifest[key] = {"image_url": f"{RAW}/{pid}.jpg"}
            made += 1
        except Exception as e:                       # noqa: BLE001
            failed += 1
            print(f"  ! {pid} ({fmt}): {type(e).__name__}: {e}")

    json.dump(manifest, open(MANIFEST, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"rendered {made}, already present {skipped}, failed {failed}")
    print(f"manifest now covers {len(manifest)} / {len(bank)} pieces")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
