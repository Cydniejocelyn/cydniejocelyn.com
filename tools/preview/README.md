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
