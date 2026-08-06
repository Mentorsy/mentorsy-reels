"""
Mentorsy — bulk script generator

Reads calendar_60.csv and expands each row into a full script JSON:
voiceover scenes, image prompts, on-screen hook, caption, hashtags, alt text.

Uses the Gemini API free tier — no cost. Resumable: already-written scripts
are skipped, so you can stop and restart at any point.

    python scriptgen.py                 # generate all 120
    python scriptgen.py --limit 10      # try 10 first
    python scriptgen.py --force         # regenerate everything
"""

import argparse
import csv
import json
import os
import re
import time

import requests

import config as C

TEXT_MODEL = "gemini-2.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{TEXT_MODEL}:generateContent"

BRIEF = """You write Instagram Reel scripts for Mentorsy — an edtech
company founded by Himanshi Dang. It is a product and learning business, not
a consultancy: never describe it as consulting or advisory work.

WHO IS SPEAKING: Mentorsy itself — the institution, not a person. Scripts are
written in the brand's voice, the way a school or a publisher speaks. Mentorsy
runs a team of trained mentors and a network of 300+ educators, several of whom
have held Head of Department and senior leadership posts inside schools. That
collective classroom experience is the authority, and it should show.

CRITICAL — NEVER FIRST PERSON SINGULAR. Never write "I", "I've", "my", "me",
or "in my experience". Never name or imply a single individual mentor, founder
or teacher. Where insider authority is needed, attribute it to the team:
"Our mentors see this every term." "Teachers who have marked these papers know."
Plural "we" and "our mentors" are correct. Singular "I" is always wrong.

WHO IS WATCHING: parents of 11-18 year olds in Dubai, the UK and the US who
are paying for, or considering, academic mentorship for their child.

VOICE: warm, authoritative, minimal. Never corporate. Never salesy. Never
self-congratulatory. Short sentences. States things plainly and does not hedge.
Generous with genuinely useful specifics.

THE FORMAT — a narrated Reel. Nobody presents to camera. The voice-over carries
everything, over documentary-style stills with slow motion. People may appear
in the imagery, but always candidly, absorbed in something, never addressing
the viewer — so the narration is clearly Mentorsy's voice, not an actor's.

HARD RULES:
- Total narration must be 70-90 words. This is a hard ceiling. Count them.
- Never open with a greeting. Never introduce a speaker. Never "Let's talk about".
- One idea only. Not two.
- Scene 1 must be the hook and must work as a cold open.
- The FINAL sentence must set up the FIRST sentence, so the Reel loops
  seamlessly when it replays. This is the most important rule here.
- Say the searchable keywords out loud in the narration where they fit
  naturally: IGCSE, A Level Mathematics, Cambridge curriculum, Dubai schools,
  GCSE. Instagram indexes spoken words.
- Write for a SEND, not a like. The payoff line should be something one
  mother forwards to another mother.
- No emojis anywhere. No exclamation marks.
- British spelling throughout ("maths", not "math").

IMAGE PROMPTS — one per scene. These go to an image model. Rules:
- People ARE allowed, but only as documentary b-roll: candid, absorbed in an
  activity, NEVER looking at or addressing the camera, never posed, never
  presenting. A student bent over a page. A parent and teenager mid-conversation
  at a kitchen table. Someone seen from behind at a desk by a window.
- Do NOT establish a recurring individual — vary who appears across scenes.
- NEVER write a teacher or presenter explaining something to camera.
- Objects and environments work equally well: exercise books, doorways,
  corridors, stacked textbooks, an empty chair.
- Describe ONE clear subject and the framing. Nothing busy.
- Never describe text, letters, numbers, logos or signage.
- Do not mention colours or lighting style — a brand style block is appended
  automatically. Describe only subject and composition.

Return ONLY valid JSON. No markdown fences, no commentary."""

SCHEMA = """{
  "hook_onscreen": "3-5 words, appears full-screen for the first 1.5 seconds. Punchy. Not a sentence.",
  "scenes": [
    {"voiceover": "one or two sentences", "image_prompt": "one clear subject and composition"}
  ],
  "caption": "Instagram caption. Line 1 is a standalone hook worded DIFFERENTLY from the narration hook. Then a blank line. Then 2-4 short lines with keywords front-loaded naturally. Then one CTA line.",
  "hashtags": ["exactly 4"],
  "alt_text": "one keyword-rich sentence describing the visuals"
}"""

