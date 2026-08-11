"""
Mentorsy — brand engine

Mentorsy teaches Mathematics, French, Public Speaking, Coding, AI and Science.
Six subjects is enough range to look incoherent if every one of them brings its
own look, so the system is deliberately narrow:

    one ground        warm paper, or aubergine for punctuation
    one type pairing  Lora for what is said, Poppins for how it is labelled
    one accent        the subject's colour, used only on the kicker,
                      the rule under it, and the list numbers

Everything structural - logo position, margin, the rule, the handle - is
identical across all six subjects. That is what makes a French post and a
coding post read as the same brand: not shared colour, shared skeleton.
"""

import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
BRAND_DIR = os.path.join(BASE, "brand")

# -- ground --------------------------------------------------------------
PAPER = (250, 247, 243)   # warm off-white. never pure white - it clips on IG
INK = (59, 30, 84)        # aubergine. every headline
BODY = (92, 78, 104)      # body copy, one step down from INK
MUTED = (138, 117, 151)   # kickers, rules, handle
DARK = (32, 16, 46)       # statement pieces only, roughly one in six

# -- subjects ------------------------------------------------------------
# The accent is a thin signal, not a theme. It appears on maybe 4 percent of
# the pixels: the kicker, its rule, and the numerals in a list.
SUBJECTS = {
    "Mathematics":     (138, 117, 151),   # muted purple
    "French":          (124, 139, 122),   # sage
    "Public Speaking": (181, 119, 106),   # clay
    "Coding":          (91, 107, 124),    # slate
    "AI":              (79, 106, 110),    # deep teal
    "Science":         (122, 116, 138),   # stone
    "Mentorsy":        MUTED,             # cross-subject
}

# Content pillars. A pillar answers "why is this post here", a subject answers
# "what is it about". Every piece carries exactly one of each.
PILLARS = [
    "Curriculum Decoded",   # how the syllabus actually works
    "Parent Scripts",       # the sentence to say, the question to ask
    "School Choice",        # choosing a school, a board, a programme
    "Confidence",           # the emotional layer under the academic one
    "Inside the Method",    # how Mentorsy teaches it
    "Future Skills",        # where coding, AI and speaking actually lead
]

# -- canvas --------------------------------------------------------------
W, H = 1080, 1350          # 4:5, the tallest ratio the feed allows
MARGIN = 88

REEL_W, REEL_H = 1080, 1920
REEL_MARGIN = 96

HANDLE = "@mentorsy.in"
STRAP = "Maths / French / Speaking / Coding / AI / Science"

LOGO_LIGHT = os.path.join(BRAND_DIR, "logo_on_light.png")
LOGO_DARK = os.path.join(BRAND_DIR, "logo_cream_lockup.png")

# The typefaces ship with the engine. Both are Open Font Licence, so they can
# live in the repo, and that means a build on a bare CI runner looks identical
# to a build on this machine rather than silently falling back to whatever
# serif happens to be installed.
_LOCAL = os.path.join(BASE, "fonts")
_GF = "/usr/share/fonts/truetype/google-fonts/"
_DEJAVU = "/usr/share/fonts/truetype/dejavu/"

# Lora carries the voice; Poppins does the labelling. Falling back to DejaVu
# keeps the renderer working on a machine without the Google fonts rather
# than failing a whole month's build over a typeface.
_FACES = {
    ("serif", True):  [os.path.join(_LOCAL, "Lora-Variable.ttf"),
                       _GF + "Lora-Variable.ttf",
                       _DEJAVU + "DejaVuSerif-Bold.ttf"],
    ("serif", False): [os.path.join(_LOCAL, "Lora-Variable.ttf"),
                       _GF + "Lora-Variable.ttf",
                       _DEJAVU + "DejaVuSerif.ttf"],
    ("sans", True):   [os.path.join(_LOCAL, "Poppins-Medium.ttf"),
                       _GF + "Poppins-Medium.ttf",
                       _DEJAVU + "DejaVuSans-Bold.ttf"],
    ("sans", False):  [os.path.join(_LOCAL, "Poppins-Light.ttf"),
                       _GF + "Poppins-Light.ttf",
                       _DEJAVU + "DejaVuSans.ttf"],
}

_CACHE = {}


def font(size, bold=True, serif=True):
    key = (size, bold, serif)
    if key in _CACHE:
        return _CACHE[key]
    for path in _FACES[("serif" if serif else "sans", bold)]:
        if os.path.exists(path):
            f = ImageFont.truetype(path, size)
            # Lora ships as a variable font; ask for the weight we want.
            if "Variable" in path:
                try:
                    f.set_variation_by_axes([700 if bold else 400])
                except Exception:
                    pass
            _CACHE[key] = f
            return f
    f = ImageFont.load_default()
    _CACHE[key] = f
    return f


def ensure_cream_lockup():
    """Derive the cream logo from the purple one so there is one file to keep."""
    if os.path.exists(LOGO_DARK) or not os.path.exists(LOGO_LIGHT):
        return
    src = Image.open(LOGO_LIGHT).convert("RGBA")
    cream = Image.new("RGBA", src.size, (*PAPER, 0))
    cream.putalpha(src.getchannel("A"))
    cream.save(LOGO_DARK)


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


def fit(draw, text, max_w, max_h, start, serif=True, bold=True,
        min_size=28, leading=1.22):
    """Shrink until the block fits its box. Returns (font, lines, line_height)."""
    size = start
    while size >= min_size:
        f = font(size, bold, serif)
        lines = wrap(draw, text, f, max_w)
        lh = int(size * leading)
        if len(lines) * lh <= max_h:
            return f, lines, lh
        size -= 2
    f = font(min_size, bold, serif)
    return f, wrap(draw, text, f, max_w), int(min_size * leading)


def paste_logo(img, width, xy, on_dark):
    ensure_cream_lockup()
    path = LOGO_DARK if on_dark else LOGO_LIGHT
    if not os.path.exists(path):
        return False
    lg = Image.open(path).convert("RGBA")
    h = max(1, int(lg.height * (width / lg.width)))
    lg = lg.resize((width, h), Image.LANCZOS)
    img.paste(lg, (int(xy[0]), int(xy[1])), lg)
    return True


def kicker(draw, subject, pillar, y, x=MARGIN, rule=True):
    """SUBJECT / PILLAR in small caps, with the rule under it. Never moves."""
    tint = SUBJECTS.get(subject, MUTED)
    label = f"{subject}  /  {pillar}".upper()
    f = font(25, False, False)
    draw.text((x, y), label, font=f, fill=tint)
    if rule:
        draw.rectangle([x, y + 50, x + 132, y + 53], fill=tint)
    return tint


def handle(draw, on_dark=False, y=None):
    draw.text((MARGIN, y if y is not None else H - 96), HANDLE,
              font=font(27, False, False), fill=MUTED)


def ground(dark=False, size=None):
    w, h = size or (W, H)
    img = Image.new("RGB", (w, h), DARK if dark else PAPER)
    return img, ImageDraw.Draw(img)
