# Mentorsy content engine

A GitHub-Actions-to-Instagram/Facebook publisher that **cannot repeat itself**.

Drop-in replacement for the current automation. Read `DIAGNOSIS.md` for what
went wrong, `STRATEGY.md` for the branding decisions, and this file to install.

```
content/
  pillars.json        brand voice, 6 pillars, CTA ladder, lead magnets, rules
  bank_p1_p2.json     authored content, split by pillar so it's editable
  bank_p3_p4.json
  bank_p5_p6.json
  bank_legacy.json    58 pieces migrated from mentorsy-reels (see MIGRATION.md)
  bank.json           generated — never edit by hand
  media.json          you create this: content_id:format -> asset URL
engine/
  slots.py            10 weekly slots. Format is LOCKED to the slot.
  dedup.py            the seven gates
  schedule.py         picks one piece for one slot
  render.py           builds the caption
  publish.py          Meta Graph API + independent duplicate check
  run.py              workflow entrypoint
state/
  ledger.json         what has been posted. Committed back after every run.
tools/merge_bank.py   validator + merger (runs in CI)
tools/migrate_legacy.py           collapses legacy post/reel twins
tools/merge_legacy_into_bank.py   cross-bank duplicate sweep
tests/simulate.py     proves the feed cannot repeat
tests/audit_no_repeats.py         standing audit over the bank itself
docs/first_30_days.*  the generated calendar
```

## The eight gates

A piece must pass **all** of these to be eligible:

1. **Slot idempotency** — one slot fires once, ever. A re-run, a duplicated
   cron, a manual dispatch and a retry all resolve to the same key and the
   second one exits clean. *This alone kills the 3x/4x posting.*
2. **Format lock** — reels only come from pieces with a purpose-written
   `reel_script`. A carousel can never be promoted into a reel to fill a gap.
3. **Content cooldown** — 120 days, checked by id *and* by body hash, so two
   differently-named rows with the same text still collide.
4. **Hook cooldown** — 30 days on the *shape* of the opening line. Catches
   "same hook, new subject", the disguised repeat.
5. **Near-duplicate** — token-overlap (Jaccard ≥ 0.62) against everything from
   the last 30 days.
6. **Variety** — no pillar twice within 2 posts, no subject within 4.
7. **No-fiction gate** — a template with unfilled `[PLACEHOLDERS]` never
   auto-publishes. The engine will not invent a student result.
8. **Idea gate** — one idea ships **once**, in **one** format, per 365 days.
   A piece declares exactly one format and carries an `idea_group`; if that
   group has already gone out as a carousel, it cannot come back as a reel.
   This is the structural fix for reels-made-from-carousels. See `MIGRATION.md`.

When nothing passes, it posts **nothing** and opens an issue. Silence beats a
fourth repost.

## Install

```bash
# 1. copy this repo over your existing one (keep your old repo on a branch)
# 2. DELETE every other workflow that calls graph.facebook.com — two workflows
#    publishing is the second most common cause of double posts
# 3. secrets: Settings -> Secrets and variables -> Actions
#      META_ACCESS_TOKEN   long-lived page token with instagram_content_publish
#      IG_USER_ID          your Instagram Business account id
#      FB_PAGE_ID          the linked Facebook page id
# 4. Settings -> Actions -> General -> Workflow permissions
#      "Read and write permissions"   <- required for the ledger commit
```

## Run it

```bash
python3 tools/merge_bank.py            # validate + merge the bank
python3 tests/audit_no_repeats.py      # audit the bank for any duplication
python3 tests/simulate.py 365          # prove a full year with zero repeats
python3 engine/run.py --slot auto --dry-run    # see what would post right now
python3 engine/run.py --slot mon-am --date 2026-08-24 --dry-run
```

Go live by triggering the workflow manually with `dry_run: false` once, then
letting the schedule take over.

## Media

The engine handles *what* and *when*. It does not render images. Create
`content/media.json`:

```json
{
  "P2-01:reel":     { "video_url": "https://cdn.mentorsy.in/reels/P2-01.mp4" },
  "P1-04:carousel": { "image_urls": ["https://.../P1-04-1.jpg", "..."] },
  "P2-11:single":   { "image_url": "https://cdn.mentorsy.in/posts/P2-11.jpg" }
}
```

Meta requires publicly reachable URLs. Canva bulk-create from
`docs/first_30_days.csv` into an S3/R2 bucket is the cheapest path — one Canva
template per format, the CSV as the data source.

## Posting schedule

| | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|---|
| 08:00 | reel | | carousel | | carousel | | |
| 11:00 | | | | | | carousel | |
| 19:30 | carousel | reel | reel | reel | reel | | single |

10 posts/week — 5 reels, 4 carousels, 1 single. The mix is set by what the bank
can actually sustain, not by taste: measured against the 108-piece bank, a
5-3-2 week starved on singles after 4.6 weeks while carousels sat unused.
Change it in `engine/slots.py`; the cron in `.github/workflows/publish.yml`
must match.

## Refilling the bank

The bank holds **108 pieces / 106 distinct ideas** and runs **10 weeks clean**
(91 unique posts, 24 Aug – 1 Nov) before it refuses to continue. At 10/week you
need ~43 new pieces a month after that. Add them to the `bank_p*.json` files
using the same shape — **exactly one format per piece, and its own
`idea_group`** — then:

```bash
python3 tools/merge_bank.py && python3 tests/audit_no_repeats.py && python3 tests/simulate.py 365
```

CI runs both on every push, so a malformed piece — or a reel without a reel
script — fails the build instead of reaching the feed.
