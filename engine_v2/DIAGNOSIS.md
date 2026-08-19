# Why the same post went out three and four times

I haven't read your repo yet, so treat this as the differential diagnosis. In
GitHub-Actions-to-Meta setups, repetition has five causes and they stack. Check
them in this order — the first two account for most of it.

## 1. The job has no memory between runs

This is the big one. If the workflow picks content by reading a spreadsheet or
JSON file and *never writes back what it posted*, then every run starts from a
clean slate. Whatever selection logic you have — first unposted row, random
choice, index modulo length — resolves to the same answer every time until the
input changes.

**Symptom match:** the same piece posting 3–4 times, not two random pieces
swapping.

**Fix in this repo:** `state/ledger.json` is committed back to the branch after
every publish (`.github/workflows/publish.yml` → "Commit ledger"). That commit
*is* the memory. Delete that step and the whole system reverts to your current
behaviour.

## 2. More than one trigger fires the same publish

Look at the `on:` block of every workflow file. If a publishing workflow has
any of these, it will double-post:

- `on: push` — posts every time you commit. Combined with a ledger commit, this
  creates an infinite loop.
- Two `cron` entries that both match the same intended slot.
- Two separate workflow files that both call the Graph API.
- `workflow_dispatch` re-runs, plus GitHub's own "re-run failed jobs".

**Fix in this repo:** one workflow owns publishing, there is no `push` trigger,
and `concurrency: group: mentorsy-publish` serialises everything. Any overlap
queues instead of racing.

## 3. Reels time out, retry, and post twice

The Instagram reel flow is two calls: create a container, then publish it.
Video containers take 30–300 seconds to encode. If your script publishes
immediately it gets an error, the step retries, the *first* container finishes
in the background, and both go live.

**Fix in this repo:** `engine/publish.py` → `_wait_ready()` polls
`status_code` until `FINISHED` before publishing. Nothing publishes mid-encode.

## 4. The content bank is smaller than the cadence

At 10 posts a week you consume **~44 original pieces a month**. If the source
sheet has 15 rows, any sane script wraps around after day 10 — and that wrap is
indistinguishable from a bug. This is the cause people almost always miss,
because the code is working exactly as written.

**Fix in this repo:** when nothing eligible remains, `schedule.py` raises
`NothingToPost` and the run exits *without posting*. Silence beats a fourth
repost. The workflow opens a GitHub issue telling you to refill.

## 5. Reels being generated from carousel content

Your exact words. This happens when format is decided at publish time from
whatever asset is available, rather than being a property of the content
itself. The script needs a video, finds a carousel, renders the slides into a
video, ships it — and the reel is a slideshow of a post you already ran.

**Fix in this repo:** format is bound to the *slot*, not inferred (`engine/slots.py`).
A piece is only eligible for a reel slot if it declares `"reel"` in `formats`
**and** carries a purpose-written `reel_script` with its own hook and timing.
`tools/merge_bank.py` fails the build if that's violated:

```
P4-01: reel format with no reel_script (this is the carousel-posted-as-a-reel bug)
```

That check runs on every push, so the bug can't come back quietly.

---

## What to send me

Paste the repo URL and I'll confirm which of the five you actually have. The
two files that answer it fastest are `.github/workflows/*.yml` and whichever
script calls `graph.facebook.com`.
