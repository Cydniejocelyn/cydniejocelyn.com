# Handoff — Cydnie Jocelyn, the resurfacing business

**Rewritten 26 August 2026, end of session.** Everything before this was appended in layers
and several of those layers now contradict each other, because decisions were reversed along
the way. This file replaces them. Where an old commit message and this file disagree, **this
file is right.**

---

## 1. Read this before touching anything

### The toolchain is installed. It is just not on PATH.

This cost three sessions. `node`, `npm`, `vercel` and `gh` all live in **`~/.local/bin/`**,
which a non-interactive shell does not inherit. Every session, first:

```
export PATH="$HOME/.local/bin:$PATH"
```

| | |
|---|---|
| `gh` 2.98.0 | logged in as `Cydniejocelyn`, scopes `read:org`, `repo` |
| `vercel` 59.5.0 | authenticated as `hello-66457178` |
| `node` v24.19.0 | |

Do **not** read `~/Library/Application Support/com.vercel.cli/auth.json` or the keychain. The
CLIs read their own credentials. That is the point of them.

### Where things are

| What | Where |
|---|---|
| The build | `~/Desktop/cydniejocelyn-v2/` |
| Home page | `index.html` |
| About page | `about/index.html` |
| Shared CSS and JS | `assets/css/site.css`, `assets/js/site.js` — **both pages share them** |
| GitHub | https://github.com/Cydniejocelyn/cydniejocelyn.com **(private)**, over HTTPS through `gh` |
| Vercel project | `cydniejocelyn-v2` under team `cydnie-jocelyn`, linked in `.vercel/` |
| Home artifact | https://claude.ai/code/artifact/df17491f-9b21-42bd-bb29-60f3d77f8cb5 |
| About artifact | https://claude.ai/code/artifact/edb8e6b0-19ba-4048-801b-ffc570b75551 |
| **About copy, source of truth** | `CydnieJocelyn-Site/about.html` |
| Refinement command | `CydnieJocelyn-Site/about-page-refinement-command.md` |
| Brand foundation | `CydnieJocelyn-Site/Minestreaming Cydnie Jocelyn/Brand-Foundation.md` |

An earlier note said `origin` was `Cydniejocelyn/cydniejocelyn`. **That repository never
existed**; it was a guess. The SSH key at `~/.ssh/id_ed25519` was never added to her account
and is now **moot** — do not spend time on it. HTTPS through `gh` works.

### The one thing still outstanding, and it is hers

**Deployment Protection is ON.** Every request to the Vercel URL bounces to a Vercel SSO login,
so only she and her team can see the site. Turning it off is a dashboard setting:

> Project Settings → Deployment Protection → Vercel Authentication → **Disabled**

**This is a trap for testing.** With protection on, a plain `curl` gets **200 on every path**,
including paths that do not exist, because it is being handed the login page. Never test the
deployment with plain `curl` and conclude anything. Use **`vercel curl`**, which carries the
auth and returns the real response.

---

## 2. Shipping anything: the exact sequence

```
export PATH="$HOME/.local/bin:$PATH"
cd ~/Desktop/cydniejocelyn-v2

python3 tools/stamp.py                  # ALWAYS, after editing site.css or site.js
python3 tools/build_artifact.py home
python3 tools/build_artifact.py about
git add -A && git commit -F <file>      # -F a file, NOT -m: see below
git push origin main
vercel deploy --prod --yes
```

Then republish both artifacts with the `Artifact` tool, passing each one's existing URL.

**Use `git commit -F` with a heredoc, never `-m` with backticks in the message.** Backticks in
a `-m` string are executed by the shell. One commit here lost a word that way.

### `tools/stamp.py` is not optional

`vercel.json` used to mark **everything** under `/assets/` immutable for a year, including
`site.css` and `site.js`, whose filenames never change. So the markup updated on every deploy
and the stylesheet never did: a returning visitor got new HTML against the CSS they first
downloaded. That is what produced the "broken hero" — the gauge with no rules rendering at the
top left, a bare hamburger dash, a wrapped nav.

Fixed two ways, and **both are needed**:

- `vercel.json` now marks only `/assets/(img|fonts|og)/` immutable. `/assets/(css|js)/` is
  `max-age=0, must-revalidate`.
- The links carry `?v=<content hash>`. `immutable` means a browser will not even *ask*, so only
  a changed URL rescues a cache that is already poisoned.

`stamp.py` regenerates that hash from the file contents. Current: `89168141`. Skip it and she
sees a stale site with no error anywhere.

---

