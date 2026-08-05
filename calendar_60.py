"""
Mentorsy — 60-day content calendar

The strategy layer. Sixty days x 2 Reels = 120 topics, each pre-assigned a
pillar and a hook formula so no formula or pillar repeats back to back.

Topics are sequenced against the real school year: August is admissions and
transition anxiety, September is settling and early-warning signs, October
runs into first assessments and half term.

    python calendar_60.py            # writes calendar_60.csv
    python calendar_60.py --start 2026-08-06
"""

import argparse
import csv
import datetime
import itertools
import os

import config as C

PILLARS = [
    "Curriculum Decoded",
    "Maths Confidence",
    "School Choice",
    "Parent Scripts",
    "Inside the Method",
    "Reactive",
]

HOOKS = [
    "1 Contradiction", "2 Cost of Inaction", "3 Insider", "4 Named Enemy",
    "5 Specific Number", "6 Direct Address", "7 Permission",
    "8 Unanswerable Question", "9 Prediction",
]

# ── The topic bank. 120 angles, grouped by pillar. ────────────────────
TOPICS = {
"Curriculum Decoded": [
 "IGCSE vs IB Maths — which actually opens more university doors",
 "What 'Extended' vs 'Core' IGCSE Maths really decides about your child's future",
 "A Level Maths vs Further Maths — who genuinely needs both",
 "The difference between Edexcel and Cambridge IGCSE Maths, in plain English",
 "Why an A* at IGCSE doesn't predict an A at A Level",
 "AS vs full A Level — the decision most parents make by accident",
 "What 'predicted grades' actually mean and who decides them",
 "The three IGCSE subjects that quietly close doors at 16",
 "IB Maths AA vs AI — the choice that decides engineering eligibility",
 "Why your child's school changed exam boards and what it means for them",
 "How Cambridge grade boundaries actually move each year",
 "What a coursework component really costs your child in a maths-heavy timetable",
 "The truth about retaking IGCSE Maths",
 "Why 'we follow the British curriculum' can mean four different things in Dubai",
 "GCSE vs IGCSE — the difference that matters for UK university applications",
 "What the UCAS points table doesn't tell you about maths grades",
 "Foundation vs Higher tier — the ceiling nobody mentions at parents' evening",
 "How many A Levels your child actually needs for a Russell Group offer",
 "The subject combination that quietly rules out medicine",
 "What happens to your child's grades when you move countries mid-key-stage",
 "Why Year 9 options evening is the most important hour of secondary school",
 "The maths content that changed in the last syllabus update",
 "What a 9-1 grade actually maps to in the old system",
 "Why some universities still ask for a specific maths module",
 "The difference between a mock grade and a predicted grade",
 "How internal assessment feeds into a final Cambridge grade",
 "What 'gold standard' means when a school says it about a curriculum",
],
"Maths Confidence": [
 "Your child isn't bad at maths — they're two topics behind",
 "The fractions gap in Year 7 that shows up as failure in Year 10",
 "Why speed drills make maths anxiety worse, not better",
 "What 'showing your working' is actually training",
 "The difference between not understanding and not remembering",
 "Why your child can do the homework but fails the test",
 "Maths anxiety is a memory problem, not a personality",
 "The negative numbers gap nobody diagnoses",
 "Why more tuition on this week's topic won't fix a three-year-old gap",
 "How to tell whether your child is stuck or just tired",
 "The reason bright children stop putting their hand up in Year 8",
 "What happens in a child's brain in the ten seconds before a timed test",
 "Why 'just practise more' is the worst advice in maths",
 "The two questions that reveal exactly where a child's maths broke",
 "Why your child's calculator dependence is a symptom, not the problem",
 "How a single humiliating maths moment can cost four years",
 "The confidence collapse that happens at every school transition",
 "Why children who are good at mental maths sometimes struggle most at A Level",
 "What genuine mathematical fluency looks like, and what it isn't",
 "The difference between a child who is behind and a child who is lost",
 "Why perfectionist children avoid the questions they'd learn most from",
 "The revision method that feels productive and teaches nothing",
 "What happens when a child is moved down a set, and how to handle it",
 "Why a child who says maths is boring usually means something else",
 "The link between handwriting speed and maths marks nobody mentions",
 "How to rebuild a child's maths confidence in six weeks",
 "Why your own maths anxiety is transmissible, and what to do about it",
],
"School Choice": [
 "Three questions to ask on a Dubai school tour that they hope you won't",
 "What the KHDA rating actually measures — and what it doesn't",
 "How to read a school's exam results page properly",
 "The class size number schools quote and the one that matters",
 "What to look for in a school's maths department specifically",
 "Why the newest school in the area is not automatically the best bet",
 "How to tell if a school actually supports children who fall behind",
 "The question about teacher turnover you should ask, and how",
 "When moving your child schools is the right call — and when it isn't",
 "What a good school's response to a complaint tells you about everything else",
 "How to compare a British curriculum school in Dubai with one in the UK",
 "The hidden costs in a Dubai school fee structure",
 "Why 'we don't set by ability' can be good news or very bad news",
 "What to watch for on a school tour in the corridors, not the classrooms",
 "How to evaluate a school's sixth form before your child is anywhere near it",
 "The admissions test your child can and can't prepare for",
 "What a founding school gets right and wrong in its first three years",
 "How to ask a head teacher a hard question without damaging the relationship",
 "Boarding in the UK versus staying in the Gulf — the honest trade-offs",
 "The single best predictor of whether a school will suit your child",
 "What a school's waiting list actually tells you",
 "How to judge a school's pastoral care in one visit",
 "The sixth form question that separates good schools from marketed ones",
 "Why league tables mislead you about value added",
 "What to do when your first-choice school says no",
 "How much a school's leadership turnover should worry you",
],
"Parent Scripts": [
 "What to say when your child says 'I'm just not a maths person'",
 "How to respond to a bad report without losing the next six months",
 "The sentence that ends a homework argument in ten seconds",
 "What to say at parents' evening to get a real answer",
 "How to ask a teacher for help without it sounding like a complaint",
 "What not to say when your child gets a grade you're disappointed by",
 "The three words that make a child stop telling you about school",
 "How to talk about a subject you personally found hard",
 "What to say when your child compares themselves to a sibling",
 "How to raise a concern about a teacher, properly",
 "What to say the night before an exam — and what to never say",
 "How to respond when your child says the teacher hates them",
 "The question to ask after school instead of 'how was your day'",
 "How to handle it when your child lies about homework",
 "What to say when your child wants to drop maths",
 "How to disagree with your child's school without making them the battleground",
 "What to say to a child who is doing fine but believes they're failing",
 "The conversation to have before choosing IGCSE options, not after",
 "How to talk to a teenager about university without them shutting down",
 "What to say when your child fails something for the first time",
 "How to praise effort without it sounding hollow",
 "What to say when your child is being compared to a cousin",
 "How to set a phone rule that survives past week two",
 "What to say when your child asks if they're clever",
 "How to apologise to your teenager and why it works",
 "What to say when a friendship problem is wrecking their schoolwork",
 "The five-minute conversation that prevents most exam-season arguments",
],
"Inside the Method": [
 "What actually happens in a Mentorsy diagnostic session",
 "How I find the exact topic where a child's maths broke",
 "Why the first session is never about the current homework",
 "What fifteen years on the school leadership side taught me about parents",
 "The one thing I check before I look at any exam paper",
 "How mentorship differs from tuition, concretely",
 "Why I turn some families away",
 "What a good progress conversation with a parent sounds like",
 "The record I keep on every student and why parents get to see it",
 "How I decide whether a child needs six weeks or six months",
 "What I learned running a maths department that changed how I teach",
 "Why I start with the parent, not the child",
 "The three-question check I run before every A Level mock",
 "How I build a revision plan that a teenager will actually follow",
 "What I do when a child refuses to engage in the first session",
 "Why I don't set homework in the first month",
 "The exact moment I know a child has turned the corner",
 "How I work with a school rather than around it",
 "What a 300-teacher network gets you that a tutor can't",
 "Why I write to parents after every session, not every term",
],
"Reactive": [
 "What this week's exam board announcement means for your child",
 "The Dubai school fee change parents should read carefully",
 "New UK university entry requirements — who is affected",
 "What the latest KHDA inspection cycle is actually rewarding",
 "A curriculum change is coming — here's the honest read",
 "The AI-in-schools debate, from someone who has run a department",
 "What the newest PISA data actually says about maths teaching",
 "Grade inflation headlines — what parents should ignore and what they shouldn't",
 "A new school opening in the area: how to evaluate it in week one",
 "What changed in university admissions this cycle",
 "The teacher shortage story and what it means in your child's classroom",
 "New assessment rules — a plain-English translation",
 "What the latest tutoring industry report gets wrong about outcomes",
 "A policy change nobody explained to parents",
 "Exam timetable changes and the revision consequence nobody mentions",
 "What the recent results-day data says about maths specifically",
 "The screen-time study everyone shared — what it actually found",
 "A new curriculum framework, and the three things that genuinely change",
 "What international school growth in the Gulf means for admissions in two years",
 "The education headline of the week, honestly assessed",
],
}

