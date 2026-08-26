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
| The Build page | `the-build/index.html` |
| Shared CSS and JS | `assets/css/site.css`, `assets/js/site.js` — **both pages share them** |
| GitHub | https://github.com/Cydniejocelyn/cydniejocelyn.com **(private)**, over HTTPS through `gh` |
| Vercel project | `cydniejocelyn-v2` under team `cydnie-jocelyn`, linked in `.vercel/` |
| Home artifact | https://claude.ai/code/artifact/df17491f-9b21-42bd-bb29-60f3d77f8cb5 |
| About artifact | https://claude.ai/code/artifact/edb8e6b0-19ba-4048-801b-ffc570b75551 |
| **About copy, source of truth** | `CydnieJocelyn-Site/about.html` |
| **Build copy, source of truth** | `The Build page/files/the-build-page-wireframe-v6.html` |
| Colour system notes | `The Build page/files/color-system-notes.md` |
| Client brand boards | `CydnieJocelyn-Site/Portfolio of Work copy/Brand Board Portfolio of Work/` |
| Refinement command | `CydnieJocelyn-Site/about-page-refinement-command.md` |
| **The link list, source of truth for every URL** | `CydnieJocelyn-Site/Website Links.pdf` |
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
                                        # it stamps all THREE pages; add any new one to it
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

**The Build page** (`/the-build/`), built from wireframe v6 and the colour notes beside it.

Order: hero -> the condition -> three areas -> the work -> **A Sounding** -> the two shapes ->
production -> full engagement -> refusals -> questions -> close.

- **It is the only page on the site that opens light**, and that is the whole colour argument.
  Home and About open dark because both open on the condition. Here the condition is the
  price, so the page runs light and goes to full depth **once**, on A Sounding, which is the
  only action offered anywhere on it. `z-deep` appears exactly once. Do not add a second.
- **The full engagement is `z-deepwater`, not `z-deep`.** It was the darkest band in v3, which
  put maximum weight behind the most expensive item, and that reads as pressure.
- **There is no sticky bottom bar.** v6 drew one; the guide forbids it, and `site.css` already
  records that the bar and the slide-in nudge were removed. The booking link stands three
  times instead: nav, door, close.
- **Held is the refusal labels and nothing else.** A warm tick in the hero was built and then
  removed, because `.refuse` already sets its labels in `--warm` and that made two.
- **The three areas are not numbered** (`.triad--flat`). They are held at once. The phase lists
  are numbered, because those run in sequence.
- Every price is published, and the figures appear in three places that must stay in sync:
  the visible page, the `Service` + `FAQPage` schema at the top of the file, and HoneyBook.

### The work block, and why the boards are not posted whole

The three client brand boards are **one template with three fills** — same title bar, same two
logo panels, same palette diagram, same mood grid, same phone. Posting them whole would show
three businesses that look exactly like each other, which is the opposite of what the caption
above them claims. So each board is taken apart, by `PIL`, into:

- `assets/img/work/<slug>-mark-{600,900}.webp`, the primary logo lockup;
- `assets/img/work/<slug>-screen-{500,800}.webp`, the phone's screen interior with the status
  bar and browser chrome trimmed off;
- and a **palette rebuilt natively in CSS** from hex values sampled off the board, which runs
  the full width of the row and is the divider between one case and the next.

**The first build of this block was rejected as gothy and blocky, and it was.** Every mark sat
on the board's own panel inside a 1px border: three hard boxes in a column, one of them near
black, on a page that is Surface from top to bottom. It has been rebuilt in the guide's own
language and the current rules are:

There was then a second pass, because the coloured fields went too. **There is no rectangle in
this section at all now** — no background, no border, no corner. The marks are transparent and
sit directly on the page.

- **Mane Alchemist's mark is repainted and this is the one thing here to check with Cydnie.**
  Its lockup is drawn cream-on-black, so on Surface it has nothing to sit on, and that is the
  only reason that case ever had a field. The script is repainted in Mane's own Foundation
  `#1C1B1A` and **the gold motif is untouched**, so the two-tone survives and only the
  colourway changes. It is the positive version of a lockup delivered reversed, which is what
  a brand kit contains — but it is still that client's artwork altered for presentation. If
  she would rather it stayed cream, the answer is to give that one case its field back.
  Pixels are classified by saturation: `sat < 0.16 and max > 120` is the script, everything
  else is the motif.
- **The shipped page floats beside the mark on the one drop shadow on the site.** With the
  field gone nothing else holds these two objects in front of the page, and a screenshot lying
  flat on Surface reads as a picture of a phone rather than a thing that is running. The
  swatch rings are inset hairlines, not shadows.
