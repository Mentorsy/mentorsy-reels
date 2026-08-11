"""
Mentorsy - hero reel

The face problem, solved by structure rather than by technology.

A generated presenter cannot hold the same face across sixty reels, and a
brand whose presenter changes every week is worse off than a brand with no
presenter at all. So the presenter appears once, at the front, for ten
seconds, and never returns:

    0-10s   a person, talking. the hook, delivered by a human face
    10-24s  b-roll. the empty desk, the marked paper, the clock.
            text carries the argument, the footage carries the feeling
    24-28s  the brand card

Because the face only ever appears in the opening shot, two reels made from
two different generated people do not read as inconsistent. They read as two
different reels. The continuity the viewer actually tracks is the typography,
the colour and the close card, and those never move.

B-roll is openly licensed documentary photography with a slow push on it.
A still with motion reads as footage at reel length, and it costs nothing,
needs no key, and never runs out of quota.
"""

import os
import shutil
import subprocess
import tempfile
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFilter

import brand as B
import audio

RW, RH, RM = B.REEL_W, B.REEL_H, B.REEL_MARGIN
FPS = 30

OPENVERSE = "https://api.openverse.org/v1/images/"
UA = {"User-Agent": "MentorsyStudio/1.0"}

PRESENTER_DIR = os.path.join(B.BASE, "presenter")
CACHE_DIR = os.path.join(B.BASE, ".broll_cache")


# -- b-roll sourcing -----------------------------------------------------

def fetch_still(query, path):
    """Openly licensed photography, cropped to 9:16. Returns True on success."""
    if os.path.exists(path):
        return True
    try:
        r = requests.get(OPENVERSE,
                         params={"q": query, "page_size": 12,
                                 "license_type": "all", "aspect_ratio": "tall",
                                 "mature": "false"},
                         headers=UA, timeout=30)
        r.raise_for_status()
        for hit in r.json().get("results", []):
            url = hit.get("url")
            if not url:
                continue
            img = requests.get(url, headers=UA, timeout=45)
            if img.status_code != 200 or len(img.content) < 20000:
                continue
            im = Image.open(BytesIO(img.content)).convert("RGB")
            if min(im.size) < 700:
                continue
            # Overscan: zoompan needs room to move without hitting an edge.
            tw, th = int(RW * 1.25), int(RH * 1.25)
            s = max(tw / im.width, th / im.height)
            im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1),
                           Image.LANCZOS)
            l, t = (im.width - tw) // 2, (im.height - th) // 2
            im.crop((l, t, l + tw, t + th)).save(path, quality=92)
            return True
    except Exception as e:
        print(f"    b-roll '{query}': {e}")
    return False


def _tone(path):
    """Desaturate and cool the photo so six different sources read as one film."""
    im = Image.open(path).convert("RGB")
    grey = im.convert("L").convert("RGB")
    im = Image.blend(im, grey, 0.55)
    wash = Image.new("RGB", im.size, B.INK)
    im = Image.blend(im, wash, 0.16)
    im.save(path, quality=92)


# -- overlays ------------------------------------------------------------

def _scrim():
    """Bottom gradient so white text survives a bright photo."""
    sc = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
    d = ImageDraw.Draw(sc)
    top = int(RH * 0.42)
    for y in range(top, RH):
        a = int(232 * ((y - top) / (RH - top)) ** 0.8)
        d.line([(0, y), (RW, y)], fill=(*B.DARK, a))
    return sc


def broll_text(caption, subject, n=None, total=None):
    """Transparent overlay: scrim, caption, counter, logo."""
    layer = Image.alpha_composite(
        Image.new("RGBA", (RW, RH), (0, 0, 0, 0)), _scrim())
    d = ImageDraw.Draw(layer)
    tint = B.SUBJECTS.get(subject, B.MUTED)

    fnt, lines, lh = B.fit(d, caption, RW - 2 * RM, 620, 84, leading=1.18)
    y = RH - 470 - len(lines) * lh
    if n:
        d.text((RM, y - 92), f"{n:02d} / {total:02d}",
               font=B.font(28, False, False), fill=tint)
        d.rectangle([RM, y - 38, RM + 132, y - 34], fill=tint)
    for ln in lines:
        d.text((RM, y), ln, font=fnt, fill=B.PAPER)
        y += lh

    tmp = Image.new("RGB", (RW, RH), B.DARK)
    B.paste_logo(tmp, 210, (RM, RH - 250), True)
    # Lift just the logo pixels out of the scratch canvas.
    mask = tmp.point(lambda v: 255 if v > 40 else 0).convert("L")
    layer.paste(tmp, (0, 0), mask)
    return layer