## 3. The preview environment. Read before debugging any motion.

Measured, repeatedly. **None of this is a bug in the site.**

- **`requestAnimationFrame` never fires.** Zero frames.
- **`IntersectionObserver` never fires.** `site.js` uses its own scroll + timer engine
  (`watch` / `pump`). Keep it.
- **CSS transitions never advance.** A 200ms transition still reports `currentTime 0` after
  1200ms. `initTweenProbe()` detects this and sets `no-tween` on the root, which drops them all
  so everything lands finished. **The probe is flaky** — it sometimes decides transitions work
  when they do not. Keep it anyway.
- **CSS keyframe animations DO advance.** This is the one reliable mechanism.
- **Direct style writes apply instantly.** The second reliable mechanism.
- `window.scrollTo(x, y)` silently does nothing. Use `scrollTo({top, behavior:"instant"})`.
- **Screenshots go stale or blank after a programmatic scroll**, and often fire before an image
  decodes. Take a second shot, or measure the DOM. **Measure, do not look.**
- The pane also reports `innerWidth: 0` at times while layout is fine. Trust
  `document.documentElement.clientWidth` and screenshots over `innerWidth`.

### How to verify motion here

Three attempts at the breath animation shipped without moving, because all three were built on
rAF or transitions. If you cannot see motion, that is why.

- **Keyframes:** `document.getAnimations()` — check `playState` and that `currentTime` advances.
- **A tween you wrote yourself:** replicate the constants in the console and drive it with
  synthetic timestamps, then read the curve out as numbers.
- **Scroll-linked motion** is verifiable directly: it is a style write on a scroll event.

### A measurement trap

Counting elements at `opacity < 0.05` **while fades are in flight** reports dozens of
"invisible" elements. Let it settle and re-count. It reads as a catastrophe and is nothing.

---

## 4. Brand guide overrides. Do not "fix" these.

The site is knowingly outside the brand guide in three places. **Cydnie overruled each one
directly.** A future audit against the guide will flag them. Leave them alone.

| Guide says | What is shipped | Why |
|---|---|---|
| "Nothing loops" | **The breath bubbles loop**, 6.4s, infinite | She asked three times. It is the original movement, restored |
| "No gradients anywhere" | **Section seams and the rise band use gradients** | A hard edge between a light and a dark section reads as two pages stapled together. She asked for "gradient flow" |
| "No motion in the account or foundation" (refinement command) | **The account has per-paragraph reveals and a drifting portrait** | She said "disregard the document on the no movement portion" |

