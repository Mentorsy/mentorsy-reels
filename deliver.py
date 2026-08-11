"""
Mentorsy - delivery

Turns a content spec into folders a human can upload from without opening a
single file to work out what it is:

    Mentorsy Instagram/
      8 August/
        11-40am_1post/
          caption.txt
          post.png
        12-00pm_2reel/
          caption.txt
          reel.mp4
        1-00pm_3carousel/
          caption.txt
          01.png 02.png 03.png ...

Times are IST. Windows will not accept a colon in a folder name, so 11:40am is
written 11-40am - the only place this deviates from the requested naming.

Carousel slides are numbered 01, 02, 03 so the upload picker keeps them in
order; Instagram takes them in the sequence they are selected, and a plain
alphabetical sort is the one thing every file picker agrees on.
"""

import os
import re

import cards
import reels

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def day_folder(date):
    """date -> '8 August'. No leading zero, matching how people say it."""
    return f"{date.day} {MONTHS[date.month - 1]}"


def slot_folder(time_str, index, kind):
    """('11:40am', 1, 'post') -> '11-40am_1post'"""
    safe = time_str.replace(":", "-").replace(" ", "").lower()
    return f"{safe}_{index}{kind}"


def _caption_text(spec):
    """Caption plus the handful of notes that make uploading fast."""
    parts = [spec["caption"].strip()]

    tags = spec.get("hashtags", [])
    if tags:
        parts.append(" ".join(tags))

    notes = []
    if spec.get("kind") == "reel":
        notes.append("Add a trending audio track in the Instagram app before "
                     "posting. Reels using Instagram's own audio library reach "
                     "further than reels with music baked in, and this one is "
                     "built to read with the sound off.")
    if spec.get("kind") == "carousel":
        notes.append("Select the slides in numbered order - Instagram keeps "
                     "the order you tap them in, not the filename order.")
    if spec.get("first_comment"):
        notes.append("First comment: " + spec["first_comment"])

    if notes:
        parts.append("-" * 46)
        parts.extend(notes)

    return "\n\n".join(parts) + "\n"


def write_piece(root, date, time_str, index, spec):
    """Render one piece into its slot folder. Returns the folder path."""
    kind = spec.get("kind", "list")
    folder_kind = {"reel": "reel", "carousel": "carousel"}.get(kind, "post")
    out = os.path.join(root, day_folder(date),
                       slot_folder(time_str, index, folder_kind))
    os.makedirs(out, exist_ok=True)

    with open(os.path.join(out, "caption.txt"), "w", encoding="utf-8") as f:
        f.write(_caption_text(spec))

    if kind == "reel":
        made = reels.render(spec, os.path.join(out, "reel.mp4"))
        if not made:
            # ffmpeg missing: still ship the frames so the day is not empty.
            for i, (img, _) in enumerate(reels.frames(spec), 1):
                img.save(os.path.join(out, f"frame_{i:02d}.png"))
    else:
        pages = cards.render(spec)
        if len(pages) == 1:
            pages[0].save(os.path.join(out, "post.png"), quality=95)
        else:
            for i, page in enumerate(pages, 1):
                page.save(os.path.join(out, f"{i:02d}.png"), quality=95)

    return out


def write_day(root, date, pieces):
    """pieces: [(time_str, spec), ...] in posting order."""
    made = []
    for i, (time_str, spec) in enumerate(pieces, 1):
        made.append(write_piece(root, date, time_str, i, spec))
    return made
