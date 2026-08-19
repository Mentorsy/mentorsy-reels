"""Anti-repetition layer.

Six independent gates. A piece must pass ALL of them to be eligible.
Any one of them alone would have prevented most of what went wrong; together
they make a repeat within the cooldown window structurally impossible rather
than merely unlikely.

  1. SLOT IDEMPOTENCY   one slot fires once, ever            (engine/slots.py)
  2. FORMAT LOCK        reels only come from reel pieces
  3. CONTENT COOLDOWN   an exact piece cannot return for N days
  4. HOOK COOLDOWN      the opening line's shape cannot return for N days
  5. NEAR-DUPLICATE     token-overlap check against recent posts
  6. VARIETY            pillar + subject spacing so the feed reads as a brand
  7. NO-FICTION GATE    a piece with unfilled [PLACEHOLDERS] never auto-posts
  8. IDEA GATE          one idea ships ONCE, in ONE format, per cooldown

Gate 8 is the structural answer to "the reels are made from the carousels".
Format lock (gate 2) stops a carousel's assets being rendered into a video.
The idea gate stops something subtler and more damaging: the same ARGUMENT
going out as a carousel on Monday morning and a reel on Monday night. In the
legacy bank that was every single day -- measured containment between the two
halves of an entry had a median of 0.84.
"""
from __future__ import annotations

import hashlib
import re
from datetime import date, timedelta

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "of", "to", "in", "on", "for",
    "with", "is", "are", "was", "were", "be", "been", "it", "its", "this",
    "that", "these", "those", "you", "your", "they", "them", "their", "we",
    "our", "i", "my", "at", "as", "by", "from", "not", "no", "do", "does",
    "did", "so", "than", "then", "there", "here", "what", "how", "why", "when",
}


def normalise(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokens(text: str) -> set[str]:
    return {w for w in normalise(text).split() if w not in STOPWORDS and len(w) > 2}


def content_hash(piece: dict) -> str:
    """Stable fingerprint of what actually reaches the feed.

    Deliberately excludes the piece id -- two rows with different ids but the
    same body are the same post to a follower, and must collide.
    """
    body = " ".join(
        str(piece.get(k, ""))
        for k in ("hook", "body", "reel_script", "slides", "caption")
    )
    return hashlib.sha256(normalise(body).encode()).hexdigest()[:16]


def hook_signature(hook: str) -> str:
    """Catches 'same hook, new subject' -- the most common flavour of
    disguised repetition. Keeps the first six meaningful words."""
    words = [w for w in normalise(hook).split() if w not in STOPWORDS][:6]
    return hashlib.sha256(" ".join(sorted(words)).encode()).hexdigest()[:12]


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


class Deduper:
    def __init__(self, ledger: list[dict], rules: dict):
        self.ledger = sorted(ledger, key=lambda e: e["posted_on"])
        self.rules = rules

    # ---- helpers -------------------------------------------------------
    def _since(self, days: int, today: date) -> list[dict]:
        cutoff = today - timedelta(days=days)
        return [e for e in self.ledger if date.fromisoformat(e["posted_on"]) > cutoff]

    def _last_n(self, n: int) -> list[dict]:
        return self.ledger[-n:] if n else []

    # ---- the six gates -------------------------------------------------
    def slot_already_fired(self, key: str) -> bool:
        return any(e.get("slot_key") == key for e in self.ledger)

    @staticmethod
    def unfilled_placeholders(piece: dict) -> list[str]:
        """Proof/testimonial templates carry [BRACKETS] until a human fills in a
        real student, mentor or result. The engine will not invent them and will
        not publish the template. This is the gate that stops the automation
        from ever fabricating a testimonial."""
        blob = " ".join(
            [str(piece.get(k, "")) for k in ("hook", "body", "reel_script")]
            + [" ".join(piece.get("slides", []) or [])]
        )
        return sorted(set(re.findall(r"\[[A-Z][A-Z0-9_ \-]{2,}\]", blob)))

    def reasons_blocked(self, piece: dict, slot_fmt: str, today: date) -> list[str]:
        r, out = self.rules, []

        # 8. idea gate -- one idea, one format, one outing
        idea = piece.get("idea_group") or piece["id"]
        for e in self._since(r.get("idea_cooldown_days", 365), today):
            if e.get("idea_group") == idea and e["content_id"] != piece["id"]:
                out.append(
                    f"idea-gate: '{idea}' already shipped as {e['format']} "
                    f"on {e['posted_on']}")
                break

        # 7. no-fiction gate
        gaps = self.unfilled_placeholders(piece)
        if gaps:
            out.append(f"needs-real-data: unfilled {', '.join(gaps[:4])}")

        # 2. format lock
        if slot_fmt not in piece.get("formats", []):
            out.append(f"format-lock: piece is {piece.get('formats')}, slot needs {slot_fmt}")
        if slot_fmt == "reel" and not piece.get("reel_script"):
            out.append("format-lock: reel slot but piece has no dedicated reel_script")

        # 3. content cooldown
        recent = self._since(r["content_cooldown_days"], today)
        if any(e["content_id"] == piece["id"] for e in recent):
            out.append(f"content-cooldown: posted within {r['content_cooldown_days']}d")
        h = content_hash(piece)
        if any(e.get("content_hash") == h for e in recent):
            out.append("content-cooldown: identical body already posted (hash match)")

        # 4. hook cooldown
        hooks = self._since(r["hook_cooldown_days"], today)
        if any(e.get("hook_sig") == hook_signature(piece["hook"]) for e in hooks):
            out.append(f"hook-cooldown: same hook shape within {r['hook_cooldown_days']}d")

        # 5. near-duplicate
        t = tokens(piece["hook"] + " " + piece.get("body", ""))
        for e in self._since(r["hook_cooldown_days"], today):
            if jaccard(t, set(e.get("tokens", []))) >= r["near_duplicate_jaccard_threshold"]:
                out.append(f"near-duplicate of {e['content_id']}")
                break

        # 6. variety
        window = self._last_n(r["pillar_no_repeat_within_posts"])
        if any(e["pillar"] == piece["pillar"] for e in window):
            out.append(f"variety: pillar {piece['pillar']} used in last {len(window)} posts")
        # "General" is a catch-all, not a subject -- exempt it, or the whole
        # parenting/study-skills half of the bank blocks itself.
        subj_window = self._last_n(r["subject_cooldown_posts"])
        if piece.get("subject") not in (None, "General") and any(
            e.get("subject") == piece["subject"] for e in subj_window
        ):
            out.append(f"variety: subject {piece['subject']} too recent")

        return out

    def eligible(self, bank: list[dict], slot_fmt: str, today: date) -> list[dict]:
        return [p for p in bank if not self.reasons_blocked(p, slot_fmt, today)]

    # ---- CTA pacing ----------------------------------------------------
    def hard_ctas_this_week(self, today: date) -> int:
        monday = today - timedelta(days=today.weekday())
        return sum(
            1 for e in self.ledger
            if date.fromisoformat(e["posted_on"]) >= monday
            and e.get("cta_strength") == "hard"
        )

    def mid_ctas_this_week(self, today: date) -> int:
        monday = today - timedelta(days=today.weekday())
        return sum(
            1 for e in self.ledger
            if date.fromisoformat(e["posted_on"]) >= monday
            and e.get("cta_strength") == "mid"
        )
