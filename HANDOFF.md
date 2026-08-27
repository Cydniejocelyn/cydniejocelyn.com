# Handoff — Cydnie Jocelyn, the resurfacing business

**Rewritten at the end of session one, extended at the end of sessions two, three and four,
26 August 2026.**
Everything before the rewrite was appended in layers and several of those layers contradicted
each other, because decisions were reversed along the way. Where an old commit message and this
file disagree, **this file is right.** Where two parts of this file disagree, that is a bug:
fix it rather than working around it.

---

## 0. State as of 26 August 2026, end of session four

**Everything below §1 is reference. This section is where a new session starts.**

**Seven pages are built. Five are live; two are built and not yet deployed.** Home, About,
**The Build** (`/the-build/`), **Retreats** (`/retreats/`) and **Greece** (`/retreats/greece/`)
are live. **A Sounding** (`/a-sounding/`) and **The Letters** (`/the-letters/`) were built in
session four and are on `main`, unshipped. Run §2.

**Every nav target on this site now has a page behind it.** That was not true before session
four: The Letters was an anchor to a form on the home page and A Sounding was a block on it.

| | |
|---|---|
| Production | the newest **Ready** row in `vercel ls --prod` |
| `main` vs production | **Session four's two pages are NOT deployed.** Everything before them is. Check with `git log --oneline` — a commit that touches `HANDOFF.md`, `README.md` or `tools/` changes nothing a visitor sees. |
| If in doubt | Run §2. Deploying twice costs nothing; shipping stale markup costs a session. |
| Interaction suite | **95 assertions, all passing** (43 Greece, 20 Retreats, 17 A Sounding, 15 The Letters) |

Do **not** write a deploy URL into this table. Session three did, and the next commit -- which
was this file -- immediately made it wrong. `vercel ls --prod` is the answer and it cannot go
stale.

**Deployment Protection is still ON,** so nobody outside the team can see any of it. See §1.

### Start here, in this order

1. `export PATH="$HOME/.local/bin:$PATH"` — nothing works without it. §1.
2. Recreate the preview: `export SP=<this session's scratchpad>` then
   `sh tools/preview/sync.sh` and `python3 tools/preview/serve.py "$SP/preview" 8791`.
   **Read `tools/preview/README.md` first.** The Claude preview pane died mid-session and the
   harnesses in there are how anything got verified. Four traps documented, all expensive once.
3. Ship with §2. It is seven pages now, and two of them have never been deployed.

### What is left, and every one of them is Cydnie's decision

| # | Waiting on Cydnie | Where |
|---|---|---|
| 1 | **Deployment Protection is ON.** One dashboard toggle. Nothing else blocks launch. | §1 |
| 2 | **The Flodesk popup cannot be reopened from the page.** The form is live and correct on `/the-letters/`, but its "Get the letters" button only works once Flodesk's own trigger is set to "on click" on `#letters-open`. **One dashboard setting.** Until then the button falls back to the email address. | §11 |
| 3 | **The home page's `#questions` form is now redundant** and still `action="#"`. `/the-letters/` does the same job with a working list behind it. Left alone in session four because the instruction was not to touch shipped pages. | §11 |
| 4 | **"Choose your path"** is the same HoneyBook URL as the branding page's "Lets talk", so which product it belongs to is unresolvable from the link list. Unwired. | §10 |
| 5 | **The sticky bar.** Brief says keep, `site.css` says the guide forbids. Currently OFF. | §7c |
| 6 | **Mane Alchemist's mark is repainted** in its Foundation ink. A client's artwork, altered. | §6 |
| 7 | **Written permission** from Mane Alchemist, SRS Performance and SolyRey before launch. | §7.8 |
| 8 | **Privacy 404s at domain cutover, and the copy for the fix has now arrived.** `Privacy terms page/privacy-terms-copy-v1.md`, 19:19 on 26 August: privacy and terms in one document, both parts written. Excluded from the deploy, **not built**. It carries its own FLAG lines, including the last-updated date. | §7.3, §11 |
| 9 | **Two client sites render broken on mobile.** Not ours, but she should know. | §7b2 |
| 10 | **The Sauk Centre retreat, 8 October 2026,** has four live checkout links and is on no page. She said leave it off. | §10 |
| 11 | **`/thequestions` is unbuilt.** A fourth wireframe arrived at 19:07 on 26 August: a QR landing page for the GATHER event tables. Excluded from the deploy, not built, and it carries three open copy decisions of its own. | §11 |
| 12 | **`IvyPresto Display` is not self-hosted.** Instrument Serif is what actually renders. | §7.4 |
| 13 | **Never verified:** a full keyboard pass and a real screen-reader pass. | §7.5 |
| 14 | **`figure` default margin is unreset on `.quote`**, so the home page's quote carousel is indented 40px each side. Fixed on `.sd-quote` only; the shared fix moves a shipped page. | §11 |
| 15 | **Angela's quote is excerpted on `/a-sounding/`.** Her full review opens "From our very first coaching call", and that page argues it is not coaching. Confirm she is comfortable appearing there. | §11 |
| 16 | **The podcast.** The footer links it; whether it is shelved is in no file. | §7.6 |
| 17 | **The brief's scope lock** was overridden on her instruction, repeatedly. | §7c |

### Decisions she made in session three. These are load bearing.

Every one of these settled a contradiction between the drafts, the shipped site and `llms.txt`.
**Each is now stated in more than one place and those places must not drift.**

1. **Greece is fifteen seats and all fifteen are taken.** Waitlist open, called in order.
   Stated in: both retreat pages, the home retreat block, `llms.txt`, and two `Offer` blocks
   marked `SoldOut`.
2. **Crete has no single occupancy.** Shared rooms only, no supplement. Stated in **four**
   places: the property rows, beside the price, the FAQ, the FAQPage schema, plus `llms.txt`.
3. **No average rating anywhere.** Six responses is not a sample. Removed from the retreats
   page *and* from the home page's `AggregateRating`, which was the same claim in the form that
   surfaces as stars in search. Individual attributed `Review` entries stay. See §10.
4. **No em dashes.** Zero in every shipped `.html`, `.txt`, `.xml`, `.css`, `.js`. En dashes
   remain in `13&ndash;20 August 2027`, which is what that mark is for. See §10.
5. **The Sauk Centre retreat stays off the site**, live checkout links and all.
6. **Greece keeps the name "Rise Into Her: The Greece Edition."** "Fifteen" is the cap, not a
   title.
7. **The Costa Rica guest photographs are approved**, faces included; she confirmed permission.
   This is the only page on the site with recognisable faces and it is deliberate.

### What session three actually did

Built `/retreats/` and `/retreats/greece/` on the shared stylesheet and chrome, then reworked
both. In order:

- **The build.** Both pages, all imagery cut locally from the source libraries, every link from
  `Website Links.pdf` wired, schema on both.
- **The picture pass** on `/retreats/`. The pool candids sold a holiday; the hero is a headland
  across still water now, which is the picture the brand is built from. April 2027 has a drawn
  US map because it has no location to photograph.
- **The Greece rework.** The page was a document; it is a funnel. Order changed (trust before
  price, objections before the number), and four blocks were rebuilt rather than trimmed.
- **Two real bugs found and fixed in shared CSS**, both of which affected more than the page
  they showed up on: the host portraits were different sizes, and a `figcaption` was falling
  out of its own figure. See §10.