# Weekly pillar rhythm — matches the master content system doc.
DAY_PILLARS = {
    0: ["Curriculum Decoded", "Parent Scripts"],      # Mon
    1: ["Maths Confidence", "School Choice"],         # Tue
    2: ["Reactive", "Curriculum Decoded"],            # Wed
    3: ["Parent Scripts", "Inside the Method"],       # Thu
    4: ["Maths Confidence", "School Choice"],         # Fri
    5: ["Reactive", "Parent Scripts"],                # Sat
    6: ["Curriculum Decoded", "Maths Confidence"],    # Sun
}


def slugify(s, maxlen=52):
    keep = "".join(c.lower() if c.isalnum() else "-" for c in s)
    while "--" in keep:
        keep = keep.replace("--", "-")
    return keep.strip("-")[:maxlen].strip("-")


def build(start_date, days=60):
    pools = {p: itertools.cycle(TOPICS[p]) for p in PILLARS}
    hook_cycle = itertools.cycle(HOOKS)
    rows = []

    for d in range(days):
        date = start_date + datetime.timedelta(days=d)
        pillars = DAY_PILLARS[date.weekday()]
        slots = [C.POST_SLOTS[0], C.POST_SLOTS[3]]   # 07:30 and 19:30

        for pillar, slot in zip(pillars, slots):
            topic = next(pools[pillar])
            hook = next(hook_cycle)
            rows.append({
                "date": date.isoformat(),
                "slot": slot,
                "pillar": pillar,
                "topic": topic,
                "hook_formula": hook,
                "slug": f"{date.isoformat()}_{slugify(topic)}",
                "status": "planned",
            })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default=None, help="YYYY-MM-DD (default: tomorrow)")
    ap.add_argument("--days", type=int, default=60)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    start = (datetime.date.fromisoformat(a.start) if a.start
             else datetime.date.today() + datetime.timedelta(days=1))
    rows = build(start, a.days)

    out = a.out or os.path.join(C.BASE_DIR, "calendar_60.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"✓ {len(rows)} posts across {a.days} days")
    print(f"  {rows[0]['date']} → {rows[-1]['date']}")
    print(f"  {out}")


if __name__ == "__main__":
    main()
