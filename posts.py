"""
Mentorsy — post builder

Five post shapes on one structural grid, so they read as a single brand
whatever the background does:

    hook      light, typographic. opening slide of a carousel
    point     numbered body slide
    statement dark. punctuation, roughly one post in six
    photo     full bleed with a caption plate
    cta       light close with the ask

Position is fixed. Only ground and imagery change.
"""

import json
import os
import sys

from PIL import Image, ImageDraw

import brandkit as B

W, H, M = B.W, B.H, B.MARGIN


def slide_hook(headline, pillar):
    img, d = B.ground(False)
    B.paste_logo(img, 300, (M, 84), False)
    d = ImageDraw.Draw(img)
    tint = B.PILLAR_TINT.get(pillar, B.MUTED)
    B.kicker(d, pillar, 240, tint)

    fnt, lines, lh = B.fit(d, headline, W - 2 * M, 620, 98)
    y = 400
    for ln in lines:
        d.text((M, y), ln, font=fnt, fill=B.INK)
        y += lh
    B.handle(d)
    sw = B.font(29, False, False)
    d.text((W - M - d.textlength("swipe", font=sw), H - 96), "swipe",
           font=sw, fill=B.MUTED)
    return img


def slide_point(n, total, heading, body, pillar):
    img, d = B.ground(False)
    B.paste_logo(img, 220, (W - 220 - M, 88), False)
    d = ImageDraw.Draw(img)
    tint = B.PILLAR_TINT.get(pillar, B.MUTED)
    d.text((M, 96), f"{n:02d} / {total:02d}", font=B.font(29, False, False),
           fill=tint)
    d.rectangle([M, 154, M + 140, 157], fill=tint)

    hf, hl, hlh = B.fit(d, heading, W - 2 * M, 300, 72)
    bf, bl, blh = B.fit(d, body, W - 2 * M, 520, 46,
                        serif=False, bold=False, min_size=32)

    block = len(hl) * hlh + 44 + len(bl) * blh
    y = 250 + max(0, (H - 250 - 190 - block) // 2)
    for ln in hl:
        d.text((M, y), ln, font=hf, fill=B.INK)
        y += hlh
    y += 44
    for ln in bl:
        d.text((M, y), ln, font=bf, fill=(92, 78, 104))
        y += blh
    B.handle(d)
    return img


def slide_statement(line, sub=None):
    img, d = B.ground(True)
    B.paste_logo(img, 300, (M, 84), True)
    d = ImageDraw.Draw(img)
    d.rectangle([M, 300, M + 140, 303], fill=B.MUTED)

    fnt, lines, lh = B.fit(d, line, W - 2 * M, 520, 106)
    y = 430
    for ln in lines:
        d.text((M, y), ln, font=fnt, fill=B.PAPER)
        y += lh
    if sub:
        d.text((M, y + 44), sub, font=B.font(50, False, True), fill=B.MUTED)
    B.handle(d, True)
    return img


def slide_photo(photo_path, caption):
    ph = Image.open(photo_path).convert("RGB")
    s = max(W / ph.width, H / ph.height)
    ph = ph.resize((int(ph.width * s) + 1, int(ph.height * s) + 1), Image.LANCZOS)
    l, t = (ph.width - W) // 2, (ph.height - H) // 2
    img = ph.crop((l, t, l + W, t + H))

    PLATE = 360
    ov = Image.new("RGBA", (W, PLATE), (*B.DARK, 210))
    img.paste(ov, (0, H - PLATE), ov)
    d = ImageDraw.Draw(img)

    fnt, lines, lh = B.fit(d, caption, W - 2 * M, PLATE - 150, 56)
    y = H - PLATE + 52
    for ln in lines:
        d.text((M, y), ln, font=fnt, fill=B.PAPER)
        y += lh
    B.paste_logo(img, 240, (W - 240 - 72, 72), True)
    d = ImageDraw.Draw(img)
    d.text((M, H - 72), "@mentorsy.in", font=B.font(28, False, False),
           fill=B.MUTED)
    return img


def slide_cta(line, sub="Cambridge · IGCSE · A Level Mathematics"):
    img, d = B.ground(False)
    B.paste_logo(img, 420, (W // 2 - 210, 300), False)
    d = ImageDraw.Draw(img)

    fnt, lines, lh = B.fit(d, line, W - 2 * M, 420, 74)
    y = 640
    for ln in lines:
        d.text((M, y), ln, font=fnt, fill=B.INK)
        y += lh
    d.text((M, H - 176), "@mentorsy.in", font=B.font(38, False, False),
           fill=B.INK)
    d.text((M, H - 120), sub, font=B.font(28, False, False), fill=B.MUTED)
    return img


def build_carousel(spec, outdir):
    os.makedirs(outdir, exist_ok=True)
    paths = []
    pts = spec["points"]
    pillar = spec.get("pillar", "Mentorsy")

    def save(im, i):
        p = os.path.join(outdir, f"slide_{i}.png")
        im.save(p, quality=95)
        paths.append(p)

    save(slide_hook(spec["hook"], pillar), 1)
    for i, pt in enumerate(pts, 1):
        save(slide_point(i, len(pts), pt["heading"], pt["body"], pillar), i + 1)
    save(slide_cta(spec["cta"]), len(pts) + 2)

    with open(os.path.join(outdir, "caption.txt"), "w", encoding="utf-8") as f:
        f.write(spec["caption"] + "\n\n" + " ".join(spec["hashtags"][:4]))
    return paths


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = os.path.join(os.path.dirname(sys.argv[1]), spec["slug"])
    ps = build_carousel(spec, out)
    print(f"{len(ps)} slides -> {out}")