Shared additions: `site.css` **section 25**, `.hero--bright`, `--hl`; `site.js` **15, 16, 16b,
17** (video, lightbox, rail, cursor); `tools/retreat_images.py`, `tools/us_map.py`,
`tools/preview/`. `stamp.py`, `build_artifact.py`, `sitemap.xml`, `llms.txt` and
`.vercelignore` all extended to five pages. Session four took every one of them to seven.

### Decisions she made in session four. These are load bearing too.

1. **The Letters is a WEEKLY letter, not twelve questions once a month.** The shipped site said
   the monthly thing in three places while the home page's own door said "A letter on Sunday
   nights", so it contradicted itself before this session started. Weekly wins, and it is
   corroborated by Flodesk: the live form's own headline reads "One letter a week."
   **The twelve questions are a different product**: a numbered card deck used on tables at
   GATHER events, which is what the `/thequestions` wireframe is for. They were never the list.
2. **Flodesk form `6a8f553c9f30a024ac4f2a82` is the letters list**, and it is a popup form.
3. **The A Sounding popup runs on four pages and is excluded from three:** `/a-sounding/`,
   `/about/` and `/retreats/greece/`. See §11.
4. **Angela's quote is excerpted, not quoted whole,** on `/a-sounding/`.

### What session four did

Built `/a-sounding/` and `/the-letters/` from the two wireframes, wired the popup, and
repointed every nav and footer that had been aimed at an anchor on the home page. See §11.

### The wireframe folders, and what became of them

`A Sounding/` and `The Letters Page/` were built in session four. `the questions/` arrived at
19:07 on 26 August, mid-session, and was **excluded from the deploy within the minute and not
built**. All three stay in `.vercelignore`: they are working documents with annotation layers,
notes toggles and, in the Letters draft, a live HoneyBook widget pointed at the retired
Collective form.

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
| Retreats page | `retreats/index.html` |
| Greece page | `retreats/greece/index.html` |
| A Sounding page | `a-sounding/index.html` |
| The Letters page | `the-letters/index.html` |
| Shared CSS and JS | `assets/css/site.css`, `assets/js/site.js` — **all seven pages share them** |
| GitHub | https://github.com/Cydniejocelyn/cydniejocelyn.com **(private)**, over HTTPS through `gh` |
| Vercel project | `cydniejocelyn-v2` under team `cydnie-jocelyn`, linked in `.vercel/` |
| Home artifact — **STALE** | https://claude.ai/code/artifact/df17491f-9b21-42bd-bb29-60f3d77f8cb5 |
| About artifact — **STALE** | https://claude.ai/code/artifact/edb8e6b0-19ba-4048-801b-ffc570b75551 |
| The Build artifact | **never published.** Put its URL in `ARTIFACT["build"]` in `tools/build_artifact.py` the first time it is |
| **About copy, source of truth** | `CydnieJocelyn-Site/about.html` |
| **Build copy, source of truth** | `The Build page/files/the-build-page-FINAL.html` — supersedes v6 |
| Build wireframe, superseded | `The Build page/files/the-build-page-wireframe-v6.html` |
| **Retreats copy, source** | `Retreat drafts/retreats-visual-v2.html` |
| **Greece copy, source** | `Greece Retreat/greece-v2 copy.html` — the `copy` is the later of the two |
| **A Sounding copy, source** | `A Sounding/a-sounding-wireframe-v2.html` |
| **The Letters copy, source** | `The Letters Page/the-letters-v2.html`, except the cadence: see §11 |
| `/thequestions`, **unbuilt** | `the questions/thequestions-wireframe-v2 (1).html` |
| Greece draft, superseded | `Greece Retreat/greece-v2.html` — still sells seats, has TKs |
| Armonia photography | `CydnieJocelyn-Site/08.13.2027-.../Armonia Retreat Center/wetransfer_.../` |
| Costa Rica photography | `Costa Rica copy/` and `Costa Rica copy/Maxime Photos copy/` |
| Costa Rica feedback, 6 responses | `CydnieJocelyn-Site/Reviews/Rise & Reground_ ... Feedback.csv` |
| Build brief, **and it conflicts** | `The Build page/files/CLAUDE-CODE-BRIEF.md` — see §7c |
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
                                        # it stamps all FIVE pages; add any new one to it
python3 tools/build_artifact.py home
python3 tools/build_artifact.py about
python3 tools/build_artifact.py build
python3 tools/build_artifact.py retreats
python3 tools/build_artifact.py greece
git add -A && git commit -F <file>      # -F a file, NOT -m: see below
git push origin main
vercel deploy --prod --yes
```

Then republish the artifacts with the `Artifact` tool, passing each one's existing URL.

**The two published artifacts are stale.** They were last published in session one and none of
session two reached them: no ink wordmark, no gauge fix, no repointed nav, no published
prices, no Build page. The `.html` files under `tools/` are current — they are rebuilt every
time — but nobody has pushed them to the artifact URLs. Republish before showing anyone an
artifact link, or send the Vercel URL instead.

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

`stamp.py` regenerates that hash from the file contents. Current: `438d51e3`. Skip it and she
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
  Currently nine offers and ten questions, verified matching in both places.
- **Site care is published, not disclosed after the quote.** $95 Essential, $200 Complete,
  $100/hr design work. A required recurring cost that appears after the quote reads as a
  hidden fee however reasonable it is; published beside the build price it reads as ownership.
  The refusals block is worded to match: it says no open ended **consulting** retainers, with
  care named as the exception, because the old wording contradicted it outright.
- **Settled by FINAL: A Sounding does not credit toward a Build.** It is complete on its own,
  and crediting it would turn a finished deliverable into a deposit. This must match the
  HoneyBook service description.
- The retreats line at the close is **body text and a link, never a button.** A retreat is a
  dated product with a cap and a price so it books directly; the single door rule governs
  consulting, not everything on the site.

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
- **The shipped page sits in a drawn iPhone.** Chassis, bezel, corner and Dynamic Island are
  CSS, not baked into the image, so the frame stays sharp at any size and the crop underneath
  stays reusable. The first version was a lozenge: its radius was a multiple of the bezel and
  landed at **23% of the device width**, where a real iPhone's corner is about 10%. Everything
  is now a fraction of `--dev-w`, taken off the real proportions:

  | | |
  |---|---|
  | screen | **393 x 852pt**, locked as `aspect-ratio` on the box, image filling it with `cover` |
  | bezel | 12.9pt (~2.2mm) = **3.08%** of body width |
  | body corner | 55pt screen corner + bezel = **16.21%** of body width |
  | screen corner | body corner minus bezel = **13.99% of SCREEN width**, which is Apple's 55/393 |
  | island | 125 x 36.7pt, 11pt down = 29.9% x 8.8% of body width |

  **Every number is derived from an iPhone 15/16 Pro, not tuned by eye.** Tuning by eye
  produced three wrong frames in a row: a lozenge at 23%, an over-correction to 11.5%, then
  12.5% picked to be concentric with a curve the screenshot happened to have. A real iPhone is
  **rounder** than all three. The check that matters: body corner minus bezel over screen width
  is 0.1399, and Apple's 55/393 is 0.1399. The curves are concentric because the arithmetic
  makes them concentric. Do not nudge one of these without re-deriving the rest.

  **The screen box owns its aspect ratio and the image fills it with `cover`.** That is what
  stops this drifting again: the frame is an iPhone whatever the source image measures, so
  swapping a screenshot can never put the proportions out.

  No side buttons: at 76–136px they land under two pixels wide and read as rendering artefacts
  rather than hardware. The corners are CSS `border-radius`, a circular arc rather than Apple's
  continuous squircle; at a 9–16px radius that difference is sub-pixel, and buying it would
  cost a mask plus a filter-based shadow plus a wrapper element.
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

Crop boxes for the marks, in the board's own 900x900 preview space, scaled by `6250/900`:
Mane `(40,72,295,316)`, SRS `(38,70,290,315)`, SolyRey `(38,70,286,315)`, each snapped to its
panel then trimmed to ink.

**The phone is `(4432, 3561) -> (5568, 6049)` in source pixels, identical on all three boards**
— 1136x2488, aspect 0.4566. Found by asking for the first and last row whose **central 60%**
is solid. The central 60% is the part that matters: SRS Performance has the board's own
"Minneapolis, MN 55403" caption running above its phone, and a naive top-edge test locks onto
that text instead. An earlier crop started one pixel high and carried a slice of it into the
shipped image.

Cydnie's own board is deliberately absent: it is the retired teal-and-cream brand.

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

**Navigation, all three pages:** The Build · Retreats · The Letters · About, with **A Sounding**
as the call. Per `about.html`. The Build now points at `/the-build/` everywhere; Retreats and
The Letters are still home-page anchors. See §7.7.

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
7. **Nav targets. CLOSED in session four.** Every nav target now has a page behind it:
   The Build, Retreats, **The Letters** (`/the-letters/`) and **A Sounding** (`/a-sounding/`).
   `/#questions` and `/#sounding` no longer appear in any href on the site.
   `index.html` still has a `#retreat` section, which is the home page's Greece block; it is
   no longer a nav target and it now links out to `/retreats/greece/`.

