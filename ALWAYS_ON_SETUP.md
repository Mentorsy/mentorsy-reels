# Always-On Setup — runs while your laptop is off

Everything moves to GitHub's servers. Your computer is only needed once, for the initial upload. After that the system writes, renders and posts on its own, day and night.

**Setup time: about an hour. Ongoing effort: none.**

---

## Why GitHub Actions

You need a machine that is always awake. Renting one costs money. GitHub gives you one free:

| | |
|---|---|
| Cost | Free — 2,000 Linux minutes/month on private repos, **unlimited on public repos** |
| Always on | Yes. Runs on GitHub's infrastructure, not yours. |
| Scheduling | Built-in cron |
| Secrets | Encrypted, never visible in the code |
| Your laptop | Can be shut, asleep, or in another country |

The whole 60-day batch uses roughly 200–250 minutes. Comfortably inside the free tier even on a private repo.

---

## Step 1 — Put the code on GitHub (15 min)

1. Create a free account at [github.com](https://github.com) if you don't have one
2. **New repository** → name it `mentorsy-reels`
3. Choose **Public**

> **Public or private?** Public gives you unlimited free Actions minutes *and* — importantly — makes your finished MP4s reachable at a plain URL, which is exactly what Instagram needs to fetch them. Your API keys never go in the repo; they live in encrypted Secrets. The only thing visible is your content calendar and scripts.
>
> If you'd rather keep it private, that works too — you'll just need Cloudflare R2 for video hosting (Step 4b) and you're capped at 2,000 minutes/month.

4. Upload the whole `sjk_reels` folder. Either drag it into GitHub's web uploader, or:

```
cd sjk_reels
git init
git add .
git commit -m "Mentorsy reel factory"
git branch -M main
git remote add origin https://github.com/Mentorsy/mentorsy-reels.git
git push -u origin main
```

---

## Step 2 — Add your secrets (10 min)

In your repo: **Settings → Secrets and variables → Actions → New repository secret**

Add these one at a time:

| Secret name | Where it comes from |
|---|---|
| `GEMINI_API_KEY` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) — free |
| `IG_USER_ID` | Meta setup, below |
| `IG_ACCESS_TOKEN` | Meta setup, below |
| `PUBLIC_VIDEO_BASE_URL` | Step 4 |
| `FB_PAGE_ID` | optional, for Facebook cross-posting |
| `FB_PAGE_TOKEN` | optional |

Secrets are encrypted. Nobody can read them back out — not even you, once saved.

---

## Step 3 — Meta credentials (30 min, one time)

Your Instagram is already a Professional account (`mentorsy.in`), so the hard part is done.

1. **Link it to a Facebook Page** if it isn't already — Instagram Settings → Account → Sharing to other apps
2. Go to [developers.facebook.com/apps](https://developers.facebook.com/apps) → **Create App** → **Business**
3. Add the **Instagram** product
4. Open **Graph API Explorer**, select your app, and request these permissions:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`
   - `pages_read_engagement`
5. Generate a token, then exchange it for a long-lived one:

```
https://graph.facebook.com/v21.0/oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id=YOUR_APP_ID
  &client_secret=YOUR_APP_SECRET
  &fb_exchange_token=YOUR_SHORT_TOKEN
```

6. Find your Instagram user ID:

```
https://graph.facebook.com/v21.0/me/accounts?access_token=YOUR_LONG_TOKEN
→ gives you PAGE_ID

https://graph.facebook.com/v21.0/PAGE_ID?fields=instagram_business_account&access_token=YOUR_LONG_TOKEN
→ gives you IG_USER_ID
```

Put both in Secrets.

> Because you're publishing only to your own account, Development mode is enough — you don't need Meta's App Review queue. Review is for apps that publish on behalf of *other people*.
>
> **The token expires every 60 days.** Put a recurring reminder in your diary. It's the one piece of genuine maintenance in this system, and it lines up neatly with each two-month content batch.

---

## Step 4 — Video hosting

Instagram downloads your MP4 from a public URL. It cannot read GitHub's private files or your hard drive.

### 4a. Public repo — nothing to do

Set `PUBLIC_VIDEO_BASE_URL` to:

```
https://raw.githubusercontent.com/Mentorsy/mentorsy-reels/main/output
```

The build workflow commits finished MP4s to the repo, and that URL serves them directly. Free, no extra account, nothing to maintain.

### 4b. Private repo — Cloudflare R2

1. [dash.cloudflare.com](https://dash.cloudflare.com) → R2 → Create bucket → `mentorsy-reels`
2. Settings → enable **Public access**, copy the public URL
3. Set `PUBLIC_VIDEO_BASE_URL` to that URL
4. Add an upload step to `build.yml` using `rclone` or the R2 API

Free tier covers this volume comfortably.

---

## Step 5 — Turn it on

In your repo, open the **Actions** tab. You'll see two workflows.

**Test the poster first, safely:**

Actions → *Post to Instagram and Facebook* → **Run workflow** → leave `dry_run` as **true** → Run.

Read the log. It will tell you what it *would* have posted without touching your account.

**Then build the content:**

Actions → *Build reels* → **Run workflow** → set `force_all` to **true** → Run.

This writes 120 scripts and renders 120 videos. Expect 2–4 hours. Close your laptop — it's running on GitHub's machines now.

**Then go live:**

Once you're happy with the rendered videos, run the post workflow again with `dry_run` set to **false**. From then on the schedules take over.

---

## What happens from here

| When | What | Where |
|---|---|---|
| 02:00 UTC daily | Renders anything due in the next 10 days | GitHub servers |
| Every hour, :30 | Checks the calendar, posts anything due | GitHub servers |
| Every 60 days | You regenerate the Meta token and run `calendar_60.py` again | 30 min of your time |

Your laptop is not involved in any of it.

---

## Timezone

**GitHub cron runs in UTC only.** Gulf Standard Time is UTC+4, so the workflows set `TZ_OFFSET_HOURS: "4"` and the poster shifts its clock accordingly. A 07:30 slot in `calendar_60.csv` fires at 07:30 Dubai time.

If you ever move your primary audience to the UK or US, change that one number in `post.yml`.

---

## Things that will catch you out

**Workflows auto-disable after 60 days of repo inactivity.** GitHub does this to everyone. The build workflow commits files most days, which counts as activity — so in practice this won't bite. But if you ever pause for two months, re-enable them in the Actions tab.

**Cron isn't punctual.** GitHub schedules can run several minutes late, occasionally longer under load. Irrelevant for content posting; worth knowing so a 07:34 post doesn't worry you.

**The free minutes reset monthly**, on your billing date, not the 1st.

**A failed render doesn't stop the run.** `ci_build.py` logs the failure and moves on; the next night's run retries it. You'll see it in the Actions summary.

---

## Checking on it

- **Actions tab** — every run, with full logs
- **`posted_log.csv`** in the repo — every post, with its Instagram media ID
- **Email** — GitHub emails you if a workflow fails
- **Locally** — `python run_all.py --status` any time

---

## Total cost

| | |
|---|---|
| GitHub Actions | free |
| Gemini API | free tier |
| edge-tts voice | free |
| Video hosting | free |
| Meta Graph API | free |
| **Monthly** | **₹0** |
