# Mentorsy Reel Factory — Setup Guide

Faceless Instagram Reels, written, voiced, illustrated, edited and posted automatically. Two months of content in one batch.

---

## What is actually automated, and what isn't

I want you to know this before you start, so nothing surprises you.

| Stage | Automated? |
|---|---|
| Choosing 120 topics across 60 days | ✅ Done — `calendar_60.csv` is written |
| Writing 120 scripts | ✅ Fully automatic |
| Voice-over | ✅ Fully automatic, no face, no recording |
| Images | ✅ Fully automatic, brand-locked |
| Video editing, captions, music | ✅ Fully automatic |
| Captions and hashtags | ✅ Fully automatic |
| Posting to Instagram + Facebook | ✅ Automatic **after** a one-time setup (Step 3) |

**The one-time setup is real work — about 90 minutes**, mostly waiting on Meta's developer console. After that you don't touch it.

If you'd rather skip Step 3 entirely, there's a no-code fallback at the bottom that costs you 10 minutes a week instead.

---

## Step 0 — Install (10 minutes)

You need **Python** and **FFmpeg** on your machine.

1. Python: [python.org/downloads](https://www.python.org/downloads/) — tick **"Add Python to PATH"** during install.
2. FFmpeg: easiest route is to open PowerShell and run `winget install Gyan.FFmpeg`
3. Then, in the `sjk_reels` folder, open a terminal and run:

```
pip install -r requirements.txt
```

Check it worked:

```
python run_all.py --status
```

You should see the 60-day calendar with three empty progress bars.

---

## Step 1 — Gemini API key (5 minutes, free)

This writes your scripts and generates your images. The free tier gives you **500 images a day**, which is roughly ten times what this system needs.

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with the same Google account as your Gemini Pro subscription
3. Click **Create API key**, copy it
4. Open `config.py` and paste it:

```python
GEMINI_API_KEY = "AIza...your key here..."
```

> This is a *separate* key from your Gemini Pro app subscription. The API free tier is its own allowance — using it doesn't eat into your Pro limits.

---

## Step 2 — Pick your voice (5 minutes)

```
python voice_samples.py
```

This writes five MP3s to `voice_samples/`. Listen to all five, then set the winner in `config.py`:

```python
VOICE = "en-GB-SoniaNeural"
```

My suggestion: **en-GB-SoniaNeural** reads as premium and international, which suits parents comparing Dubai and UK schools. But **en-IN-NeerjaNeural** is closer to your own voice, and if you ever move to showing your face, the transition won't jar. Worth listening before deciding — this voice becomes your brand.

---

## Step 3 — Auto-posting (60–90 minutes, one time, free)

Skip to the fallback at the bottom if you'd rather not do this now. Everything else works without it.

### 3a. Account setup

1. Your Instagram account must be a **Professional (Business or Creator)** account. Settings → Account type → Switch.
2. It must be **linked to a Facebook Page**. Create one if you don't have it — it can be minimal.

### 3b. Meta developer app

1. Go to [developers.facebook.com/apps](https://developers.facebook.com/apps) → **Create App** → type **Business**
2. Add the **Instagram** product
3. Under **App roles**, add yourself as Admin
4. In the Graph API Explorer, generate a token with these permissions:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`
   - `pages_read_engagement`

> **Because you're only publishing to your own account**, you can operate the app in Development mode and skip the full App Review queue. If Meta prompts you for review, that's for apps publishing on *behalf of other people* — not your case.

### 3c. Long-lived token

Short tokens expire in an hour. Exchange yours for a 60-day one:

```
https://graph.facebook.com/v21.0/oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id=YOUR_APP_ID
  &client_secret=YOUR_APP_SECRET
  &fb_exchange_token=YOUR_SHORT_TOKEN
```

Then get your Instagram user ID:

```
https://graph.facebook.com/v21.0/me/accounts?access_token=YOUR_LONG_TOKEN
```

Take the Page ID from that, then:

```
https://graph.facebook.com/v21.0/PAGE_ID?fields=instagram_business_account&access_token=YOUR_LONG_TOKEN
```

Put both into `config.py`:

```python
IG_USER_ID      = "1784...."
IG_ACCESS_TOKEN = "EAAG...."
```

> **Diary note:** the token expires after 60 days. Set a reminder to regenerate it — exactly when this two-month batch runs out, which is convenient.

### 3d. Public video hosting

Instagram downloads your MP4 from a public URL — it can't read your hard drive. **Cloudflare R2** has a free tier that covers this comfortably.

1. Sign up at [dash.cloudflare.com](https://dash.cloudflare.com) → R2 → Create bucket → name it `sjk-reels`
2. Settings → **Public access** → enable, and copy the public URL
3. Add to `config.py`:

```python
PUBLIC_VIDEO_BASE_URL = "https://pub-xxxx.r2.dev"
```

4. Upload your finished MP4s from `output/` to the bucket. Cloudflare's dashboard takes drag-and-drop, or install `rclone` to sync the folder in one command.

### 3e. Facebook cross-posting (optional)

Set two environment variables and the poster mirrors every Reel to your Page:

```
setx FB_PAGE_ID "your_page_id"
setx FB_PAGE_TOKEN "your_page_token"
```

---

## Step 4 — Build the two months

```
python run_all.py --build
```

This writes 120 scripts, then renders 120 videos. **Expect 3–5 hours.** Start it and leave it running — go and do something else.

It's resumable. If it stops, or you close the laptop, run the same command again and it picks up exactly where it left off.

**Test on a small batch first:**

```
python run_all.py --build --limit-render 4
```

Watch those four. Check the voice, the pacing, the images. Adjust `config.py` if you want to change anything, delete the four MP4s from `output/`, and re-run. Much better than discovering a problem after 120 renders.

---

## Step 5 — Schedule it

### Windows Task Scheduler (fully automatic)

1. Open **Task Scheduler** → **Create Task**
2. **General:** name it `Mentorsy Reel Factory`, tick *Run whether user is logged on or not*
3. **Triggers:** New → Daily → 07:00 → repeat every 1 hour for 24 hours (so it catches every posting slot)
4. **Actions:** New → Start a program
   - Program: `python`
   - Arguments: `run_all.py --daily`
   - Start in: the full path to your `sjk_reels` folder
5. Save

Each run renders anything missing in the next five days and publishes whatever is due. You do nothing.

**Test it first** with no risk:

```
python post.py --due --dry-run
```

---

## Fallback — no API setup at all

If Step 3 feels like more than you want to take on right now, everything up to the finished MP4 still works automatically. You just upload them yourself:

**Meta Business Suite** — free, schedules up to **75 days ahead**, which covers your full 60-day batch in one sitting. Planner → Create Reel → upload from `output/`, paste the caption from the matching `.json`, set the date and time from `calendar_60.csv`. Roughly 10 minutes per week of content.

**Canva Pro Content Planner** — you already pay for this, and it posts to both Instagram and Facebook. Same idea: upload, schedule, done. Slightly nicer interface, slightly shorter scheduling horizon.

Either way you keep the automation that matters — the writing, voicing, illustrating and editing. You're only doing the upload.

---

## Daily and weekly rhythm

| When | What | Time |
|---|---|---|
| Daily 06:30 | Trend brief lands in Cowork (already scheduled) | 5 min to read |
| Daily | Reels post themselves | 0 min |
| Daily | **Reply to every comment within an hour** | 15 min |
| Friday | `python run_all.py --status`, log metrics in the tracker | 10 min |
| Every 60 days | Regenerate the Meta token, run `--build` again | 30 min |

That comment replying is not optional busywork. Sends and DM conversations outrank likes in 2026 — your replies are part of the distribution, not an afterthought.

---

## Everyday commands

```
python run_all.py --status              where everything stands
python run_all.py --build               build the full two months
python run_all.py --daily               render upcoming + post what's due
python render.py scripts/NAME.json      re-render one reel
python post.py --due --dry-run          see what would post, change nothing
python post.py --slug NAME              post one reel immediately
python scriptgen.py --force             rewrite all scripts from scratch
python calendar_60.py --start 2026-10-05  plan the next two months
```

---

## When something breaks

**"No Gemini API key"** — Step 1 not done, or the key still says `PASTE_...`

**Images come out as purple gradient cards** — the API key is wrong or the daily quota is spent. The gradients are the deliberate fallback so a bad key never halts a render. Fix the key, delete the `work/<slug>/` folder, re-render.

**"Cannot connect to speech.platform.bing.com"** — edge-tts needs internet. Check the connection, or a VPN/firewall blocking it.

**Instagram: "media_url is not accessible"** — the MP4 isn't public yet. Paste the URL into a private browser window; if it doesn't download, the bucket isn't public.

**Reel posts as a normal video, not a Reel** — it's over 90 seconds. Scripts are capped at 90 words to prevent this, but check `duration` in the output `.json`.

**"Application request limit reached"** — you've hit Instagram's publishing cap. `MAX_POSTS_PER_DAY` in `config.py` keeps you at 5, well under it. Wait an hour.

---

## Cost

| | |
|---|---|
| Gemini API (scripts + images) | free tier — 500 images/day |
| edge-tts (voice) | free, no key |
| FFmpeg (editing) | free |
| Cloudflare R2 (hosting) | free tier |
| Meta Graph API (posting) | free |
| **Total** | **₹0/month** |

Your existing Gemini Pro and Canva Pro subscriptions aren't needed for this pipeline at all — keep them for the hero content and carousels.