- **Marks are matched on their WORDMARK, and this took four attempts.** Their bounding boxes
  are not comparable objects. Measured:

  | | box | ink in box | wordmark fills |
  |---|---|---|---|
  | Mane Alchemist | 900x883 | 11.6% | **54%** of the height |
  | SRS Performance | 900x396 | 32.2% | **100%** of the height |
  | SolyRey | 900x433 | 9.2% | **70%** of the height |

  Mane's box is square only because its deco motif runs the full height behind a wordmark that
  fills just over half of it. So matching widths made Mane twice as tall as the others;
  matching heights made it a postage stamp beside a 17rem SRS; and matching bounding-box
  **area** — which is what shipped first and was rejected — still read wrong, because most of
  Mane's area is empty. None of those three is the invariant.

  What the eye compares is the wordmark, so each case is scaled by roughly the inverse of the
  fraction above: `--mark-x` of **2.08 / 1 / 1.32** against a single `--mark-base` on `.cases`.
  One base and three multipliers, so they cannot drift apart at some width nobody checked.
  The multipliers are the measured inverses nudged by eye — Mane's delicate italic needs to run
  a little larger than SRS's bold geometric letters to hold the same weight, so the rendered
  wordmark heights are 74/66/62px rather than dead level. That is deliberate. Retune the
  multiplier on the case, never the rule.
- **The shipped page sits in a drawn device.** Chassis, bezel, corner radius and earpiece slot
  are all CSS off a single `--bezel`, not baked into the image, so the frame stays sharp at any
  size and the underlying crop stays reusable. A bare screenshot on an empty ground read as a
  cropped picture rather than something running.
- The mark's **height drives and width follows** (`width: auto`). `width: 100%` made the box
  wider than the ink, and on a phone that letterboxing opened a visible void between the mark
  and the phone beside it. For the same reason `.case-show` is `minmax(0, auto) auto` with
  `justify-content: center`: on `1fr` the mark cell absorbed every spare pixel.
- **The mark and the copy swap sides down the run** (`.case--flip`), so three cases do not
  land as three identical stamps.
- **The palette is circles with air between them**, the way the client boards draw it. The
  flush bar of colour it replaced was the blockiest thing on the page.
- **The cases are parted by the guide's divider**, a hairline with the four point mark at its
  centre. Drawn with straight edges at 13px it read as a plus sign; it is concave at 16px now.

Un-matting is why the marks have no fringe. A mark drawn light on black has edge pixels
blended toward black, so setting alpha while keeping RGB leaves a dark halo on any other
ground; `F = (P - (1-a)*BG) / a` recovers the foreground. Two traps if these are ever recut:
the board's own page shows around each panel (255 beside a 250 panel), so the crop has to snap
to the panel's own bounding box first; and **Mane's second lockup panel is dark too**, so a box
that reaches it makes the snap span both panels and turns the white page gap between them into
an opaque bar across the finished mark.

Crop boxes, in the board's own 900x900 preview space, scaled by `6250/900`: Mane
`(40,72,295,316)`, SRS `(38,70,290,315)`, SolyRey `(38,70,286,315)`, each snapped to its panel
then trimmed to ink; screen `(639,536) -> (802,818)`. Cydnie's own board is deliberately
absent: it is the retired teal-and-cream brand.

Fixed in the same pass, site wide: **the depth gauge's numeric read was printing over the text
column on any phone under 480px.** The gutter bottoms out at 20px there and the read is 16px
wide starting at 8px. It is hidden below `30rem`, leaving the track and dot, which sit at 16px
and clear it — "the instrument without the words", which is what mobile was always meant to be.

### Two shared-asset fixes this page forced, which affect every page

1. **`.is-surfaced` never reached the gauge.** Four rules in `site.css` invert the depth gauge
   on a light ground, written as bare `.is-surfaced .gauge-*` descendant selectors. `.gauge` is
   a **sibling** of `.hdr`, not a child, so they never matched and the instrument stayed pale
   teal over every light section on the whole site. `initHeader` now mirrors the flag onto
   `document.documentElement`. Every other `is-surfaced` rule is prefixed `.hdr`, so nothing
   else moved.
2. **`mark-horiz-dark-*.webp` is unreadable on Surface.** It is the wordmark drawn half
   submerged: the top half fades to near white and the subline is Breath. On `#E7ECE8` the
   logo washed out, and on The Build, which is light from the first pixel, that was the first
   thing anyone saw. `mark-horiz-ink-{500,800,1200}.webp` is the same drawing repainted from
   the light mark's alpha channel — Fathom for the wordmark, Meniscus for the subline, same
   aspect ratio so the swap does not shift the header. All three pages now use it. The old
   asset is still on disk and is no longer referenced.

