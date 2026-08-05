"""
Mentorsy — carousel generator

Makes a 7-slide 1080x1350 Instagram carousel entirely offline. No API keys,
no internet, no AI services. Pure typography on the brand palette.

Carousels earn the highest saves-per-reach on Instagram, and saves now
outrank likes. This is the cheapest reliable post you can make.

    python carousel.py posts/today.json
"""

import json
import os
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

import config as C

W, H = 1080, 1350
MARGIN = 96


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


PURPLE, GOLD, LAV, WHITE = (hexrgb(C.PURPLE), hexrgb(C.GOLD),
                            hexrgb(C.LAVENDER), (255, 255, 255))
INK = (26, 12, 40)


def font(size, bold=True, serif=True):
    """DejaVu Serif is the closest widely-available stand-in for Bookman Old
    Style. Swap in bookos.ttf here if you want an exact brand match."""
    candidates = [
        "C:/Windows/Fonts/BOOKOS.TTF" if bold else "C:/Windows/Fonts/BOOKOS.TTF",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    if not serif:
        candidates = ["C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
                      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
                      else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def wrap_to_width(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, max_w, max_h, start, min_size=34, serif=True, bold=True):
    """Shrink until the block fits. Returns (font, lines, line_height)."""
    size = start
    while size >= min_size:
        f = font(size, bold, serif)
        lines = wrap_to_width(draw, text, f, max_w)
        lh = int(size * 1.28)
        if len(lines) * lh <= max_h:
            return f, lines, lh
        size -= 3
    f = font(min_size, bold, serif)
    return f, wrap_to_width(draw, text, f, max_w), int(min_size * 1.28)


def base_slide(dark=True):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    top = PURPLE if dark else LAV
    bot = INK if dark else WHITE
    for y in range(H):
        t = (y / H) ** 1.15
        d.line([(0, y), (W, y)],
               fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    return img, d


def gold_rule(d, y, w=180):
    d.rectangle([MARGIN, y, MARGIN + w, y + 6], fill=GOLD)


LOGO_PATH = os.path.join(C.BASE_DIR, "brand", "logo.png")


def paste_logo(img, width, xy, anchor="left"):
    """Composite the real SJK Mentorsy mark. Silently skipped if missing."""
    if not os.path.exists(LOGO_PATH):
        return False
    logo = Image.open(LOGO_PATH).convert("RGBA")
    h = max(1, int(logo.height * (width / logo.width)))
    logo = logo.resize((width, h), Image.LANCZOS)
    x, y = xy
    if anchor == "right":
        x -= width
    elif anchor == "center":
        x -= width // 2
    img.paste(logo, (int(x), int(y)), logo)
    return True


def footer(d, text, dark=True):
    f = font(30, False, False)
    d.text((MARGIN, H - 78), text, font=f, fill=GOLD if dark else PURPLE)


def slide_hook(text, kicker):
    img, d = base_slide(True)

    has_logo = paste_logo(img, 340, (MARGIN, MARGIN - 10))
    d = ImageDraw.Draw(img)

    top = MARGIN + (110 if has_logo else 0)
    f = font(34, False, False)
    d.text((MARGIN, top), kicker.upper(), font=f, fill=GOLD)
    gold_rule(d, top + 62)

    fnt, lines, lh = fit_text(d, text, W - MARGIN * 2, H - 620, 106)
    y = top + 150 + max(0, (H - top - 150 - 170 - len(lines) * lh) // 2)
    for ln in lines:
        d.text((MARGIN, y), ln, font=fnt, fill=WHITE)
        y += lh

    f2 = font(30, False, False)
    d.text((MARGIN, H - 78), "@mentorsy.in", font=f2, fill=GOLD)
    d.text((W - MARGIN - d.textlength("swipe →", font=f2), H - 78),
           "swipe →", font=f2, fill=WHITE)
    return img


def slide_point(n, total, heading, body):
    img, d = base_slide(True)
    f = font(30, False, False)
    d.text((MARGIN, MARGIN), f"{n:02d} / {total:02d}", font=f, fill=GOLD)
    gold_rule(d, MARGIN + 56)

    hf, hlines, hlh = fit_text(d, heading, W - MARGIN * 2, 340, 72)
    bf, blines, blh = fit_text(d, body, W - MARGIN * 2, 560, 50,
                               min_size=34, serif=False, bold=False)

    # centre the whole block in the space between header and footer
    block = len(hlines) * hlh + 46 + len(blines) * blh
    y = MARGIN + 190 + max(0, (H - MARGIN - 190 - 150 - block) // 2)

    for ln in hlines:
        d.text((MARGIN, y), ln, font=hf, fill=GOLD)
        y += hlh
    y += 46
    for ln in blines:
        d.text((MARGIN, y), ln, font=bf, fill=WHITE)
        y += blh

    f3 = font(28, False, False)
    d.text((MARGIN, H - 78), "@mentorsy.in", font=f3, fill=GOLD)
    return img


def slide_cta(text, handle):
    img, d = base_slide(True)

    paste_logo(img, 420, (W // 2, 200), anchor="center")
    d = ImageDraw.Draw(img)

    fnt, lines, lh = fit_text(d, text, W - MARGIN * 2, H - 720, 74)
    y = 480 + max(0, (H - 480 - 260 - len(lines) * lh) // 2)
    gold_rule(d, y - 76)
    for ln in lines:
        d.text((MARGIN, y), ln, font=fnt, fill=WHITE)
        y += lh

    f = font(38, False, False)
    d.text((MARGIN, H - 200), handle, font=f, fill=GOLD)
    f2 = font(30, False, False)
    d.text((MARGIN, H - 140), "Cambridge · IGCSE · A Level Mathematics",
           font=f2, fill=LAV)
    return img


def build(spec, outdir):
    os.makedirs(outdir, exist_ok=True)
    paths = []
    pts = spec["points"]

    s = slide_hook(spec["hook"], spec.get("kicker", "Mentorsy"))
    p = os.path.join(outdir, "slide_1.png")
    s.save(p, quality=95)
    paths.append(p)

    for i, pt in enumerate(pts, 1):
        s = slide_point(i, len(pts), pt["heading"], pt["body"])
        p = os.path.join(outdir, f"slide_{i + 1}.png")
        s.save(p, quality=95)
        paths.append(p)

    s = slide_cta(spec["cta"], spec.get("handle", "@mentorsy.in"))
    p = os.path.join(outdir, f"slide_{len(pts) + 2}.png")
    s.save(p, quality=95)
    paths.append(p)

    with open(os.path.join(outdir, "caption.txt"), "w", encoding="utf-8") as f:
        f.write(spec["caption"] + "\n\n" + " ".join(spec["hashtags"][:5]))

    return paths


if __name__ == "__main__":
    spec_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        C.BASE_DIR, "posts", "today.json")
    spec = json.load(open(spec_path, encoding="utf-8"))
    out = os.path.join(C.OUTPUT_DIR, spec["slug"])
    paths = build(spec, out)
    print(f"✓ {len(paths)} slides → {out}")
    for p in paths:
        print(f"   {os.path.basename(p)}")