8. **Client permission for the work block.** Three clients' marks and shipped pages are now
   published at `/the-build/#work`. Confirm written permission from Mane Alchemist, SRS
   Performance and SolyRey before this goes public. Nothing else on the page is blocked.

9. **The prices are public in four places and they must not drift.** The page, the JSON-LD in
   its head, the home page's Build door (`index.html`, `$1,500 to $15,000`), and HoneyBook.
   Change one, change all four in the same commit. Currently nine offers and ten questions,
   verified matching between the markup and the schema.

   **v6's open question is closed.** FINAL settles it: a Sounding does **not** credit toward a
   Build. It is complete on its own and crediting it would turn a finished deliverable into a
   deposit. **This has to match the HoneyBook service description** — worth checking that it
   does, because nothing here can verify it.

10. **The sticky bottom bar.** `CLAUDE-CODE-BRIEF.md` says keep it. `site.css` records that it
    was removed because the brand guide forbids it, along with the nudge, the modal and the
    exit intent. Both cannot be right. **It is currently off.** See §7c.

11. **Mane Alchemist's mark is repainted and Cydnie has not seen the question.** Its lockup is
    cream on black and vanishes on Surface, so the script is repainted in Mane's own Foundation
    `#1C1B1A` with the gold motif untouched. That is the positive version of a lockup delivered
    reversed, which is what a brand kit contains — but it is still a client's artwork altered
    for presentation. If she would rather it stayed cream, the fix is to give that one case a
    coloured field back. See §6.

12. **Two of the three live client sites render broken on a phone**, which is not this repo's
    problem but is worth telling her before anyone follows a link from the portfolio. §7b2.

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

## 7b2. The live client sites cannot be screenshotted, and that is worth knowing

Asked to rebuild the phone visuals from the real sites, all three were captured with headless
Chrome at a true iPhone viewport (393x852 at DPR 3). **Two of the three render broken on a
phone:**

