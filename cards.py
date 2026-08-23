"""
Mentorsy — still formats

Five shapes, all on one grid. The grid is the brand; the shape is the argument.

    statement   one sentence on aubergine. punctuation, roughly one in six
    list        headline plus numbered points on a single frame
    carousel    cover, one point per slide, close. for ideas that need room
    quote       a line worth repeating, set large
    compare     two columns. "this, not that"

A note on list vs carousel. A carousel earns its slides when each point needs
a sentence of its own to land; a list card wins when the points are short,
because it delivers the whole idea in the feed without asking for a swipe,
and that is what gets it saved and sent on.
"""

import os

from PIL import Image, ImageDraw

import brand as B

W, H, M = B.W, B.H, B.MARGIN


def _foot(d, note, on_dark=False):
    if note:
        d.text((M, H - 152), note, font=B.font(28, False, False),
               fill=B.MUTED)
    B.handle(d, on_dark)


# -- statement -----------------------------------------------------------

def statement(headline, sub=None, subject="Mentorsy", pillar="Confidence"):
    img, d = B.ground(True)
    B.paste_logo(img, 268, (M, 84), True)
    d = ImageDraw.Draw(img)
    tint = B.SUBJECTS.get(subject, B.MUTED)
    d.rectangle([M, 288, M + 132, 291], fill=tint)

    fnt, lines, lh = B.fit(d, headline, W - 2 * M, 520, 100, leading=1.16)
    y = 420
    for ln in lines:
        d.text((M, y), ln, font=fnt, fill=B.PAPER)
        y += lh
    if sub:
        # The sub is a sentence, not a label: it has to wrap and shrink inside
        # what the headline left behind. Drawing it as one d.text() call ran it
        # off the right edge and the canvas clipped it mid-word.
        y += 40
        box_h = max(70, (H - 170) - y)          # stop clear of the handle
        sf, sl, slh = B.fit(d, sub, W - 2 * M, box_h, 46,
                            serif=True, bold=False, min_size=28, leading=1.34)
        for ln in sl:
            d.text((M, y), ln, font=sf, fill=B.MUTED)
            y += slh
    B.handle(d, True)
    return img


# -- list ----------------------------------------------------------------

def list_card(headline, items, subject, pillar, foot=None):
    img, d = B.ground(False)
    B.paste_logo(img, 250, (M, 78), False)
    d = ImageDraw.Draw(img)
    tint = B.kicker(d, subject, pillar, 208)

    hf, hl, hlh = B.fit(d, headline, W - 2 * M, 300, 76, leading=1.18)

    NUM_W = 64
    body_w = W - 2 * M - NUM_W
    sized = None
    for size in range(44, 27, -2):
        f = B.font(size, False, False)
        rows, total = [], 0
        for it in items:
            ln = B.wrap(d, it, f, body_w)
            rows.append(ln)
            total += len(ln) * int(size * 1.3) + 28
        if total <= 690:
            sized = (f, rows, int(size * 1.3))
            break
    if not sized:
        f = B.font(28, False, False)
        sized = (f, [B.wrap(d, it, f, body_w) for it in items], 37)
    bf, rows, blh = sized

    y = 322
    for ln in hl:
        d.text((M, y), ln, font=hf, fill=B.INK)
        y += hlh

    y += 48
    d.rectangle([M, y, W - M, y + 2], fill=(228, 220, 232))
    y += 44

    nf = B.font(29, True, False)
    for i, ln in enumerate(rows, 1):
        d.text((M, y + 3), f"{i:02d}", font=nf, fill=tint)
        for k, part in enumerate(ln):
            d.text((M + NUM_W, y), part, font=bf,
                   fill=B.INK if k == 0 else B.BODY)
            y += blh
        y += 28

    _foot(d, foot or "Save this.")
    return img


# -- quote ---------------------------------------------------------------

def quote(line, attrib=None, subject="Mentorsy", pillar="Confidence"):
    img, d = B.ground(False)
    B.paste_logo(img, 250, (M, 78), False)
    d = ImageDraw.Draw(img)
    tint = B.kicker(d, subject, pillar, 208)

    d.text((M - 6, 300), "“", font=B.font(150, True, True), fill=tint)
    fnt, lines, lh = B.fit(d, line, W - 2 * M, 560, 84, leading=1.2)
    y = 440
    for ln in lines:
        d.text((M, y), ln, font=fnt, fill=B.INK)
        y += lh
    if attrib:
        d.text((M, y + 36), attrib, font=B.font(30, False, False), fill=B.MUTED)
    _foot(d, None)
    return img


# -- compare -------------------------------------------------------------

