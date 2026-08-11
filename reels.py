"""
Mentorsy - reel renderer

Builds a 9:16 reel as a sequence of typographic beats, then stitches them with
ffmpeg. No network, no API keys, no per-clip cost, so a month of reels renders
in the time it takes to make tea.

Three deliberate choices:

1. Music is baked in, and the reel still reads with the sound off. Instagram's
   publishing API cannot attach a track from Instagram's own music library -
   anything published through it carries only the audio already inside the
   file - so a reel that goes out automatically has to bring its own. The bed
   comes from _engine/music/ and sits well under the type, because these reels
   argue in typography and music that competes with the reading is worse than
   silence.

2. The first beat holds for two full seconds with the hook already legible.
   Retention is decided in the first second and a half; an animated build-on
   spends that budget on decoration.

3. A presenter clip is optional, not required. Drop a 9:16 mp4 into
   _engine/presenter/ named after the slug and it becomes the opening two
   seconds with the brand frame composited over it. Without one, the reel
   opens on the hook card. Either way the rest is identical, so the feed keeps
   its rhythm whether or not a face was available that week.
"""

import os
import shutil
import subprocess
import tempfile

from PIL import Image, ImageDraw

import brand as B
import audio

RW, RH, RM = B.REEL_W, B.REEL_H, B.REEL_MARGIN
FPS = 30

PRESENTER_DIR = os.path.join(B.BASE, "presenter")


def _bar(d, y, tint, w=132):
    d.rectangle([RM, y, RM + w, y + 4], fill=tint)


def beat_hook(text, subject, pillar):
    img, d = B.ground(False, (RW, RH))
    B.paste_logo(img, 300, (RM, 150), False)
    d = ImageDraw.Draw(img)
    tint = B.SUBJECTS.get(subject, B.MUTED)
    label = f"{subject}  /  {pillar}".upper()
    d.text((RM, 330), label, font=B.font(28, False, False), fill=tint)
    _bar(d, 386, tint)

    fnt, lines, lh = B.fit(d, text, RW - 2 * RM, 780, 112, leading=1.16)
    y = 620
    for ln in lines:
        d.text((RM, y), ln, font=fnt, fill=B.INK)
        y += lh
    d.text((RM, RH - 190), B.HANDLE, font=B.font(32, False, False),
           fill=B.MUTED)
    return img


def beat_line(text, subject, n=None, total=None, dark=False):
    img, d = B.ground(dark, (RW, RH))
    tint = B.SUBJECTS.get(subject, B.MUTED)
    fg = B.PAPER if dark else B.INK
    if n:
        d.text((RM, 330), f"{n:02d} / {total:02d}",
               font=B.font(28, False, False), fill=tint)
        _bar(d, 386, tint)

    fnt, lines, lh = B.fit(d, text, RW - 2 * RM, 900, 96, leading=1.2)
    block = len(lines) * lh
    y = (RH - block) // 2
    for ln in lines:
        d.text((RM, y), ln, font=fnt, fill=fg)
        y += lh
    B.paste_logo(img, 210, (RM, RH - 230), dark)
    return img


def beat_close(line, sub=None):
    img, d = B.ground(False, (RW, RH))
    B.paste_logo(img, 440, (RW // 2 - 220, 620), False)
    d = ImageDraw.Draw(img)
    fnt, lines, lh = B.fit(d, line, RW - 2 * RM, 400, 76, leading=1.2)
    y = 1000
    for ln in lines:
        d.text((RM, y), ln, font=fnt, fill=B.INK)
        y += lh
    d.text((RM, RH - 300), B.HANDLE, font=B.font(42, False, False), fill=B.INK)
    d.text((RM, RH - 236), sub or B.STRAP, font=B.font(26, False, False),
           fill=B.MUTED)
    return img


def frames(spec):
    """spec -> [(PIL image, seconds), ...]"""
    subject = spec.get("subject", "Mentorsy")
    pillar = spec.get("pillar", "Curriculum Decoded")
    beats = [(beat_hook(spec["hook"], subject, pillar), 2.4)]

    lines = spec.get("beats", [])
    total = len(lines)
    for i, ln in enumerate(lines, 1):
        # Every third beat lands on aubergine so the reel has a pulse rather
        # than eight identical cream cards in a row.
        beats.append((beat_line(ln, subject, i, total, dark=(i % 3 == 0)), 2.2))

    beats.append((beat_close(spec.get("cta", "Follow for the rest.")), 2.6))
    return beats


def _has_presenter(slug):
    if not os.path.isdir(PRESENTER_DIR):
        return None
    for ext in (".mp4", ".mov", ".webm"):
        p = os.path.join(PRESENTER_DIR, slug + ext)
        if os.path.exists(p):
            return p
    return None


def render(spec, out_path):
    """Write an mp4. Returns the path, or None if ffmpeg is unavailable."""
    if not shutil.which("ffmpeg"):
        return None

    tmp = tempfile.mkdtemp(prefix="reel_")
    try:
        concat = os.path.join(tmp, "list.txt")
        with open(concat, "w", encoding="utf-8") as f:
            for i, (img, secs) in enumerate(frames(spec)):
                p = os.path.join(tmp, f"f{i:03d}.png")
                img.save(p)
                # ffmpeg's concat demuxer needs the last entry repeated or it
                # drops the final frame's duration.
                f.write(f"file '{p}'\nduration {secs}\n")
            f.write(f"file '{p}'\n")

        clip = os.path.join(tmp, "cards.mp4")
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", concat, "-vf", f"fps={FPS},format=yuv420p",
             "-c:v", "libx264", "-preset", "medium", "-crf", "20", clip],
            check=True)

        presenter = _has_presenter(spec.get("slug", ""))
        if presenter:
            intro = os.path.join(tmp, "intro.mp4")
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", presenter,
                 "-t", "3", "-vf",
                 f"scale={RW}:{RH}:force_original_aspect_ratio=increase,"
                 f"crop={RW}:{RH},fps={FPS},format=yuv420p",
                 "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                 intro], check=True)
            joined = os.path.join(tmp, "list2.txt")
            with open(joined, "w", encoding="utf-8") as f:
                f.write(f"file '{intro}'\nfile '{clip}'\n")
            merged = os.path.join(tmp, "merged.mp4")
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat",
                 "-safe", "0", "-i", joined, "-c", "copy", merged],
                check=True)
            clip = merged

        # Anything published through the API carries only the audio inside the
        # file, so the bed goes on here rather than in the Instagram app.
        audio.attach(clip, spec.get("slug", "reel"), out_path)
        return out_path
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