- **srsperform.com** — content sits in a white gutter offset to the right and the wordmark is
  clipped off the right edge. (`srsperformance.com` is a parked for-sale domain; the live one
  is `srsperform.com`, which is also what the mockup's own browser bar says.)
- **solyrey.com** — the hero headline reads "Wander Freely. Discov" and the buttons read
  "CURATED JOURNEY" and "PLAN MY TR". Still clipped at 430px wide.

Not a capture artefact: identical at device pixel ratio 1 and 3, and at 393 and 430 wide. Both
sites genuinely overflow horizontally on phones. **manealchemistsalon.com is clean.** SRS also
carries a cookie banner that would have to be dismissed to get a clean shot, and dismissing it
is consenting on Cydnie's behalf, which is not ours to do.

So the section still uses the board mockups. They are her delivered work, they are consistent
with each other, and they render correctly. **Tell Cydnie about the overflow** — it is a real
bug on two client sites and she may want to fix it before anyone follows a link from her
portfolio.

## 7c. The brief in the build folder, and where this build departs from it

`CLAUDE-CODE-BRIEF.md` arrived with `the-build-page-FINAL.html`. Both were sitting **inside
`the-build/`**, which is a deployed directory, so both were publicly reachable. They are in
`The Build page/files/` now. Do not put working documents in a served folder.

The brief says: **"Only `/the-build` may be created or modified. Every other file in this
repository is off limits."** It also says do not extract or use shared components, define the
page's tokens locally, and keep the sticky bottom bar.

**This build does not comply, on Cydnie's own instruction each time.** She asked, in order, to
publish the prices and repoint the home page's Build door so the two stopped disagreeing; to
add the links from the PDF across the whole site; and to rework the client section. Those are
site-wide by definition. Files touched outside `/the-build/`:

`assets/css/site.css`, `assets/js/site.js`, `index.html`, `about/index.html`, `tools/stamp.py`,
`tools/build_artifact.py`, `sitemap.xml`, `llms.txt`, `.gitignore`, plus new images under
`assets/img/work/` and `assets/img/mark-horiz-ink-*`.

The page is also built **on** the shared stylesheet rather than defining tokens locally, which
is the opposite of what the brief asks. That is a deliberate trade: a local token block would
have meant a second copy of the palette to keep in sync, and two of the bugs this page exposed
(the gauge inversion, the washed-out wordmark) were shared-stylesheet bugs that a scoped page
would have hidden rather than surfaced. **If the brief's scope lock still matters to someone,
this is the conversation to have, and it is not a small one.**

**Still unresolved from the brief:** it says to keep the sticky bottom bar. `site.css` says the
bar was removed because the brand guide forbids it, along with the nudge, the modal and the
exit intent. Those cannot both be right. The bar is currently **not** on the page.

## 8. Recreate the preview each session

**Everything below is now in `tools/preview/`, with its own README. Use that rather than
rebuilding it.** Two commands:

    export SP=<this session's scratchpad>
    sh tools/preview/sync.sh
    python3 tools/preview/serve.py "$SP/preview" 8791

That folder also holds the three harnesses session three had to write when the Claude preview
pane stopped responding: `_shot.html` for screenshots at a real viewport, `_test.html` for the
63-assertion interaction suite, `_probe.html` for measuring one thing. **Read
`tools/preview/README.md` before debugging anything visual** — it documents four traps that
each cost real time once, including the one where a programmatic `scrollTo` inside an iframe
does not fire a `scroll` event in headless Chrome and every scroll-driven behaviour therefore
looks broken when it is not.

The rest of this section is the reasoning behind those files.

The preview sandbox **cannot read `~/Desktop`**, so the server serves a mirror in the session
scratchpad, and **the scratchpad path changes every session.** `.claude/launch.json` is
gitignored for exactly that reason: it points at last session's path and is always stale.

Set `SP` to the new session's scratchpad, then:

- **`$SP/sync.sh`** — `rsync -a --delete` from `/Users/cydniebrown/Desktop/cydniejocelyn-v2/`
  into `$SP/preview/`, excluding `CydnieJocelyn-Site`, `cydniejocelyn`, `* copy`, `.git`,
  `.vercel` and `The Build page`. The excludes are not optional: without them rsync copies
  ~59GB of brand library and video into the scratchpad.
- **`$SP/serve.py`** — a `SimpleHTTPRequestHandler` bound to `$SP/preview` that adds
  `Cache-Control: no-store, max-age=0` in `end_headers`. **Not optional either.** Without it
  you debug a stale `site.js`. That cost an hour once.
- Write `.claude/launch.json` with `runtimeExecutable: "python3"` and
  `runtimeArgs: ["$SP/serve.py", "$SP/preview", "8787"]`, `port: 8787`, then `preview_start`.

**Run `sync.sh` after every edit**, and again after `build_artifact.py`. Nothing you change is
visible in the preview until you do.

`.gitignore` excludes the ~59GB of source material inside the project folder, the three built
artifacts, `.vercel`, and `.claude/`. Keep it that way.

### Screenshotting a live site

Headless Chrome is the only way to get a real page to disk here: the preview pane can render
one but cannot save it. Chrome **does not exit** after `--screenshot`, so background it, poll
for the file, then kill it, or the call hangs until the tool times out.

    CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    UA="Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 \
    (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
    ( "$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-first-run \
        --user-data-dir="$SP/cp" --window-size=393,852 --force-device-scale-factor=3 \
        --user-agent="$UA" --virtual-time-budget=12000 \
        --screenshot="$SP/out.png" "https://example.com/" >/dev/null 2>&1 ) &
    pid=$!; for i in $(seq 1 40); do [ -s "$SP/out.png" ] && sleep 2 && break; sleep 1; done
    kill $pid 2>/dev/null

393x852 at DPR 3 gives 1179x2556, which is an iPhone 15/16 Pro screen exactly. A fixed cookie
banner can be pushed out of frame by capturing taller (`--window-size=393,1150`) and cropping
the top 852. **Do not dismiss a consent banner to get a clean shot** — that is consenting on
her behalf, and it is not ours to do.

### Reading the boards and the marks

`PIL` and `numpy` are both available; ImageMagick and `cwebp` are not. Pillow writes WebP with
alpha (`exact=True`). The three brand boards are **pixel-identical apart from their screens**,
which is the trick that made every measurement in §6 possible: diff two boards and what differs
is the screen, what matches is the chassis. Thresholding fails on SRS, whose screenshot is
nearly as dark as the frame around it.

---

## 9. What is next, and one trap that just cost a deploy

### The Greece retreat page — BUILT. See §10.

Both drafts in `Greece Retreat/` were resolved and the page shipped. The `copy` was indeed the
later of the two and is what the page was built from. **The seat-count contradiction is
settled:** fifteen, all taken, waitlist open. `llms.txt` and the home page were corrected to
match rather than the other way round. The waitlist links are wired, including the two
`/1-Contact_Information` variants for pay-in-full and the six month plan.

Per the colour notes, **retreats is still the one page family allowed to run deeper than the
others**, and both pages use that: each opens deep, comes up for the practical middle, and goes
back down for the close.

### Working documents get served. Check `.vercelignore` first.

`vercel deploy` uploads the working directory, **not** what git tracks, and `.vercelignore` is
explicit rather than inherited. Two documents were live in production for several deploys:

- `the-build-page-FINAL.html` and `CLAUDE-CODE-BRIEF.md` sat inside `the-build/`, a route
  directory, and were reachable at `/the-build/…`.
- Moving them to `The Build page/files/` did **not** fix it. That folder was not in
  `.vercelignore` either, so `/The Build page/files/CLAUDE-CODE-BRIEF.md` kept returning 200.

Both folders are excluded now. **The rule: the same day a folder of working documents lands,
add it to `.vercelignore`, and never park one inside a route directory.** Verify with
`vercel curl "$URL/<path>"` and expect a 404 — plain `curl` cannot tell you anything while
Deployment Protection is on.

---

## 10. The two retreat pages

Built in session three from `Retreat drafts/retreats-visual-v2.html` and
`Greece Retreat/greece-v2 copy.html`. Both drafts define their own token block and their own
palette; **neither was used**. The pages are built on `site.css` in the shared chrome, the same
trade The Build made and for the same reason: a second copy of the palette is a second thing to
keep in sync, and a scoped page hides shared bugs instead of surfacing them.

### The captions were wrong in the drafts, and that is the important part

Both v2 drafts hotlinked `static.showit.com` URLs. Several of those frames are **Costa Rica
photographs captioned as Crete**, and the rest are mislabelled against each other:

| Draft caption | What the file actually is |
|---|---|
| "The coastline of western Crete" | Costa Rica |
| "The harbour at Chania" (`img_5366`) | the lounge at Armonia |
| "A trail above the village" (`img_5369`) | the stone house at Armonia |
| "A meal at the retreat" (`img_5367`) | the sauna interior |
| "Cretan ingredients" (`img_5370`) | the house at night |
| "The table set for dinner" (`img_5376`) | a window nook with plants |
| "The lounge" (`mk_09949`) | a second bedroom |
| "The pool" (`mk_00944`) | a plastered arch |

Every mapping on the shipped pages was checked against the actual pixels. **The rule this
page now follows: where a caption cannot be honoured by a real photograph, the figure is
dropped and the fact becomes prose.** That is why the Greece page has no picture of Chania
harbour, of Kera Beach, or of the gorge trails — there is no photograph of any of them. They
are rows in the place section instead. If she supplies real Crete landscape photography later,
those rows are where the figures go.

Three consequences worth keeping:

- **Nothing crosses between `assets/img/greece/` and `assets/img/retreats/`.** Greece is
  Armonia and Douliana. Retreats is Costa Rica and Kris. The split is enforced by
  `tools/retreat_images.py` having two tables and two destinations.
- **Kris's portrait is captioned "Costa Rica, April 2026"** on the Greece page, because it is,
  and neither host has been photographed in Crete yet.
- **`tools/retreat_images.py` and `PICK` in `build_artifact.py` are the same list.** The first
  pass generated the whole shortlist and shipped a subset, which left 3.5MB of frames on disk
  that no page pointed at, and `PICK` kept them looking alive. Add a row and a stem in the same
  commit, or do not add either.

### `tools/retreat_images.py`

Cuts every retreat photograph out of the source libraries. Re-runnable, idempotent, no
upscaling. Quality falls with width (82 / 76 / 70) because these two pages carry twenty
photographs between them and the wide variants alone ran over 4MB at a flat 82.

**Several Armonia sources are only 1000–1075px wide**, so the emitted widths are capped at the
source. That is why the gallery tiles top out at 1000w while the pool, which came from a
5917px original, goes to 1800.

**Kris is identified by her vest.** `DSC08832` and `DSC08962` both show a black tank printed
"Your Time Fitness · Sauk Centre MN", which is her company. That is how the portrait was picked
out of 127 unlabelled candids.

### The picture pass, and why the pool candids came off the Retreats page

The first build of `/retreats/` ran on the Costa Rica pool candids: the group with their hands
up in the hero, a hug, Kris on the deck, a jump. They are true and they all said the same
thing, and the hero in particular sold a holiday rather than the format.

Cydnie has 296 photographs in `Costa Rica copy/` and the best of them are not of people at all.
A third of that library is sea, sky and headland shot from the boat -- which is the picture the
whole brand is built from. The Retreats page now runs on those:

| Where | Frame | Why |
|---|---|---|
| Hero | `IMG_4352` | A headland across still water. A level surface with a far shore, which is the same picture the home page opens on, except she took this one on one of these weeks |
| Costa Rica, wide | `IMG_0784` | The pavilion, mats down, the group seated. What a morning actually looks like |
| Pair, left | `DSC09127` | Hands laying cards on a floor, one foot in frame. The board's own direction: from behind, above, or in fragment |
| Pair, right | `IMG_4900` | One woman walking out of the surf on her own. "Alone in a group of fifteen", literally |
| Full bleed | `e0a610b5-…` | Low tide holding the whole sky. The page's one unguarded moment, captioned with the evening it happened on |
| Greece card | `greece/dinner` | **Not** `greece/house`: that is the Greece page's own hero, and a card showing the same picture as the page it opens reads as a thumbnail |

The three figures each carry a line of prose now rather than a label, because the request was
storytelling and a caption that says "Costa Rica, April 2026" is a filename. The last-evening
band is the only place on this site that uses the sunset register at all; it is allowed there
because it is a photograph of a week that happened, dated, not an image of a feeling.

**`.hero--bright` is on Greece and not on Retreats.** It exists for a photograph that is bright
where the words are. The headland is already dark; with the bright scrim over it the left two
thirds went to near black and the picture was wasted. Measured on the shipped render, the worst
case behind the headline is 6.17:1 and everything below it is over 11:1.

### April 2027 has a map, not a photograph

There is no location yet, so there is nothing to photograph. A picture of somewhere it is not
would be the one dishonest thing on the page and an empty box is a hole in the layout. So the
card carries the contiguous United States, drawn by `tools/us_map.py`: about ninety border
points on a Lambert conformal conic, which is why the northern border curves rather than
running flat. Lake Michigan is cut out with `fill-rule: evenodd`, because without it Michigan
has no Lower Peninsula and that is the one omission a reader in Minnesota would notice.

**The marker is an open ring and that is the site's own motif.** The Fifteen mark on the home
page fills fourteen circles and leaves the fifteenth open, and the open one is the whole
argument. Here the same shape says the same thing about a location that has not been decided.
It is placed at 40.5N 95W, in the middle of the country, so it reads as "somewhere here" rather
than as a pin in a town nobody has been told about.

**The SVG is inlined into the page, and `us_map.py` does the inlining** between
`<!-- US-MAP:START -->` and `<!-- US-MAP:END -->`. An `<img src=".svg">` cannot be coloured or
animated from the stylesheet and this one is both, so the markup has to hold a copy of the
geometry; the copy is written by the script rather than pasted. Re-run the script, do not edit
the path.

One trap in it, and it cost a render: the textbook LCC formula gives y increasing north, and
screen y increases south. Getting that backwards draws a map that is upside down and still
looks vaguely plausible, which is worse than one that looks obviously wrong.

### The scroll motion, and what it is not

The guide's register is 8px, 400ms, once, no scale, stagger capped at 60ms. Nothing added here
leaves it:

- **Three `.par` targets** on the Retreats page -- the Greece card, the pavilion, the last
  evening -- using the engine that already existed, hard capped at 12px of travel. The two
  inside full-bleed bands ride on `.layer-band--par`, which oversizes the image to 118% and
  offsets it -9% so the box itself never moves and no edge can appear.
- **The map draws its border on entry**, once, 1400ms, and the resting state is the drawn one.
  Same rule as the waterline: a keyframe starting at a dashoffset of 1 would leave the country
  invisible for as long as the animation sat on its first frame. The ring fades in 900ms later.
- Everything else is the reveal classes that already existed.

Nothing loops. Nothing is scroll-scrubbed except the parallax, which was already here.

### The Greece rework: the page is a funnel now, not a document

The first build shipped every fact the retreat has, in order, in prose. Cydnie's read was
right: it was a long read with big pictures in it, and it did not take a buyer anywhere. The
rework is structural, not cosmetic.

**The order changed, and that is the conversion move.** The hosts block used to sit *after* the
booking band, where it could only reassure someone who had already decided. Trust is what a
woman buys before she buys a seat, so it is now above the price. And the four things that
actually stop a booking were nine-tenths of the way down inside a list of nine questions; they
are a picker directly above the figure now.

Order: hero → premise → the lane in → **the week, stepped** → who this is not for → the place →
the property → **the two of us** → included → **objections → the price** → getting there →
questions → the grounds → close.

**Four blocks were rebuilt rather than trimmed:**

| Was | Is | Why |
|---|---|---|
| The week: four paragraphs | **`.cond`, the home page's stepped section.** Five moments, pinned, advanced by the scroll | It was the longest unbroken block on the page, in the place a reader decides whether she wants the week at all |
| The place: a heading and five `<dl>` rows | **Four figures, then four disclosure rows** | A woman deciding on Crete wants to know how far the water is before she wants a paragraph about the water |
| The property: a heading, a wall, five tiles | **Four figures, a sixteen-tile rail, four disclosure rows** | Five tiles showed a sample of the house and left her to guess at the rest |
| Getting there: five `<dl>` rows | **`.trip`, five stops on one rule** | It is a sequence with dates on it, not a table of facts. The two things people get wrong -- the arrival time and the buffer night -- are stops, not a footnote |
| Questions: nine, one column | **Eight, two columns.** Four objections lifted out entirely | Nine in a stack was a second scroll at the point the page should be closing |

**Everything reuses machinery that was already here.** `initCondition` drives the week,
`initReversal` drives the objections, `initGallery` opens rail tiles as well as grid tiles.
The only new component is the rail.

### The rail, and why it does not auto-advance

`initRail` in `site.js`. The markup is a real overflow container with CSS scroll snapping, so
it works before any JS: a touch screen scrolls it natively, a keyboard tabs the tiles. The
script adds pointer dragging, two arrows, and the rule that reads position. `is-live` goes on
last, so the grab cursor and the arrows never appear before they do something.

**Cydnie asked for "scrolling loop/gallery" and this is the gallery.** "Nothing loops" is the
most cited rule in the handoff and a carousel that moves on its own is the plainest case of
breaking it. If she wants it to advance on its own that is a fourth deliberate override and
belongs in §4 beside the other three.

**Tiles are one height and the width follows the photograph.** Fixing the width and varying the
aspect gave three different caption heights across the rail, which reads as an accident rather
than a rhythm. One height means the tops and the captions line up and the right edge is ragged
because the pictures are different shapes.

**Fifteen of the sixteen tiles never load until she scrolls the rail.** They are lazy and they
sit off to the right, so a vertical read of the page fetches one of them. That is the point.
The test asserts on images within reach rather than on all of them.

### A figcaption was falling out of its own figure, site wide

`.layer-fig img` carried `height: 100%`, which was there so a picture filled a figure that a
grid row had stretched. Inside `.pair` that made a loop: the row was sized from the image and
the image was sized from the row, so the figure ended up **exactly as tall as its picture** and
its `<figcaption>` hung out of the bottom, over whatever came next. On the Greece page that was
the caption of the deck photograph printing on top of the excursion note.

The aspect ratio already gives every one of these a height, so nothing needed the 100%. It is
`height: auto` now. Swept afterward: 57 figures across all five pages, none with a caption
outside its figure.

`.pair--calm` also stopped 250px short of the right edge that the stats, the disclosure rows
and the rail all run to, because it was capped at `58rem` to keep it short. It runs the full
wrap now and the height comes out of a 4:3 ratio instead.

### No average rating, anywhere

The Costa Rica form got six responses. That was published two ways: **9.7 out of 10** in the
lede of the Costa Rica block on `/retreats/`, and an **`AggregateRating` of 4.8 from a
`ratingCount` of 6** in the home page's structured data, which is the same claim in the form
that surfaces as stars in a search result.

**Cydnie took both out on 26 August 2026** and her reasoning is the right one: six is not a
sample. One person moves it by two tenths, and printing it invites the arithmetic that makes
the week look worse than the women's own words do.

- The visible line now points at the quotes instead of scoring them.
- `llms.txt` says explicitly that no average is published and none should be quoted.
- The three individual `Review` entries on the home page **stay**. Each is a real, attributed
  quotation already visible on the page; the objection was to an average, not to testimony.

If a real sample ever exists, the figure goes back in **three places in the same commit**: the
retreats page, `llms.txt`, and an `aggregateRating` on `#retreat-service`. The raw responses
are in `CydnieJocelyn-Site/Reviews/`.

### No em dashes

Cydnie asked for them out. There were three, all `&mdash;`, all on the Greece page, all from
this session, and all three read fine as commas. **The sweep covers every shipped `.html`,
`.txt`, `.xml`, `.css` and `.js`, ignoring comments, and it is at zero.** Re-run it before
shipping copy:

    grep -rn '—\|&mdash;\|&#8212;' index.html about/ the-build/ retreats/ llms.txt

**En dashes are a different mark and three remain, all in `13&ndash;20 August 2027`.** That is
the correct mark for a date range and she did not ask about it. If she wants those gone too the
answer is "13 to 20 August 2027" in three places plus `llms.txt`.

### The two portraits were different sizes, and it was a real bug

`.rt-person--flip` set `order: 2` on the figure but left the columns at `4fr 8fr`, so reversing
the pair moved Kris's portrait into the **wide** column. She was drawn half again as big as
Cydnie. The flip modifier now reverses the column definition as well, and both images are
cropped to 4:5 by the stylesheet rather than relying on the two source files matching.
Measured on the shipped page: both 340 x 425.

**Cydnie's portrait is new to the site.** `cydnie-hero`, `cydnie-reading` and `cydnie-veil` are
all seated and all spoken for by the home and About pages. This one stands, three-quarter,
warm ground, which is the same shape as Kris's, out of the 154-frame brand shoot in
`CydnieJocelyn-Site/Branding copy/`.

### The hover highlight

`--hl` is a new role token, defined on `:root` and redefined per ground the same way `--ink`
and `--rule` are, so hover means one thing on Surface and on Fathom. It is a background wash
rather than a colour change, so nothing moves. Links get it as a wipe from the left in the
same 380ms their underline already uses, so the two read as one gesture.

### Melissa's video is a phone Short, and the poster proves it

`DrrP4hdw0lo` is 9:16, recorded on her phone in her car on the drive home. YouTube's
`maxresdefault` is that frame padded onto a 16:9 plate with a blurred fill, and using it would
have framed a phone selfie as a produced piece. `melissa-poster-405.webp` is the true frame,
centre-cropped out of the plate at `round(H*9/16)`, and `.rt-play` is `aspect-ratio: 9/16`.

There is **no `oardefault.jpg`** for this video; it 404s. `frame0.jpg` is the right aspect but
only 268px wide.

### The three new behaviours in `site.js`

All three follow §3's rules: nothing depends on `requestAnimationFrame`, on
`IntersectionObserver`, or on a CSS transition advancing.

- **`initVideo` (15).** `.rt-play` ships as an **anchor to the watch URL**, so with no JS it is
  a working link rather than a dead button. On click it swaps in a `youtube-nocookie` iframe.
  **Nothing is fetched from YouTube until she presses it.**
- **`initGallery` (16).** Builds the button inside each `.rt-shot`, the one lightbox for the
  page, and adds `is-live` only once both exist — so nothing on the page advertises an
  interaction that is not there. Escape, arrows and a focus cycle all work; the page behind is
  locked; focus returns to the tile. **The tile is passed into `open()` rather than read off
  `document.activeElement`**, because a click does not always leave focus on what was clicked
  and closing to `<body>` puts the reader back at the top of the page.
- **`initRail` (16b).** The property rail. See the section above.
- **`initCursor` (17).** A disc that follows the pointer and names what is under it: View,
  Play, Drag. Scoped to `[data-cursor]`, never a site-wide cursor replacement, and off for
  coarse pointers and for reduced motion. Every element that declares `data-cursor` also sets a
  real CSS cursor, so the meaning survives with JS off.

  **It is two elements and that is not decoration.** The outer one is moved by a direct style
  write, the inner one is scaled by a keyframe — the only two mechanisms §3 says always work.
  Put both on one element and the keyframe overwrites the position every frame and the disc
  sits in the corner.

### `.hero--bright`, and why the shared scrim was not enough

The shared `.hero-scrim` falls to `.06` opacity at 22% of the height, because the home page's
photograph is already dark through the middle. Both retreat heroes are bright exactly where the
words are — a pool at noon and a lit house against a dusk sky — and Surface type over open
water measured around 3:1. `.hero--bright` is the same two gradients, same construction, higher
floor. **Greece uses it; Retreats does not** -- see the picture pass above. Do not raise the
floor on the shared scrim instead: it would flatten the home page's photograph, which does not
need it.

### Held is spent once per page, and both pages spend it on the same thing

The status line. `.rt-status--full` is `--warm`, and it is the only Held element on either
page. **The hero's first action is deliberately not `.hero-go--paid`** — that class carries a
Held underline that marks the home page's one paid entry point, and neither retreat hero's
first action is a payment. One is an anchor, the other is a free waitlist.

Measured: 5.42:1 on Surface, 5.01:1 on Silt, 6.78:1 on Fathom. Every other new pairing on both
pages is between 4.80:1 and 14.93:1.

### The case-insensitive folder trap, which cost a real detour

`Retreats/` held the drafts. The new route directory is `retreats/`. **On macOS those are the
same directory**, so writing `retreats/index.html` put the new page inside the drafts folder,
and `git mv Retreats "Retreat drafts"` then carried both new pages away with it.

Worse, it was nearly a production bug: `.vercelignore` had `Retreats/` in it, and Vercel
uploads from that same case-insensitive filesystem, so the ignore could have taken the real
`/retreats/` page out of the deploy with no error anywhere.

**The drafts folder is `Retreat drafts/` now and `.vercelignore` names it.** The rule: never
give a working-document folder a name that differs from a route directory only by case.

### `sounding-popup.js` appeared, and wiring it is a brand decision, not a task

A self-contained site-wide popup for A Sounding landed at the repo root during session three,
with instructions in its own header to add `<script src="/sounding-popup.js" defer></script>`
before `</body>` on every page. It fires after 45 seconds, remembers a dismissal for 30 days,
and points at the correct 1:1 scheduling link.

**It is not wired to any page, deliberately.** `site.css` records that the sticky bar, the
slide-in nudge, **the modal** and the exit intent were all removed because the brand guide
forbids them, and §4 and §7c both turn on that. A timed interstitial is the same category. It
is also the one interaction on this site that would interrupt the About page, which is a
first-person account of postpartum depression, a child's diagnosis and a husband's stroke.

The file is committed and it deploys, and unreferenced it does nothing. **Ask Cydnie before
adding the script tag**, and if the answer is yes, ask whether About is in `SKIP_PATHS`.

### Two folders appeared mid-session, and one of them answers §7.2

`A Sounding/a-sounding-wireframe-v2.html` and `The Letters Page/` (a wireframe plus
`FlodeskPopup (1).tsx`) were not there at the start of session three and were not created by
it. Both are working documents in folders that were not in `.vercelignore`, so both would have
been served. **Both are excluded now.** Nothing was built from either; if those pages are
wanted, they are a new job.

**The Flodesk component is the missing half of §7.2.** That section records that the twelve
questions form is a native POST expecting a Flodesk endpoint, that the link list has no Flodesk
URL, and that it was left at `action="#"` rather than pointed at a guess. The component carries
a form id:

    FLODESK_FORM_ID = '6a8f553c9f30a024ac4f2a82'

That is a **popup embed**, not a POST endpoint, so the native form still cannot be pointed at
it as-is: the choice is a Flodesk-hosted form URL, or replacing the markup with their embed.
Worth asking her whether that id is the twelve questions list before wiring anything, because
a signup landing on the wrong list is still worse to unpick than one that never fired.

### Verifying these pages when the preview pane dies

The Browser pane went unresponsive partway through session three — `computer` timed out with
"the Browser pane is currently hidden" and would not come back. Headless Chrome is the fallback
and **a naive tall-window full-page capture does not work here**: `.hero { min-height: 100vh }`
means a 9600px window gives a 9600px hero.

Two throwaway harnesses were written into the served tree, and they are the reason anything
could be checked at all. Both are in the session scratchpad, not in the repo, and both must be
re-laid after every `sync.sh` because that runs `rsync --delete`:

- **`_shot.html?p=<path>&y=<px>&w=&h=`** — loads the page in a fixed-size iframe and walks the
  scroll down to `y` in 600px steps, so lazy images load and the scroll watcher fires. `100vh`
  resolves against the iframe, not the capture window. `&id=<element-id>` scrolls to an element
  instead.
- **`_test.html?p=<path>`** — drives the real page in an iframe and prints PASS/FAIL lines big
  enough to screenshot. It covers the gallery, the lightbox including focus and scroll lock,
  the cursor, the video facade, the FAQ, the reveals, overflow and image decoding. **38
  assertions, all passing** at the end of session three (19 on Retreats, 27 on Greece). Re-run it after touching `site.js`.

Three traps inside these harnesses, and the third is the expensive one:

1. A real pointer event targets the element under the cursor, so dispatching `pointermove` on
   `document` gives `e.target === document` and no `closest()` will ever match it.
2. Setting two `<details open>` in the same tick races their `toggle` events, so the
   exclusive-FAQ check has to open them one at a time.
3. **A programmatic `scrollTo` inside the iframe does not reliably fire a `scroll` event in
   headless Chrome.** Anything driven by the scroll handler -- the parallax, the depth gauge --
   therefore never runs, and the test reports a site bug that does not exist. Both harnesses
   now `dispatchEvent(new Event('scroll'))` after every step, which is what a real scroll does
   anyway. Before that patch the parallax read 0/3 driven; after it, 3/3.

Headless Chrome also reports **`prefers-reduced-motion: reduce` by default in some runs**, which
correctly turns the parallax and the pointer companion off. The test probes the media query and
asserts the right thing either way rather than assuming.

### What is deliberately not on these pages

- **No seats-remaining count anywhere.** "Full" is a fact; "3 seats left" is a countdown, and
  this brand does not run countdowns.
- **No sticky bar**, matching The Build and §7c.
- **Single occupancy: there is none, and the page says so three times.** The draft carried
  `TK, offered or not, and at what supplement`; Cydnie answered it on 26 August 2026. Crete is
  shared rooms only, two to a room, twin beds, en-suite, no supplement to buy a single. It is
  stated in the property rows, beside the price in the booking band, and as its own question in
  the FAQ and the FAQPage schema, plus `llms.txt`. **Four places. Change one, change all four.**
- **"Choose your path"** (`69fa372ccd31fefc073c5d28`) is unwired. It is the same URL as the
  branding page's "Lets talk", so which product it belongs to is not resolvable from the link
  list. Item 9 in §0. Same principle as the twelve questions form in §7.2: a form pointed at a
  guess is worse to unpick than a form that never fired.
- **The four Sauk Centre checkout links** stay unwired on her instruction. Item 10 in §0.

---

## 11. Session four: A Sounding, The Letters, and the popup

### The two pages

Both are built on the shared stylesheet and the shared chrome, the same way The Build and the
retreat pages are. Neither defines a local token block. New CSS is **section 26** (A Sounding)
and **section 27** (The Letters); there is no new JavaScript in `site.js` at all, because
between `.grid-12`, `.refuse`, `.faq`, `.quote`, `.wl-rule`, `.bd-cross` and the reveal classes
there was nothing either page needed that the site did not already have.

**`/a-sounding/` opens dark.** Home and About open dark because they open on the condition;
The Build opens light because its subject is the price. This page opens on the condition, so it
opens dark. That contrast is the argument and it is not a default. Its nav button is the only
one on the site that does not leave for the scheduler: it scrolls to `#book`, because sending a
reader off-site from the page making the argument loses the argument.

**`/the-letters/` is the thesis, drawn.** A full-bleed waterline runs across the page twice.
Above the first is light ground with the name, one sentence and one action. Between the two is
Fathom, carrying the argument and the writing. Below the second is light again for the exit.
The specimen letter is the only light object below the waterline, and that is the point: it is
the product. The two rules are `hr` elements rather than borders because on that page they are
content, not decoration.

**Copy still to replace:** the specimen is the wireframe's placeholder. It is in her voice but
it is not a letter she actually sent, and a specimen that was never mailed is a claim about the
product rather than evidence of it. Swap in a real one before launch.

### The popup: on four pages, off three

`sounding-popup.js` is wired. The script tag is on the home page, The Build, Retreats and The
Letters. It is **not** on three pages, and each of those is also named in `SKIP_PATHS` so the
exclusion survives someone pasting the tag onto a page later:

| Excluded | Why |
|---|---|
| `/a-sounding` | It exists to push a reader to that page. There it pushes her where she is. |
| `/about` | A first-person account of postpartum depression, a child's diagnosis and a husband's stroke. Nothing interrupts that to sell a $300 call. |
| `/retreats/greece` | A sold-out waitlist funnel with its own action. A consult modal competes with it. |

**The file as delivered would have rendered salmon pink.** Its CSS was written against the
wireframe's placeholder palette, where `--held-lift` was a near-white paper colour. On this site
`--held-lift` is `#CE908A`, the hover state for the warm note, and `--breath` is mint, so the
card came out pink with a mint border. It also asked for `--display`, `--body` and `--mono`,
which this site calls `--carved`, `--level` and `--utility`. All of that is repointed at the
real tokens, with literal hex behind each one so the modal survives the stylesheet failing.

Three other things were added to it: a **focus trap**, because `aria-modal="true"` is a promise
to assistive tech that focus is contained and Tab walked straight out of it; a **visibility
guard**, so a background tab does not count down and fire the moment a reader returns to it; and
a **560px breakpoint**, because at 375px the 38px title inside 38px of padding nearly touched
both edges.

### The Flodesk form, and the one thing that cannot be done from here

The form is a **popup**, confirmed live: it fires on its own configured trigger and its own copy
reads "One letter a week." The React component in `The Letters Page/` was translated into plain
JS because this site has no React in it. Same script, same form id, same double-load guard.

**Reopening it after a reader closes it is not possible from this repo.** Cydnie supplied
Flodesk's own embed snippet on 26 August and it is exactly what ships: same arguments, same
order, same `?v=` cache key, plus a guard against double loading. It also confirms the API
surface is one command, `fd('form', {formId})`. Four approaches were tried against a modal
confirmed hidden, and all four failed:

| Tried | Result |
|---|---|
| `fd('open', {formId})` | Not a command their dispatcher answers |
| Re-calling `fd('form', {formId})` | No effect. The trigger is evaluated once, at init. |
| Toggling classes on their markup | Open and closed are byte for byte identical in class list and every attribute; they swap an injected stylesheet instead |
| Clearing their dismissal storage, then retrying both | Still nothing |

**Only a full page load re-evaluates the trigger.** Measured, not assumed.

**Flodesk caps its own frequency, and it will look like a bug while you test.** It records a
dismissal in three places and then declines to show the popup at all:

    sessionStorage   fd-form-<id>-dismissed          this browsing session
    localStorage     fd-form-<id>-dismissed-count    across sessions
    cookie           fd-form-<id>-dismissed-count    same value

The good news is that the popup does not nag. The trap is that after a few test dismissals it
goes quiet and looks broken. Clear those three and reload. This is separate from, and stacks
with, the A Sounding popup's own `sd_pop_dismissed` key.

**The fix is one dashboard setting.** In Flodesk, set the form's display trigger to "on click"
and point it at `#letters-open`. Nothing in the repo changes when you do. Until then the button
tries anyway, checks 600ms later whether the modal actually became visible, and if it did not,
puts the email address on screen instead. A reader is never left holding a dead button.

### What was touched on the five shipped pages, and nothing else was

The instruction was to leave finished pages alone apart from the popup. Three things had to
happen anyway, because otherwise the new pages were orphaned and the site contradicted itself:

1. **Nav and footer repointing.** `/#questions` became `/the-letters/` and `/#sounding` became
   `/a-sounding/`, everywhere. Both were anchors into the home page.
2. **The popup script tag**, on three of them.
3. **The weekly copy fix**, in three sentences: the home page form's description, the home FAQ
   answer under "What if I am not ready to spend $300?", and one line on About.

The home page's `#questions` form was **not** touched beyond its description, and its hidden
`tag` field still reads `twelve-questions`. It is still `action="#"` and still dead. Now that
`/the-letters/` exists with a working list behind it, that form is redundant and the honest move
is to replace it with a link. That is a design change to a shipped page, so it is item 3 in §0
rather than something session four did unasked.

### Two shared-stylesheet bugs, one fixed narrowly and one reported

- **`.sd-panel` was invisible.** It was painted `var(--field)`, and on `.z-light` that resolves
  to `var(--surface)`, which is the ground it sits on. It is `#DCE4E1` now, the same one step
  off the light ground that `.z-silt` uses for its whole band.
- **`figure` keeps its browser default `margin: 0 40px` on `.quote`.** Every other figure in the
  stylesheet clears it: `.layer-fig`, `.retreat-fig`, `.story-fig figure`, `.rt-person figure`.
  `.quote` never did, so the home page's quote carousel is indented 40px on each side, which
  costs 80px of a 375px measure. **Fixed on `.sd-quote` only.** The one-line shared fix is
  `.quote { margin: 0 }` and it moves a shipped page, so it is item 14 in §0.

### The FAQ schema was drifting from the visible page

The wireframe's `FAQPage` block and its visible questions were written separately and had
already diverged: four of six answers differed, and two questions were worded differently.
Google wants those identical. The schema on `/a-sounding/` is now **generated from the markup**,
so the two cannot disagree. If you edit a question, regenerate rather than hand-editing both.

### The harness grew, and it had two bugs of its own

`_test.html` covers the new pages: **17 assertions on A Sounding, 15 on The Letters.** With the
existing 43 on Greece and 20 on Retreats that is **95, all passing.**

Both new-page runs failed at first, and neither was a site bug:

1. **`cursor: companion built` failed on A Sounding.** `initCursor()` returns early on a page
   with no `[data-cursor]` targets, which is every page that is not a gallery. The assertion was
   unguarded. It now checks whether the page declares any targets first.
2. **The whole run threw on The Letters.** The FAQ block indexed `det[0]` without checking the
   count, and that page has no questions. It took the run down before any of the page's own
   assertions executed. The block is guarded on the count now and the remainder of the suite
   was lifted into a `rest()` function so both branches reach it.

**The pane lies before it dies, and that is new.** Session three recorded that the preview pane
went unresponsive. Session four found the worse failure that comes first: **it returns wrong
answers while it is still answering.** Greece reported 41 pass / 2 fail on a page nothing had
touched, because an IntersectionObserver does not fire in a pane the compositor has stopped
drawing, so every reveal read as unrevealed. Headless Chrome, same URL, same second: 43 / 0.
Only afterwards did the pane start returning "the Browser pane is currently hidden".
`tools/preview/runsuite.sh` runs the suite headless and is the answer. **If the suite fails on a
page you did not touch, run it headless before you believe it.**

**A third trap, for whoever tests the popup next:** a selector of `[aria-label="Close"]` matches
the popup's own close button. Clicking it writes the 30-day dismissal into `localStorage`, and
the popup then silently declines to run on every page for a month. If it will not appear, run
`localStorage.removeItem('sd_pop_dismissed')` before concluding anything is broken.

**And one that is not ours:** a `serve.py` from an earlier session can still hold port 8791 and
answer from a scratchpad that no longer exists, so new pages 404 while the old ones return 200.
Check `lsof -nP -iTCP:8791 -sTCP:LISTEN` before debugging a route. Session four moved to 8814.

### Two more folders arrived after the session's instructions, and neither was built

Five working folders now sit in this root. **Every one of them is in `.vercelignore`**, and the
two that arrived during session four were excluded within a minute of appearing, because an
unexcluded folder here is a served folder and the build brief was once live at a guessable path.

| Folder | Arrived | State |
|---|---|---|
| `A Sounding/` | session three | **Built** as `/a-sounding/` |
| `The Letters Page/` | session three | **Built** as `/the-letters/` |
| `the questions/` | 26 Aug, 19:07 | Excluded, not built. See below. |
| `Privacy terms page/` | 26 Aug, 19:19 | Excluded, not built. See below. |

**`Privacy terms page/privacy-terms-copy-v1.md` is the answer to §7.3** and it is not a sketch:
privacy and terms in one document, both parts written, covering HoneyBook payments, Flodesk for
The Letters, Google Analytics, retreat health disclosures, the MakeWellness affiliate
relationship, intellectual property, a not-professional-advice clause, per-offer terms for A
Sounding, The Build and Retreats, limitation of liability, governing law and accessibility.

It was not built because building it was not asked for and because it carries decisions that are
hers, flagged in the file itself: the last-updated date is to be set **on launch day and not
before**, and the affiliate section is written for MakeWellness alone and expands or comes down
depending on that partnership.

**When it is built, it closes the cutover trap.** The footer of all seven pages links
`https://cydniejocelyn.com/privacy-policy` absolutely, which resolves to the OLD site today and
404s the moment the domain points here. The page has to exist at that path in this build, or a
redirect has to. The document also settles the other half of §7.3: **terms now exist.**

### `/thequestions` is a fourth page, and it was not built

`the questions/thequestions-wireframe-v2 (1).html` arrived at 19:07 on 26 August, after the
session's instructions were given. It is a QR destination for the GATHER event tables: someone
picks a numbered card, scans the code, and gets the other eleven questions on one screen. It is
`noindex` by design, its nav is stripped to the wordmark and one button, and it points its
second door at The Letters.

It was **excluded from the deploy immediately and not built**, because building it was not
asked for and it carries three open decisions of its own: which of three copy variants to use in
zone 6, whether the eyebrow swaps per event, and confirmation of the twelve questions as listed.
It also records three fixes needed on the **old** live page at `cydniejocelyn.com/thequestions`:
a typo in question 11, inconsistent casing, and the order running backwards.
