"""
Mentorsy — image generation

Uses the Gemini API free tier (gemini-2.5-flash-image, "Nano Banana"):
500 images per day at zero cost. Get a key at https://aistudio.google.com/apikey

Every prompt gets the brand STYLE_LOCK appended, which is what makes
the whole feed look like it came from one art director.

If no API key is set, falls back to generating branded gradient cards so
you can test the pipeline before wiring anything up.
"""

import base64
import hashlib
import re
import os
import random
import time

import requests
from PIL import Image, ImageDraw, ImageFilter

import config as C

API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent"
)


def _hex(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _placeholder(prompt: str, path: str):
    """Deterministic branded gradient — same prompt always gives the same card."""
    seed = int(hashlib.md5(prompt.encode()).hexdigest()[:8], 16)
    rnd = random.Random(seed)
    W, H = C.WIDTH, C.HEIGHT

    top, bot = _hex(C.PURPLE), _hex("#160A22")
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)],
               fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))

    gold, lav = _hex(C.GOLD), _hex(C.LAVENDER)
    layer = Image.new("RGB", (W, H), (0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for _ in range(7):
        cx, cy = rnd.randint(0, W), rnd.randint(int(H * 0.35), H)
        r = rnd.randint(160, 460)
        ld.ellipse([cx - r, cy - r, cx + r, cy + r],
                   fill=gold if rnd.random() < 0.5 else lav)
    layer = layer.filter(ImageFilter.GaussianBlur(150))
    img = Image.blend(img, layer, 0.30)

    for _ in range(4):
        x = rnd.randint(0, W)
        d.line([(x, int(H * 0.45)), (x + rnd.randint(-260, 260), H)],
               fill=gold, width=2)

    img.save(path, quality=95)
    return path


STOCK_ENABLED = os.environ.get("USE_STOCK_IMAGES", "true").lower() == "true"
OPENVERSE = "https://api.openverse.org/v1/images/"

_NOISE = re.compile(
    r"\b(seen|slightly|from|the|side|close|overhead|view|of|a|an|in|on|at|with|"
    r"soft|natural|daylight|light|blurred|background|focus|shot|angle|no|"
    r"readable|detail|neither|facing|camera|front|resting|across|beside|"
    r"pulled|out|tucked|under|quiet|empty|wide|tall|distance)\b", re.I)


def _stock_query(prompt: str) -> str:
    """Reduce an image prompt to 3-4 concrete subject words."""
    words = _NOISE.sub(" ", prompt).split()
    seen, out = set(), []
    for w in words:
        k = w.strip(",.").lower()
        if k and k not in seen and len(k) > 2:
            seen.add(k)
            out.append(k)
        if len(out) == 4:
            break
    return " ".join(out) or "study desk"


def _fetch_image(url):
    """Download and decode one candidate. Returns a PIL image or None."""
    from io import BytesIO
    r = requests.get(url, timeout=45, headers={
        "User-Agent": "Mozilla/5.0 (compatible; MentorsyReelFactory/1.0)",
        "Accept": "image/*",
    })
    if r.status_code != 200:
        return None, f"http {r.status_code}"
    if len(r.content) < 8000:
        return None, f"only {len(r.content)}b"
    try:
        return Image.open(BytesIO(r.content)).convert("RGB"), "ok"
    except Exception as e:
        return None, f"decode {e}"


def _fit_frame(im, path):
    tw, th = C.WIDTH, C.HEIGHT
    scale = max(tw / im.width, th / im.height)
    im = im.resize((int(im.width * scale) + 1, int(im.height * scale) + 1),
                   Image.LANCZOS)
    left, top = (im.width - tw) // 2, (im.height - th) // 2
    im.crop((left, top, left + tw, top + th)).save(path, quality=92)


def _stock_image(prompt: str, path: str) -> bool:
    """Free, keyless documentary photography. Every branch logs why it failed."""
    if not STOCK_ENABLED:
        print("       stock: disabled")
        return False
    q = _stock_query(prompt)
    try:
        r = requests.get(OPENVERSE,
                         params={"q": q, "page_size": 20, "mature": "false"},
                         headers={"User-Agent": "MentorsyReelFactory/1.0"},
                         timeout=30)
        if r.status_code != 200:
            print(f"       stock: search http {r.status_code} for '{q}'")
            return False
        results = r.json().get("results", [])
    except Exception as e:
        print(f"       stock: search failed for '{q}': {e}")
        return False

    if not results:
        print(f"       stock: no results for '{q}'")
        return False

    reasons = []
    for hit in results:
        for field in ("url", "thumbnail"):
            u = hit.get(field)
            if not u:
                continue
            im, why = _fetch_image(u)
            if im is None:
                reasons.append(f"{field}:{why}")
                continue
            if min(im.size) < 380:
                reasons.append(f"{field}:small {im.size}")
                continue
            _fit_frame(im, path)
            print(f"       stock: '{q}' -> {im.size[0]}x{im.size[1]} via {field}")
            return True

    print(f"       stock: {len(results)} results for '{q}', none usable "
          f"({'; '.join(reasons[:4])})")
    return False


def _gemini_image(prompt: str, path: str, retries: int = 3) -> bool:
    key = C.GEMINI_API_KEY
    if not key or key.startswith("PASTE_"):
        return False

    full = f"{prompt.strip()}\n\n{C.STYLE_LOCK}"
    body = {
        "contents": [{"parts": [{"text": full}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }

    for attempt in range(retries):
        try:
            r = requests.post(
                API_URL.format(model=C.IMAGE_MODEL),
                headers={"x-goog-api-key": key,
                         "Content-Type": "application/json"},
                json=body, timeout=120,
            )
            if r.status_code == 429:
                wait = 20 * (attempt + 1)
                print(f"       rate limited, waiting {wait}s…")
                time.sleep(wait)
                continue
            r.raise_for_status()
            data = r.json()
            for part in data["candidates"][0]["content"]["parts"]:
                inline = part.get("inlineData") or part.get("inline_data")
                if inline:
                    with open(path, "wb") as f:
                        f.write(base64.b64decode(inline["data"]))
                    return True
            print("       no image in response, retrying…")
        except Exception as e:
            print(f"       image attempt {attempt + 1} failed: {e}")
            time.sleep(4)
    return False


IMAGE_GAP_SECONDS = float(os.environ.get("IMAGE_GAP_SECONDS", "7"))
MAX_CONSECUTIVE_PLACEHOLDERS = 3


class ImageGenerationUnavailable(RuntimeError):
    """Raised when generation fails repeatedly, so the run fails loudly."""


def generate_images(prompts, work_dir):
    """Returns a list of local image paths, one per prompt."""
    paths = []
    misses = 0
    have_key = bool(C.GEMINI_API_KEY) and not C.GEMINI_API_KEY.startswith("PASTE_")

    for i, p in enumerate(prompts):
        out = os.path.join(work_dir, f"img_{i}.jpg")
        if os.path.exists(out):
            paths.append(out)
            continue

        if _stock_image(p, out):
            print(f"       scene {i + 1}: stock photo")
            misses = 0
            paths.append(out)
            continue

        if i:
            time.sleep(IMAGE_GAP_SECONDS)

        if _gemini_image(p, out):
            print(f"       scene {i + 1}: generated")
            misses = 0
        else:
            _placeholder(p, out)
            misses += 1
            print(f"       scene {i + 1}: PLACEHOLDER - generation failed")
            if have_key and misses >= MAX_CONSECUTIVE_PLACEHOLDERS:
                raise ImageGenerationUnavailable("quota spent or key rejected")
        paths.append(out)
    return paths
