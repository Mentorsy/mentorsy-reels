"""
Mentorsy — batch post builder

Reads posts_spec.json and renders every post that isn't already rendered.
Runs on GitHub so finished PNGs land in the repo at public URLs, which is
what Canva needs in order to ingest and schedule them.

    python build_posts.py                # build anything missing
    python build_posts.py --force        # rebuild everything
    python build_posts.py --limit 14     # one week at a time

Resumable: a post whose folder already exists is skipped, so this can be run
repeatedly as the spec file grows.
"""

import argparse
import json
import os

import posts

BASE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(BASE, "posts_spec.json")
OUT = os.path.join(BASE, "posts_out")


def build_one(spec):
    """Returns the number of images written for this post."""
    outdir = os.path.join(OUT, spec["slug"])
    kind = spec.get("kind", "carousel")

    if kind == "carousel":
        return len(posts.build_carousel(spec, outdir))

    os.makedirs(outdir, exist_ok=True)
    if kind == "statement":
        img = posts.slide_statement(spec["hook"], spec.get("sub"))
    elif kind == "photo":
        # A local file if supplied, otherwise pull free documentary
        # photography at build time so CI stays self-contained.
        src = spec.get("photo") and os.path.join(BASE, spec["photo"])
        if not src or not os.path.exists(src):
            from images import _stock_image
            src = os.path.join(outdir, "_source.jpg")
            if not _stock_image(spec.get("stock_query", "student study desk"), src):
                raise RuntimeError("no photo available for this post")
        img = posts.slide_photo(src, spec["hook"])
    else:
        raise ValueError(f"unknown post kind: {kind}")

    img.save(os.path.join(outdir, "post.png"), quality=95)
    with open(os.path.join(outdir, "caption.txt"), "w", encoding="utf-8") as f:
        f.write(spec["caption"] + "\n\n" + " ".join(spec["hashtags"][:4]))
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()

    if not os.path.exists(SPEC):
        print("No posts_spec.json yet — nothing to build.")
        return 0

    specs = json.load(open(SPEC, encoding="utf-8"))
    if a.limit:
        specs = specs[:a.limit]

    os.makedirs(OUT, exist_ok=True)
    made = skipped = failed = 0

    for i, spec in enumerate(specs, 1):
        outdir = os.path.join(OUT, spec["slug"])
        if os.path.isdir(outdir) and not a.force:
            skipped += 1
            continue
        try:
            n = build_one(spec)
            print(f"[{i}/{len(specs)}] {spec['date']} {spec['slug'][:44]} -> {n} img")
            made += 1
        except Exception as e:
            print(f"[{i}/{len(specs)}] FAILED {spec['slug'][:44]}: {e}")
            failed += 1

    print(f"built {made} - skipped {skipped} - failed {failed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
