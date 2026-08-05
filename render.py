"""
Mentorsy — Faceless Reel Factory :: render engine

Turns a script JSON into a finished, captioned, 1080x1920 MP4.

    python render.py scripts/2026-08-06_igcse-vs-ib.json

Pipeline:
  1. edge-tts speaks the script and reports exact WORD timings (free, no key)
  2. Gemini generates the scene images from the locked brand style (free tier)
  3. ffmpeg applies Ken Burns motion, burns karaoke captions, mixes music
"""

import asyncio
import json
import os
import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFilter

import config as C
from images import generate_images


# ─────────────────────────────────────────────────────────────
# helpers
# ─────────────────────────────────────────────────────────────

def hex_to_ass(hex_color: str, alpha: float = 1.0) -> str:
    """ASS subtitle colours are &HAABBGGRR — reversed RGB, with alpha inverted."""
    h = hex_color.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    a = f"{int((1 - alpha) * 255):02X}"
    return f"&H{a}{b}{g}{r}"


def ass_time(seconds: float) -> str:
    seconds = max(0.0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def run(cmd: list, desc: str = ""):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"\n[ffmpeg failed] {desc}\n{proc.stderr[-2500:]}")
        raise SystemExit(1)
    return proc


# ─────────────────────────────────────────────────────────────
# 1. voice-over with word-level timings
# ─────────────────────────────────────────────────────────────

