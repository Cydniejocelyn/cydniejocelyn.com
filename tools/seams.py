"""Check every zone seam against the section actually above it.

WHY THIS EXISTS
---------------
Each section fades out of the ground of the section above it, and it names
that ground BY HAND in a `--from` custom property:

    <section class="section z-silt" data-zone style="--from:var(--surface)">

Nothing computes that value. So the moment a section's own ground changes, or
sections are reordered, or one is deleted, the section below it is fading from
a colour that is no longer there. It shows as a hard edge across the page, and
it is very hard to see on purpose because the two colours are often close.

This has bitten twice, both times in session twenty-four:

  Demoting the surplus Deepwater bands changed six sections' grounds and left
  ten seams pointing at colours that had moved. The risk was written down in
  the audit and then not checked.

  Reordering the home page in Phase 2 of the brief broke four more, which was
  the exact conflict flagged at the Phase 0 gate.

Run it after ANY change to a section's zone class, to the order of sections,
or after deleting one:

    python3 tools/seams.py

It prints one line per mismatch and a total. Zero is the only acceptable
number. It fixes nothing: repointing a seam is a judgement about which ground
is correct, and the answer is almost always "whatever is directly above it",
but not always, so it stays a report.

The two pre-existing mismatches this found on first run, on /retreats/ and
/retreats/greece/, were real and are fixed.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The ground each zone class paints. `.z-silt` hardcodes its colour rather
# than using a token, which is why #DCE4E1 appears raw here and in the pages.
GROUND = {
    "z-deep":      "var(--fathom)",
    "z-deepwater": "var(--deepwater)",
    "z-light":     "var(--surface)",
    "z-silt":      "#DCE4E1",
    "z-breath":    "var(--breath)",
}

# `--from` is written either way in the pages, so compare resolved values.
ALIAS = {
    "var(--fathom)":    "#071A1F",
    "var(--deepwater)": "#0C2830",
    "var(--surface)":   "#E7ECE8",
    "var(--breath)":    "#9FCCC6",
    "#DCE4E1":          "#DCE4E1",
}

PAGES = (
    "index.html",
    "about/index.html",
    "a-sounding/index.html",
    "the-build/index.html",
    "the-letters/index.html",
    "thequestions/index.html",
    "privacy-policy/index.html",
    "contact/index.html",
    "retreats/index.html",
    "retreats/greece/index.html",
    # Pre-launch and noindex. In here anyway: seams are a build
    # correctness check, not a search one, and the page has fourteen
    # of them. Its absence from sitemap.xml is the deliberate part.
    "retreats/gatlinburg/index.html",
)


def check(page):
    """Yield one message per seam that names the wrong ground."""
    path = os.path.join(ROOT, page)
    if not os.path.exists(path):
        return
    previous = None
    for n, line in enumerate(io.open(path, encoding="utf-8").read().split("\n"), 1):
        if not line.lstrip().startswith("<section"):
            continue
        classes = re.search(r'class="([^"]*)"', line)
        classes = classes.group(1) if classes else ""
        zone = next((z for z in GROUND if re.search(r"\b%s\b" % z, classes)), None)
        declared = re.search(r"--from:\s*([^;\"]+)", line)

        if declared and previous:
            want = ALIAS.get(previous)
            got = ALIAS.get(declared.group(1).strip())
            if want and got and want != got:
                yield ("%s:%d  --from:%s  but the section above it is %s"
                       % (page, n, declared.group(1).strip(), previous))

        # A section with no zone class does not change the ground beneath it.
        if zone:
            previous = GROUND[zone]


def main():
    bad = [m for page in PAGES for m in check(page)]
    for m in bad:
        print("  " + m)
    print("seam mismatches: %d" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
