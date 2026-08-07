"""
Mentorsy — brand engine

The single source of truth for how a Mentorsy post looks.

The system in one line: purple is the INK, not the wallpaper. A warm paper
ground, aubergine type, one muted secondary, and dark used as punctuation
roughly one post in six. No gold anywhere — it was retired because a lone
metallic accent belonged to nothing once the palette went light.

Recognition comes from structure, not colour: the typography, the logo
position, the rule under the kicker and the handle never move. Backgrounds
and photography are free to vary.
"""

import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))

# ── palette ──────────────────────────────────────────────────────────────
PAPER = (250, 247, 243)   # warm off-white. never pure #FFFFFF — it clips on IG
INK = (59, 30, 84)        # aubergine. all headline type
MUTED = (138, 117, 151)   # kickers, rules, handle, secondary lines
DARK = (32, 16, 46)       # statement posts only, ~1 in 6
WHITE = (255, 255, 255)

# optional pillar chips — thin accents only, never a background
PILLAR_TINT = {
    "Curriculum Decoded": (124, 139, 122),   # sage
    "Parent Scripts":     (181, 119, 106),   # clay
    "School Choice":      (91, 107, 124),    # slate
    "Maths Confidence":   (138, 117, 151),   # muted purple
    "Inside the Method":  (122, 116, 138),   # stone
    "Reactive":           (150, 120, 120),
}

W, H = 1080, 1350          # 4:5 — the tallest ratio Instagram allows in feed
MARGIN = 88

# The purple lockup is the one logo asset in the repo. The cream version for
# dark grounds is derived from its alpha, so there is only one file to keep
# in sync.
LOGO_LIGHT = os.path.join(BASE, "brand", "logo_on_light.png")
LOGO_DARK = os.path.join(BASE, "brand", "logo_cream_lockup.png")


def _ensure_cream_lockup():
    if os.path.exists(LOGO_DARK) or not os.path.exists(LOGO_LIGHT):
        return
    src = Image.open(LOGO_LIGHT).convert("RGBA")
    cream = Image.new("RGBA", src.size, (*PAPER, 0))
    cream.putalpha(src.getchannel("A"))
    cream.save(LOGO_DARK)


_FONTS = "/usr/share/fonts/truetype/dejavu/"


def font(size, bold=True, serif=True):
    """Serif for headlines, sans for kickers and handles."""
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for path in (os.path.join(_FONTS, name),
                 "C:/Windows/Fonts/BOOKOS.TTF"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
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


def fit(draw, text, max_w, max_h, start, serif=True, bold=True, min_size=30):
    """Shrink until the block fits its box. Returns (font, lines, line_height)."""
    size = start
    while size >= min_size:
        f = font(size, bold, serif)
        lines = wrap(draw, text, f, max_w)
        lh = int(size * 1.24)
        if len(lines) * lh <= max_h:
            return f, lines, lh
        size -= 3
    f = font(min_size, bold, serif)
    return f, wrap(draw, text, f, max_w), int(min_size * 1.24)


def paste_logo(img, width, xy, on_dark):
    _ensure_cream_lockup()
    path = LOGO_DARK if on_dark else LOGO_LIGHT
    if not os.path.exists(path):
        return False
    lg = Image.open(path).convert("RGBA")
    h = max(1, int(lg.height * (width / lg.width)))
    lg = lg.resize((width, h), Image.LANCZOS)
    img.paste(lg, (int(xy[0]), int(xy[1])), lg)
    return True


def kicker(draw, text, y, tint=MUTED):
    """Small caps label plus the thin rule. Never moves."""
    draw.text((MARGIN, y), text.upper(), font=font(29, False, False), fill=tint)
    draw.rectangle([MARGIN, y + 58, MARGIN + 140, y + 61], fill=tint)


def handle(draw, on_dark=False, text="@mentorsy.in"):
    draw.text((MARGIN, H - 96), text, font=font(29, False, False), fill=MUTED)


def ground(dark=False):
    img = Image.new("RGB", (W, H), DARK if dark else PAPER)
    return img, ImageDraw.Draw(img)