async def _speak(text: str, out_mp3: str):
    import edge_tts

    comm = edge_tts.Communicate(
        text, C.VOICE, rate=C.VOICE_RATE, pitch=C.VOICE_PITCH
    )
    words = []
    with open(out_mp3, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words.append(
                    {
                        "start": chunk["offset"] / 1e7,
                        "dur": chunk["duration"] / 1e7,
                        "text": chunk["text"],
                    }
                )
    return words


def synthesize(text: str, out_mp3: str):
    """Returns [{start, dur, text}, ...] with real spoken timings."""
    return asyncio.run(_speak(text, out_mp3))


def audio_duration(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True,
    ).stdout.strip()
    return float(out)


# ─────────────────────────────────────────────────────────────
# 2. karaoke caption track (.ass)
# ─────────────────────────────────────────────────────────────

def build_captions(words, offset, out_path, total_dur):
    """
    Groups words into short lines and emits one ASS event per word, so the
    spoken word lights up in gold while its neighbours stay white.
    Muted viewers read these — they carry most of your retention.
    """
    n = C.CAPTION_WORDS_PER_LINE
    lines = [words[i:i + n] for i in range(0, len(words), n)]

    margin_v = int(C.HEIGHT * (1 - C.CAPTION_Y_FRACTION))

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {C.WIDTH}
PlayResY: {C.HEIGHT}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Serif,{C.CAPTION_FONT_SIZE},{hex_to_ass(C.CAPTION_BASE_CLR)},{hex_to_ass(C.CAPTION_ACTIVE_CLR)},{hex_to_ass(C.CAPTION_BOX_CLR)},{hex_to_ass('#000000', 0.55)},-1,0,0,0,100,100,1,0,3,26,0,2,90,90,{margin_v},1
Style: Hook,DejaVu Serif,{C.HOOK_FONT_SIZE},{hex_to_ass(C.WHITE)},{hex_to_ass(C.GOLD)},{hex_to_ass(C.PURPLE)},{hex_to_ass('#000000', 0.6)},-1,0,0,0,100,100,2,0,3,30,0,5,90,90,90,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    events = []
    for line in lines:
        for i, w in enumerate(line):
            start = w["start"] + offset
            # hold each word until the next one begins, so there are no gaps
            if i + 1 < len(line):
                end = line[i + 1]["start"] + offset
            else:
                end = w["start"] + w["dur"] + offset + 0.12
            end = min(end, total_dur)
            if end <= start:
                continue

            parts = []
            for j, ww in enumerate(line):
                txt = ww["text"].replace("{", "").replace("}", "")
                if j == i:
                    # colour only — scaling the active word would break the
                    # opaque caption box into uneven blocks
                    parts.append(
                        f"{{\\c{hex_to_ass(C.CAPTION_ACTIVE_CLR)}}}{txt}"
                        f"{{\\c{hex_to_ass(C.CAPTION_BASE_CLR)}}}"
                    )
                else:
                    parts.append(txt)
            text = " ".join(parts)
            events.append(
                f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Cap,,0,0,0,,{text}"
            )

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

    return out_path


def append_hook_card(ass_path, hook_text):
    """The first 1.5s: big centred hook text over the opening image."""
    wrapped = "\\N".join(textwrap.wrap(hook_text.upper(), width=18))
    ev = (
        f"Dialogue: 1,{ass_time(0)},{ass_time(C.HOOK_DURATION)},Hook,,0,0,0,"
        f",{{\\fad(150,200)}}{wrapped}"
    )
    with open(ass_path, "a", encoding="utf-8") as f:
        f.write(ev + "\n")


# ─────────────────────────────────────────────────────────────
# 3. visual segments with Ken Burns motion
# ─────────────────────────────────────────────────────────────

def prep_still(src, dst):
    """Cover-crop to 9:16 at 2x, so zoompan has real pixels to work with."""
    W, H = C.WIDTH * 2, C.HEIGHT * 2
    im = Image.open(src).convert("RGB")
    sr, tr = im.width / im.height, W / H
    if sr > tr:
        nh = H
        nw = int(nh * sr)
    else:
        nw = W
        nh = int(nw / sr)
    im = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - W) // 2, (nh - H) // 2
    im = im.crop((left, top, left + W, top + H))

    # subtle brand vignette — pushes the eye to the captions
    vign = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(vign)
    d.ellipse([-W * 0.35, -H * 0.22, W * 1.35, H * 1.22], fill=255)
    vign = vign.filter(ImageFilter.GaussianBlur(W // 9))
    dark = Image.new("RGB", (W, H), (18, 8, 28))
    im = Image.composite(im, dark, vign)

    im.save(dst, quality=95)
    return dst


def ken_burns_segment(img, dur, out_mp4, idx):
    frames = max(2, int(dur * C.FPS))
    z = C.KEN_BURNS_ZOOM
    # alternate zoom-in / zoom-out so consecutive scenes don't feel repetitive
    if idx % 2 == 0:
        zexpr = f"1+{z}*on/{frames}"
    else:
        zexpr = f"{1 + z}-{z}*on/{frames}"

    vf = (
        f"scale={C.WIDTH * 2}:{C.HEIGHT * 2},"
        f"zoompan=z='{zexpr}':d={frames}:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"s={C.WIDTH}x{C.HEIGHT}:fps={C.FPS},"
        f"format=yuv420p"
    )
    run(
        ["ffmpeg", "-y", "-loop", "1", "-i", img, "-vf", vf,
         "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "medium",
         "-crf", "18", "-pix_fmt", "yuv420p", out_mp4],
        f"ken burns segment {idx}",
    )
    return out_mp4


# ─────────────────────────────────────────────────────────────
# 4. main
# ─────────────────────────────────────────────────────────────

def render(script_path: str) -> str:
    with open(script_path, encoding="utf-8") as f:
        S = json.load(f)

    slug = S.get("slug") or os.path.splitext(os.path.basename(script_path))[0]
    work = os.path.join(C.WORK_DIR, slug)
    os.makedirs(work, exist_ok=True)

    scenes = S["scenes"]
    narration = " ".join(s["voiceover"].strip() for s in scenes)

    print(f"\n▸ {slug}")
    print("  1/5  generating images…")
    image_paths = generate_images(
        [s["image_prompt"] for s in scenes], work
    )

    print("  2/5  synthesizing voice…")
    mp3 = os.path.join(work, "vo.mp3")
    words = synthesize(narration, mp3)
    vo_dur = audio_duration(mp3)
    total = C.HOOK_DURATION + vo_dur + 0.6   # brief tail so the loop lands
    print(f"       {vo_dur:.1f}s narration · {len(words)} words · {total:.1f}s total")

    if total > 90:
        print("  !!   over 90s — Instagram will not treat this as a Reel. Trim the script.")

    # split total runtime across scenes, weighted by each scene's word count
    weights = [max(1, len(s["voiceover"].split())) for s in scenes]
    wsum = sum(weights)
    durations = [(w / wsum) * total for w in weights]

    print("  3/5  building motion segments…")
    segs = []
    for i, (img, dur) in enumerate(zip(image_paths, durations)):
        still = prep_still(img, os.path.join(work, f"still_{i}.jpg"))
        segs.append(ken_burns_segment(still, dur, os.path.join(work, f"seg_{i}.mp4"), i))

    concat_txt = os.path.join(work, "concat.txt")
    with open(concat_txt, "w") as f:
        for s in segs:
            f.write(f"file '{os.path.abspath(s)}'\n")
    silent = os.path.join(work, "silent.mp4")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
         "-c", "copy", silent], "concat")

    print("  4/5  burning captions…")
    ass = build_captions(words, C.HOOK_DURATION, os.path.join(work, "cap.ass"), total)
    append_hook_card(ass, S["hook_onscreen"])

    print("  5/5  mixing audio and encoding…")
    out = os.path.join(C.OUTPUT_DIR, f"{slug}.mp4")

    music = None
    if os.path.isdir(C.MUSIC_DIR):
        beds = [f for f in sorted(os.listdir(C.MUSIC_DIR))
                if f.lower().endswith((".mp3", ".m4a", ".wav"))]
        if beds:
            music = os.path.join(C.MUSIC_DIR, beds[hash(slug) % len(beds)])

    ass_esc = os.path.abspath(ass).replace("\\", "/").replace(":", "\\:")
    delay = int(C.HOOK_DURATION * 1000)

    logo = os.path.join(C.BASE_DIR, "brand", "logo.png")
    use_logo = os.path.exists(logo)

    inputs = ["-i", silent, "-i", mp3]
    if music:
        inputs += ["-stream_loop", "-1", "-i", music]
    if use_logo:
        inputs += ["-i", logo]
    logo_idx = 3 if music else 2

    # video chain: burn captions, then stamp the brand mark top-right
    vchain = f"[0:v]subtitles='{ass_esc}'[vsub];"
    if use_logo:
        vchain += (
            f"[{logo_idx}:v]scale={int(C.WIDTH * 0.30)}:-1,format=rgba,"
            f"colorchannelmixer=aa=0.92[lg];"
            f"[vsub][lg]overlay=W-w-56:56[v];"
        )
    else:
        vchain += "[vsub]null[v];"

    if music:
        filt = (
            vchain +
            f"[1:a]adelay={delay}|{delay},apad[vo];"
            f"[2:a]volume={C.MUSIC_VOLUME},afade=t=out:st={total - 1.2}:d=1.2[bed];"
            f"[vo][bed]amix=inputs=2:duration=first:dropout_transition=0[a]"
        )
    else:
        filt = vchain + f"[1:a]adelay={delay}|{delay},apad[a]"

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filt, "-map", "[v]", "-map", "[a]"]

    cmd += ["-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium",
            "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(C.FPS),
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags",
            "+faststart", out]
    run(cmd, "final encode")

    # write the caption/hashtag sidecar for the poster
    meta = {
        "slug": slug,
        "video": out,
        "caption": S["caption"],
        "hashtags": S["hashtags"],
        "alt_text": S.get("alt_text", ""),
        "duration": round(total, 2),
        "pillar": S.get("pillar", ""),
        "hook_formula": S.get("hook_formula", ""),
    }
    with open(os.path.join(C.OUTPUT_DIR, f"{slug}.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    size = os.path.getsize(out) / 1e6
    print(f"  ✓ {out}  ({size:.1f} MB, {total:.1f}s)")
    return out


if __name__ == "__main__":
    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    else:
        targets = [os.path.join(C.SCRIPTS_DIR, f)
                   for f in sorted(os.listdir(C.SCRIPTS_DIR)) if f.endswith(".json")]
        if not targets:
            print("No scripts found in scripts/. Drop a script JSON there first.")
            raise SystemExit(1)

    for t in targets:
        render(t)