HOOK_GUIDE = {
    "1 Contradiction": "Open by contradicting what the parent already believes. '[Common solution] is making it worse.'",
    "2 Cost of Inaction": "Open with the window they are about to miss and what it costs.",
    "3 Insider": "Open from the school leadership side, attributed to the team. 'Our mentors have sat on the other side of that table.'",
    "4 Named Enemy": "Open by renaming the problem precisely. 'It's not X. It's this specific Y.'",
    "5 Specific Number": "Open with a concrete number drawn from what Mentorsy's mentors see across their students.",
    "6 Direct Address": "Open by naming exactly who this is for. 'If your child is in Year 9 in Dubai...'",
    "7 Permission": "Open by giving permission for something parents feel guilty about.",
    "8 Unanswerable Question": "Open with a question the parent cannot answer, then answer it.",
    "9 Prediction": "Open with a forward-looking claim about schools or admissions.",
}


def call_gemini(prompt, retries=4):
    key = C.GEMINI_API_KEY
    if not key or key.startswith("PASTE_"):
        raise SystemExit(
            "No Gemini API key. Get one free at https://aistudio.google.com/apikey "
            "and put it in config.py (or set GEMINI_API_KEY)."
        )
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.95, "responseMimeType": "application/json"},
    }
    for a in range(retries):
        try:
            r = requests.post(URL, headers={"x-goog-api-key": key,
                                            "Content-Type": "application/json"},
                              json=body, timeout=120)
            if r.status_code == 429:
                wait = 15 * (a + 1)
                print(f"    rate limited — waiting {wait}s")
                time.sleep(wait)
                continue
            r.raise_for_status()
            txt = r.json()["candidates"][0]["content"]["parts"][0]["text"]
            txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
            return json.loads(txt)
        except Exception as e:
            print(f"    attempt {a + 1} failed: {e}")
            time.sleep(5)
    return None


def word_count(scenes):
    return sum(len(s["voiceover"].split()) for s in scenes)


QUOTED = re.compile("[\"'\u201c\u201d\u2018\u2019][^\"'\u201c\u201d\u2018\u2019]{0,120}"
                    "[\"'\u201c\u201d\u2018\u2019]")

FIRST_PERSON = re.compile(
    r"\b(I|I'm|I've|I'll|I'd|me|my|mine|myself)\b", re.I)


def first_person_hits(data):
    """Catch singular first person before it reaches 120 finished scripts."""
    text = " ".join(s.get("voiceover", "") for s in data.get("scenes", []))
    text += " " + data.get("caption", "")
    text = re.sub(QUOTED, " ", text)
    return sorted(set(m.group(0) for m in FIRST_PERSON.finditer(text)))


def generate(row):
    hook_note = HOOK_GUIDE.get(row["hook_formula"], "")
    prompt = f"""{BRIEF}

TOPIC: {row['topic']}
PILLAR: {row['pillar']}
HOOK FORMULA TO USE: {row['hook_formula']} — {hook_note}

Write 5 scenes. Return exactly this JSON shape:
{SCHEMA}"""

    for attempt in range(3):
        data = call_gemini(prompt)
        if not data:
            return None
        scenes = data.get("scenes", [])
        wc = word_count(scenes)
        if not scenes or not data.get("caption"):
            continue
        if wc > 105:
            prompt += f"\n\nYour last attempt was {wc} words. That is too long. Cut it to 70-90 words."
            continue

        hits = first_person_hits(data)
        if hits:
            print(f"    first person {hits} — rewriting in brand voice")
            prompt += (f"\n\nYour last attempt used first person singular: "
                       f"{', '.join(hits)}. Mentorsy is a company, not a person. "
                       f"Rewrite using 'our mentors', 'we', or no subject at all.")
            continue

        tags = data.get("hashtags", [])[:4]
        if "#Mentorsy" not in tags:
            tags = (tags + ["#Mentorsy"])[-4:]
        data["hashtags"] = tags
        data["word_count"] = wc
        return data
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calendar", default=os.path.join(C.BASE_DIR, "calendar_60.csv"))
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    rows = list(csv.DictReader(open(a.calendar, encoding="utf-8")))
    if a.limit:
        rows = rows[:a.limit]

    made = skipped = failed = 0
    for i, row in enumerate(rows, 1):
        out = os.path.join(C.SCRIPTS_DIR, f"{row['slug']}.json")
        if os.path.exists(out) and not a.force:
            skipped += 1
            continue

        print(f"[{i}/{len(rows)}] {row['date']} · {row['pillar']} · {row['topic'][:52]}")
        data = generate(row)
        if not data:
            print("    FAILED — will retry on next run")
            failed += 1
            continue

        data.update({
            "slug": row["slug"],
            "date": row["date"],
            "slot": row["slot"],
            "pillar": row["pillar"],
            "topic": row["topic"],
            "hook_formula": row["hook_formula"],
        })
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"    ✓ {data['word_count']} words · \"{data['hook_onscreen']}\"")
        made += 1
        time.sleep(6.5)   # free tier allows ~10 req/min; stay under it   # stay comfortably inside the free-tier rate limit

    print(f"\n✓ written {made} · skipped {skipped} · failed {failed}")
    if failed:
        print("  Re-run the same command to pick up the failures.")


if __name__ == "__main__":
    main()