def compare(headline, left_title, left_items, right_title, right_items,
            subject, pillar, foot=None):
    """Two columns. Reads as "this, not that" without saying it."""
    img, d = B.ground(False)
    B.paste_logo(img, 250, (M, 78), False)
    d = ImageDraw.Draw(img)
    tint = B.kicker(d, subject, pillar, 208)

    hf, hl, hlh = B.fit(d, headline, W - 2 * M, 220, 68, leading=1.18)
    y = 322
    for ln in hl:
        d.text((M, y), ln, font=hf, fill=B.INK)
        y += hlh

    top = y + 54
    col_w = (W - 2 * M - 56) // 2
    d.rectangle([W // 2 - 1, top, W // 2 + 1, H - 240], fill=(228, 220, 232))

    for idx, (title, items, x) in enumerate(
            [(left_title, left_items, M),
             (right_title, right_items, M + col_w + 56)]):
        d.text((x, top), title.upper(), font=B.font(25, False, False),
               fill=tint if idx else B.MUTED)
        yy = top + 56
        bf = B.font(34, False, False)
        for it in items:
            for k, part in enumerate(B.wrap(d, it, bf, col_w - 34)):
                if k == 0:
                    d.ellipse([x + 4, yy + 15, x + 14, yy + 25], fill=tint)
                d.text((x + 34, yy), part, font=bf, fill=B.BODY)
                yy += 44
            yy += 18

    _foot(d, foot or "Save this.")
    return img


# -- carousel ------------------------------------------------------------

def _cover(headline, subject, pillar):
    img, d = B.ground(False)
    B.paste_logo(img, 292, (M, 84), False)
    d = ImageDraw.Draw(img)
    B.kicker(d, subject, pillar, 236)

    fnt, lines, lh = B.fit(d, headline, W - 2 * M, 640, 96, leading=1.16)
    y = 396
    for ln in lines:
        d.text((M, y), ln, font=fnt, fill=B.INK)
        y += lh
    B.handle(d)
    sw = B.font(27, False, False)
    d.text((W - M - d.textlength("swipe", font=sw), H - 96), "swipe",
           font=sw, fill=B.MUTED)
    return img


def _point(n, total, heading, body, subject, pillar):
    img, d = B.ground(False)
    B.paste_logo(img, 210, (W - 210 - M, 88), False)
    d = ImageDraw.Draw(img)
    tint = B.SUBJECTS.get(subject, B.MUTED)
    d.text((M, 94), f"{n:02d} / {total:02d}", font=B.font(27, False, False),
           fill=tint)
    d.rectangle([M, 148, M + 132, 151], fill=tint)

    hf, hl, hlh = B.fit(d, heading, W - 2 * M, 300, 70, leading=1.18)
    bf, bl, blh = B.fit(d, body, W - 2 * M, 500, 44, serif=False, bold=False,
                        min_size=30, leading=1.36)

    block = len(hl) * hlh + 42 + len(bl) * blh
    y = 246 + max(0, (H - 246 - 190 - block) // 2)
    for ln in hl:
        d.text((M, y), ln, font=hf, fill=B.INK)
        y += hlh
    y += 42
    for ln in bl:
        d.text((M, y), ln, font=bf, fill=B.BODY)
        y += blh
    B.handle(d)
    return img


def _close(line, sub=None):
    img, d = B.ground(False)
    B.paste_logo(img, 400, (W // 2 - 200, 300), False)
    d = ImageDraw.Draw(img)
    fnt, lines, lh = B.fit(d, line, W - 2 * M, 400, 70, leading=1.2)
    y = 640
    for ln in lines:
        d.text((M, y), ln, font=fnt, fill=B.INK)
        y += lh
    d.text((M, H - 178), B.HANDLE, font=B.font(36, False, False), fill=B.INK)
    d.text((M, H - 122), sub or B.STRAP, font=B.font(25, False, False),
           fill=B.MUTED)
    return img


def carousel(spec):
    """Returns a list of PIL images: cover, one per point, close."""
    subject = spec.get("subject", "Mentorsy")
    pillar = spec.get("pillar", "Curriculum Decoded")
    pts = spec["points"]
    pages = [_cover(spec["hook"], subject, pillar)]
    for i, p in enumerate(pts, 1):
        pages.append(_point(i, len(pts), p["heading"], p["body"],
                            subject, pillar))
    pages.append(_close(spec.get("cta", "Follow for the rest.")))
    return pages


# -- dispatch ------------------------------------------------------------

def render(spec):
    """spec -> list of PIL images (one for stills, several for a carousel)."""
    kind = spec.get("kind", "list")
    subject = spec.get("subject", "Mentorsy")
    pillar = spec.get("pillar", "Curriculum Decoded")

    if kind == "carousel":
        return carousel(spec)
    if kind == "statement":
        return [statement(spec["hook"], spec.get("sub"), subject, pillar)]
    if kind == "quote":
        return [quote(spec["hook"], spec.get("attrib"), subject, pillar)]
    if kind == "compare":
        return [compare(spec["hook"],
                        spec["left_title"], spec["left"],
                        spec["right_title"], spec["right"],
                        subject, pillar, spec.get("cta"))]
    return [list_card(spec["hook"], [p["heading"] for p in spec["points"]],
                      subject, pillar, spec.get("cta"))]
