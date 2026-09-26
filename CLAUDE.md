# Working on this site

This file is a pointer, not a second source of truth. **`HANDOFF.md` sections
71-72 are the current state of the site**: the 2026 rebuild, on branch
`site-2026` (main = the live site), launching all pages at once (69-70 have
the detail; 68 is Arizona) (67 has the Arizona reasoning): /retreats/gatlinburg/ launched on
16 September 2026, and /retreats/arizona/ went live on 24 September as an
unlinked, noindex landing page (not on /retreats/, not in the sitemap, on
her word). Read it before doing anything. Where
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

**/retreats/gatlinburg/ launched on 16 September 2026.** It is indexed, in
the sitemap, linked from home and Retreats, and announced by
`gatlinburg-popup.js`, which shares a one-popup-a-visit key with
`sounding-popup.js`. The early rate ends 31 October; section 62 lists every
place that says so.

**HoneyBook and Flodesk are the CRM.** Every form on the site goes to one
of them, including the Flodesk popup on /the-letters/, and that is settled.
Replacing them is out of scope unless Cydnie reopens it.

**There is a database, and it is switched off.** `api/` is in
`.vercelignore`, so the four endpoints do not deploy and nothing on the site
calls them. Deleting that line is what makes them live. Every form still goes
to HoneyBook, and the Flodesk popup on /the-letters/ stays. Section 51.

**The build refuses to ship a secret.** `.env.local` was copied into `dist/`
once, which a push would have published. If `check_no_secrets()` ever fires,
nothing deployed, and whatever it names still has to be rotated.

**The site speaks to founders and leaders, not women.** Widened on
11 September across thirteen strings. The retreats are the exception and
stay women only, labelled on their own pages. Section 53.

**Never measure a hero from a screenshot.** `tools/shot.sh` returns
different contrast answers run to run and three attempts at the home hero
shipped wrong numbers that way. Compute the composite in a browser instead:
canvas, real object-fit mapping, gradients per pixel, worst pixel under the
glyphs. Section 53 has the method.

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
oversight to correct. On 14 September 2026 Cydnie said "brand guide isn't
always right": when her ask conflicts with the guide, name the conflict in a
line and build what she asked for.
