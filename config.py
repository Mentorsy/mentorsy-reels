"""
Mentorsy — Faceless Reel Factory
Configuration. This is the only file you normally need to edit.
"""
import os

# ─────────────────────────────────────────────────────────────
# 1. API KEYS  — paste yours here, or set them as env variables
# ─────────────────────────────────────────────────────────────

# Google AI Studio key (FREE — 500 images/day). Get it at:
# https://aistudio.google.com/apikey
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "PASTE_YOUR_GEMINI_KEY_HERE")

# Instagram Graph API (only needed for auto-posting — see SETUP_GUIDE.md)
IG_USER_ID      = os.environ.get("IG_USER_ID", "")
IG_ACCESS_TOKEN = os.environ.get("IG_ACCESS_TOKEN", "")

# Public host for finished MP4s. Instagram must be able to download the file
# over plain HTTPS. Cloudflare R2 free tier or a GitHub Releases URL both work.
PUBLIC_VIDEO_BASE_URL = os.environ.get("PUBLIC_VIDEO_BASE_URL", "")


# ─────────────────────────────────────────────────────────────
# 2. VOICE  — run `python voice_samples.py` to hear these
# ─────────────────────────────────────────────────────────────
# en-GB-SoniaNeural   warm British female — reads premium, international  (default)
# en-GB-LibbyNeural   younger British female — warmer, less formal
# en-IN-NeerjaNeural  Indian English female — authentic, closest to your own voice
# en-US-AriaNeural    American female — best if US parents become the priority
# en-AU-NatashaNeural Australian female — distinctive, cuts through a UK/US feed

VOICE       = "en-GB-SoniaNeural"
VOICE_RATE  = "+8%"    # slightly quicker than default — better retention
VOICE_PITCH = "+0Hz"


# ─────────────────────────────────────────────────────────────
# 3. BRAND LOCK  — do not change once you have started posting
# ─────────────────────────────────────────────────────────────
PURPLE   = "#3B1E54"
GOLD     = "#C9A96A"
LAVENDER = "#E8DCF5"
WHITE    = "#FFFFFF"

# Caption styling
CAPTION_FONT_SIZE   = 76
CAPTION_ACTIVE_CLR  = GOLD      # the word currently being spoken
CAPTION_BASE_CLR    = WHITE     # the rest of the visible line
CAPTION_BOX_CLR     = PURPLE
CAPTION_BOX_ALPHA   = 0.82
CAPTION_Y_FRACTION  = 0.62      # vertical position, 0 = top, 1 = bottom
CAPTION_WORDS_PER_LINE = 3      # 3 keeps text large and readable while muted

# Hook card (the first 1.5 seconds, before narration starts)
HOOK_FONT_SIZE = 92
HOOK_DURATION  = 1.5

# Video
WIDTH, HEIGHT = 1080, 1920
FPS           = 30
KEN_BURNS_ZOOM = 0.12   # how far each still image zooms across its segment


# ─────────────────────────────────────────────────────────────
# 4. IMAGE STYLE LOCK — appended to every image prompt
# ─────────────────────────────────────────────────────────────
STYLE_LOCK = (
    "Editorial documentary photography. Palette: deep purple #3B1E54 dominant, "
    "gold #C9A96A accents, lavender #E8DCF5 in the light areas. "
    "Soft warm single-source window light from the left. "
    "Shallow depth of field, matte finish, fine grain. Not glossy, not stock-photo. "
    "Vertical 9:16 composition. Subject sits in the lower two thirds; keep the "
    "TOP THIRD clean and uncluttered for a text overlay. "
    "Calm, premium, trustworthy mood. "
    "STRICTLY NO text, NO letters, NO numbers, NO logos, NO watermarks in the image. "
    # ── People rule ──────────────────────────────────────────────────
    # People appear as documentary b-roll, never as a presenter. Nobody
    # addresses the camera and no recurring individual is established, so
    # no viewer can mistake an image for the person narrating.
    "People may appear, photographed candidly and absorbed in what they are "
    "doing — studying, writing, reading, talking at a kitchen table. "
    "NEVER looking at the camera. NEVER posed or presenting. "
    "Faces are often partially turned, in profile, softly out of focus, or "
    "framed from behind or over the shoulder. "
    "Vary age, gender and appearance between images; do not establish one "
    "recurring individual. No teacher figure addressing the viewer."
)

# People rule in one line, injected into script generation as well.
PEOPLE_RULE = (
    "Documentary b-roll only. People may appear but are candid and absorbed "
    "in an activity, never looking at or addressing the camera, never posed. "
    "No recurring character, no presenter, no teacher figure."
)

# Gemini free-tier image model. 500 images/day at no cost.
IMAGE_MODEL = "gemini-2.5-flash-image"


# ─────────────────────────────────────────────────────────────
# 5. PATHS
# ─────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")   # input JSON scripts
WORK_DIR    = os.path.join(BASE_DIR, "work")      # temp audio/images
OUTPUT_DIR  = os.path.join(BASE_DIR, "output")    # finished MP4s + captions
MUSIC_DIR   = os.path.join(BASE_DIR, "music")     # optional background beds

# Background music level relative to the voice. Keep it low —
# on Instagram the voice must stay dominant.
MUSIC_VOLUME = 0.06

for _d in (SCRIPTS_DIR, WORK_DIR, OUTPUT_DIR, MUSIC_DIR):
    os.makedirs(_d, exist_ok=True)


# ─────────────────────────────────────────────────────────────
# 6. POSTING
# ─────────────────────────────────────────────────────────────
MAX_POSTS_PER_DAY = 5

# Times are local to the account's audience (Gulf Standard Time).
POST_SLOTS = ["07:30", "12:30", "15:00", "19:30", "21:30"]
