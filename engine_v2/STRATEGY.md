# Mentorsy content strategy

## The correction that matters most

You told me the audience is students. Your site sells to **parents** — every
page is written to a mother deciding whether to spend money on her child.
Students are the end user; parents are the buyer, and on Instagram they are two
completely different content strategies.

Everything in this repo is written **to the parent**, with the child as the
subject. A 14-year-old will not book a trial class. Their mother will, at
10:40pm, after a report card.

That single change is worth more than any posting cadence.

## The offer ladder

Nobody books a ₹-per-month tutoring commitment from a reel. They book a free
class. So the content only ever has to do one job: make a parent believe *you
can find what's actually wrong with my child*.

```
Reel / carousel (value)  →  DM keyword (lead magnet)  →  WhatsApp  →  Free trial  →  Plan
```

Three CTA strengths, paced automatically by the engine:

| Strength | What it asks | Cap | Where the lead is captured |
|---|---|---|---|
| **soft** | Nothing. Save / share. | unlimited | Nowhere — this buys the right to ask later |
| **mid** | Comment a keyword | 4/week | The comment. Auto-DM sends the magnet, DM becomes the lead |
| **hard** | Book the free trial | 2/week | Link in bio → your existing form |

Roughly 6 asks per 10 posts, and never two hard asks back to back. A feed that
asks every time gets scrolled past; a feed that never asks gets saved and
forgotten.

## The six pillars

| Pillar | Job | Share | Why it earns |
|---|---|---|---|
| **Report Card Reality** | Name the specific cause behind a bad grade | 20% | Parent feels *understood*, not sold to |
| **60-Second Lesson** | Actually teach one thing | 28% | Saves and shares. Proves teaching quality without a testimonial |
| **Proof & Progress** | A real student arc, or the method | 15% | Belief that change is possible |
| **Curriculum Decoded** | Boards, criteria, exam patterns | 17% | Highest authority. Parents forward these to other parents |
| **Meet the Mentor** | Faces, vetting, the note home | 10% | Kills "who will actually teach my child" |
| **The Ask** | The free trial, plainly | 10% | Converts everything above |

**60-Second Lesson is the biggest pillar on purpose.** It is the only pillar
that gets shared into parent WhatsApp groups, which is where your buyers
actually live. A trigonometry trick travels further than a testimonial.

## The eight lead magnets

Each keyword auto-DMs one asset. Build these once; they run forever.

| Keyword | Asset |
|---|---|
| `MATHS` | The 12 Chapters That Quietly Break Grade 9 Maths (parent checklist) |
| `EXAM` | The 3-Week Board Exam Revision Plan |
| `BOARDS` | CBSE vs ICSE vs IGCSE — one page |
| `IB` | IB MYP → DP Transition Guide for Parents |
| `SPEAK` | 10 Public Speaking Drills You Can Run at Home |
| `FRENCH` | A1–A2 French Vocabulary Pack, Grades 6–10 |
| `CODE` | What Coding Actually Teaches a 10-Year-Old |
| `TRIAL` | Free trial class booking link |

Set the auto-DM rules in Meta Business Suite (Inbox → Automations → Comment
reply). One rule per keyword, ten minutes total.

## Cadence maths — read this before anything else

You asked for 10+ posts a week. Here is what that actually costs:

```
10 posts/week  ×  4.3 weeks  =  43 original pieces per month
```

There is no way around it. Repetition is not a bug you can code away — it is
what a script does when the bank is smaller than the cadence. Your current
system almost certainly has 12–20 pieces feeding a 10/week schedule, which is
why the same post appeared four times.

This repo ships **108 pieces across 106 distinct ideas** — 50 written fresh and
58 salvaged from your existing bank after the duplicate halves were deleted
(see `MIGRATION.md`). It runs **10 weeks clean: 91 unique posts, 24 Aug to
1 Nov**, then stops rather than repeat. After that you have three honest
options:

1. **Refill monthly.** ~43 new pieces a month, forever. Realistic only if
   writing is systemised — the pillar + hook structure here makes it about a
   half-day a month, not a full-time job.
2. **Drop to 7/week** (5 reels, 1 carousel, 1 single) → ~30 pieces a month.
3. **Drop to 5/week** → ~21 a month. This is what I'd actually recommend while
   you're solo. Five original posts beat ten with four repeats, and Instagram's
   ranking punishes the repeats specifically.

My recommendation: run 10/week for these ten weeks, watch which pillars pull
DMs, then settle at 5–7/week weighted toward whatever won. Ten weeks is enough
signal to stop guessing.

## One idea, one post, one format

Your old bank paired a carousel and a reel about the same point every single
day — median containment 0.84, and not one of the 60 pairs came in under 0.30.
That is why the feed felt repetitive even when the scheduler was "working".

The rule now: **a piece declares exactly one format and carries an
`idea_group`.** The build fails if a piece claims two formats, and the
scheduler refuses to publish any idea that has shipped in the last 365 days —
in any format. A carousel on Monday cannot come back as a reel on Monday night,
or in March.

## Voice rules the validator enforces

Banned outright (`tools/merge_bank.py` fails the build):
guaranteed results · topper guaranteed · 100% marks · secret formula ·
don't let your child fail · every parent's nightmare · limited seats only

Because fear-based tutoring marketing converts once and poisons the brand. You
are selling calm competence to an anxious parent. Adding to the anxiety is the
wrong trade.

## The one thing I will not automate

Six pieces (`P3-01/02/03/06/07`, `P5-02`) are **templates with `[BRACKETS]`** —
real student results, real mentor bios, real before-and-afters. The engine
refuses to publish anything with an unfilled placeholder, and the 90-day
simulation asserts it never happens.

I'm not going to invent a student who improved from 42 to 78, and you shouldn't
either — it's the one thing that would actually damage the brand if a parent
ever checked. Fill those six in with real people (with permission) and they
become your highest-converting posts in the bank.
