# Verifying this site when the preview pane will not cooperate

The Claude preview pane went unresponsive partway through session three and
would not come back: `computer` timed out with "the Browser pane is currently
hidden". These three harnesses are what made it possible to check anything,
and they are here so the next session does not rewrite them.

They are **not part of the site**. `tools/` is in `.vercelignore`.

## Setup, once per session

The preview sandbox cannot read `~/Desktop`, and the scratchpad path is
different every session.

    export SP=/private/tmp/claude-501/.../scratchpad
    sh tools/preview/sync.sh
    # then serve it, with no-store headers, on a free port:
    python3 tools/preview/serve.py "$SP/preview" 8791

`serve.py` sets `Cache-Control: no-store`. Without it you debug a stale
`site.js`, which cost an hour once.

**Re-run `sync.sh` after every edit.** Nothing you change is visible until
you do, and it re-lays the harnesses, which `rsync --delete` wipes.

## `_shot.html` — screenshots at a real viewport

    /_shot.html?p=/retreats/greece/&y=4300&w=1440&h=1000
    /_shot.html?p=/retreats/&id=booking&w=1440&h=1000

Loads the page in a fixed-size iframe and walks the scroll down to `y` (or to
the element with `id`) in steps, so lazy images load and the scroll watcher
fires. Then screenshot the harness with headless Chrome.

**Why the iframe:** a naive tall-window full-page capture does not work here.
`.hero { min-height: 100vh }` means a 9600px window gives you a 9600px hero.
Inside the iframe, `100vh` resolves against the iframe.

## `_test.html` — the interaction suite

    /_test.html?p=/retreats/greece/

Drives the real page and prints PASS/FAIL lines big enough to screenshot.
43 assertions on Greece, 20 on Retreats at the end of session three, all
passing. Covers the gallery and rail, the lightbox (focus, scroll lock,
keyboard), the pointer companion, the video facade, the story scroll, the
objection picker, the FAQ, the reveals, the parallax, the map, the two host
portraits matching, overflow and image decoding.

**Run it after touching `site.js` or `site.css`.**

### Run it headless. The pane lies before it dies.

    sh tools/preview/runsuite.sh "$SP" 8814            # all four covered pages
    sh tools/preview/runsuite.sh "$SP" 8814 /a-sounding/

The preview pane degraded again in session four, and the important part is that
**it returned wrong answers before it returned errors.** Greece reported
41 pass / 2 fail on a page nothing had touched: an IntersectionObserver does not
fire in a pane the compositor has stopped drawing, so every reveal read as
unrevealed and the images check read as half the page missing. The identical URL
in headless Chrome: 43 / 0. Only after that did the pane start answering "the
Browser pane is currently hidden".

If the suite fails on a page you did not touch, run it headless before you
believe it. Coverage is 95 assertions: 43 Greece, 20 Retreats, 17 A Sounding,
15 The Letters.

## `_audit.html` — is it actually usable on a phone

    /_audit.html?p=/retreats/&w=375

Loads one page at one width in a fixed iframe and reports the things that
bite on a phone: horizontal blowout, elements wider than the viewport, tap
targets under 44px, stacked buttons of different sizes, undecoded images,
carousel slides that leave the view empty, text under 11px, and oversized
empty runs. Run it with the same headless pattern as the suite.

**The check that matters is "wider than the viewport", not "does the page
scroll sideways".** `body { overflow-x: hidden }` clips a blowout and reports
a clean page while the layout underneath is five times too wide. That is how
the Retreats carousel hid for three sessions: `.rt-video` was a bare
`display: grid`, its implicit column sized to max-content, and the quote
track's max-content is 2028px. On a 375px phone the whole Costa Rica block
laid out 2028px wide, two of the five reviews could not be reached at all,
and the section rendered as most of a screen of empty dark.

Four false positives it now knows about, so it does not cry wolf:

1. Elements inside something that scrolls or clips **on purpose** -- a rail,
   the lightbox, `.ab-head`'s bleeding rule, a parallax image.
2. **Inline links inside prose.** "Read the letters" in the middle of a 270
   character answer is part of that line; padding it to 44px breaks the
   paragraph. Only free-standing controls are held to the tap target.
3. **Hit areas grown with a pseudo-element.** `.door-note--link` measures
   18px on the box and 44px under a thumb, deliberately. The audit measures
   the `::after`.
4. **Buttons side by side at natural widths.** That reads as a pair and is
   fine. Only *stacked* buttons of different widths are the defect.

## `_menu.html` — can you read the mobile menu

    /_menu.html

Opens the mobile menu on all seven pages at **two scroll positions each** and
measures every item in it against the panel behind it: the four nav links,
the A Sounding button, the close toggle and the wordmark. 112 measurements.

**Both scroll positions matter, and the first one is the one that hides
things.** At the top of a page that opens light (The Build, The Letters) the
header is already `is-surfaced` but not yet `is-stuck`, so `.hdr::before`,
which is the bar's own background, is still `opacity: 0`. The wordmark and
the toggle have inverted to ink for a light ground that is not painted.
Scroll down the same page and `is-stuck` paints the bar light, everything
looks right, and the bug is gone. That is why it read as page-specific.

Two separate failures it caught, both the same shape:

1. **Three of the four nav links at contrast 1.00.**
   `.hdr.is-surfaced .nav-links a { color: var(--fathom) }` is (0,3,1) and
   `.has-menu .nav-links a` is (0,2,1), so Fathom text landed on the Fathom
   panel. Only the current page survived, by accident: its `[aria-current]`
   rule also computes (0,3,1), ties, and comes later in the file. The reader
   saw one legible item, the page she was already on.
2. **The wordmark and the close button, invisible in the same state.** A dark
   rectangle with no mark and no visible way out of it.

The button had been patched for this once already, years of sessions ago; the
links and the bar chrome never were. If you add anything to that panel,
add it here.

## `_probe.html` — measuring one thing

Edit it. It is a scratch file for answering "what is this element actually
doing", which is how the figcaption overflow and the parallax question were
both settled. Measure, do not look.

## Four traps, all of them expensive once

1. **A programmatic `scrollTo` inside the iframe does not reliably fire a
   `scroll` event in headless Chrome.** Anything driven by the scroll handler
   never runs and the test reports a site bug that does not exist. Both
   harnesses `dispatchEvent(new Event('scroll'))` after every step. Before
   that patch the parallax read 0/3 driven; after it, 3/3.
2. **Headless Chrome reports `prefers-reduced-motion: reduce` in some runs.**
   That correctly turns the parallax and the pointer companion off. The suite
   probes the media query and asserts the right thing either way.
3. **A real pointer event targets the element under the cursor.** Dispatching
   `pointermove` on `document` gives `e.target === document` and no
   `closest()` will ever match it. Dispatch on the element.
4. **Two `<details open>` set in the same tick race their `toggle` events.**
   The exclusive-FAQ check has to open them one at a time.

## Screenshotting a live site

Headless Chrome is the only way to get a real page to disk here. Chrome does
**not** exit after `--screenshot`, so background it, poll for the file, then
kill it, or the call hangs until the tool times out. See HANDOFF.md section 8.
