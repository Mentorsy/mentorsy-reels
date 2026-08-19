"""Turns a bank piece into the exact caption that goes out.

Caption anatomy (fixed, so the feed has a recognisable shape):
    hook            <- line 1, must earn the "more" tap
    body            <- the teaching / the point
    cta             <- one line, chosen by pillar strength + weekly pacing
    signature       <- brand line, rotated so it isn't wallpaper
    hashtags        <- rotated pool, never the same block twice
"""
from __future__ import annotations

import random

SIGNATURES = [
    "Mentorsy — live 1:1 mentors for Grades 1–12.",
    "Mentorsy — one child, one mentor, one plan.",
    "Mentorsy — CBSE, ICSE, IGCSE, IB and American curricula.",
    "Mentorsy — tutoring that matches your child's actual syllabus.",
]

HASHTAG_POOL = {
    "core": ["#Mentorsy", "#OnlineTutoring", "#1on1Learning"],
    "board": ["#CBSE", "#ICSE", "#IGCSE", "#IBDP", "#IBMYP", "#BoardExams2027"],
    "subject": {
        "Mathematics": ["#MathsTutor", "#MathHelp", "#Algebra", "#Geometry"],
        "Science": ["#ScienceTutor", "#Physics", "#Chemistry", "#Biology"],
        "English": ["#EnglishTutor", "#Grammar", "#ReadingSkills"],
        "French": ["#LearnFrench", "#FrenchForKids", "#DELF"],
        "Coding": ["#CodingForKids", "#Python", "#Scratch"],
        "Public Speaking": ["#PublicSpeaking", "#ConfidentKids", "#DebateSkills"],
        "General": ["#ParentingTips", "#StudyTips", "#HomeworkHelp"],
    },
    "audience": ["#IndianParents", "#ParentsOfTeens", "#SchoolLife", "#StudySmart"],
}


def hashtags_for(piece: dict, seed: int) -> str:
    rng = random.Random(seed)
    subj = piece.get("subject", "General")
    pool = HASHTAG_POOL["subject"].get(subj, HASHTAG_POOL["subject"]["General"])
    tags = (
        rng.sample(HASHTAG_POOL["core"], 2)
        + rng.sample(HASHTAG_POOL["board"], 2)
        + rng.sample(pool, min(3, len(pool)))
        + rng.sample(HASHTAG_POOL["audience"], 2)
    )
    return " ".join(tags)


def build_cta(piece: dict, strength: str, cfg: dict, seed: int) -> str:
    rng = random.Random(seed)
    line = rng.choice(cfg["cta_ladder"][strength]["lines"])
    kw = piece.get("keyword")
    if kw:
        line = line.replace("{KEYWORD}", kw).replace(
            "{MAGNET}", cfg["lead_magnets"].get(kw, "guide")
        )
    return line


def render_caption(piece: dict, strength: str, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 7)
    parts = [
        piece["hook"],
        "",
        piece.get("body", "").strip(),
        "",
        build_cta(piece, strength, cfg, seed),
        "",
        rng.choice(SIGNATURES),
        "",
        hashtags_for(piece, seed),
    ]
    return "\n".join(p for p in parts if p is not None).strip()
