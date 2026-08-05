# START HERE

Faceless Instagram Reels for Mentorsy, from topic to published post.
60 days planned. 120 Reels. Zero cost. No face on camera.

## Pick your path

**You want it running 24/7 while your laptop is off** → read **`ALWAYS_ON_SETUP.md`**.
Everything runs on GitHub's servers. About an hour of setup, then nothing.

**You want to run it on your own machine** → read **`SETUP_GUIDE.md`**.

## Local route, in order

1. **`SETUP_GUIDE.md`** — read this first. 90 minutes of one-time setup.
2. `pip install -r requirements.txt`
3. Paste your free Gemini key into `config.py`
4. `python voice_samples.py` — pick your voice
5. `python run_all.py --build --limit-render 4` — make four, watch them
6. `python run_all.py --build` — make the other 116 (leave it running)
7. Schedule `python run_all.py --daily` in Windows Task Scheduler

## What's in here

| File | What it does |
|---|---|
| `config.py` | **The only file you normally edit.** Keys, voice, brand colours. |
| `calendar_60.csv` | Your 120 topics, dated and slotted. Already built. |
| `calendar_60.py` | Rebuilds the calendar for the next two months |
| `scriptgen.py` | Turns calendar rows into full scripts |
| `render.py` | Script → finished captioned MP4 |
| `images.py` | Brand-locked image generation |
| `post.py` | Publishes to Instagram and Facebook |
| `run_all.py` | Runs the whole thing |
| `voice_samples.py` | Five voices to choose from |
| `carousel.py` | 7-slide carousels, fully offline, no API keys |
| `ci_build.py` | What GitHub Actions calls to render |
| `.github/workflows/` | The always-on build and post schedules |
| `scripts/` | Generated scripts |
| `output/` | Finished MP4s + caption files |
| `music/` | Drop MP3s here for background beds (optional) |

## The one number that matters

Watch time. Every Reel is built to loop — the last line sets up the first, so
it replays seamlessly. A rewatch is the strongest signal you can send
Instagram, and it's free.
