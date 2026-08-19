# What happened to your old content bank

You asked for nothing repeated — "not even the reels from carousels". That
turned out to be the whole job, because the legacy bank was *built* to repeat.

## The measurement

Every one of the 60 entries in `content_a.py` / `content_b.py` /
`content_2026_09.py` held a `post` and a `reel` about the same idea, and
`pieces_for()` shipped the post at 09:00 and the reel at 20:30 **on the same
day**. That is the thing you were seeing in the feed.

Jaccard similarity said median 0.49 — bad but arguable. Jaccard is the wrong
instrument here: when a short reel restates a long carousel, the union is
dominated by the carousel's extra words and the score looks safe. The honest
measure is **containment** — how much of the shorter piece already exists
inside the longer one:

| containment | meaning | entries |
|---|---|---|
| ≥ 0.70 | the same post twice | **52 (87%)** |
| 0.50–0.69 | mostly overlapping | 6 (10%) |
| 0.30–0.49 | related | 2 (3%) |
| < 0.30 | genuinely different | **0 (0%)** |

Median containment: **0.84**. Not one pair in sixty was a genuinely different
piece of content.

Entry 0 is the pattern in miniature:

- post: *"What a maths report tells you, and what it hides"* — 62 percent could be strong algebra with collapsed geometry, or steady mediocrity
- reel: *"The number on the report is the least useful thing on it"* — 62 percent could be strong algebra with collapsed geometry, or steady mediocrity

## What I did with it

**Collapsed all 60 entries to 60 single pieces.** 60 duplicate halves deleted.
For each entry the survivor is whichever format the material actually suited —
carousel where there were four or more real list points, reel otherwise — and
the reel script is written from the reel's own `beats`, never from slides.

Then merged with the 50 pieces I wrote, and ran every pair against every other
pair. Two more collided and were dropped:

- `L11R` "IGCSE or IB? Wrong question." lost to `L21R` (containment 0.45)
- `L22R` "Do not ask what they are working on." lost to `L56R` (0.42)

Three pairs share no vocabulary but make the same point — text similarity is
blind to those. I found them by reading and tied them together with a shared
`idea_group`, so the scheduler keeps them a year apart.

## The result

**108 pieces. 106 distinct ideas. Maximum text overlap between any two: 0.37.**

| | |
|---|---|
| authored fresh | 50 |
| migrated from your bank | 58 |
| duplicate halves deleted | 60 |
| cross-bank collisions removed | 2 |

## The rule that stops it coming back

A piece now declares **exactly one format**. `tools/merge_bank.py` fails the
build otherwise:

```
a piece must declare exactly ONE format (got ['reel', 'carousel']) —
multi-format pieces are how the same idea ends up as both a carousel and a reel
```

And gate 8, the idea gate, refuses to publish anything whose `idea_group` has
shipped in the last 365 days — in *any* format. A carousel on Monday means its
idea cannot return as a reel on Monday night, or in March.

Reproduce any of this:

```bash
python3 tools/migrate_legacy.py          # the collapse, with per-entry decisions
python3 tools/merge_legacy_into_bank.py  # the cross-bank duplicate sweep
python3 tests/audit_no_repeats.py        # the standing audit
```
