"""Posting slots. One slot = one guaranteed-unique publish opportunity.

The slot is the unit of idempotency. A slot fires at most ONCE, ever.
Re-running a workflow, a duplicated cron, a manual re-dispatch, a retry after a
network blip -- all of them resolve to the same slot key and the second one
exits without posting. This is the single change that kills 3x/4x reposting.

Times are IST (Asia/Kolkata). The UTC cron equivalents live in the workflow.
"""
from __future__ import annotations
from dataclasses import dataclass

IST_OFFSET_MINUTES = 330


@dataclass(frozen=True)
class Slot:
    id: str            # stable identifier, e.g. "mon-am"
    weekday: int       # 0 = Monday
    hhmm_ist: str
    fmt: str           # "reel" | "carousel" | "single"  -- HARD format lock


# 10 posts/week: 5 reels, 4 carousels, 1 single.
# The mix is set by what the BANK can actually sustain, not by taste: with
# 51 reels / 36 carousels / 15 singles available, a 5-3-2 week starved on
# singles after seven weeks while carousels sat unused.
# Format is bound to the slot, never inferred from the content piece, so a
# carousel can never be "promoted" into a reel to fill a gap.
SLOTS: list[Slot] = [
    Slot("mon-am", 0, "08:00", "reel"),
    Slot("mon-pm", 0, "19:30", "carousel"),
    Slot("tue-pm", 1, "19:30", "reel"),
    Slot("wed-am", 2, "08:00", "carousel"),
    Slot("wed-pm", 2, "19:30", "reel"),
    Slot("thu-pm", 3, "19:30", "reel"),
    Slot("fri-am", 4, "08:00", "carousel"),
    Slot("fri-pm", 4, "19:30", "reel"),
    Slot("sat-am", 5, "11:00", "carousel"),
    Slot("sun-pm", 6, "19:30", "single"),
]

BY_ID = {s.id: s for s in SLOTS}


def slot_key(date_ist_iso: str, slot_id: str) -> str:
    """The idempotency key written to the ledger."""
    return f"{date_ist_iso}#{slot_id}"


def slots_for_weekday(weekday: int) -> list[Slot]:
    return [s for s in SLOTS if s.weekday == weekday]