Also fixed in passing: `about/index.html` closed its footer with `.ftr-base`, which is not a
class that exists. It is `.ftr-btm`.

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
2. **One form is still unwired, and the link list does not resolve it.** The twelve questions
   form in the closing section of `index.html` is still `action="#"`, so a submission reloads
   the page and the address is lost. Two things block it:

   - The form is built as a native POST expecting a **Flodesk** endpoint. The link list has no
     Flodesk URL at all.
   - The nearest thing on the list is **Join the collective**,
     `honeybook.com/widget/cydnie_jocelyn_collective_299013/cf_id/6a19d46a5cb4c5d7f86446a9`,
     filed under Home Page. That is a **hosted HoneyBook form page, not a POST endpoint**, so
     the native form cannot be pointed at it: it would have to become a link, or a HoneyBook
     embed. And "the collective" is not obviously the same product as "twelve questions, one a
     month, not a newsletter."

   It was left alone rather than wired to a guess, because a signup landing on the wrong list
   is worse to unpick than a signup that never fired. **Ask Cydnie which one it is.** Keep the
   hidden `tag` field either way.
3. **Privacy is linked. Terms still does not exist, and privacy has a cutover trap.**
   `https://cydniejocelyn.com/privacy-policy` is on the client's link list, returns 200 today,
   and is now in the footer of all three pages. It is **absolute on purpose**: it resolves now
   on the Vercel URL, and it resolves to the same place after the domain cuts over.

   **The trap:** that page lives on the OLD site. The moment `cydniejocelyn.com` points at this
   build, the path 404s unless `/privacy-policy/index.html` exists here. Either port the copy
   into this repo before cutover or add a redirect. Terms was never written and stays out of
   the markup; the line to restore is commented at the footer of `index.html`.
4. **`IvyPresto Display` is not self-hosted.** It is licensed, not on Google Fonts, and the
   files are **not in this workspace**. The stack names it first and falls back to Instrument
   Serif, which is what is actually rendering. Ask her for the Adobe license files.
5. **Never verified since the rebuilds:** a full keyboard pass, and a real screen-reader pass.
   Contrast has been checked in places, not swept.
6. **The podcast.** The home footer still links "She Rises Through It". The old wireframe said
   it was shelved. Whether that is true is not in any file.
7. **Nav targets.** The Build is now a real page at `/the-build/` and every nav, footer and
   hero-path link across all three pages points at it. **Retreats** (`/#retreat`) and
   **The Letters** (`/#questions`) are still anchors on the home page; `about.html` implies
   standalone pages for both. Those two do not exist yet.

8. **Client permission for the work block.** Three clients' marks and shipped pages are now
   published at `/the-build/#work`. Confirm written permission from Mane Alchemist, SRS
   Performance and SolyRey before this goes public. Nothing else on the page is blocked.

9. **The prices are now public, in three places.** The page, the JSON-LD in its head, and
   HoneyBook. If one figure changes, all three change, and the home page's Build door
   (`index.html`, `$1,500 to $15,000`) is a fourth. There is one open copy question v6 left
   unanswered: **does the $300 credit toward a Build?** v6's read is no, because crediting
   turns a complete deliverable into a deposit. If Cydnie decides yes, a line goes in the
   A Sounding block and in the HoneyBook service description.

---

## 7b. The links, and the three booking IDs that are not interchangeable

`CydnieJocelyn-Site/Website Links.pdf` is the authority. All eight URLs used from it were
checked and return 200. **There are three different scheduling IDs and they are three
different offers:**

| ID | What it is | Where it belongs |
|---|---|---|
| `6a185c26693e14802690e9f6` | **1:1 Session** | This is **A Sounding**. Every "Book one conversation" on all three pages. Correct everywhere already. |
| `69f9f2a095c611cc2401eec7` | **Branding session** (also listed as "Book a consult" and "Discovery call") | The Build. **Deliberately not used** — see below. |
| `6a18613d417c9c7126ec42e3` | **Book a call**, filed under Home Page | Not used. A generic call from the old site with no equivalent block here. |

**The Build has no branding-session link and that is deliberate.** Wireframe v6 gives the page
exactly one door and says so on the page: "Every engagement below begins here. There is no
other way in." Adding `69f9f2a09...` would be a second door and would undo the block. If Cydnie
wants the branding consult sold directly, that is a copy decision, not a missing link.

Wired this pass: the Greece waitlist on the home retreat block (it pointed at `#start`, which
sent a woman who wanted a retreat seat to a $300 call), Pinterest in the footer socials, the
privacy policy on all three footers, and Melissa's recorded review under the written quotes.

Not wired, and why: the twelve questions form (§7.2); the specific podcast episode
"The Messy Middle" filed under Home Page, because this build has no podcast section to hang it
on and the podcast's status is itself unresolved (§7.6); and the retreat forms that have no
section on the site yet — private retreat inquiry, choose your path, pre-register early bird,
and the four Sauk Centre room checkouts. Those belong to a Retreats page that does not exist.

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
