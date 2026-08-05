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


def generate_images(prompts, work_dir):
    """Returns a list of local image paths, one per prompt."""
    paths = []
    for i, p in enumerate(prompts):
        out = os.path.join(work_dir, f"img_{i}.jpg")
        if os.path.exists(out):
            paths.append(out)
            continue
        if _gemini_image(p, out):
            print(f"       scene {i + 1}: generated")
        else:
            _placeholder(p, out)
            print(f"       scene {i + 1}: placeholder (no API key or generation failed)")
        paths.append(out)
    return paths
