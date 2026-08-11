"""
Mentorsy - audio bed

The Instagram Content Publishing API cannot attach a track from Instagram's
music library. Anything published through the API carries only the audio
already inside the file, so a reel that is going out automatically needs its
music baked in at render time.

Two rules about that music:

1. It has to be licensed for commercial use. Canva Pro includes a library that
   is, and exporting four or five tracks from it costs nothing on top of a
   subscription already being paid for. Drop the mp3s in _engine/music/ and
   the renderer picks one per reel, keyed by slug so a given reel always gets
   the same track.

2. It has to sit a long way down. These reels argue in typography; music that
   competes with the reading is worse than silence. The bed runs at about
   fourteen percent, fades in over a second and out over two.

With no tracks present the renderer still attaches a silent stereo track.
Reels with no audio stream at all are unreliable through the publishing API,
and a silent stream costs nothing.
"""

import hashlib
import os
import subprocess

MUSIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "music")

# Loud enough to be heard on a phone speaker, quiet enough to stay behind the
# reading. Measured rather than guessed: at 0.14 a finished reel came out at
# -35 dB mean, which is effectively silence once a phone is in a room with
# other people in it. 0.5 lands around -22 dB, which sits under the type
# without disappearing. Under a presenter's voice the mix drops this by a
# further two thirds - see hero._mix.
BED_VOLUME = 0.5
FADE_IN = 1.0
FADE_OUT = 2.0


def tracks():
    if not os.path.isdir(MUSIC_DIR):
        return []
    return sorted(
        os.path.join(MUSIC_DIR, f) for f in os.listdir(MUSIC_DIR)
        if f.lower().endswith((".mp3", ".m4a", ".wav", ".aac", ".ogg"))
    )


def pick(slug):
    """Same reel, same track, every rebuild."""
    pool = tracks()
    if not pool:
        return None
    n = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)
    return pool[n % len(pool)]


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0


def attach(video_path, slug, out_path):
    """Mux the bed under a silent video. Returns out_path."""
    dur = duration(video_path)
    track = pick(slug)

    if track:
        fade_start = max(0.0, dur - FADE_OUT)
        af = (f"volume={BED_VOLUME},"
              f"afade=t=in:st=0:d={FADE_IN},"
              f"afade=t=out:st={fade_start:.2f}:d={FADE_OUT}")
        args = ["ffmpeg", "-y", "-loglevel", "error",
                "-i", video_path,
                "-stream_loop", "-1", "-i", track,
                "-filter_complex", f"[1:a]{af}[a]",
                "-map", "0:v", "-map", "[a]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                "-shortest", out_path]
    else:
        args = ["ffmpeg", "-y", "-loglevel", "error",
                "-i", video_path,
                "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "96k",
                "-shortest", out_path]

    subprocess.run(args, check=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.PIPE)
    return out_path
