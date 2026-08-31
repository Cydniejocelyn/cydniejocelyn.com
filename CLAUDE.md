# Working on this site

This file is a pointer, not a second source of truth. **`HANDOFF.md` section
48 is the current state of the site.** Read it before doing anything. Where
this file and HANDOFF disagree, HANDOFF is right and this file is stale: fix
it rather than working around it.

## The four things that cost the most if you do not know them

**A push to `main` is a live deploy.** A Vercel git integration runs
`python3 tools/build.py` and serves `dist/`, so pushing puts the site live in
about four seconds. `ship.sh` still works but is no longer the usual path.
Do not push anything you are not willing to have live.

**Plain curl can no longer prove a deploy.** Vercel's bot protection answers
`403` with `x-vercel-mitigated: challenge` and an identical challenge page for
every path, and **that page contains zero HTML comments**, so the usual
"comments == 0 means the build shipped" check passes on it. Use `vercel ls`
for status, then read one page in a real browser. Do not poll.

**Run `python3 tools/seams.py` after any change to a section's zone class or
to section order.** Every section names the ground of the section above it by
hand and nothing computes it. Zero is the only acceptable number.

**Never edit this codebase by line number.** Match on the string, assert the
count. Editing by line index once deleted an entire interaction because the
indices had shifted under an earlier edit in the same session.

## Before shipping anything

    python3 tools/build.py                      always
    python3 tools/seams.py                      0 mismatches
    sh tools/preview/runsuite.sh "$SP" 8814     455 pass / 0 fail, nine pages

If the suite fails on a page you did not touch, delete `$SP/cr-*` and run it
again before believing it. Those are per-page Chrome profiles and they cache.

## How Cydnie reviews work

From the real page, not from a description and not usually from a screenshot.
`python3 tools/build_artifact.py home` folds a page into one self-contained
file; publish that as an artifact and send her the link. She will say what she
wants changed. **Do not push before she has seen it** unless she has said so.

## What this site will not do

The brand guide forbids a sticky bar, a scroll progress bar, a slide-in
nudge, a modal, an exit intent, countdown timers and invented statistics.
Several of these have been asked for more than once and declined each time,
with the evidence recorded in `assets/js/site.js` at section 7-8-9 and beside
`.door` in `assets/css/site.css`. Read those notes before building any of
them, and treat a fresh request for one as a decision to confirm, not an
oversight to correct.