Also: **Held appears twice on the home page** (the hero's paid link and the five refusals). The
guide says one per page. She asked for the refusals to go warm. The refusals use `--warm`
(`#8F4A47`, the darkened Held the light zones already define) rather than raw Held, because raw
Held measured 3.74:1 there and the darkened one measures 5.01:1.

---

## 5. The copy freeze

`CydnieJocelyn-Site/about.html` is the source of truth for About copy, and the About page was
rebuilt from it verbatim. The prose is a first-person account of postpartum depression, a
child's rare genetic diagnosis, a husband's stroke at thirty-six, and a baptism.

**Change nothing about the words.** Specifically, and every one of these will look like an
improvement:

- Do **not** split the paragraph beginning "Then it got loud."
- Do **not** tighten run-on clauses joined with "and". The accumulation is the voice.
- Do **not** lengthen "Days before, I almost backed out." It is where the reader stops.
- Do **not** elevate register: "bawling my eyes out", "hustling to prove I was competent" stay.
- Do **not** add subheads, pull quotes, bullets, testimonials, logos, stats or counters.

The full reasoning is in `about-page-refinement-command.md`. It wins on copy. It has been
overruled on motion (see §4).

---

## 6. What is built

**About page order:** hero (typographic) → the reader → what happened → the personal bit →
the rise band → what held → what I do now → where to start → close.

- **Hero is typographic.** No photograph. Full-bleed Fathom, a 1px Meniscus rule at **38%**
  overhanging both edges, name and lede below, and a single **Held tick** crossing the rule at
  the left margin. That tick is the page's one Held element.
- **The account:** ten paragraphs, portrait **sticky** beside it with 12px drift, **each
  paragraph reveals as it is reached** (3 of 8, then 6, then 8, measured).
- **What held:** the three beliefs are a sentence, each opening its verse on a **checkbox
  toggle** — works with no JS.
- Long two-column sections use `.grid-12--hold`, which makes the heading sticky so the other
  side is never empty for a long scroll.

**Home page:** hero, condition, re-diagnosis, rise band, the work, differentiator band, before
you book, fifteen, proof, story, retreat, refusals, statement, questions, close, footer.

**Navigation, both pages:** The Build · Retreats · The Letters · About, with **A Sounding** as
the call. Per `about.html`.

### The three movements

- **The breath** — `@keyframes breath-rise`, 6.4s, infinite, negative delays so the cycle never
  jumps anyone back down where it can be seen. Loops deliberately (§4).
- **Fifteen** — fills fourteen circles in ring order over ~370px of scroll, stopping at the one
  that stays open. The divisor `vh * 0.38 + h * 0.30` is the whole dial.
- **The movement bar** — the depth gauge on the left. On mobile it is the instrument without
  the words. Hides behind the open menu via `menu-open` on the root.

### The rise band, which took several passes

Three separate bugs, all fixed, all easy to reintroduce:

1. **`max-height` next to `aspect-ratio`** made the band *narrower than the screen* above about
   1419px: the cap clamped the height and aspect-ratio derived the width back from it. Width is
   authoritative now. **Never put a max-height on `.rise-band`.**
2. **A mask killing the image from 62% down** chopped the water flat. It is a short dissolve at
   each end now.
3. **A hard line across the middle** was the two fallback grounds meeting on an edge behind a
   layer at 92% opacity. They blend over a third of the height now and the layer is at 1.

Each band declares `--band-into` for whatever follows it. The About one runs into Deepwater.

### The reveal backstop, which is subtle

`initReveals` used to reveal **every** target at 2.6s. That is right for anything on screen and
wrong for anything below the fold — the whole account was up before the reader arrived, so
nothing ever appeared to move. Now:

- **2.6s** — reveal only what is on screen or above.
- **12s** — reveal everything, **but only if the scroll watcher has never fired.** If the
  watcher demonstrably works, a slow reader is not robbed of the arrival.

Nothing can end up permanently invisible. Verified: nothing revealed at the top 11.8s after
load, all revealed once scrolled past, and **with JS off every paragraph is visible**.

---

## 7. Open, in priority order

1. **Deployment Protection.** §1. Hers to turn off. Nothing else blocks launch.
2. **One form is unwired.** `index.html:782`, `action="#"` — the twelve questions form in the
   closing section. Needs the Flodesk endpoint. Keep the hidden tag field.
3. **Privacy and Terms do not exist.** Both links were removed from the footer rather than
   shipped as 404s. The exact line to restore is **commented out in the markup** at the footer.
   Restore it once `/legal/privacy/index.html` and `/legal/terms/index.html` exist. (A regex
   link-checker will report these as 404s; they are inside that comment, not live. `/` and
   `/about/` are the only live internal links and both resolve.)
4. **`IvyPresto Display` is not self-hosted.** It is licensed, not on Google Fonts, and the
   files are **not in this workspace**. The stack names it first and falls back to Instrument
   Serif, which is what is actually rendering. Ask her for the Adobe license files.
5. **Never verified since the rebuilds:** a full keyboard pass, and a real screen-reader pass.
   Contrast has been checked in places, not swept.
6. **The podcast.** The home footer still links "She Rises Through It". The old wireframe said
   it was shelved. Whether that is true is not in any file.
7. **Nav targets.** The Letters points at `/#questions` and The Build at `/#build`, both
   anchors on the home page. `about.html` implies standalone pages (`/the-build`, `/letters`).
   Those pages do not exist yet.

---

## 8. Recreate the preview each session

The preview sandbox **cannot read `~/Desktop`**, so the server serves a mirror in the session
scratchpad, and **the scratchpad path changes every session**.

1. `sync.sh`: `rsync -a --delete` from the project to `<scratchpad>/preview/`, **excluding**
   `CydnieJocelyn-Site`, `cydniejocelyn`, and the `* copy` folders — otherwise it copies ~59GB
   of brand library and video into the scratchpad.
2. A server on `$PORT` with **`Cache-Control: no-store`**. Without it you debug a stale
   `site.js`. This cost an hour once.
3. Point `.claude/launch.json` at it, then `preview_start`.
4. **Run `sync.sh` after every edit**, and again after `build_artifact.py`.

To look at one section, cut it into a short standalone page and navigate fresh — full-page
screenshots after a programmatic scroll are unreliable. There is a working pattern for this in
the session transcript; recreating it takes a minute.

`.gitignore` excludes the ~59GB of source material that lives inside the project folder, the
two built artifacts, `.vercel`, and `.claude/`. Keep it that way.