def presenter_frame(subject, pillar):
    """Lower-third for the opening shot, so the face arrives already branded."""
    layer = Image.new("RGBA", (RW, RH), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    tint = B.SUBJECTS.get(subject, B.MUTED)

    plate = Image.new("RGBA", (RW, 250), (*B.DARK, 205))
    layer.paste(plate, (0, RH - 250), plate)
    d = ImageDraw.Draw(layer)
    d.text((RM, RH - 205), f"{subject}  /  {pillar}".upper(),
           font=B.font(26, False, False), fill=tint)
    d.rectangle([RM, RH - 158, RM + 132, RH - 154], fill=tint)
    d.text((RM, RH - 128), B.HANDLE, font=B.font(34, False, False),
           fill=B.PAPER)
    return layer


def cold_open(subject, pillar, hook):
    """
    The opening when no presenter clip has been supplied.

    This is not a placeholder. A hero reel has to be publishable the week it
    is written, whether or not anyone got round to generating a face, so the
    faceless version is designed rather than apologised for: the claim alone
    on aubergine, held long enough to read twice, with a slow push added at
    render time so it moves like an opening shot instead of sitting there like
    a slide.

    When a presenter clip does arrive it replaces this and nothing else
    changes, which is what lets the two versions live in the same feed.
    """
    img, d = B.ground(True, (RW, RH))
    B.paste_logo(img, 300, (RM, 190), True)
    d = ImageDraw.Draw(img)
    tint = B.SUBJECTS.get(subject, B.MUTED)
    d.text((RM, 400), f"{subject}  /  {pillar}".upper(),
           font=B.font(28, False, False), fill=tint)
    d.rectangle([RM, 456, RM + 132, 460], fill=tint)

    fnt, lines, lh = B.fit(d, hook, RW - 2 * RM, 720, 106, leading=1.16)
    y = 700
    for ln in lines:
        d.text((RM, y), ln, font=fnt, fill=B.PAPER)
        y += lh

    d.text((RM, RH - 250), B.HANDLE, font=B.font(32, False, False),
           fill=B.MUTED)
    return img


def close_card(line):
    img, d = B.ground(False, (RW, RH))
    B.paste_logo(img, 440, (RW // 2 - 220, 640), False)
    d = ImageDraw.Draw(img)
    fnt, lines, lh = B.fit(d, line, RW - 2 * RM, 380, 76, leading=1.2)
    y = 1020
    for ln in lines:
        d.text((RM, y), ln, font=fnt, fill=B.INK)
        y += lh
    d.text((RM, RH - 300), B.HANDLE, font=B.font(42, False, False), fill=B.INK)
    d.text((RM, RH - 236), B.STRAP, font=B.font(26, False, False), fill=B.MUTED)
    return img


# -- assembly ------------------------------------------------------------

def _run(args):
    subprocess.run(args, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def _still_clip(png, secs, out, zoom_in=True, overscan=True):
    """
    Ken Burns. A slow push is the difference between a slide and a shot.

    overscan=False is for cards rendered at exactly 1080x1920: the push has to
    be gentler, because there is no spare image outside the frame to move into
    and a hard zoom would crop the typography.
    """
    n = int(secs * FPS)
    rate = 0.0009 if overscan else 0.00035
    top = 1.22 if overscan else 1.05
    z = (f"min(1+{rate}*on,{top})" if zoom_in
         else f"max({top}-{rate}*on,1.0)")
    vf = (f"zoompan=z='{z}':d={n}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          f":s={RW}x{RH}:fps={FPS},format=yuv420p")
    _run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", png,
          "-t", str(secs), "-vf", vf, "-c:v", "libx264", "-preset", "medium",
          "-crf", "20", out])


def _overlay(base, png, out):
    _run(["ffmpeg", "-y", "-loglevel", "error", "-i", base, "-i", png,
          "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto",
          "-c:v", "libx264", "-preset", "medium", "-crf", "20", out])


def _card_clip(img, secs, out):
    p = out + ".png"
    img.save(p)
    _run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", p,
          "-t", str(secs), "-vf", f"fps={FPS},format=yuv420p",
          "-c:v", "libx264", "-preset", "medium", "-crf", "20", out])
    os.remove(p)


def _clip_named(name):
    if not os.path.isdir(PRESENTER_DIR):
        return None
    for ext in (".mp4", ".mov", ".webm", ".m4v"):
        p = os.path.join(PRESENTER_DIR, name + ext)
        if os.path.exists(p):
            return p
    return None


def find_presenter(slug):
    """presenter/<slug>.mp4 - the talking head."""
    return _clip_named(slug)


def find_broll(slug, i):
    """
    presenter/<slug>_b1.mp4, _b2.mp4 ...

    Generated footage beats stock photography here, and not by a little. A
    stock photo of a stressed teenager is the most over-used image in
    education marketing; it reads as a stock photo, and a brand built on
    restraint cannot afford one. A ten second Veo clip of hands on a maths
    paper, or a pen stopping, has no face in it at all - which means
    consistency between reels is a non-issue - and it looks like it was shot
    for this.

    Same Gemini session as the presenter clip. Two minutes more work.
    """
    return _clip_named(f"{slug}_b{i}")


def render(spec, out_path, presenter_seconds=10):
    """
    spec:
      slug, subject, pillar, hook
      broll: [{"query": "...", "caption": "..."}, ...]
      cta
    """
    if not shutil.which("ffmpeg"):
        return None
    os.makedirs(CACHE_DIR, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="hero_")
    parts = []
    try:
        subject = spec.get("subject", "Mentorsy")
        pillar = spec.get("pillar", "Confidence")

        # 1. the face
        #
        # The presenter speaks, and the speech is the whole point of the shot -
        # a silent face is a stock photo that moves. So the clip's own audio is
        # kept and becomes the audio for this stretch of the reel; the music
        # bed starts afterwards, under the b-roll.
        clip = find_presenter(spec.get("slug", ""))
        seg = os.path.join(tmp, "00_open.mp4")
        speech = None
        if clip:
            raw = os.path.join(tmp, "00_raw.mp4")
            _run(["ffmpeg", "-y", "-loglevel", "error", "-i", clip,
                  "-t", str(presenter_seconds), "-vf",
                  f"scale={RW}:{RH}:force_original_aspect_ratio=increase,"
                  f"crop={RW}:{RH},fps={FPS},format=yuv420p",
                  "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                  raw])
            ov = os.path.join(tmp, "00_lower.png")
            presenter_frame(subject, pillar).save(ov)
            _overlay(raw, ov, seg)

            if _has_audio(clip):
                speech = os.path.join(tmp, "speech.wav")
                # loudnorm so a quiet generation does not arrive as a whisper
                # between two louder sections.
                _run(["ffmpeg", "-y", "-loglevel", "error", "-i", clip,
                      "-t", str(presenter_seconds), "-vn",
                      "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                      "-ar", "44100", "-ac", "2", speech])
        else:
            # A slow push on the card. Barely perceptible frame to frame, but
            # the difference between an opening shot and a slide.
            p = os.path.join(tmp, "00_open.png")
            cold_open(subject, pillar, spec["hook"]).save(p)
            _still_clip(p, 4.2, seg, zoom_in=True, overscan=False)
        parts.append(seg)

        # 2. the b-roll
        beats = spec.get("broll", [])
        for i, beat in enumerate(beats, 1):
            # Preference order: a generated clip, then a licensed still with a
            # push on it, then a typographic beat. The argument survives all
            # three - only the texture changes.
            bclip = find_broll(spec.get("slug", ""), i)
            if bclip:
                raw = os.path.join(tmp, f"{i:02d}_raw.mp4")
                _run(["ffmpeg", "-y", "-loglevel", "error", "-i", bclip,
                      "-t", "3.4", "-vf",
                      f"scale={RW}:{RH}:force_original_aspect_ratio=increase,"
                      f"crop={RW}:{RH},fps={FPS},"
                      f"eq=saturation=0.45:contrast=1.04,format=yuv420p",
                      "-an", "-c:v", "libx264", "-preset", "medium",
                      "-crf", "20", raw])
                ovp = os.path.join(tmp, f"{i:02d}_ov.png")
                broll_text(beat["caption"], subject, i, len(beats)).save(ovp)
                seg = os.path.join(tmp, f"{i:02d}.mp4")
                _overlay(raw, ovp, seg)
                parts.append(seg)
                continue

            key = "".join(c if c.isalnum() else "_" for c in beat["query"])[:48]
            still = os.path.join(CACHE_DIR, key + ".jpg")
            if not fetch_still(beat["query"], still):
                # No photograph for this beat: fall back to a typographic
                # card rather than dropping the line from the argument.
                seg = os.path.join(tmp, f"{i:02d}_card.mp4")
                img, d = B.ground(i % 2 == 0, (RW, RH))
                dd = ImageDraw.Draw(img)
                fnt, lines, lh = B.fit(dd, beat["caption"], RW - 2 * RM, 800,
                                       92, leading=1.2)
                y = (RH - len(lines) * lh) // 2
                for ln in lines:
                    dd.text((RM, y), ln, font=fnt,
                            fill=B.PAPER if i % 2 == 0 else B.INK)
                    y += lh
                B.paste_logo(img, 210, (RM, RH - 240), i % 2 == 0)
                _card_clip(img, 3.0, seg)
                parts.append(seg)
                continue

            _tone(still)
            base = os.path.join(tmp, f"{i:02d}_kb.mp4")
            _still_clip(still, 3.2, base, zoom_in=(i % 2 == 1))
            ovp = os.path.join(tmp, f"{i:02d}_ov.png")
            broll_text(beat["caption"], subject, i, len(beats)).save(ovp)
            seg = os.path.join(tmp, f"{i:02d}.mp4")
            _overlay(base, ovp, seg)
            parts.append(seg)

        # 3. the close
        seg = os.path.join(tmp, "99_close.mp4")
        _card_clip(close_card(spec.get("cta", "Follow for the rest.")), 3.4,
                   seg)
        parts.append(seg)

        lst = os.path.join(tmp, "list.txt")
        with open(lst, "w", encoding="utf-8") as f:
            for p in parts:
                f.write(f"file '{p}'\n")
        silent = os.path.join(tmp, "silent.mp4")
        _run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe",
              "0", "-i", lst, "-c", "copy", silent])

        _mix(silent, speech, spec.get("slug", "hero"), out_path)
        return out_path
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _has_audio(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
         "stream=codec_type", "-of", "csv=p=0", path],
        capture_output=True, text=True).stdout.strip()
    return "audio" in out


def _mix(video, speech, slug, out_path):
    """
    Speech in front, music behind it.

    The presenter's voice runs at full level for as long as the shot lasts.
    The music bed runs underneath the whole reel but ducks to a third of its
    already-low level while anyone is talking, so the sentence is never
    competing with a soundtrack.
    """
    total = audio.duration(video)
    track = audio.pick(slug)

    if not speech and not track:
        audio.attach(video, slug, out_path)
        return

    if speech and track:
        sdur = audio.duration(speech)
        fade = max(0.0, total - audio.FADE_OUT)
        fc = (
            f"[1:a]adelay=0|0,apad=whole_dur={total}[v];"
            f"[2:a]volume={audio.BED_VOLUME},"
            f"afade=t=in:st=0:d={audio.FADE_IN},"
            f"afade=t=out:st={fade:.2f}:d={audio.FADE_OUT},"
            # quiet under the voice, full once the b-roll starts
            f"volume=enable='lt(t,{sdur:.2f})':volume=0.33[m];"
            f"[v][m]amix=inputs=2:duration=first:dropout_transition=0,"
            f"volume=1.6[a]"
        )
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", video,
             "-i", speech, "-stream_loop", "-1", "-i", track,
             "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
             "-t", str(total), out_path],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return

    if speech:
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", speech,
             "-filter_complex", f"[1:a]apad=whole_dur={total}[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
             "-b:a", "160k", "-t", str(total), out_path],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return

    audio.attach(video, slug, out_path)
