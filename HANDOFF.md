# Handoff — Cydnie Jocelyn, the resurfacing business

> ## READ SECTION 48 FIRST. It is at the end of this file.
>
> This file is five thousand lines and grows by a section per session, so the
> newest state is the furthest from the top. **Section 48 is the current state
> of the site**, written to be read cold, and it names the two other sections
> worth reading and in what order. Section 0 below was accurate on 28 August
> 2026 and several of its statements are now out of date, the deployment ones
> especially. Where section 0 and section 48 disagree, **48 is right.**
>
> The three things most likely to cost you if you do not know them:
> **a push to main is a live deploy in about four seconds**; **plain curl can
> no longer prove a deploy**, because the bot-protection page it may return
> has zero HTML comments and passes the usual check; and **`tools/seams.py`
> must be run after any change to a section's zone or order.**

**Rewritten at the end of session one, extended at the end of sessions two, three and four,
26 August 2026. Section 0 re-measured at the end of session twenty-three, 28 August 2026.**
Everything before the rewrite was appended in layers and several of those layers contradicted
each other, because decisions were reversed along the way. Where an old commit message and this
file disagree, **this file is right.** Where two parts of this file disagree, that is a bug:
fix it rather than working around it.

---

## 0. State as of 28 August 2026

### Picking this up cold

Everything is committed, pushed and deployed. Verified at the end of session
twenty-three, not assumed:

    git status --short          empty
    main vs origin/main         0 behind, 0 ahead   (1abe9ad)
    a fresh build changes       nothing
    local stamp vs live alias   b8862031 == b8862031
    interaction suite           439 pass / 0 fail
    analytics suite             141 pass / 0 fail

**There is no work in flight.** Nothing is half-done and nothing is waiting on
a decision from me. The four things still open are all Cydnie's, and she has
said she is handling the first two herself:

1. **Launch day and the DNS move.** Hers. When it happens, Deployment
   Protection comes off and the privacy policy's "Last updated" date changes
   in the same commit. §0 item 8.
2. **HSTS without `includeSubDomains` or `preload`.** Left conservative on
   purpose: it binds `clients.cydniejocelyn.com`, which HoneyBook operates,
   and it cannot be withdrawn quickly. §31.
3. **A dead `tools/sync.sh`** with a hardcoded path to a directory that no
   longer exists. Flagged rather than deleted. See the warning in the start
   sequence below.
4. **A dead `.hero { padding-bottom: var(--s-5); }`** at `site.css:4522` that
   has never applied — a later rule sets `padding-block` and wins. Its comment
   describes an effect it does not have. Deleting it is a one-line cleanup
   that was deliberately not bundled into an unrelated change.

The two reference documents for this build are `tools/analytics-reference.html`
(every GA4 event, where it fires, what it carries) and `tools/ux-review.html`
(nine measured interface frictions, all fixed). Both are excluded from the
deploy and both are also published as Artifacts.



**Everything below §1 is reference. This section is where a new session starts.
If this section and anything below it disagree, this section is right.**

**All nine pages are built, shipped and live.** Home, About,
**The Build** (`/the-build/`), **Retreats** (`/retreats/`), **Greece**
(`/retreats/greece/`), **A Sounding** (`/a-sounding/`), **The Letters**
(`/the-letters/`), **Privacy and terms** (`/privacy-policy/`) and
**The Questions** (`/thequestions/`). Every one returns 200 in production.

The last two were built on 28 August. `/privacy-policy/` closes the domain
cutover trap: the footer link was absolute, pointed at the OLD site, and would
have 404'd from every page the moment the domain moved. It is relative now on
all nine pages and the suite asserts it. `/thequestions/` is a QR destination
for the GATHER tables and is **noindex and deliberately out of `sitemap.xml`**:
the URL is event scoped and the page names the event. See §18.

**Sessions eleven through twenty-one were all on 28 August too**, and they were
polish rather than construction: a page-load audit (§19), mobile pacing (§20),
six mobile corrections (§21), a new photograph (§22), the home page colour arc
(§23), soft edges on every photograph (§24 to §26), an image audit (§27), SEO
and fifteen service locations (§28), and one overlap on About (§29).

**Sessions twenty-two and twenty-three, also 28 August, were wiring and
correction rather than pages.** In order: the Adobe font licence and GA4
(§30), a security pass that added the whole header set (§31), a deploy that
read the wrong `vercel.json` (§32), twelve GA4 events and a nine-point UX
review (§33), all nine of those fixed (§34), the font kit read as a restyle
and reverted (§35), the display scale cut too far (§36), rebalanced (§37),
iCloud corrupting a deploy (§38), four passes at one component's spacing
(§39 to §42), and finally the kit pulled, the Greece images halved on phones,
and real cookie consent (§43).

**If you read only one of those, read §41.** A scripted CSS edit computed a
splice bound with an unanchored `str.index` and silently duplicated 2,300
lines of `site.css`; it shipped twice, because duplicate CSS is legal and the
stale copies simply won. **Check the line count after any scripted edit to
that file.**

**Every nav target has a page behind it and every form goes somewhere real.**
Neither was true two days ago: The Letters was an anchor to a dead form on the home page,
A Sounding was a block on it, and the home page carried a `<form action="#">` that reloaded
the page and threw the address away. There is no `action="#"` and no `<form>` element
anywhere on the site now.

| | |
|---|---|
| Production | the newest **Ready** row in `vercel ls --prod` |
| `main` vs production | **In sync.** Verify rather than assume: `git status --short` should be empty and `git rev-parse --short HEAD origin/main` should print the same hash twice. To prove production matches the tree, hash a page both ways: `shasum index.html` against `vercel curl <prod>/ -s \| shasum`. |
| If in doubt | Run §2. Deploying twice costs nothing; shipping stale markup costs a session. |
| Interaction suite | **439 assertions, all passing** (82 Greece, 61 Retreats, 50 Home, 45 A Sounding, 45 The Letters, 41 Privacy, 39 About, 38 The Build, 38 The Questions). Six pages run by default; Home, About and The Build must be asked for by path. Run it against `dist/`, not the source: see §2 |
| Analytics suite | **141 assertions, all passing** across nine pages. `sh tools/preview/runga.sh "$SP" 8817`. Separate from the interaction suite because analytics is a sequence of events, not a state. |
| Analytics | **GA4 `G-KDB3GWPNHC`, twelve events, and it does not load until a reader accepts cookies.** `assets/js/consent.js` injects the tag; before consent there is no `gtag`, no `dataLayer` and no request to any Google domain. See §43 and `tools/analytics-reference.html`. |
| Speed | **TTFB 64ms, FCP 148ms, 11 requests, CLS 0** on the home page, measured on production. Greece on a phone is 1,479KB of images after §43, down from 1,947. |
| Third parties | **None on the critical path.** The Adobe kit was the only one and was removed in §43. Flodesk loads on `/the-letters/` only; YouTube is click-to-load on `/retreats/`. |
| Responsive audit | **9 pages clean at 320, 375, 430 and 768** |
| Mobile scroll | **Measured at 375x812, 390x844 and 360x800.** Home 20.9 screens, Greece 26.1. See §20 |
| Local SEO | **A LocalBusiness node with the same fifteen cities in `areaServed` on all eight indexable pages**, and one sentence in the footer. Asserted in the suite. See §28 |
| Photographs | **Every photographic plate has soft edges.** Seven things deliberately do not: see the table in §25 |
| Mobile menu | **128 contrast measurements, 0 failing** |
| Touch carousel | **19 on Retreats, 21 on Home, 0 failing** |
| Footer | **One footer, byte for byte on all nine pages.** Asserted in the suite. |

Do **not** write a deploy URL into this table. An earlier session did, and the very next
commit -- which was this file -- immediately made it wrong. `vercel ls --prod` is the answer
and it cannot go stale.

**Deployment Protection is ON for per-deploy URLs, and the stable alias is
NOT covered by it.** This was checked, not assumed:

    https://cydniejocelyn-v2.vercel.app          200, public, no login
    https://cydniejocelyn-v2-<hash>-...app       302 to vercel.com/login

So the alias is the link to send anybody, and it is also **already reachable
by the public and by crawlers.** `robots.txt` allows indexing; the canonical
on every page points at `cydniejocelyn.com`, so there is no duplicate-content
risk, but analytics on the alias counts as real traffic. Treat the alias as
live, because it is.

**The apex is still the old Showit site.** Verified live on 28 August:
`cydniejocelyn.com` answers from Showit behind Cloudflare. None of the
security headers, and none of this build, exist there until the DNS moves.
Cydnie is handling launch day and the DNS move herself. See §1.

### Start here, in this order

1. `export PATH="$HOME/.local/bin:$PATH"` — nothing works without it. §1.
2. Recreate the preview:

       export SP=<this session's scratchpad>
       sh tools/preview/sync.sh
       python3 tools/preview/serve.py "$SP/preview" 8814

   **Check the port first.** A `serve.py` from an earlier session can still be holding one and
   answering from a scratchpad that no longer exists, so new pages 404 while old ones return
   200. `lsof -nP -iTCP:8814 -sTCP:LISTEN` before you debug a single route. **Nothing is held
   at the end of session twenty-one.** Every port used across sessions eleven to
   twenty-one (8814, 8817, 8820 to 8831) was released deliberately. Do the same.

   **THERE ARE TWO FILES NAMED `sync.sh` AND ONE OF THEM IS DEAD.**
   `tools/preview/sync.sh` is the live one and derives its source from its own
   location. `tools/sync.sh` still has a hardcoded
   `/Users/cydniebrown/Desktop/Claude Code/cydniejocelyn-v2/` in it, a
   directory that no longer exists, and nothing references it. Running the
   wrong one rsyncs from nowhere and leaves you debugging an empty preview.

   **Re-run `sync.sh` after every edit.** Nothing you change is visible until you do, and it
   re-lays the six committed harnesses, which `rsync --delete` wipes.

   **IT ALSO WIPES ANY HARNESS YOU WRITE YOURSELF.** Measuring anything on this site means
   writing a throwaway probe into `$SP/preview/`, and the next `sync.sh` deletes it. Keep them
   in `$SP/harness/` and `cp` them back after every sync. This cost real time twice.

3. **Read `tools/preview/README.md` before debugging anything visual.** Six harnesses live in
   `tools/preview/` and each exists because something expensive happened once:

   | | |
   |---|---|
   | `runsuite.sh` | The **200-assertion** interaction suite, headless, six pages by default. Run after touching `site.js`, `site.css` or any footer. **Point it at `dist/`, not the source:** §2. |
   | `_audit.html` | Nine pages at four widths: overflow, tap targets, stacked buttons, carousel, tiny text. |
   | `_menu.html` | The open mobile menu, measured against its panel, at two scroll positions per page. |
   | `runcarousel.sh` | The reviews on a touch screen. **Must run with the coarse-pointer flags or it tests the desktop path and passes.** |
   | `_shot.html` | Screenshots at a real viewport. A tall window does not work here; `100vh` needs an iframe. |
   | `runga.sh` + `_ga.html` | The **141-assertion** analytics suite. Drives every tracked interaction on a page and asserts what came out. **It builds an opaque, on-screen iframe on purpose:** in an `opacity:.001` one, headless Chrome runs neither `scroll` nor `requestAnimationFrame`, and it dispatches its own scroll events because the preview pane fires none at all. §33. |
   | `_probe.html` | Scratch file for measuring one thing. |

4. **Run the suite headless, and believe it over the preview pane.** The pane returns *wrong
   answers* before it returns errors: it reported 41 of 43 on a page nothing had touched,
   because an IntersectionObserver does not fire in a pane the compositor has stopped drawing.
   It also suppresses `scroll` events on sub-scrollers entirely. If something fails on a page
   you did not touch, run it headless before you believe it.

5. Ship with §2. **The deploy comes out of `dist/`,** not the working directory, and
   `tools/ship.sh` is the whole sequence in one command. Two things about it,
   both of which took a production deploy down on 28 August:

   **Never put `--cwd dist` back on the deploy.** `vercel deploy --cwd dist`
   uploads `dist/` and then reads `vercel.json` from the SHELL's directory,
   which is the repo root. Those two files differ: `build.py` seals the CSP
   script hashes into the dist copy. That shipped a production CSP containing
   the literal string `__INLINE_SCRIPT_HASHES__`, which blocked every inline
   script on the site while the HTML, the CSS and the suite were all correct.
   `ship.sh` cds into `dist/` now and curls the deployed headers afterwards.
   §32.

   **This project is on the Desktop and the Desktop is synced to iCloud.**
   `build.py` wipes and recreates `dist/`, iCloud reads that as a conflict and
   writes `about 2`, `assets 3`, `sounding-popup 2.js` beside the real files.
   One of them vanished mid-scan and killed a deploy with a bare `ENOENT`.
   Both `build.py` and `ship.sh` sweep them, deliberately in two places,
   because iCloud can write a fresh one in the seconds between. §38.

### If you are measuring anything

Most of what these sessions got right came from measuring first, and most of what nearly went
wrong came from reasoning about CSS instead. Four things specific to this site:

- **On a phone, check the `clamp()` minimum before anything else.** Three
  separate components were reported as wrong on mobile in one session and all
  three had the same cause: the `vw` term sits below the minimum at 375, so
  every value on the phone is its floor and the scale collapses. The display
  type, the section rhythm and the story scroll each looked like a design
  problem and each was this. §36, §39.
- **`site.js` gets the bubble phase before anything loaded after it.** Any
  listener that needs to read state `site.js` is about to change has to be on
  capture. This cost three silently-wrong analytics events -- an inverted
  menu state, a `video_start` that never fired, and every desktop header
  click reported as a mobile menu. §33.
- **`--accent` is a RULES colour and fails as text on a dark ground.** It
  resolves to Meniscus on Fathom and Deepwater: measured 2.02:1 in the last
  instance. `--label` is the ground-aware token for emphasis. This has now
  happened three times; the suite asserts the measured contrast of every
  `em` inside a heading rather than the token name. §37.
- **Never compute a splice bound from an unanchored `str.index` in
  `site.css`.** Selectors in that file differ only by which media block they
  sit in and `index` cannot tell them apart. One bound landed before its own
  start and duplicated 2,300 lines, which shipped twice because duplicate CSS
  is legal and the later copy wins. Slice the media block first, or match a
  string unique in the whole file, and **check the line count afterwards.**
  §41.
- **Force reveals before measuring geometry.** `.r-up` uses `translateY`, which MOVES
  `getBoundingClientRect`. Add `no-tween` to the root and `is-in` to every
  `.r-up, .r-fade, .r-img, .split` first, or you are measuring an animation frame.
- **Use the coarse-pointer flags for anything touch.** They are in
  `tools/preview/runcarousel.sh:13`. Without them `matchMedia('(pointer: coarse)')` is false,
  the cursor companion builds and hover states apply: all three wrong for a phone.
- **Get element bounds from the DOM before sampling pixels near the top of the viewport.**
  The header is fixed and 68 to 92px tall, and it will silently be the thing you measure. §24.
- **Composite an alpha image over its real ground before computing SSIM.** Grayscale SSIM on
  an RGBA logo compares undefined RGB inside transparent pixels and returns 0.58 for a file
  that is actually 0.9998. §27.

### What changed in sessions eleven to twenty-one, in one table

Nothing in this stretch built a page. It was all correction, and every entry
is a thing that was measured wrong or looked right and was not.

| | |
|---|---|
| §19 | Comments stopped shipping (45% of the CSS), `immutable` caching, the duplicate wordmark, self-hosted fonts, 1MB of unreferenced assets. **The deploy moved to `dist/`.** |
| §20 | Mobile pacing: 3.28 screens of scroll removed sitewide. Two "fixes" refused because they make the phone worse. |
| §21 | The gauge off below 56rem, the seams eased, the hero's dark air, the hand's crop, the rise band larger. |
| §22 | A new re-diagnosis photograph, square, from two that arrived that morning. |
| §23 | The home page colour arc: it had **no middle**, Fathom or Surface and nothing between. Two contrast failures fell out of it. |
| §24 to §26 | Soft edges on every photographic plate, and the seven things excluded on purpose. |
| §27 | The images were already WebP. Re-encoding was worth 0.4%; the real win was missing `srcset` candidates, 55% off The Build on a phone. |
| §28 | SEO audit and fifteen service locations. Five pages had no LocalBusiness node. |
| §29 | The About rule was running through "I'm Cydnie." at 375x812. |

### A note on the section numbering below

§11 through §17 are labelled "session four" through "session nine". **They were one
continuous working session** across 26 and 27 August 2026, not six separate ones. Treat those
labels as work phases in order, not as calendar sessions. Everything in them is current.

### Where the recent work is

| Looking for | Go to |
|---|---|
| A Sounding and The Letters, how they were built | §11 |
| The A Sounding popup: which pages, and why three are excluded | §11 |
| Flodesk, and why the popup cannot be reopened from the page | §11, §12 |
| **The six HoneyBook form ids and what each one is** | §12 |
| The Costa Rica picture pass, and the image grade and crop tooling | §12 |
| **The single-column grid guard, and the blowout it prevents** | §13 |
| The phone pass: buttons, tap targets, micro labels | §13 |
| The mobile menu contrast bug | §14 |
| **The reviews carousel: two implementations, and three bugs inside the fix** | §15 |
| The one canonical footer, and the unboxed social marks | §16 |
| The held heading, and the seam rule for full-bleed photographs | §17 |
| **Privacy and terms, and the two things still open inside them** | §18 |
| The questions page, and what is event scoped on it | §18 |
| The page load audit, and the two suspicions it cleared | §19 |
| **Mobile vertical pacing, and the two fixes that would have hurt** | §20 |
| **The build step, why the deploy comes out of `dist/`, and the `immutable` guard** | §19, §2 |
| Six mobile corrections, and the gauge being off below 56rem | §21 |
| The hand photograph, and why the plate is square | §22 |
| **The home page colour arc, and `--accent` misused as a text colour** | §23 |
| **Mach bands: why a seam or an edge reads as a drawn line** | §21, §24 |
| Soft edges on photographs, and the seven things excluded from it | §25, §26 |
| **Images: why re-encoding was the wrong answer and candidates were the right one** | §27 |
| SEO, the fifteen locations, and why there are no city landing pages | §28 |
| The About head overlap, and why 375x812 is the width that fails | §29 |

**The bold rows will bite hardest if you do not read them:** they are the ones
where the correct-looking thing is wrong.

### Four traps this project keeps re-learning

Every one of these has cost a session at least once. They are in the section
notes too, collected here because a new session will hit them before it reads
that far.

1. **A linear gradient between two flat fields reads as a drawn line.** It is a
   Mach band: the eye exaggerates the break in the GRADIENT, not the colour.
   It has been reported twice as "there is a line here" and both times there
   was no border within a hundred pixels. Ease the ramp; do not lengthen it.
   §21, §24.
2. **`--accent` is Meniscus on a dark ground, and Meniscus is a rules colour.**
   Used as text it measures 2.0 to 2.3:1. Two live contrast failures came from
   this. `--label` or `--muted` are the text tokens. §23.
3. **Specificity: `.hdr.is-surfaced .btn` is (0,3,0).** Any single-class
   modifier on a header control loses to it silently and renders ink on ink.
   Three separate bugs. §18, and the note under `.has-menu .nav-links a`.
4. **`rsync --delete` in `tools/preview/sync.sh` wipes any harness you wrote
   into the scratchpad preview.** It re-lays the six committed ones and
   nothing else. Keep scratch harnesses somewhere else and copy them in after
   every sync.

### What is left, and every one of them is Cydnie's decision

| # | Waiting on Cydnie | Where |
|---|---|---|
| 1 | **Deployment Protection is ON.** One dashboard toggle. Nothing else blocks launch. | §1 |
| 2 | **The Letters collects into two systems and nothing reconciles them.** Every button goes to HoneyBook `6a19d46a`; the Flodesk popup on `/the-letters/` still fires and still collects. Cydnie chose to keep both on 26 August. **Export both and merge before any letter goes out**, and expect duplicates. | §11, §12 |
| 3 | **The specimen letter on `/the-letters/` was never sent.** It is the wireframe's placeholder, in her voice. A specimen that was never mailed is a claim about the product rather than evidence of it. Swap in a real one. | §11 |
| 4 | ~~"Choose your path" is unresolvable.~~ **CLOSED 26 August.** `69fa372c` is the **contact form**. It is the footer Contact on all seven pages and the ask block on Greece. | §12 |
| 5 | **The sticky bar.** Brief says keep, `site.css` says the guide forbids. Currently OFF. | §7c |
| 6 | **Mane Alchemist's mark is repainted** in its Foundation ink. A client's artwork, altered. | §6 |
| 7 | **Written permission** from Mane Alchemist, SRS Performance and SolyRey before launch. | §7.8 |
| 8 | ~~Privacy 404s at domain cutover.~~ **CLOSED 28 August.** Built at `/privacy-policy/`, one document, both parts, and the footer link is relative on all nine pages. **One thing is still open inside it: the last-updated date reads August 2026 and has to change on launch day, in the same commit that turns Deployment Protection off.** It is the one line on that page people check. | §18 |
| 9 | **Two client sites render broken on mobile.** Not ours, but she should know. | §7b2 |
| 10 | **The Sauk Centre retreat, 8 October 2026,** has four live checkout links and is on no page. She said leave it off. | §10 |
| 11 | ~~`/thequestions` is unbuilt.~~ **CLOSED 28 August.** Built, noindex, out of the sitemap. **The eyebrow, the `<title>` and the meta description are event scoped and have to be swapped per event**; they currently read GATHER / The Journey / Minneapolis. Nothing else on the page moves. | §18 |
| 12 | ~~`IvyPresto Display` is not self-hosted.~~ **CLOSED 28 August.** Cydnie supplied an Adobe Fonts kit, `jmh2wyp`. It carries **IvyJournal, not IvyPresto Display** — four faces, roman and bold, each with an italic. `--carved` names `ivyjournal` first now and the headlines are the licensed face on all nine pages. **If IvyPresto was what she meant, the fix is her Web Project, not this repo:** add the family there and change one token. | §30 |
| 13 | **Never verified:** a full keyboard pass and a real screen-reader pass. | §7.5 |
| 18 | **HSTS ships without `includeSubDomains` or `preload`, and there is no consent banner.** Both deliberate, both Cydnie's call, neither one a bug. | §31 |
| 19 | **The security headers do not exist until cutover.** The apex still answers from Showit. Verified live 28 August. | §31 |
| 21 | ~~Nine measured UX frictions.~~ **CLOSED 28 August. All nine fixed**, suite 356 → 385. Two halves deliberately left as Cydnie's call: the visible booking hand-off line, and redrawing the gauge. | §34 |
| 23 | ~~The hero headings are taller.~~ **CLOSED 28 August. Reverted.** The kit was the Adobe licence, not a restyle. `--carved` is Instrument Serif again and the hero is two lines. | §35 |
| 27 | ~~The story scroll does not pin below 768.~~ **REVERTED, and it should never have been done.** The pin is back at every width; the gap was closed by sizing the stage to its content instead. Two suite assertions now check the phone case. | §40 |
| 26 | **The home hero is 982px in an 812px viewport at 375**, because `.hero-path` stacks under the copy and adds 238px. Not a type problem and not fixed: laying it out horizontally, dropping it on mobile, or accepting it are all composition calls. | §36 |
| 24 | ~~The kit is linked on nine pages and the site uses none of its faces.~~ **CLOSED 28 August. Removed.** 243-323ms of render-blocking time for a font nothing used. | §43 |
| 24b | ~~No consent banner.~~ **CLOSED 28 August.** Nothing reaches Google before a reader accepts. | §43 |
| 24c | ~~The kit is linked on nine pages and the site uses none of its faces.~~ No font file is fetched from Adobe, but the kit stylesheet is render blocking and imports a second one. Keep it for the licence, or drop the link: Cydnie's call. | §35 |
| 25 | **The kit has `ivypresto-text`, not IvyPresto _Display_.** The brand board names Display, which is the cut drawn for headline sizes. Only matters if the licensed face is ever put on the site. | §35 |
| 22 | **site.js gets the bubble phase before analytics.js, always.** Anything reading state site.js is about to change must listen on capture. Cost three silently-wrong events in one session. | §33 |
| 20 | **`vercel deploy --cwd dist` reads vercel.json from the SHELL's directory, not from `--cwd`.** It shipped a broken CSP to production once. `ship.sh` cds into dist now and verifies the deployed headers. Never reintroduce `--cwd` on a deploy. | §32 |
| 14 | **`figure` default margin is unreset on `.quote`**, so the home page's quote carousel is indented 40px each side. **Verified still true on 28 August.** Fixed on `.sd-quote` only; the shared fix is one declaration but widens 14 slides across two live pages and touches the touch-carousel geometry, so it wants doing deliberately rather than in passing. | §11 |
| 15 | **Angela's quote is excerpted on `/a-sounding/`.** Her full review opens "From our very first coaching call", and that page argues it is not coaching. Confirm she is comfortable appearing there. | §11 |
| 16 | ~~The podcast.~~ **CLOSED 27 August.** Cydnie had all three references removed: the named link and the Spotify and Apple Podcasts icons, which both went to the same show. **It is still in `sameAs` on the home page and in `llms.txt`,** which is identity data rather than a link and was left deliberately. If the podcast is actually retired, those go too. | §16 |
| 17 | **The brief's scope lock** was overridden on her instruction, repeatedly. | §7c |
| 18 | **The Build is 5.84 screens to its first CTA**, the deepest on the site; every other page has one inside the first screen. Under 56rem its header CTA is inside the hamburger. Fixing it needs either new hero copy, which is under the freeze, or exposing the header CTA site wide, which is a design change. **Her call, not a bug.** | §20 |
| 19 | **The second hand photograph was not used.** `underwater hand.png` is still in `CydnieJocelyn-Site/Website Images/`. It is the brighter, more saturated of the two, measured at 0.44 against 0.12; the palette argued hard for the one that shipped. **If she prefers it, it is a two line swap.** | §22 |
| 20 | **`og/home.png` is a 91.6KB PNG.** A JPEG would be roughly half that with identical platform support. Never on a page's critical path, only fetched by crawlers, so it was left alone rather than risk social previews. | §27 |
| 21 | **Greece reports thirteen 10px spans at exactly 768px.** Verified pre-existing, not from any recent pass: the phone pass raises micro labels to 11px below 767.84px, so 768 gets the deliberate desktop size. A tablet is not a phone, so it was out of scope. **Worth a decision at some point.** | §20 |

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

**THE DEPLOY COMES OUT OF `dist/` NOW, NOT THE WORKING DIRECTORY.** That changed on
28 August. `tools/build.py` writes a comment-free copy of the site to `dist/` and the
source stays exactly as commented as it has always been. The comments are 45% of
`site.css`, and `site.css` is render blocking, so shipping them made every first-time
reader wait for 25KB of notes-to-ourselves before the page painted. See §19.

```
export PATH="$HOME/.local/bin:$PATH"
cd ~/Desktop/cydniejocelyn-v2

sh tools/ship.sh "$SP"                  # stamp, build dist/, run the suite AGAINST
                                        # dist/, then deploy dist/. One command.
git add -A && git commit -F <file>      # -F a file, NOT -m: see below
git push origin main
```

`ship.sh` is the whole sequence and nothing in it is optional. By hand it is:

```
python3 tools/stamp.py                  # ALWAYS, after editing site.css or site.js
                                        # it stamps all NINE pages; add any new one to it
python3 tools/build.py                  # writes dist/. REFUSES to run on a stale stamp
sh tools/preview/runsuite.sh "$SP" 8817 # 182 assertions, run against dist/, not the source
vercel deploy --prod --yes --cwd dist
```

**Run the suite against `dist/`, not against the working tree.** `dist/` is what
readers get, and it has been through a transformation the working tree has not.
`ship.sh` serves `dist/` on 8817 and points the suite at it for exactly this reason.

**`build.py` will refuse to build on a stale stamp, and that refusal is load bearing.**
`/assets/css/` and `/assets/js/` are `immutable` for a year in `vercel.json` now. That
is only safe because `stamp.py` puts a content hash in the URL, so a changed file is a
changed URL. A stale stamp plus `immutable` pins a returning reader to an old
stylesheet **and she never even revalidates it.** That is the exact failure the header
was reverted for once before; the difference now is that the stamp exists and the build
enforces it.

`tools/build_artifact.py` takes seven page names -- `home about build retreats greece
sounding letters` -- and is only needed when republishing an artifact, which nothing has done
since session one. It is not part of shipping the site, and it has not been extended to the
two pages built in session ten.

**Then verify, because "Ready" only means the build finished.** Deployment Protection makes
plain `curl` useless here: it returns 200 with a login page for every path including ones that
do not exist. Use `vercel curl`.

```
URL=<the deployment URL the deploy printed>
for p in / /about/ /the-build/ /retreats/ /retreats/greece/ /a-sounding/ /the-letters/; do
  printf "%-20s %s\n" "$p" "$(vercel curl "$URL$p" -s -o /dev/null -w '%{http_code}')"
done
```

Seven 200s. Then prove production is actually *this* tree rather than merely a recent one, by
hashing both sides:

```
shasum index.html | cut -c1-8
vercel curl "$URL/" -s | shasum | cut -c1-8
```

Two identical hashes means production is the working tree, byte for byte. A deploy that
succeeded and a deploy that shipped what you wrote are different claims.

**The working documents must stay 404.** Twelve folders in this repo are excluded in
`.vercelignore`: five media libraries totalling about 59GB, and **seven folders of working
documents** -- `The Build page/`, `Greece Retreat/`, `Retreat drafts/`, `A Sounding/`,
`The Letters Page/`, `the questions/` and `Privacy terms page/`. The build brief was once live
at a guessable path. **Add a folder to `.vercelignore` the same day it lands**, before doing
anything else with it. After any deploy that
added a folder, check:

```
vercel curl "$URL/HANDOFF.md" -s -o /dev/null -w '%{http_code}'      # must be 404
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

`stamp.py` regenerates that hash from the file contents. Current: `33b9e7a7`, and it changes every time you touch either file, so do not trust a hash written down here over `python3 tools/stamp.py`. Skip it and she
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
   aspect ratio so the swap does not shift the header. All seven pages use it. The old
   asset is still on disk and is no longer referenced.

Also fixed in passing: `about/index.html` closed its footer with `.ftr-base`, which is not a
class that exists. It is `.ftr-btm`.

**Navigation, all seven pages:** The Build · Retreats · The Letters · About, with **A Sounding**
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
3. **Privacy and terms. CLOSED 28 August, and the cutover trap with it.** Both are one
   document at `/privacy-policy/`, terms at `#terms`, built from
   `Privacy terms page/privacy-terms-copy-v1.md`.

   The link **was** absolute, `https://cydniejocelyn.com/privacy-policy`, and the note here
   used to say that was on purpose because it resolved both before and after cutover. That was
   half right and the dangerous half. It resolved to the **old site**, and the moment
   `cydniejocelyn.com` pointed at this build every one of those links would have 404'd. It is
   `/privacy-policy/` on all nine pages now, and two assertions in the suite fail if anyone
   makes it absolute again. See §18.
4. ~~**`IvyPresto Display` is not self-hosted.**~~ **CLOSED 28 August.** The kit arrived and it
   is **IvyJournal**. See §30. Nothing is self-hosted about it and nothing can be: Adobe's
   terms require serving from their CDN, so the carved face is the one third-party dependency
   on this site's first paint. Instrument Serif stays in the stack behind it.
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
| `6a185c26693e14802690e9f6` | **1:1 Session** | This is **A Sounding**. Every "Book one conversation" across the site, and the destination of the A Sounding popup. |
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
    python3 tools/preview/serve.py "$SP/preview" 8814   # check the port is free first

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
`height: auto` now. Swept afterward: 57 figures across the five pages that existed then, none with a caption
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
Check `lsof -nP -iTCP:<port> -sTCP:LISTEN` before debugging a route. 8791 was still held at the end of 27 August; 8814 is what everything since has used.

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

---

## 12. Session five: the retreat pages, and where the forms go

### The links, and the two ids that were finally resolved

Cydnie supplied both on 26 August 2026, and the second closes an open item
that had been unresolvable from the link list alone.

| Form | Where it goes |
|---|---|
| `cf_id/6a19d46a5cb4c5d7f86446a9` | **The Letters.** Every "Get the letters" on the site: the hero and the signup block on `/the-letters/`, and the home page block. |
| `cf_id/69fa372ccd31fefc073c5d28` | **Contact.** The footer of all seven pages, and the ask block on `/retreats/greece/`. |

`69fa372c` was filed on the link list as "Choose your path" against the same
URL as the branding page's "Lets talk", which is why §10 recorded that it was
not resolvable from the list and left it unwired. It is the contact form.
**Item 4 in §0 is closed.**

Both were checked and both return 200.

**The home page's dead form is gone.** It posted to `action="#"`, which
reloaded the page and lost the address, and it collected a first name and an
email with nowhere to send either. It is a link to the real form now. Two
fields fewer here is not a loss: the form on the other end asks for them, and
a signup that completes somewhere beats one that looks complete and is not.

**There is now no `action="#"` anywhere on the site.**

### Two lists, on purpose, and the bill comes later

The Letters collects in two places and this was decided rather than
overlooked. Every button goes to HoneyBook. The Flodesk popup on
`/the-letters/` still fires on its own trigger and still collects into
Flodesk. Cydnie expects the popup to convert better than the button and wants
both; the button also catches the reader who dismissed the popup, or whose
browser is already past Flodesk's dismissal cap.

**Nothing reconciles them and nothing on the page can.** Export both and
merge before any letter goes out, and expect duplicates from anyone who did
both. Item 2 in §0.

Flodesk is on `/the-letters/` and no other page. Checked, and worth keeping
that way: one popup on the page about the thing it sells is a signup, and the
same popup site wide is the pattern the guide forbids.

### The second picture pass on `/retreats/`

Cydnie's note was that two frames clashed with the site and one was too
vibrant. In both of the first two cases **the clash was the subject, not the
grade**, so they were replaced rather than reprocessed:

| Was | Why it went | Now |
|---|---|---|
| `cr-cards`, DSC09127 | Amber floorboards under low sun with a spread of rainbow oracle cards on them. Two saturated colour families the palette does not contain, in one frame. | `cr-floor`, DSC09043. The whole group on the pavilion floor among palms, most of them from behind. Green is the dominant mass, which sits beside Breath and Meniscus. |
| `cr-water`, IMG_4900 | A guest facing camera, posed, holding a coconut. The one frame on the page that read as stock. | `cr-surf`, IMG_4894. Two women from behind in the shallows. The coolest frame in the library. |

**The old `cr-water` alt text described a different photograph entirely** --
"walking alone out of the surf" against a picture of someone standing still
facing the lens. That is the same class of bug as the captions in the drafts
(§10), and it survived because the slug still said what the first pick meant.
**Slugs were renamed with the pictures** for exactly that reason.

**The sunset stays and is graded.** Cydnie likes the photograph and it is the
one unguarded thing on the page, so it was not replaced. It had been through
heavy HDR before it arrived and rendered as neon teal against neon orange.
`tools/retreat_images.py` now takes an optional grade, and `cr-dusk` is at
0.60 saturation with a 0.94 contrast pull. 0.75 was still hot; 0.50 went flat
and lost the light on the water. `cr-floor` takes a lighter 0.85, enough to
settle the floorboards and one coral vest without bleaching the palms.

The tool also grew a **crop**, because `.pair .layer-fig img` is
`aspect-ratio: 0.62/1` with `object-fit: cover` and DSC09043 is a 3:2 frame.
Dropped in raw, the viewport chose the crop and cut two women in half. The
framing is a decision in a file now.

### The ring, on the Retreats page

The same mark and the same movement as the home page, and **the geometry is
copied from `index.html` rather than re-derived**, so the two cannot drift.
`initFifteen()` finds it by class and needed no change at all.

It sits inside the left column, under "Fifteen." and its rule, because that
column was otherwise empty for the height of the copy beside it and the ring
is the picture of the word above it. Two things it needs that the home page
does not: **Meniscus rather than Breath**, since Breath on Silt is nearly
invisible, and a **15rem cap**, since unconstrained it runs to 22rem in the
middle of a wide page and starts reading as a logo.

### The questions stopped being a list

Seven accordions in one stack read as a form to be worked through, which is
the opposite of what that page argues. They are in **two movements** now, in
the order the worry actually arrives: whether the week is for her at all,
and then, only once that is settled, what it costs and what has to be
arranged. Each movement opens with **one line of prose**, not a second and
third eyebrow, which would have turned the grouping back into a list.

The questions themselves are unchanged, still exclusive-open, and **the
FAQPage schema is generated from the markup** as on A Sounding. It had already
drifted: six entries in the schema against seven on the page, with different
wording. Edit a question, regenerate; do not hand-edit both.

One answer linked "A Sounding" to `/the-build/`, from before that page
existed. Fixed.

### The ask block on Greece

Directly after the questions, because that is where the one she still has
actually surfaces: a page of answers is also a list of things that did not
answer her. **It is not a second door to the retreat** -- the waitlist is the
action and it is stated three times already -- so it is one button to the
contact form and one quiet link back to the waitlist.

It says who replies and roughly when, because "get in touch" that says
neither is the thing this brand refuses everywhere else.

Silt, so it separates from the light FAQ above without going to depth. The
section under it is a full-bleed photograph and still declares no `--from`,
which is correct: a photograph edge to edge is its own transition.

### The suite is 109 now

43 Greece plus 4, 20 Retreats plus 7, 17 A Sounding plus 1, 15 The Letters
plus 2. Run it headless (`tools/preview/runsuite.sh`); the pane returns wrong
answers before it returns errors. See §11.

---

## 13. Session six: the phone pass, and the bug that was hiding behind it

### The grid blowout, which is the important one

`.rt-video` was a bare `display: grid` below 48rem. **A grid with no
`grid-template-columns` gets one implicit column, and an implicit column is
sized `auto`, which resolves to max-content.** A max-content track does not
shrink to its container; it grows to whatever the widest thing inside it
wants to be and takes the whole subtree with it.

The quote carousel lives inside that grid. Its track is five 300px slides and
four 32px gaps, so its max-content is **2028px**. On a 375px phone the entire
Costa Rica block was laid out 2028px wide. Two of the five reviews sat off
the side of the screen where no swipe could reach them, and the section
rendered as most of a screen of empty dark. That is both of the things
Cydnie reported: "the reviews are blank for two swipes" and the dead space in
her screenshot. One cause.

**`body { overflow-x: hidden }` is why it survived three sessions.** It clips
the evidence, so every check for horizontal scrolling came back clean while
the layout underneath was five times too wide.

The fix is `grid-template-columns: minmax(0, 1fr)` on every single-column
grid: the same one column, allowed to be smaller than its contents. The list
is in **section 5** of `site.css` with the reasoning above it. **If you add a
grid that holds a carousel, a rail, a long unbroken string or a wide table,
put it in that list.** The audit checks for it.

### Section 28 of `site.css` is the phone pass, and it is at the foot on purpose

These are overrides, and an override that loses to source order is not an
override. The first draft of that block was written up beside the layout
rules and **silently lost three of its five fixes.** It has two breakpoints
and they mean different things: `47.99rem` is anything a thumb drives,
`33.99rem` is a phone specifically. Tap targets run wider still, to
`63.99rem`, because a tablet at 1024 is also a thumb.

What it fixes:

- **Stacked buttons of different widths.** The Greece booking pair came out
  295px and 309px, one above the other. In a group they are now the width of
  the column, capped at 26rem so a stacked button at 767px does not run the
  full 690px and stop being a button.
- **The carousel bar ran 21px off the screen.** Two 44px arrows, one 24px dot
  per quote and the gaps came to more than the 335px of column there is at
  375. That was the entire horizontal scroll the home page had. The dots take
  the slack and wrap; the arrows stay at the ends.
- **Free-standing links shorter than a fingertip.** Links inside `.actions`
  and the three practice areas are controls and get 44px. **Inline links in
  prose are deliberately untouched.**
- **10px micro labels**, raised to 11px on phones only.

### `_audit.html`, and why it earns its place

Seven pages at four widths, checking eight things. It found all of the above
and it is the reason "the entire site needs to be mobile ready" is a
checkable claim rather than an opinion. See `tools/preview/README.md` for the
four false positives it knows about, each of which would otherwise report a
deliberate decision as a bug.

**Current state: 7 of 7 pages clean at 320, 375, 430 and 768.** At 1024 it
still reports inline links under 44px, which is correct and not a defect:
that is a desktop with a mouse.

### The Retreats page, on Cydnie's three notes

**The ring was stacked and the section was lopsided.** At 15rem under the
heading it ran the left column 460px tall against 320px of copy on the right,
which left a hole in the middle of the section and put the paragraph visibly
above the mark it belongs to. It is on its side now at 8.5rem with the
caption beside it, and the two columns land within a line of each other.

**The bottom half was five consecutive sections on one frame:** small label,
large heading, rule, body in the right hand column. On a phone, where the
columns collapse, five of those in sequence is a list rather than a page.
Three changes:

1. **Terms folded into the questions**, which is now one section in three
   movements: what you are agreeing to, then whether the week is for you,
   then what it costs. Terms lead, because a non-refundable deposit that
   surfaces after the decision reads as a trap however plainly it is written.
   Inside a movement they are stacked rows rather than three columns; at
   130px per track the copy broke to seven short lines.
2. **The private block dropped the section frame** for a compact aside. The
   change of frame is what makes it a beat instead of another entry.
3. **Connective leads** on the refusals and the holds blocks, so the argument
   travels rather than restarting.

Five headed sections became four, one of which no longer looks like the
others. The FAQPage schema is regenerated from the markup, as on A Sounding.

### One accessibility fix found by the sweep

The five steps in the Greece journey list were `h4` under an `h2`, skipping a
level, which a screen reader reads as a missing section. They are `h3` now
and the selector followed the markup.

### The six form ids, and the one that got swapped

Six HoneyBook forms are in play and several differ only in their first few
characters. **Rewriting the private block on 26 August swapped `69fa33ac` for
`69fa372c`,** which pointed a private retreat inquiry at the general contact
mailbox and demoted its button to a link. Nothing caught it: the link still
worked, still returned 200, and still looked right on the page. Restored the
same day, and the suite pins every id now.

| id | What it is | Where |
|---|---|---|
| `69fa33ac59c6a6842e88b725` | Private retreat inquiry | `/retreats/#private` |
| `69fa372ccd31fefc073c5d28` | Contact | Footer of all seven, and the Greece ask block |
| `69fa3c69e63a7a4c9bb354f1` | April 2027 pre-registration | `/retreats/`, twice |
| `6a19d46a5cb4c5d7f86446a9` | The Letters | Every "Get the letters" |
| `6a21d07b6dcfbe3d85c663b6` | Greece waitlist, paying in full | Home, `/retreats/`, Greece |
| `6a21d63a1b6caddcac951777` | Greece waitlist, six month plan | Greece booking band |

**Change a destination on purpose, change it in `_test.html` in the same
commit.** An unknown id now fails the suite, which is how the sixth one above
was found: it was on the page and in nobody's list.

**Nothing was removed from the Greece page, but three of its waitlist
controls did not reach the waitlist.** The hero, the ask block and the close
all said "Join the waitlist" and all three were `#booking` anchors: they
scrolled to the payment plans and stopped. The home page and `/retreats/` had
been linking straight out to `public/6a21d07b6dcfbe3d85c663b6` all along;
Greece was the only page where that plain link did not exist. Cydnie supplied
the URL on 26 August and all three are links out now.

The booking band keeps both payment plans, because choosing one is a real
choice and the bare form does not ask. **Open question:** the bare link and
the "paying in full" button are the same form id, so a reader who takes the
plain link is on the pay-in-full record without being asked. Cydnie may want
those labels revisited. The suite asserts three plain links, both plan forms,
and that no control saying "waitlist" is left as a scroll anchor.

---

## 14. Session seven: three quarters of the mobile menu was invisible

Cydnie reported that some menu items were not readable "depending on what
page we're on". They were not readable depending on **where she had scrolled
to when she opened it**, which is why it looked page-specific.

### One cause, two failures

`.hdr::before` is the bar's own background and it is `opacity: 0` until the
header is `.is-stuck`. At the **top** of a page that opens light, The Build
and The Letters, the header is already `.is-surfaced` and not yet stuck. So
every rule that inverts the chrome for a light bar has fired, and the light
bar it inverted for has not been painted. Open the menu and the dark panel is
the only thing behind any of it.

1. **Three of the four nav links, contrast 1.00.**
   `.hdr.is-surfaced .nav-links a { color: var(--fathom) }` computes (0,3,1);
   `.has-menu .nav-links a { color: var(--muted) }` computes (0,2,1). The
   first wins on specificity wherever it sits in the file, so the panel drew
   Fathom on Fathom. Not dim. Gone.

   **The current page survived by accident.** Its
   `[aria-current="page"]` rule also computes (0,3,1), ties, and comes later
   in the file. So the reader saw exactly one legible item: the page she was
   already on.

2. **The wordmark and the close toggle, invisible in the same state.** A dark
   rectangle with no mark and no visible way out.

The A Sounding button was already patched for exactly this, with the comment
"the panel is its own dark ground, so it does not invert with the bar". That
comment was right and was only ever applied to the button.

### The fix

Four rules, all inside the mobile media query, all at (0,4,x) or better so
they win outright:

    .hdr.is-surfaced .nav-menu .nav-links a                     --muted
    .hdr.is-surfaced .nav-menu .nav-links a[aria-current]       --breath
    .menu-open .hdr.is-surfaced .brand-mark--light              display:block
    .menu-open .hdr.is-surfaced .nav-toggle                     --ink

**Nothing on a desktop changes**; the whole block is `max-width: 55.99rem`.

### `_menu.html`

Seven pages at two scroll stops, measuring every item in the open panel
against the panel behind it. **112 measurements, 0 failing**, minimum
9.62:1. Testing only one scroll position would have missed the wordmark
entirely, which is the trap worth remembering: on this site the header has
four states, and `surfaced` without `stuck` is the one nobody thinks to
check.

---

## 15. The reviews carousel has two implementations now

On a mouse it drags a transform under the pointer and snaps on release. That
is right for a mouse: there is no competing gesture, and one to one tracking
feels like handling the thing. **None of that changed.**

On a touch screen it was wrong in a way that could not be tuned out.
`pointerdown` captured the pointer and `pointermove` moved the track by raw
`dx` **with no axis lock**, so a vertical flick that began anywhere on a
review dragged it sideways by however far the thumb wandered while the page
scrolled underneath. Then `touch-action: pan-y` did its job, the browser
claimed the gesture as a scroll and fired `pointercancel`, and the release
handler animated the track back. Jerk, then snap, every time you scrolled
past the section.

**On a coarse pointer none of that runs now.** `site.js` sets `q-native`, the
view becomes a real horizontal scroller with CSS scroll snapping, and the
browser owns the gesture: it picks the axis, it carries the momentum, and it
cannot fight itself. The JS only listens, to keep the dots and the dimming in
step. The whole fork is one `matchMedia("(pointer: coarse)")` and a class.

### Three things that were wrong inside the fix

Worth reading, because two of them would have shipped looking fine.

1. **`offsetLeft` is relative to the nearest positioned ancestor, not to the
   scroller.** Nothing between a slide and `.wrap` is positioned, so every
   scroll target came back measured from the wrap and was about 60px out. The
   arrows scrolled to not-quite-a-slide and the snap dragged it the rest of
   the way, which looked like the carousel arguing with itself. It measures
   from rectangles now.
2. **The scroll sync threw its work into `requestAnimationFrame` behind a
   `pending` guard.** rAF does not tick in a frame the compositor has stopped
   drawing: a background tab, an offscreen iframe, a device saving power. The
   guard then stayed true and the dots stopped following the scroll
   permanently. There is a timer behind rAF now, whichever arrives first
   wins. **This is the kind of bug that only appears in the conditions nobody
   tests in**, and it was only found because the harness itself runs in one
   of them.
3. **Trailing padding on a flex scroll container is not reliably counted in
   `scrollWidth`.** The scroller ran out before the last review reached the
   middle and it sat about 19px right of centre. The leading side is padding;
   the trailing side is a real spacer element, which is always counted.

### Verifying it

`tools/preview/runcarousel.sh`. **It must run with a coarse pointer or it
tests the desktop path and passes.** See `tools/preview/README.md` for the
flags and for the two things an offscreen frame will not do.

---

## 16. Session eight: one footer instead of seven

The footer was different on every page, and not subtly:

| | |
|---|---|
| "Questions" | Five different targets. `#faq` on home, `/#faq` on About (which is the home page's FAQ, from a page that has none), `/the-build/#faq`, `/a-sounding/#faq` on two pages. |
| "Client work" | A same-page anchor on home, a cross-page one everywhere else. |
| Third slot, second column | Questions, or Greece 2027, or Costa Rica 2026, depending where you stood. |
| Socials | The home page only. Six other pages had none. |
| The Letters | In the footer of six pages and **missing from the home page**, which had the podcast in its place. |

There is one footer now, byte for byte identical on all seven apart from the
asset prefix, and **the suite asserts the whole link list in order** on every
page. Move it in one place and the other six fail.

**"Questions" is gone rather than pinned to one target.** Every page that has
questions answers them in its own body, and a footer link that lands
somewhere different depending on the page you left is worse than no footer
link at all.

**The podcast is gone, all three of it.** The named link and the Spotify and
Apple Podcasts icons, which both pointed at the same show. Cydnie's call on
27 August, and it closes item 16 in §0. It is **still in `sameAs` on the home
page and in `llms.txt`**: that is identity data rather than a link, and
"remove it from the footer" is not the same claim as "this podcast does not
exist". If it is actually retired, those two go too.

### The social marks came out of their boxes

They were 44px circles with a hairline each. On a phone that is four more
rectangles in a footer that already has plenty, and the borders were
separating things that space had already separated. They read as buttons in a
block where nothing else is a button.

The mark is the mark now. The tap target is still 44px, made of space rather
than drawn, and hover moves the icon to full ink instead of lighting a box.

**No horizontal gap between them, and that is deliberate.** The Elsewhere
column is about 192px at 1280 and four 44px targets are 176px of it, so any
gap at all wrapped them three-and-one, which looks like a bug in a block
whose whole job is to look settled. The separation is inside the targets: a
21px mark centred in 44px leaves 23px between marks, more air than the 2rem
gap around the old circles ever gave them. A negative margin pulls the first
mark back into line with the type above it.

On a phone the socials span both columns rather than sitting alone in a
half-width cell with the icons wrapping two and two, and the footer's top
padding drops from 6rem to 3rem, which was a screen and a half of nothing.

---

## 17. Session nine: a held heading, and a white line

### The questions hold their heading now

Grouping the questions into movements in session five helped and did not
finish the job: it was still a long right hand column with a heading that
scrolled away at the top of it, so from the second question onward you were
reading an unlabelled list.

`grid-12--hold` was already in the stylesheet, holding the heading column on
the three longest About sections. **Before you book** is the longest column on
the Retreats page, three terms and seven questions, and it uses the same
class now. One class, no new CSS, and the heading stays on the left while the
movements travel past it.

Measured: the heading holds at 144px from the top of the viewport for the
first ~1100px of the section and releases as the section ends, which is what
`position: sticky` inside a container does and what the About sections do.
**Above 56rem only.** Below that the columns are stacked and there is nothing
to hold against.

### The white line under the Greece ask block

The ask block is Silt `#DCE4E1`. The photograph section under it was Surface
`#E7ECE8` **with its own top padding**, so between the two there was a hard
edge and then a strip of a second, lighter near-white before the picture
started. That strip was the white line.

The note previously sitting on that section said a full bleed photograph is
its own transition and needs no `--from` seam. **That is true only when the
photograph starts at the section's edge.** With padding above it, the padding
is the transition, and a padding strip in a colour that appears nowhere else
on the page is a seam drawn badly.

The photograph section is Silt now, the same ground as the block above it, so
nothing changes colour until the picture does. The close below it seams
`--from:#DCE4E1` rather than `var(--surface)`, because that is the ground
actually above it now.

**The general rule, since this is the second time it has bitten:** a section
whose first painted thing is a full bleed image can skip the seam. A section
with padding before the image cannot, and must either carry the ground above
it or declare a `--from` that matches it.

---

## 18. Session ten: the two pages that were sitting in folders

Both wireframes had been in the root for two days, both excluded from the
deploy on sight, and neither built. They are built now, and the site is nine
pages.

### `/privacy-policy/`, and the trap it closes

Every page's footer linked **`https://cydniejocelyn.com/privacy-policy`**,
absolute. The note in §7.3 defended that: it resolves today and it resolves
after the domain cuts over. The first half was true. The second was exactly
backwards.

That absolute URL resolves to the **old site**, which is what is answering
`cydniejocelyn.com` right now. The instant the domain points at this build,
that path 404s unless the page exists here, and it did not. So the footer
link on all seven pages was a live 404 scheduled for cutover day, sitting
behind a note explaining why it was safe.

The fix is both halves: the page exists, and the link is **relative**,
`/privacy-policy/`, on all nine pages. Two assertions in the suite fail if
anyone makes it absolute again.

**Terms is the same page, at `#terms`.** The copy deck wrote privacy and
terms as one document and that is how it shipped. Two files would drift
apart the first time one of them changed. The footer carries both links and
they both land on this page.

### What is still open on it, and it is one line

**The date reads "Last updated: August 2026" and it has to change on launch
day, not before.** That is FLAG one of four in the copy deck and it is the
only one still open. It is the one line on that page anybody checks. Change
it in the same commit that turns Deployment Protection off.

The other three FLAGs are resolved:

| FLAG | Resolution |
|---|---|
| Retreat minimum, "eight to ten" | **Eight.** Cydnie's call, 28 August. A published minimum has to be one number she can hold herself to, and eight is the one where a retreat at eight or nine runs rather than being cancelled into credits. |
| Affiliate section, MakeWellness only | Shipped as written. There is no favourites page yet. If one is built the section expands; if the partnership ends it comes down the same day. |
| Travel insurance questionnaire | Shipped as written. Recommended coverage plus a signed acknowledgment, which is a better position than a requirement nobody could verify. |

**Eight is now a published number and it lives in exactly two places**: this
page and `llms.txt`. Fifteen, the cap, lives in six. If either moves, it
moves in all of them in one commit.

### It runs light from top to bottom, and that is the argument

Every other page uses the depth arc to make a case. This one is a reference
document somebody opens because they are looking for a single sentence, and
a ground that changes under them while they scan for it is the arc
performing on a page with nothing to perform. Silt for the title block,
Surface for the document, and the header inverts on its own because
`initHeader()` watches for `.z-light` and `.z-silt`.

Body copy is **1rem, not the site's 1.125rem**, and the measure is 40rem
rather than the 34rem `--measure`. Four thousand words of terms at the
reading size the rest of the site uses is a wall, and a 34rem measure breaks
the numbered obligations every six words.

**The contents is eight entries, not twenty eight.** A list of every heading
is not an index, it is the document again in smaller type. Above 56rem it is
a sticky sidebar. Below it, it goes to **two columns**: ten links at the
44px tap target the audit enforces is 450px of index before the first
sentence, on a page opened to find one sentence. Two columns makes that five
rows.

### `/thequestions/`, the QR destination

Someone at a GATHER table picked a numbered card, scanned the code, and is
standing there holding a phone. One screen, one thread, one action. Built
from `the questions/thequestions-wireframe-v2 (1).html`.

**Three things about it depart from the rest of the site and each is on
purpose.**

**1. It is `noindex` and it is deliberately not in `sitemap.xml`.** The URL
is event scoped rather than permanent and the page names the event, so it
should not be what someone finds when they search her. `follow` stays: the
links out are to real pages and there is no reason to strand them.

**2. The header is bare.** `.hdr--bare` is the wordmark and the one button,
at every width, with no `.nav-toggle`. The shared header collapses under
56rem by putting the A Sounding button **inside** the panel behind the two
bar mark, which is right on a page someone is reading and wrong on a page
whose only job is one tap. `initNav()` returns early without a toggle, so
nothing had to be told about this. The five item nav lives in the footer, so
there is a single forward path and still no dead end.

**3. It is light from top to bottom,** same reasoning as the privacy page: a
reader with thirty seconds in a lit room does not earn a rise by scrolling.
Sections are told apart by a hairline, not by alternating grounds.

### Three fixes carried in from the old live page

These are why the list of twelve is worth reading twice before editing it.

| | |
|---|---|
| Question 11 | Read "what would you say **yest** to". A typo, live. |
| Casing | Inconsistent on the live page: wHERE, wHO, wHAT. Sentence case throughout now. |
| Order | Ran 05 down to 01 and then 12 down to 06. **It runs 01 to 12 now, and that is functional rather than tidy:** the cards on the table are numbered and someone holding card 07 has to be able to find 07. |

The old page's two competing calls, "Let's Build What's Next" and "Let's
Talk", pointed at two different scheduling links. Both are replaced by A
Sounding, on the same HoneyBook session record `6a185c26693e14802690e9f6`
that `/a-sounding/` and the site-wide popup use. **$300 has to match that
record and The Build page.**

### What is event scoped on it

Four things, and nothing else on the page moves when they change:

    the eyebrow in the hero      GATHER  /  The Journey  /  Minneapolis
    <title>                      The Questions | Cydnie Jocelyn
    meta description             names GATHER
    the OG image                 now /assets/og/home.png

The OG image was a wedding photographer's file from a previous library on
the old page. It is the site's own card now.

### The second door is variant D, and it is a fourth option

The wireframe offered three lines for the closing link to The Letters and
recommended the flattest, B: "I also write letters. They're here." All three
were written before the cadence was settled, and the wireframe said so:
"I don't know the cadence or subject of The Letters well enough to describe
them."

We do now. It ships as **"I also write letters. One a week, free. They're
here."** Cydnie's choice, 28 August: B's flatness, but it answers the
question B leaves open. **A text link, never a button.** That is the whole
difference between a second door and a second ask, which is why that block
has no `.actions` row.

### The popup is off on both, and both are in SKIP_PATHS

`sounding-popup.js` now skips five paths rather than three.

| | |
|---|---|
| `/privacy-policy` | She is looking up what happens to her data or what she signed. Interrupting that with a $300 offer is the one place on this site where the popup reads as exactly what the brand guide bans. |
| `/thequestions` | That page already **is** this push. A modal selling what the page is selling is the page arguing with itself. |

Neither page carries the script tag either. The `SKIP_PATHS` entry is the
belt: it survives someone pasting the tag on later.

### The specificity trap bit again, in a new place

`.btn--ink` is Deepwater fill and a Surface label, per the wireframe's token
note. It rendered **Fathom on Deepwater** the first time it was built:
invisible, and invisible from the first frame, because the whole page is
light so the header is `is-surfaced` at scroll zero.

`.hdr.is-surfaced .btn { color: var(--fathom) }` is `(0,3,0)`. Plain
`.btn--ink` is `(0,1,0)`. It lost. **This is the third time this exact trap
has cost something on this project** -- see the note under
`.has-menu .nav-links a` for the session seven version, which took out three
of the four mobile nav links. The fix is matched at `(0,3,0)` and placed
later so it wins in both directions, and there is now an assertion that
fails if a bare header's button label ever equals its own fill.

### What was touched outside the two new pages

Each of these moves the whole site, so they are listed rather than left to
be discovered.

| | |
|---|---|
| **The footer on all seven shipped pages** | The privacy link went relative and a Terms link was added beside it. `.ftr-legal` is the two-link row. |
| `assets/css/site.css` | New sections **29** and **30**, plus `.ftr-legal` in section 20 and the `.hdr.is-surfaced .btn--ink` fix. |
| `tools/stamp.py` | Seven pages to **nine**. Add any new page here or it ships with a stale `?v=`. |
| `tools/preview/runsuite.sh` | Four pages to **six** in the default run. |
| `tools/preview/_test.html` | Four new assertions: the two footer legal links, and two for the bare header. |
| `tools/preview/_menu.html` | `/privacy-policy/` added, 112 measurements to **128**. `/thequestions/` is **not** there and cannot be: it has no mobile menu to open. |
| `tools/preview/sync.sh` | Excludes the two working-document folders, which it never did. |
| `sitemap.xml` | `/privacy-policy/` added. `/thequestions/` deliberately absent, with a comment saying why. |
| `llms.txt` | The published retreat terms, a **Legal** section, and the contact URL, which named a `/contact/` page that has never existed on this site. |
| `.vercelignore` | Both wireframe folders stay excluded and the comments say what became of them. |

---

## 19. Session eleven: the page load audit

Measured first, then changed. The measurements are below because the next
person to touch any of this needs to know what was true, not what was hoped.

### What the audit found, including what it cleared

Two of the four things worth suspecting turned out to be innocent, and
saying so is as useful as the fixes:

| Suspected | Measured | Verdict |
|---|---|---|
| Unused CSS | 818 selectors across nine pages, **69 unmatched, about 5.7KB of 69KB** | **Not the problem.** And most of the 69 are false positives: `.rt-shot`, `.rt-gal` and the `.q-native` variants are built by `site.js` at runtime, so a static match cannot see them. There is no dead-CSS problem here to fix. |
| Redundant JS imports | There are no imports. `site.js` is one IIFE, `sounding-popup.js` is standalone by design | **Nothing to remove.** |
| Uncompressed assets | Vercel already serves `content-encoding: br` on HTML, CSS and JS | **Already compressed.** The waste was elsewhere. |
| Synchronous loading | `site.js` and `sounding-popup.js` both carry `defer`; the Flodesk snippet injects async | **One real case:** the third-party font stylesheet. Fixed below. |

The actual weight was in four places nobody had looked: comments on the wire,
a cache header that had been made deliberately weak, an image that was
downloaded and then hidden, and a render-blocking hop to Google.

### The five changes, and what each bought

Measured on a phone-width load of the home page, brotli, which is what
Vercel actually sends.

| | before | after | saved | |
|---|---|---|---|---|
| `index.html` | 13,059 | 10,907 | 2,152 | blocking |
| `site.css` | 39,870 | 15,180 | **24,690** | **render blocking** |
| `site.js` | 14,452 | 7,839 | 6,613 | deferred |
| `sounding-popup.js` | 2,826 | 1,883 | 943 | deferred |
| `fonts.googleapis.com` css | 676 | 0 | 676 | **render blocking, third party** |
| `mark-horiz-ink-500` | 18,412 | 0 | **18,412** | eager image, never visible |
| `icon-512.png` | 18,253 | 0 | 18,253 | fetched to draw a 32px tab |
| **total** | **107,548** | **35,809** | **71,739** | |

Plus two DNS and TLS handshakes that no longer happen, and repeat views that
revalidate neither the stylesheet nor the script.

**1. The comments stopped shipping, and the source kept them.**
45% of `site.css`, 36% of `site.js`, 16% of the HTML. That is not a
criticism of the comments: they are the only place the institutional memory
of this project lives and they should never leave the source. They should
also never be sent to a reader. `tools/build.py` writes a comment-free copy
to `dist/` and the deploy comes out of there. It is **not a minifier**: it
removes comments and the blank lines they leave, and touches nothing else,
because that is where nearly all the win is and it is the only
transformation that cannot change behaviour.

The strippers fail closed. The block-comment one walks the file rather than
running a regex, so an opener inside a string is skipped. The HTML one
splits on `<script>` and `<style>` first, because a `<!--` inside a script
is JavaScript and a stripper that does not know that will cut to the next
`-->` anywhere in the file. JS line comments are **deliberately not
touched**: `//` is in every URL in this codebase, and both JS files were
checked and contain zero `//` comments, so there was nothing to win and a
site to lose.

**2. The hashed assets are `immutable` now, and the build enforces the
precondition.**
`vercel.json` said `max-age=0, must-revalidate` on `/assets/css/` and
`/assets/js/`, which cost two revalidation round trips on every repeat view
of every page. That header was correct **when it was written**: `immutable`
had once pinned readers to a stale stylesheet because the filename never
changed. `stamp.py` fixed the cause by putting a content hash in the URL,
but the header was never revisited.

It is `immutable` again, and `build.py` **refuses to build on a stale
stamp**. Not warns. Refuses. That is what makes the header safe rather than
a bet on somebody remembering.

**3. The wordmark was downloaded twice on every page and one copy was always
invisible.**
The header carried two `<img>` elements, light and ink, and
`.brand-mark--dark { display: none }` hid whichever was wrong for the ground.
A `display: none` image is still in the DOM, so the browser fetches it: 18.4KB
on every page for a picture that renders only if the reader scrolls onto a
light section. **On six of the nine pages that was the entire eager image
payload apart from the mark you can actually see.**

The ink mark is a `background-image` on `.brand` now, in an `image-set()`,
so it is fetched only when a rule that uses it applies to a rendered
element. The second `<img>` declared itself decorative (`alt=""`,
`aria-hidden="true"`), which is exactly what belongs in CSS.

**The menu contrast harness caught a regression inside this fix and it is
worth knowing why.** Bringing the light mark back over an open menu panel
used to be `display: block`, which is not transitionable and therefore
switched on the frame the panel opened. Opacity **is** transitionable and
`.brand-mark` carries a 380ms opacity transition, so the first version of
this faded the wordmark in over the panel: a third of a second of the dark
rectangle with no mark in it that session seven existed to fix. The rule
carries `transition: none` for that reason.

`_menu.html` was reading `display !== 'none'` on the light mark to decide
which was showing. That is now always `block` and only opacity changes, so
the check would have passed on a header with no visible wordmark at all,
which is the exact bug it was written to catch. It reads what is actually
painted now, and reports BOTH or NEITHER as a failure.

**4. The fonts are self hosted, and the render-blocking third party is gone.**
Every page had two `preconnect`s and a blocking `<link>` to
`fonts.googleapis.com`. The preconnects were softening a hop that did not
need to exist: DNS and TLS to googleapis.com, a stylesheet, then DNS and TLS
to gstatic.com for the files. The `@font-face` rules live in `site.css` now,
which is already blocking, so it costs **no extra request at all**, and the
files sit under `/assets/fonts/` where the immutable header already applies.

Google was serving **thirteen** `@font-face` blocks for this stack,
including cyrillic, cyrillic-ext and vietnamese, parsed on every page load
by a site that has never needed them. Eight are kept, latin and latin-ext,
with Google's own `unicode-range` preserved exactly so latin-ext still
downloads only when a page contains a character in it. All three families
are OFL. **IvyPresto is still not self-hosted and still not in this
workspace**; `--carved` still falls through to Instrument Serif.

**5. A megabyte that nothing referenced.**
20 files in `assets/img/`, 1,006,314 bytes, referenced by no page,
stylesheet or script: superseded lockups, JPEG originals of files that ship
as WebP, hero crops replaced during the picture passes. They cost no page
load, because nothing asked for them, and they were uploaded on every
deploy.

They are **moved to `assets/_unused/`, not deleted and not
`.vercelignore`d**, and the distinction matters. An ignore rule leaves a
file working in preview and 404ing only in production, which is the worst
available failure mode and one this project has hit twice. Moved, a stale
reference breaks in front of you the moment you look at the page. That
folder's README says what each file was. `build.py` prints a warning if
`assets/img/` grows another one, so the pile cannot rebuild itself quietly.

`icon-512.png` is in there because the `<link rel="icon" sizes="512x512">`
that named it was removed: a browser picking it to draw a 32px tab fetches
18KB to do it, and there is no web app manifest here that wants a 512.

### What was looked at and deliberately not changed

- **The wordmark rasters.** Re-encoding at q80 saves about 25% and it is
  brand artwork; the honest fix is an SVG, and the SVG is not in this
  workspace. Worth asking Cydnie for it: a wordmark as line art would be
  2-5KB instead of 21.7KB, resolution independent, and recolourable in CSS,
  which would delete the two-file problem in change 3 rather than deferring
  half of it.
- **The 9.1MB under `assets/img/greece`, `/retreats` and `/work`.** All of
  it is referenced and all of it is lazy gallery tiles, so none of it is on
  any initial load.
- **`sounding-popup.js` as a separate request.** It could fold into
  `site.js`. It is standalone deliberately and 1.9KB brotli is not worth
  the coupling.

---

## 20. Session twelve: mobile vertical pacing

Measured before anything moved: nine pages at 375x812, 390x844 and 360x800,
driven through so lazy images load and scroll handlers fire, with every
reveal forced to its resting state first. **`.r-up` uses `translateY`, which
moves `getBoundingClientRect`,** so measuring mid-reveal measures a lie. The
three viewports differ by under 8% on every metric; 360x800 is always the
longest.

### Four things that looked like findings and were not

Worth recording, because each cost a measurement to disprove and the next
person will suspect all four again.

| Looked like | Actually |
|---|---|
| `.door-note` links are 126x18, far under 44px | Their hit area is **146x44** via `::after { inset: -13px -10px }`. Already correct. |
| `.crs` is fixed chrome eating 5% of the viewport | Gated on `(hover: hover) and (pointer: fine)`. **Not built** under coarse pointer. Confirmed with the runcarousel flags. |
| Greece's first CTA is 20.6 screens down | The selector had missed `.hero-go`. It is at **0.52 screens.** |
| Home and Greece have 2,266px of dead space | That is `.cond-track`, a sticky pinned sequence. Content is there the whole way. A density metric cannot see sticky. |

**Run the touch measurements with the runcarousel flags** or the answers are
about a desktop:

    --blink-settings=primaryPointerType=2,availablePointerTypes=2,primaryHoverType=1,availableHoverTypes=1

### What changed

Three things, all mobile only, none touching a desktop.

**1. The section padding FLOOR, not the curve.** `.section` is
`clamp(var(--s-6), 7vw, var(--s-9))` and `7vw` only wins above about 686px,
so every phone sat exactly on the 48px minimum: 96px at every boundary,
1,501px on the home page and the same again on Greece. The floor is
**2.5rem** now. Nothing at 768px or above moves, because the vw term is
already larger than either floor.

**2. The seam floor, which had to move with it.** `[data-zone]::before` was
`clamp(2.5rem, 6vw, 5.5rem)`, so 40px on a phone against 48px of padding.
The seam paints from the TOP of the section, so a seam taller than the
padding renders behind the first line of text and that line sits on a tint
of the ground the page just left. It is `clamp(2rem, ...)` now: **32px
against 40px, the same 8px of headroom the pair had before either moved.**
Verified on every boundary of both seam-heavy pages, not argued from the CSS.

**3. A row gap is not a column gap.** `gap` on a two column grid is
horizontal space; the moment the columns stack it becomes vertical space
that never existed on the desktop the value was chosen for. Nine containers
were still at their desktop size, 48px or 64px. Measured: 544px on home,
384px on Greece, 304px on The Build.

**The override is at 41.99rem and that is the entire safety argument.** Each
of those grids picks up real columns at a different width: `.grid-12`,
`.fifteen` and `.close-grid` at 42rem, `.ab-split`, `.shapes`, `.pv-doc` and
`.cond-in` at 56rem, `.hero-in` at 62rem, `.turn-split` at 900px. Below 42rem
every one is stacked, so `row-gap` there **cannot** touch a column gap,
because at that width there are no columns.

**4. `--cond-run` on phones only.** 46vh per recognition is right on a
desktop. On an 844px phone it made the block 3.53 screens to deliver five
sentences, on the two longest pages on the site. It is 34svh under 47.99rem,
which is 287px per step: still most of a thumb flick, so nothing goes past
unread. **Not lower.** Below about 30svh a step is shorter than one flick and
a reader can skip a recognition without seeing it, and the five ARE the
argument.

### Result

| | before | after | |
|---|---|---|---|
| home | 21.80 | **20.69** | -1.11 screens |
| greece | 27.11 | **26.11** | -1.00 |
| the `.cond` block | 3.53 | **2.87** | on both pages |
| build | 14.40 | 14.07 | -0.33 |
| retreats | 16.48 | 16.24 | -0.24 |
| about | 11.35 | 11.16 | -0.19 |
| sounding | 8.77 | 8.58 | -0.19 |
| questions / letters / privacy | | | -0.08 each |
| **the site** | **124.08** | **120.80** | **-3.28 screens** |

Slices under 50% filled: home 4 to 3, Greece 4 to 3, sounding 2 to 1.

### Two measured problems deliberately NOT fixed, because both make it worse

**`.q-dot` is 24px wide against a 44px guideline. Widening it is the wrong
move.** There are seven dots on the home page. Seven 44px targets is 308px
before gaps and the column at 375px is 335px with two 44px arrows already in
it, so they wrap to two rows: vertical space added, on the page this pass
exists to shorten, to fix a control that is the third way to reach the same
slide. The arrows are 44px and the rail is swipeable. The dots are already
44px TALL, so the thumb has a full-height target on the axis it approaches
from. The comment at `.q-dots` in section 28 records that these already
overflowed once.

**Line length is 38 characters at 390px against a 45 to 75 guideline, on
every page, and it cannot be fixed.** 390px less two 20px gutters is 350px,
and 350px at the 18px body size IS 38 characters. The only lever is
font-size and the size that reaches 45 characters is about 15px, under the
16px floor. The guideline is written for a desktop reading distance. Nothing
should be tightened to chase it.

### Still open, and it is a copy decision rather than a CSS one

**The Build is 5.84 screens to its first CTA**, the deepest on the site.
Every other page has an action inside the first screen. `/thequestions/` is
3.12 screens but carries a persistent A Sounding button in its bare header;
The Build does not, because under 56rem its header CTA is inside the
hamburger like every other page.

This was left alone. Fixing it means either new copy in the hero, which is
under the freeze in §5, or exposing the header CTA site wide, which is a
design change nobody asked for. **Ask Cydnie.** The page's own argument is
"every price is published, you will not need a call", so a hero CTA may be
against its intent, and a quiet anchor to the prices may be the right answer
rather than a booking link.

### One pre-existing thing the audit flags at 768px

`/retreats/greece/` reports thirteen 10px spans at exactly 768px. **This is
not from this pass** and was confirmed identical with the change stashed.
The micro labels are raised to 11px by `@media (max-width: 47.99rem)`, and
767.84px is where that stops, so 768px gets the base 10px. That is the
deliberate desktop size from session six. A tablet is not a phone and it was
out of scope here.

---

## 21. Session thirteen: six mobile corrections

All six are Cydnie's own notes from reading the site on a phone. Every one
is scoped to a phone and **nothing in section 28c may change a desktop**,
which was verified by measuring the same page at 1440x900 afterwards: the
gauge still `flex`, the seam still the original two stop gradient, the hero
padding still 144/126, the rise band still 552px.

### 1. The surfacing gauge is off below 56rem

It reads how far up the reader has come, and on a wide page it is a quiet
instrument at the edge. On a phone it is a line and a travelling dot about
12px from the text column, moving continuously for twenty screens in the
reader's peripheral vision. Cydnie's words: too much movement.

56rem because that is this site's own line between mobile and desktop, the
width where the nav collapses and the twelve column grid arrives.

### 2. The line between two sections, and what it actually was

**This is the one worth reading.** Two boundaries were reported as having a
drawn line across them: the light method block into the dark
"Sometimes the answer is that you don't need me", and the Silt proof block
into the dark section that opens with the photograph of Cydnie.

There is no border anywhere near either. Sampling a text free column down
the boundary, pixel by pixel, showed what it really was:

    y=178   (231,236,232)   flat Surface
    y=180   (227,232,229)   ramp begins
    ...     twenty units of luminance every two pixels, dead even
    y=212   (7,26,31)       flat Fathom

**A linear ramp between two flat fields is the textbook recipe for a Mach
band.** The eye exaggerates a discontinuity in the GRADIENT, not in the
colour, so both ends of an even ramp read as drawn lines. The top one is
the line that was reported.

The seam is eased now, approximating smoothstep over the same 32px, so it
leaves and arrives at zero slope. Measured after: the first and last steps
are 3 units per row instead of 20, with the steepness moved to the middle
where no edge is created. **It costs nothing.** Same height, same colours,
same scroll; it just stops announcing where it starts.

`color-mix()` builds the alpha steps, because `--from` is a different colour
on every section and CSS cannot otherwise take an arbitrary custom property
to a partial alpha. **The fallback is clean:** a browser without
`color-mix` discards the declaration at parse time and the base rule's
original gradient still applies.

If a seam ever looks like a line again, sample it before changing a height.
The instinct is to make the ramp longer. The ramp was never too short.

### 3. The dark air under the hero

Measured 204px of empty Fathom between the last thing in the hero and the
first thing in the condition. The hero's own bottom padding was 118px of
it, on a block that is already `min-height: 100svh` and vertically centred.
It is 4rem on a phone now.

**What is left is not spacing and cannot be fixed by changing padding.**
The condition's stage is a pinned panel, `height: 100svh` with
`align-items: center`, holding about 358px of content. The rest is the
panel centring its content in the screen, which is what it is supposed to
do while pinned. Padding changes there just redistribute: reduce the top
padding and the centring hands the space straight back. Moving it to
`flex-start` would put the content at the top of the screen with 370px of
dark under it for 2.87 screens, which is worse. Left alone deliberately.

After the change, **no empty dark run anywhere on the home page is over
120px** apart from the pinned track itself.

### 4. The hand fits its frame now

The source is 632x1018, a portrait photograph of a hand reaching down a
wall. The mobile rule cropped it to **4:3 landscape**, which cut the
fingertips off at the bottom edge: the one thing the picture is of.

It is 4:5 on a phone now, the same plate the desktop uses. The reason
desktop caps it at 4:5 rather than the source's 0.62 is written in the CSS,
"so it does not out-tower the copy beside it". On a phone there is no copy
beside it, it is stacked underneath, so there is nothing to out-tower and
no reason to crop harder than the desktop does.

### 5. The rise band is larger

`aspect-ratio: 1800/690` on a 390px screen is 149px, so the band sat on its
`min-height` floor at 208px: the surface, the three bubbles and the words
all inside a fifth of the screen. This is the moment the whole site is
named after. 17rem on a phone, so 272px.

### 6. The third line under the retreat heroes

`.rt-facts` carries a `border-top`, and above 30rem that is right: the three
facts are a row there and the border is the divider above it.

Below 30rem the row becomes a stacked list and the border stops dividing
anything. The two `.hero-go` links above it each draw their own
`border-bottom`, so the hero ended with **three stacked rules**: two short
ones under the links, then a full width one under those, belonging to
nothing above it. Being the only one of the three that spans the column is
what made it read as a stray mark rather than part of the pattern.

**Scoped to 29.99rem rather than to a general phone breakpoint on purpose.**
30rem is exactly where `.rt-facts` picks up its three columns, so the border
is off in precisely the case where it has nothing to divide and on
everywhere it works. Verified across ten widths: no line at 360 to 479,
line at 480 through 1440.

The padding goes with it, because it existed to hold the rule off the text
and with no rule it is a 24px hole. `margin-top: var(--s-6)` already
separates the block.

It is a shared class, so **both retreat heroes are corrected.** Only
`/retreats/` was reported, but `/retreats/greece/` has the identical
construction and had the identical stray line.

### What this cost, and why that is the right trade

Home went from 20.69 screens to **20.91**. The hand gained 175px and the
band gained 64px; the hero gave back 54px. **Two of the six corrections
were requests to make things bigger,** so the page getting slightly longer
is the ask being met, not a regression. Session twelve's reductions all
still hold.

---

## 22. Session fourteen: the re-diagnosis photograph

`#turn` on the home page, the section that says **"Nothing is wrong with
you. Something is on top of you."**

### Which of the two, and why

Two hand photographs arrived in `CydnieJocelyn-Site/Website Images/` on
28 August, both 1254x1254:

| | measured | |
|---|---|---|
| **`Reaching through water.png`** | saturation **0.12**, value 0.34, nearest palette token Meniscus at distance 31 | **shipped** |
| `underwater hand.png` | saturation **0.44**, value 0.50, distance 47 | not used, still in the folder |

They are the same gesture in different water. The second is a vivid cyan
and would have been the brightest, most saturated thing on a site whose
whole palette is desaturated deep teal: on a Fathom ground it reads as a
swimming pool. The first is three and a half times less saturated and
lands almost exactly on Meniscus, which is the token the section is built
from. **If Cydnie prefers the brighter one it is a two line swap**, the
file is still there, but the palette argues hard for the one that shipped.

### What it replaced, and why that mattered

`reaching-shadow-*` was a hand and its shadow on a **sunlit wall**. It
illustrated reaching but not water, and water is the entire argument of
that section: "You are not lacking anything. You are UNDER something."
The new picture is that sentence rather than a metaphor for it.

It also fixes a second thing for free. The old photograph was a bright
warm wall sitting as a hard rectangle on a near black ground. The new one
is dark water at its edges, so the plate's lower and side edges melt into
Fathom instead of being cut out of it.

### The plate is square now, at every width

The source is square. The frame used to be **4:5 on desktop with a 4:3
mobile variant**, both of them cropping a portrait photograph, and the 4:3
was what cut the fingertips off in session thirteen.

`aspect-ratio: 1 / 1` at every width now, so `object-fit` has no aspect
mismatch left to resolve and nothing is cut off to make the picture fit a
shape it was not taken in.

**`max-height` had to move with it and this is the part that is easy to
miss.** The cap was 30rem, chosen when the plate was 4:5. A square plate
at 1440 wants 500x500 and the cap clamped it to **500x480**, so
`aspect-ratio: 1/1` was being quietly overruled at exactly the width most
people read the site on. Measured, not assumed. It is 34rem now, which
clears every normal desktop column and still caps an ultra wide screen
where 40vw is 900px and a square really would become a picture with a
caption. Verified square at 390, 430, 1440 and 1920.

### `sizes` was lying and now is not

It said `100vw` on mobile. The figure is inside `.wrap`, so it is the wrap
width, not the viewport, and every phone was fetching a candidate one size
too large. It is `calc(100vw - 2.5rem)` now.

Three widths ship, 600/900/1200 at q82: 23KB, 44KB, 65KB. A 390px phone at
2x now takes the 900, and a 1440 desktop at 1x takes the 600.

### The square is shorter than what it replaced

`#turn` loses 87px on a phone, because a square plate at 350px wide is
350px tall where the 4:5 was 437px.

---

## 23. Session fifteen: the home page arc

Cydnie: the home page is too dark, and the colour should feel like coming
up from being under something. Measured before changing anything, by
sampling the ground luminance every 4% down the page.

### What was actually wrong: the palette on this page was binary

    FLOOR (Fathom)      8157px   46.5%
    MID                    0px    0.0%
    LIGHT (Silt/Surface) 9401px   53.5%

**Zero pixels of intermediate ground.** Every section was either 0.088 or
0.887+. The Foundation's arc is "submerged, underwater, resurface, breath,
flight", five stages, and the page had two: black and white. So the rise
was not a rise, it was a light switch, thrown four times.

Worse, Fathom, the absolute floor, kept coming back AFTER the rise band.
Two full-dark sections immediately after the surfacing, and three more
screens of it at 60%.

### The rule that fixed it

**Fathom is the bottom, so it only belongs where the reader is at the
bottom.** After the rise band nothing returns below Deepwater. Depth still
returns, twice, deliberately: it just stops going all the way down.

Nothing was invented for this. `.z-deepwater` already existed as a full
ground class with every token override, used on The Letters and Greece,
and had simply never been used on the home page.

| section | was | now | |
|---|---|---|---|
| hero, condition | Fathom | Fathom | the floor, where she starts |
| **turn** | Fathom | **Deepwater** | the re-diagnosis IS the first lift. It was the same black as the hero |
| method | Surface | Surface | surfaced |
| **band** | Fathom | **Deepwater** | "Sometimes the answer is that you don't need me" looks back down; it does not fall to the floor |
| **before you book** | Fathom | **Silt** | reassurance was the darkest thing on the page |
| **story** | Fathom | **Deepwater** | still the deliberate return to depth the stylesheet has always described, one step off the floor |
| footer | Fathom | Fathom | |

    FLOOR    4477px   25.5%   (was 46.5%)
    MID      3061px   17.4%   (was 0%)
    LIGHT   10020px   57.1%

**Every seam was re-pointed in the same commit.** `--from` names the ground
ABOVE a section, so five of them moved: `#turn` gained one, `before you
book` and `#fifteen` gained one each, `#retreat` changed from `var(--fathom)`
to `var(--deepwater)`, and the rise band's `--band-from` went to Deepwater
because what is above it is no longer Fathom. A seam naming the wrong
ground is a visible edge; see §21.

### Two contrast bugs fell out of it, same root cause

Running a per-section contrast sweep afterwards turned up two failures, and
both were the same mistake: **`--accent` used as a text colour.** On a dark
ground `--accent` is Meniscus, which the palette's own comment reserves for
"hairline rules and small caps labels only".

| | was | now |
|---|---|---|
| `.cond-ticks button[aria-current="true"]` | `--accent`, **2.34:1** | `--label`, **9.62:1** |
| `.story-lede` | `--accent`, 2.34:1 on Fathom and 2.02:1 once the section moved | `--muted`, **8.31:1** |

The tick one was the more interesting failure: **the LIT tick was the least
readable of the five**, because the four unlit ones sit on `--muted` at
9.62:1. The indicator was backwards.

`--label` is Breath on a dark ground and Deepwater on a light one, and on a
light ground `--accent` and `--label` both already resolve to Deepwater, so
that change is **byte-identical on Greece**, where `.cond` sits on Surface.
Only the home page moves.

**Nine sections, zero contrast failures** after. Before: two.

### One thing worth noticing

The re-diagnosis photograph, which is a hand under water, now sits on
Deepwater rather than Fathom. The ground is much closer to the tone of the
photograph's own edges, so the plate integrates instead of being a
rectangle cut out of black. That was not the reason for the change but it
is the clearest single improvement on the page.


---

## 24. Session sixteen: the plate stops being a rectangle

Cydnie: the hand picture looks blocky. It did. It was a hard rectangle on a
near black ground, which is the one place a photograph of water should not
have a straight edge.

### A mask, not a matching-colour vignette

An inset shadow in Deepwater would have looked identical today and broken
the moment that section's ground moved, which it did one session ago. A
mask fades the picture to **transparent**, so it dissolves into whatever is
behind it and cannot go stale.

### The first attempt was not enough, and measuring said why

A plain linear alpha ramp fixed three edges and left the fourth. Measured
down the middle of the plate, the top edge still went **52 luminance units
in three pixels**, because the top of this photograph is the lit surface
and the ground behind it is Deepwater.

**Same fault as the section seams in §21.** A straight ramp has a hard
onset, and the eye reads the break in the gradient as a line. The stops
approximate smoothstep now, so the fade leaves and arrives at zero slope.

    boundary   max step per pixel
    top          2.9   (was 52 over three pixels)
    bottom       0.9
    left         1.7
    right        0.8

The four edges are deliberately unequal. The bottom is dark water meeting a
dark ground, so it travels furthest and disappears entirely. **The top gets
the shortest fade of the four**, because it is fading the subject: it only
has to stop the light ending on a ruled edge, not erase it.

### A trap worth writing down

The first measurement was taken at a scroll position where **the fixed
header covered the plate's top 8 pixels**, so the 27-unit step being
measured was the header's own bottom edge and it was identical before and
after the change. Get the plate's real bounds out of the DOM before
sampling pixels near the top of the viewport.

### Fallback

A browser that supports neither `mask-composite: intersect` nor
`-webkit-mask-composite: source-in` keeps the plain rectangle, which is
exactly what shipped before. `#depth` exists only on the home page.


---

## 25. Session seventeen: soft edges on every photograph

The `#depth` treatment from §24, generalised across the site on Cydnie's
instruction: "all images vs. having them be just boxy images."

**It is applied to photographs presented as plates, and deliberately not to
seven other things.** The inventory that decided it is below, because "all
images" and "all photographs" are not the same list and the difference is
what keeps this from looking broken.

### One rule, `site.css` section 29b

Same construction as §24: an eased, smoothstep-approximating mask on four
edges, driven by `--e-t`, `--e-b`, `--e-x`, `--e-xr` so any slot can tune
without a new mask. **A mask and not a matching-colour vignette**, because
an inset shadow has to know the ground, and one rule here serves Fathom,
Deepwater, Silt and Surface at once. The home page's grounds moved one
session ago; a colour-matched vignette would have gone stale that day.

### Where the mask sits, and why it is split in two

| | |
|---|---|
| **on the container** | `#depth`, `.ab-portrait`, `.rt-date-fig`. Each clips an OVERSIZED image inside `overflow: hidden` for the parallax drift, so masking the image would fade it outside the visible box and leave the real edges hard |
| **on the image** | `.story-fig`, `.retreat-fig`, `.layer-fig`, `.rt-person figure`. Every one of these carries a figcaption, and a mask on the figure fades the caption text along with the picture |
| **vertical only** | `.layer-band` runs edge to edge, so its left and right edges are the screen and there is nothing there to soften |

### What is deliberately NOT masked, and why

Verified afterwards by querying computed `mask-image` on each, on every
page it appears: all seventeen clean.

| | |
|---|---|
| the wordmark, header and footer | it is the logo |
| `.case-mark` | a client's logo. Not ours to dissolve |
| `.case-screen` | a UI screenshot. Soft edges there read as broken rendering rather than as a treatment |
| `.rt-play` | an interactive target. A control needs an edge you can see the end of |
| `.gal-item` | grid tiles. Fading tile edges destroys the grid rhythm, which is the entire point of a grid |
| `.lbx-stage` | the lightbox. A viewer, not a plate |
| `.rt-date-fig--map` | a drawn map, not a photograph |
| `.hero-water`, `.rise-band .layer-band` | already carry their own scrims. **Two fades stacked are not softer, they are muddy** |

### The light-ground question, which was the real risk

On Fathom or Deepwater the fade goes into water and the picture dissolves.
**On Silt or Surface the same mask fades to near-white**, which could have
read as a bleached print rather than a treatment. It does not: it reads as
a soft edged print, and the captions stay crisp because on every
light-ground slot the mask is on the image rather than the figure. Checked
on `/`, `/retreats/` and `/retreats/greece/` before shipping rather than
reasoned about.


---

## 26. Session eighteen: two the soft-edge sweep missed

Both reported by Cydnie against the Retreats page, and both were wrong
assumptions in §25 rather than bugs in the mask itself.

### 1. A band is not always full bleed

`.layer-band` was given the vertical pair only, on the reasoning that a
band runs edge to edge so its left and right edges are the screen. Measured
at 1440 and at 390, that is true of three of the four:

    /retreats/         --tall   1176 of 1440   INSET, inside .wrap
    /retreats/         --wide   1440 of 1440   full bleed
    /retreats/greece/  --wide   1440 of 1440   full bleed  (x2)

`.layer-band--tall` is the pavilion at nine in the morning. It sits inside
`.wrap` at 76vw and had two hard vertical edges the rest of the site no
longer has.

**The test is structural, not a variant name.** `.wrap .layer-band` gets
the four-edge mask: if it is inside a wrap it is inset, and inset means it
has real side edges. A `--wide` dropped into a wrap later picks this up on
its own and a `--tall` pulled out to full bleed drops it, without anyone
having to remember this note.

### 2. The control needs an edge. The picture behind it does not

`.rt-play` was excluded as an interactive target, on the reasoning that a
control needs an edge you can see the end of. **That is true of the
control and not of the photograph**, and the two are separate elements:
the play button is `span.rt-play-btn` and the scrim is `.rt-play::after`,
both siblings of the image.

So `.rt-play img` is masked and the anchor is not. The photograph dissolves
and the button stays completely crisp. It is the largest photograph on that
page, so leaving it square had made it the only boxy thing left once
everything around it had been softened.

The verification harness still reports it under the exclusion list, now as
`!! MASKED`, which is correct and intended: **the anchor is unmasked, the
image inside it is masked.** Every other exclusion is still clean.


---

## 27. Session nineteen: the images were already WebP

Cydnie asked for all photos to be optimised as WebP. **They already were**,
and measuring that first is what stopped this becoming a session of
generation loss for nothing.

    referenced images:  101 webp,  3 png
    the three png:      favicon-32, apple-touch-icon, og/home

**Those three must stay PNG and converting them would break things.** iOS
does not accept a WebP `apple-touch-icon`, and Facebook, LinkedIn and X do
not reliably render a WebP Open Graph image, so `og/home.png` would silently
stop producing link previews. Not an oversight. A requirement.

### Re-encoding buys 0.4%, and costs a generation

`tools/retreat_images.py` already writes a deliberate quality ladder,
q82 at 700px and under, q76 to 1200, q70 above, with a comment recording
that q82 on the wide variants ran over 4MB. Re-encoding an already-lossy
WebP is a second generation, and swept across all 95 files:

| | |
|---|---|
| files with >15% headroom at SSIM >= 0.99 | **4** |
| what they are worth | **33KB, 0.4%** of the image payload |

Several files get BIGGER when re-encoded: `greece/olive-1200` goes 341KB to
374KB at q82, because the artifacts of the first encode cost bits to
reproduce. **If a future session is asked to "optimise the images", measure
before converting.** The answer here was almost entirely no.

### What was actually wrong: missing candidates, not encoding

`sizes` was accurate everywhere. The waste was that `srcset` had no small
enough file to offer.

`/the-build/` declares `20vw` for `.case-screen`, which is 71 CSS px on a
390 phone. **The smallest candidate was 500w.** So a phone downloaded a
500px image to draw 71px, six times over:

    work block on a phone   390,864 bytes

300w screens and 400w marks were generated FROM THE 800w AND 900w
VARIANTS rather than re-encoded at the same size, because downscaling
averages the first generation's artifacts away instead of compounding them.

    work block on a phone   173,942 bytes   -55%

### A measurement trap worth recording

SSIM on the marks first read **0.58 to 0.77**, which looked like serious
damage. It was not. They are RGBA logos, and grayscale SSIM was comparing
the undefined RGB inside fully transparent pixels, which is noise.

**Flatten an alpha image over the ground it actually sits on before
measuring it.** Composited over Silt, the same files measure **0.9988 to
0.9998**, with the alpha channel itself at exactly 1.0000.

### The four re-encodes, and why banding was checked separately

SSIM is weak at detecting posterisation in smooth gradients, and two of the
four are the home hero, which is mostly a smooth water gradient. Distinct
luminance levels per row in the calmest fifth of each image, before and
after: 25.8 to 25.2, 25.4 to 25.2, 79.4 to 78.2, 24.1 to 25.0. **No
posterisation introduced**, so they were applied.

`hero-line` has a source at the same 1717x916 in `Website Images/`, but it
measures SSIM 0.32 against the shipped file: **the shipped one is graded**,
and the grade is not in any tool. Regenerating from that source would have
thrown the grade away. Same-size re-encode was the only safe route.

### Net

    /the-build/ on a phone   -216,922 bytes  (-55%)
    hero, veil, srs re-encode  -33,176 bytes
    on disk                    +140,766 bytes, six new smaller variants

Disk goes up because candidates were added. What a browser downloads goes
down, which is the number that matters.


---

## 28. Session twenty: SEO, and fifteen places

Cydnie named fifteen locations to highlight. The audit came first, and most
of it came back clean.

### What was already right, and is worth not breaking

Every page: exactly **one H1**, a canonical, Open Graph, Twitter card, valid
JSON-LD, **zero images missing alt text**, and **no heading-level skips** on
any of the nine. That is a better baseline than most sites ever reach.

### What was actually wrong

| | |
|---|---|
| six meta descriptions | 164 to 178 characters, so Google truncated them mid-sentence. All now 120 to 159 |
| two titles | Retreats 67 and About 63 characters, both truncated. Now 59 and 45 |
| **five pages had no LocalBusiness node at all** | About, Retreats, Greece had no organisation node; The Letters and Privacy had one with no `areaServed`. **Retreats and Greece are the pages most likely to rank for a Minnesota retreat search** and they were the ones carrying no local signal |
| `index.html` | its org node was typed `Organization`, not `LocalBusiness`. A bare Organization does not carry local ranking signal. Widened |
| sitemap `lastmod` | stale on five pages |

### The fifteen, and where they live

**The precise list is `areaServed` on the LocalBusiness node in the head of
all eight indexable pages.** That is the machine-readable half and it is
where a search engine actually reads a service area from. Fifteen cities,
plus Anoka, Isanti, Washington and Chisago counties, plus the Twin Cities
metro, Minnesota and the United States.

`/thequestions/` has no organisation node and should not: it is `noindex`
because its URL is event scoped. The suite asserts that absence rather than
asserting a node, so the deliberate decision cannot be reported as a bug.

**The human-readable half is ONE SENTENCE in the footer**, `.ftr-area`, on
all nine pages. That was a deliberate limit. A block of fifteen city names
repeated across nine pages is 135 city mentions sitewide, which is what a
keyword pile looks like to a reader and to Google, and the structured data
already carries the precision. One sentence gives the local signal without
the site starting to read like a directory listing.

Also updated: `llms.txt`, which now names the same fifteen and points at
`areaServed` so an answer engine can find the canonical form.

### Three assertions, because there are now two copies of one fact

The footer sentence and the `areaServed` array are the same claim written
twice. Edit one and not the other and the site makes two different claims
about where Cydnie works. The suite checks the line exists, that all fifteen
cities appear in it, and that the same fifteen appear in `areaServed` on
every indexable page. **182 assertions became 200.**

### Not done, and why

**No city landing pages.** The obvious next SEO move is a page per town, and
it is the wrong move here: fifteen near-identical pages differing only by a
place name is the textbook doorway-page pattern Google penalises, and it
would wreck a site whose whole argument is that it does not run templates.
If local pages are ever wanted they need to be genuinely different pages,
with real local content, and there are only a few towns where that is true.


---

## 29. Session twenty-one: the rule was running through her name

Reported as "I'm Cydnie is extremely close to the top line". Measured, it
was not close. **At 375x812 the heading sat 13px ABOVE the rule and the
line ran straight through the words.**

### Why it only failed at one width

`.ab-head-rule` is absolutely positioned at **38% of the section**. The copy
is **bottom aligned**. So the clearance between them is not set anywhere: it
is whatever is left after the copy has taken the height it needs.

    gap = 0.62 x sectionHeight - paddingBottom - copyHeight

At 375x812 the lede wraps to **four** lines rather than three, so the copy
block is 291px against 265px at 390. The section was `min-height: 68svh`,
552px at that viewport, and the arithmetic came out negative.

**The tightest case is 375x812, not the narrowest screen.** 320 is fine and
390 was only 23px. If this is ever retuned, measure 375 first: it is the one
that fails, and testing 320 and 390 would have passed it.

### The fix keeps the composition and changes the room

The refinement command specifies a rule at 38% with **nothing above it**.
That is what was being violated, so 38% was not the thing to change. The
section is `min-height: 80svh` now, so 38% has enough page to be 38% of.

    rule to heading, measured after
    375x812     -13px  ->   47px
    390x844      23px  ->   86px
    1440x900     18px  ->   85px
    768x1024     97px  ->  173px

`.ab-head--type` exists only on the About page, so nothing else moves. The
page grows about 108px on a desktop, roughly a tenth of a screen on an
eleven screen page, which is the cost of the heading not having a line
through it.


---

## 30. Session twenty-two: the licensed face, and the tag that was already promised

Two wirings, both of which had been sitting open, and one of them had been
open in a way that made the site say something untrue.

### The font is IvyJournal, not IvyPresto Display

`--carved` has named `"IvyPresto Display"` since the first build and nothing
has ever served it. Every headline on this site, for twenty-one sessions,
has rendered in **Instrument Serif**, the fallback. The stack looked wired.
That is the whole failure mode: a font stack cannot tell you the difference
between "loaded and rendering" and "named and skipped".

Cydnie's Adobe Fonts Web Project, kit `jmh2wyp`, was fetched and read before
anything was changed. It contains **ivyjournal** in four faces — roman and
bold, each with an italic — and no IvyPresto at all.

**This may be exactly what she wants and it may be the wrong family in the
kit.** It was wired as-is, because IvyJournal is a serif and `--carved` is
the only serif slot on the site, so there is nowhere else it could go. If
IvyPresto was meant, the fix is in her Web Project and then one token here.

    --carved: "ivyjournal", "Instrument Serif", Georgia, serif;

**Lowercase and unspaced.** Adobe's kit defines the family as `ivyjournal`.
`"IvyJournal"` with a capital and a space matches nothing and falls straight
through to the fallback, which is precisely how `"IvyPresto Display"` sat in
this file for eight sessions looking correct.

### What it costs, measured

IvyJournal sets wider than Instrument Serif. On the home hero at 1440 the
headline goes from **two lines to four**. Checked at 375x812, the width this
codebase already knows is the tightest (§29): no horizontal overflow on any
of the nine pages, nothing spills its container, and the About page's
`.ab-head-rule` clearance — the bug §29 was written about — measured
**47px before, 46px after**. The lede under it is `--level`, so the wrap
that drives that arithmetic never changed.

### The preload that became dead weight the moment this landed

`instrument-serif-latin.woff2` was preloaded on all nine pages because it
drew the first screen. Once ivyjournal took the carved stack it stopped
drawing anything, and the preload kept going: **15,340 bytes fetched on the
critical path, zero characters rendered**, confirmed against `document.fonts`
which had ivyjournal loaded and had never asked for Instrument Serif. The
preload is removed. The face is still in the stack, still what renders if
the kit fails, and is now discovered from the stylesheet the way the mono
always has been.

**The one thing this trades away.** The site had no third-party dependency
on its first paint — session one deliberately pulled the Google Fonts links
out for exactly that reason. It has one now and it cannot not have one:
Adobe's licence requires serving from their CDN. Both hosts are
preconnected, because the kit `@import`s a second stylesheet from
`p.typekit.net` and without the hint the browser does DNS and TLS twice in
series before a headline can paint.

**A lapsed Creative Cloud seat or an unpublished Web Project takes the
headlines out silently, with no error on this end.** That is a new way for
this site to break and it is worth knowing about on a renewal date.

### Google Analytics 4, `G-KDB3GWPNHC`

The interesting part is that **the privacy policy has been promising this
since it was built on 28 August**. It names Google Analytics twice, once
under "Information collected automatically" with a specific list of what it
collects, and again under "Third party tools". The cookie paragraph says the
site runs analytics and asks the reader to accept them.

None of that was true. The site set no analytics cookie and collected
nothing. **This change makes the policy accurate rather than making the
policy need changing**, which is the reverse of the usual order and is the
reason it went in without a copy edit.

`gtag.js` sits **last in the head, not first**. It is `async` and never
blocks the parser wherever it goes, but a script tag high in the head still
enters the fetch queue ahead of the stylesheet and the preloaded sans, and
those are what the first paint waits on. Verified firing: a real
`/g/collect` hit to `tid=G-KDB3GWPNHC`.

### Still open, and both are Cydnie's calls, not code

1. **Adobe Fonts is not in the policy's "Third party tools" list.** Vercel,
   HoneyBook, Flodesk, Google Analytics and Google Workspace are. Serving
   the kit sends every visitor's IP to Adobe, which is the same kind of fact
   as the other five. One line, in legal copy, so it was not written unasked.
2. **Consent is implied, not collected.** "Continuing to use the site means
   you accept them" is the standard US posture and is fine for a Minnesota
   business. It is not GDPR consent, and GA4 fires before any reader has
   agreed to anything. If the Greece retreat is expected to draw EU traffic
   this is worth a real decision rather than a default.

### The suite

**Eight assertions added, and they assert the loaded face, not the token.**
"`--carved` names it" is what was true for twenty-one sessions while the
headlines were wrong, so the checks are `document.fonts.check` and the
computed `font-family` on the `h1`. Plus: the kit link exists exactly once,
both preconnects are present, Instrument Serif is in the stack and *not* in
the preloads, `gtag.js` is present and `async`, and `gtag` is a live
function with a populated `dataLayer`.

    the six pages runsuite.sh runs by default    254 pass / 0 fail
    home, About and the-build, run singly          97 pass / 0 fail
    all nine                                      351 pass / 0 fail

**Read that as nine pages, not as a delta against the 200 in §28.** That
number was the six-page default run at the time it was written and later
sessions added to the suite without updating it, so the two are not the same
measurement and subtracting them would invent a figure.


---

## 31. Session twenty-two, part two: the legal copy, and a security pass

### The policy now describes the site it is on

Two claims on `/privacy-policy/` were false the day it was written and one of
them became true earlier in this session. Both are true now.

| | |
|---|---|
| **Google Analytics** | Named twice in the policy, running nowhere. Closed by wiring GA4 in §30. |
| **Third party tools** | Listed five platforms. The type had just started coming from a sixth. **Adobe Fonts** added. |
| **Cookies** | Said "cookies, to run analytics" and named none. Now names `_ga` and `_ga_KDB3GWPNHC`, read off the running site rather than copied from a template, with the two year expiry and an explicit statement that there are no advertising cookies. |
| **A new paragraph, "Fonts"** | Serving type from Adobe's CDN sends the reader's IP address and the page they are on to a company they have never heard of. That is the same class of fact as the analytics paragraph above it and it now sits next to it. |

**The sharp assertion is the cookie name.** `_ga_KDB3GWPNHC` carries the
measurement id, so the policy and the page head are two copies of one string.
Repoint GA at a different property and the policy names a cookie that does
not exist, which is worse than naming none: it is a specific, checkable,
wrong claim in a legal document. The suite reads the id out of the `gtag`
src and looks for it in the prose, so it cannot be hardcoded wrong twice.

### The security pass

Audited: every external origin the shipped pages reach, XSS sinks in both
scripts, secrets, what the deploy actually uploads, and the response headers.

**Clean already, and worth not breaking.** No inline event handlers anywhere.
No `javascript:` URLs. No page reads a URL parameter, a hash or
`document.referrer`, so there is no reflected-XSS surface at all. No secrets
in the tree. Every `target="_blank"` already carries `rel="noopener"`. The
video embed was already `youtube-nocookie` and already click-to-load.

#### What was actually wrong

**1. `.claude/launch.json` was being deployed.** `EXCLUDE_DIRS` in build.py
listed `.git` and `.vercel` and not `.claude`, and `.vercelignore` did not
have it either, so `os.walk` descended into it and copied a local tooling
config — absolute paths to a preview server on Cydnie's machine — into
`dist/`, where it was uploaded on every deploy and served at
`/.claude/launch.json`. Excluded in both files now. The drift check at the
bottom of build.py keeps the two lists honest with each other.

**2. Six response headers were missing.** `vercel.json` sent `nosniff` and a
`Referrer-Policy` and nothing else: no CSP, no HSTS, nothing against
clickjacking. All added, and **all verified against a server sending the real
headers rather than a `<meta>` tag** — `frame-ancestors` and
`upgrade-insecure-requests` are ignored in meta, so a meta test cannot see
them at all. Framing the site from itself now returns no document.

**3. A `textContent` -> `innerHTML` round trip** on the lightbox button label
in `site.js`. Never an injection — nothing on this site is reader-supplied —
but a caption containing an ampersand or an angle bracket would have come out
wrong, and a photograph caption is exactly the copy that eventually contains
"R&D" or a measurement in inches. Builds the node now.

**4. The YouTube frame delegated more than a video needs.** `allow` carried
`clipboard-write`, which lets a frame on a domain we do not control write to
the reader's clipboard and has nothing to do with playback, plus
`accelerometer` and `gyroscope`, which only matter for 360-degree footage and
none of these embeds are. Now `autoplay; encrypted-media; picture-in-picture`
and a `referrerpolicy` so Google gets the origin rather than the full URL.

#### The CSP, and why it is generated

`script-src` is strict: `'self'`, two named third parties, and a sha256 for
each of the three inline scripts. **No `'unsafe-inline'`.** That is only
affordable because of the "clean already" list above, and it closes the
reflected-XSS class outright.

The hashes are computed by `seal_csp()` in build.py **from the built files,
after the comment strippers have run**, because comments are 16% of the HTML
and stripping them changes the bytes inside an inline script. A hash taken
from the source would be wrong for the thing that ships. Same reason
`stamp.py` runs before the build.

    script-src   'self' + 3 sha256 + googletagmanager + assets.flodesk
    style-src    'self' 'unsafe-inline' + typekit + flodesk
    connect-src  'self' + google-analytics + googletagmanager + flodesk
    frame-src    youtube-nocookie only
    form-action  'self' + form.flodesk.com
    frame-ancestors / base-uri / object-src   'none'

**`'unsafe-inline'` is kept in `style-src` and cannot be removed.** There are
hundreds of `style="--d:120ms"` attributes carrying per-element custom
properties, and `sounding-popup.js` injects a `<style>` block. Hashing does
not apply to style attributes. This is the ordinary trade and it is a far
smaller exposure than the script equivalent.

**`check_headers()` fails the build** if any required header disappears, if
`script-src` gains `'unsafe-inline'`, `'unsafe-eval'`, `'strict-dynamic'`,
`http:` or `*`, or if the hash placeholder is removed. A CSP is the easiest
header in the world to "fix" by pasting a wildcard into it when something
breaks, which leaves a policy that closes nothing while still showing up in
every header dump.

#### What was tested, on every page

Nine pages under the real headers: zero violations. The Flodesk signup on
`/the-letters/` renders all ten inputs and keeps its POST target. The
YouTube embed plays. The Greece lightbox opens. IvyJournal loads and GA fires
on all nine.

    suite   356 pass / 0 fail across the nine

#### Left open, because they are Cydnie's calls and not code

1. **HSTS is `max-age=31536000` with no `includeSubDomains` and no
   `preload`.** Deliberately conservative. `clients.cydniejocelyn.com` is
   HoneyBook's and answers on HTTPS today, so `includeSubDomains` would very
   likely be fine — but it is a commitment that cannot be withdrawn quickly,
   it binds a subdomain someone else operates, and `preload` is harder still
   to reverse. Escalate on purpose, after cutover, not as a side effect.
2. **There is no consent banner.** GA4 sets its cookies before any reader
   agrees to anything, and the policy takes the implied-consent posture
   ("continuing to use the site means you accept them"). Standard for a US
   business and fine for Minnesota. It is not GDPR consent. If Greece is
   expected to draw EU traffic, that is a real decision, and it is a build —
   a banner plus holding GA until consent — not a copy edit.
3. **The apex is still the old Showit site.** Checked live during this
   session: `cydniejocelyn.com` answers from Showit behind Cloudflare. None
   of these headers exist until cutover, and Deployment Protection has to
   come off in the same move (see §0 item 8, which also carries the
   last-updated date on the policy).


---

## 32. The deploy read a different file than the one it uploaded

Everything in §30 and §31 was verified before shipping and the site still
went out broken, in the one place nothing in this repo can see.

### What happened

`ship.sh` ended in `vercel deploy --prod --yes --cwd dist`. That uploads
`dist/`, and then **reads `vercel.json` from the shell's working directory**,
which `ship.sh` had already set to the repo root. Those two files are
deliberately not the same: `build.py` seals the CSP script hashes into
`dist/vercel.json` and the root copy was left holding the placeholder.

So production received a `script-src` containing the literal string
`__INLINE_SCRIPT_HASHES__`. A browser drops a source expression it does not
recognise and **enforces the rest of the directive**, so the effective policy
was `script-src 'self' <two origins>` with no hashes at all, and every inline
script on the site was blocked: the analytics config, the `js-motion` flip,
and the Flodesk signup on `/the-letters/`.

**The HTML was right. The CSS was right. The build was right. Only the header
was wrong**, and the header is the one artefact that no part of this project
had ever looked at, because the preview server sends none and the suite runs
against the preview server.

### How it was found, which is the part worth keeping

By curling the deployment after shipping instead of trusting the build log.
The build had printed `CSP sealed with 3 inline script hash(es)` and it was
telling the truth about the file it sealed.

Two deploys with `--cwd` reproduced it. The same `dist/` deployed from inside
`dist/` came out correct, which is what confirmed the cause rather than
guessing at it.

### The three locks, because one was not enough

1. **`ship.sh` cds into `dist/`** rather than passing `--cwd`. Never put it
   back.
2. **`seal_csp()` now seals both copies**, dist and root. There is no longer
   a deployable `vercel.json` anywhere in this repo carrying an
   unsubstituted placeholder, so a stray `vercel deploy` from any directory
   cannot reproduce this.
3. **`ship.sh` curls the deployment afterwards** and fails loudly if the
   placeholder appears or any required header is missing. Plain `curl` is
   useless while Deployment Protection is on, so it goes through
   `vercel curl`.

### The general lesson for this codebase

The suite is thorough about markup, geometry, fonts and behaviour, and it is
structurally blind to response headers, because it tests a static server that
sends none. **Anything configured in `vercel.json` is unverified until
something asks production for it.** That is now the last step of `ship.sh`
rather than a thing to remember.


---

## 33. Session twenty-three: twelve events, and nine frictions

### The measurement plan

`assets/js/analytics.js`, twelve events, documented in
`tools/analytics-reference.html` and tested by `tools/preview/runga.sh`.

**It is a separate file from site.js on purpose.** site.js is the site
working; this is the site being watched. Keeping them apart means a
measurement change can never be the reason a carousel stopped moving, and the
whole thing can be removed in one line. Every listener is delegated off
`document`, nothing calls `preventDefault`, nothing writes to the DOM. The
behaviour suite was **356 pass / 0 fail before and after**, which is the
evidence that "without modifying existing functionality" actually held.

### Two of the four things asked for do not exist on this site

Copy-to-clipboard on code samples, and filter/search on component listings.
There is not one `<pre>`, `<code>`, clipboard call or search input anywhere in
the nine pages — it is a consulting practice, not a documentation site.
**Nothing was invented to fill the gap**, because a tracker firing on an
element that does not exist produces a number nobody can act on. The nearest
real equivalent, the four-tab objection picker, is tracked as `filter_select`
because it genuinely is one. This is written up on the reference page rather
than buried here, since the reference page is the thing anyone will read.

### Three bugs the harness caught that review would not have

Every one of these produced plausible, wrong data rather than an error.

1. **Every desktop header click reported as `mobile_menu`.** `.nav-menu` is
   one element serving both the bar and the phone panel, and `has-menu` is on
   the root at every width, so neither the markup nor that class can tell them
   apart. Only the width can. Reads as a site whose visitors are almost
   entirely on phones, using a menu most of them never open.
2. **`menu_toggle` was exactly inverted.** site.js registered its click
   handler first and flips `aria-expanded` inside it, so a bubble-phase reader
   always saw the state already changed. Every open reported as a close. Now
   on capture.
3. **`video_start` never fired at all**, for the same reason: site.js adds
   `is-playing` before a bubble-phase listener can check for it. Also on
   capture now. The same click was additionally being counted as an
   `outbound_click` it never makes — the poster carries a real YouTube href as
   a no-JS fallback, and with JS it never navigates.

**The pattern in all three: site.js is the earlier `<script>`, so it always
gets the bubble phase first.** Anything in analytics.js that needs to read
state site.js is about to change has to be on capture.

### `tools/preview/runga.sh`, and why the pane cannot test this

Analytics is not state, it is a sequence of things that happened, so it can
only be tested by performing the interactions and watching what comes out.

**Setting `scrollTop` in the Claude preview pane moves the page and fires no
scroll event at all.** Measured: a plain `window.addEventListener('scroll')`
counted zero while `pageYOffset` went 0 → 4000. Every `scroll_depth`
assertion read as a failure against code that was correct. Same family as the
IntersectionObserver failure in session four.

Headless Chrome was not the whole answer either: in an `opacity: .001` iframe,
the kind `_test.html` uses, **neither `scroll` nor `requestAnimationFrame`
runs** — measured `raf=0`, `rawScroll=0`. The frame is opaque in `_ga.html`,
and the harness dispatches the scroll event itself. That is not testing around
the problem: a browser firing `scroll` when a document scrolls is platform
behaviour, and everything downstream of it — the arming gate, the threshold
arithmetic, firing once each across down-up-down — is ours and is exercised.

`analytics.js` also no longer depends on rAF actually running: the scroll
measurement is `requestAnimationFrame` **or** a 200ms timeout, whichever wins.

### One thing that bit twice in one session

`stamp.py` and `build.py` each had their own copy of the `?v=` arithmetic.
Adding `analytics.js` to the stamped set made them disagree and the build
refused to run. **The guard was right and the duplication was the bug**;
`build.py` imports `stamp.version()` now, and the stale-stamp scan looks at
`analytics.js` too, or a stale stamp on the new file would be invisible to the
guard that exists to catch it.

    suites now:   behaviour  356 pass / 0 fail across nine pages
                  analytics  141 pass / 0 fail across nine pages

### The interface review

`tools/ux-review.html`. Nine findings, every one measured on the built site at
375 and 1440 rather than eyeballed, ordered by cost rather than by effort.

**The headline is that seven of the nine are the same shape:** a decision that
is correct in one context, applied in a second one where it stops working.

| | | |
|---|---|---|
| 1 | In-copy links draw their underline only on hover, and measure **1.00 to 2.49:1** against the text around them. `hello@cydniejocelyn.com` is the *identical* colour. No hover on a phone, so on touch they are not links at all. | High |
| 2 | `:focus-visible` is `--breath` at every ground. **10.14:1** on Fathom, **1.36:1** on Silt — and **32 of 66 interactive elements on the home page sit on a light band.** Reusing `--accent` is not the fix; it is 2.34:1 on dark. Wants its own ground-aware token. | High |
| 3 | The Letters email field is `type="text"`. No email keyboard on a phone, for the conversion the site funnels toward. Flodesk's markup, so it is a setting rather than a commit. | High |
| 4 | That form has **zero live regions** and no `aria-invalid`. A failed signup is announced to nobody, so the reasonable conclusion is that it worked. | High |
| 5 | **Every `[aria-current="page"]` rule lives inside `@media (max-width: 55.99rem)`.** At 1440 the current nav link measures **1.00:1** against its neighbours. The markup is right and a screen reader announces it; sighted desktop readers get nothing. | Medium |
| 6 | All **14** external links open in the same tab unmarked, including the booking button that hands the reader to HoneyBook's differently-branded scheduler after twenty screens of a very specific voice. | Medium |
| 7 | `.gauge` is a fixed vertical track with a moving indicator and **no handler**. On pages of **20.5 screens** it reads as a scrubber, invites a drag, and does nothing. No back-to-top anywhere. | Medium |
| 8 | The Greece rail holds **16 photographs, 3 visible**, with a progress rule but no count. A reader who misses the affordance sees a three-photograph gallery. | Low |
| 9 | The questions are exclusive accordions, so opening one closes the answer you were comparing it against. Deliberate, and asserted in the suite. | Low |

**Findings 1, 2 and 3 are the three to do.** The first two are single-rule CSS
edits that between them fix the site for touch readers and keyboard readers
and change nothing for anyone else. The third is the only one costing
subscribers today.

### What the review says NOT to change

Written down because a generic audit would flag all of these and be wrong.
The 18px door links are grown to 44px by `.door-note--link::after { inset:
-13px -10px }`, which is a better answer than a min-height and has its reason
in a comment already. Inline text links under 24px are explicitly exempt from
the target-size rule. Click-to-load `youtube-nocookie` is right twice over.
Smooth scrolling is already off under `prefers-reduced-motion`.


---

## 34. Session twenty-three, part two: the nine fixed, and the hero measured

All nine frictions from §33 were fixed. The suite went **356 → 385
assertions, 0 failing**, and six of the new ones exist to stop these specific
things coming back silently.

### The ones that were one rule each

**Inline links draw at rest.** `.link::after` was `scaleX(0)` until hover and
now retracts on hover instead. The note that used to sit above it said the
shared `.link` was being left alone because changing it moves five shipped
pages — the measurement is what overruled that: 1.16:1 for "Watch Melissa's
review", **1.00:1** for the email address, against the text around them. Not
dim, not there. The rule is an absolutely positioned pseudo element, so those
five pages changed in colour and not in layout.

**Focus got its own ground-aware token, `--focus`.** `--breath` was named
directly, which is 10.14:1 on Fathom and **1.36:1 on Silt**, with 32 of the
66 interactive elements on the home page sitting on a light band. Now 13.79
and 14.93 there. **`--accent` was checked first and is not the answer**: it
resolves to Meniscus on dark, 2.34:1. Focus needs the opposite end of the
palette from its ground, which is a different job from accent.

**`[aria-current="page"]` applies at every width.** Every rule that coloured
it lived inside `@media (max-width: 55.99rem)`. It is paired with a hairline
rather than shipped as colour alone, and the surfaced state is stated
explicitly at (0,4,1) because `.hdr.is-surfaced .nav-links a` is (0,3,1) and
is the same specificity trap that blanked the menu in session seven.

### The Flodesk form, repaired from outside

`initSignup()` upgrades the email field to `type="email"` with `inputmode`
and `autocomplete`, and mirrors the widget's error text into a
`role="status"` region with `aria-invalid` on the fields. Before this a
screen reader user pressed the button and heard nothing.

**It keys on the visible label text, and that took two goes.** Field `name`
and `placeholder` are randomised per render as an anti-bot measure — the
email input was `mLYUaHN` on one load and `T1U9Mlg` on the next. So is the
label, in a subtler way: Flodesk splits it into decoy spans and hides one, so
`textContent` reads **"YourI email"** and only `innerText` reads "Your
email". The live region announced the decoy out loud before that was found.

This reaches into somebody else's DOM and is written to fail silently rather
than throw. **The durable answer is owning the form.**

### Off-site links, and the two that no source pass could see

53 off-site links now carry an announcement. 38 social and video links open
in a new tab; booking stays in the tab, because a purchase flow should not
open one, and carries a hidden "opens my scheduling page".

**Two were invisible to a search of the nine pages and the suite caught
both.** "Book a Sounding" is injected by `sounding-popup.js`, and Flodesk's
own "Privacy policy" link does not exist until their script runs.

**And one was a lie in the other direction.** The video poster is an
`<a href="youtube.com/...">` so it works without JS; with JS it never
navigates. It had been given `target="_blank"` and an announcement, both
false the moment `initVideo` runs, so `initVideo` now strips them and sets an
accurate label instead. The label is set as an *attribute* because the click
handler does `a.innerHTML = ""` to make room for the iframe, which destroys
any hidden span inside it — which is exactly how the assertion caught it.

### The other three

The rail says **"1 / 16"**. The questions no longer close each other, and the
suite assertion that encoded the old behaviour was inverted with the reason
written beside it. The gauge takes `pointer-events: none` and a "Back to the
top" link sits at the head of every footer, in the flow rather than floating.

**Two things were deliberately NOT done, and both are Cydnie's call, not
defects.** The visible line under the booking button is copy on nine pages
and a change to the header composition. And the gauge was not redrawn:
making it read as instrumentation rather than as a track is a change to the
visual identity on every page.

### The hero headings did get bigger, and here is by how much

Reported as a feeling, and it is correct. **`font-size` never changed** — the
same 69.6px at 1440, same line height. The typeface changed in §30.

    at an identical 100px      Instrument Serif   IvyJournal   change
    cap height                       66.2            72.8      +10.0%
    x-height                         44.9            53.1      +18.3%
    width of "YOU'RE NOT BROKEN."   1067.6          1130.0      +5.8%

**The x-height number is the one that explains the feeling.** x-height, not
point size, is what the eye reads as "how big is this type". Compounded with
the extra width, the home hero went from two lines to four at 1440.

**If it is ever pulled back, the factor is 0.91**, which matches the old cap
height and is the right target for an all-caps hero. Matching x-height
instead wants 0.85, which suits mixed-case headings like "I'm Cydnie." and
would leave the hero smaller than it used to be. One number cannot serve both
perfectly; 0.91 is the one to try first. **Not applied** — nothing is broken
and it is a taste decision.


---

## 35. Session twenty-three, part three: the kit was the licence, not a restyle

Reported as "my hero headers got bigger... too big now and potentially wrong
font", and then, decisively: **"Fonts were just the key for Adobe, not to
change the site."**

That is the whole thing. The Adobe kit was supplied so the licence would be
in place. §30 read it as an instruction to put the licensed face on the site,
put `ivyjournal` at the front of `--carved`, and changed the appearance of
every heading on all nine pages as a side effect. **Reverted.**

### What the change actually did, measured

`font-size` was never touched. The typeface was, and these two faces are
simply bigger letters at the same nominal size. At an identical 100px,
against Instrument Serif:

    ivyjournal       cap +10.0%   x-height +18.3%   caps width +5.8%
    ivypresto-text   cap +10.0%   x-height +16.7%   caps width -2.9%

**x-height is the number that explains the complaint.** x-height, not point
size, is what the eye reads as "how big is this type", so an 18% increase at
an unchanged `font-size` is very visible. The home hero went from **two lines
to four** at 1440. It is two lines again.

### The kit had changed under us, which is worth knowing

The first fetch, 18:41 UTC, returned one family: `ivyjournal`. The kit was
republished at **20:12 UTC the same day** and returned two: `ivyjournal` and
`ivypresto-text`. That is how "potentially wrong font" was diagnosed rather
than guessed — the browser reported eight `@font-face` rules where the
morning's kit had four.

**Neither of them is IvyPresto _Display_**, which is the family the brand
board names and the one the codebase spent eight sessions waiting for.
`ivypresto-text` is the text cut: sturdier hairlines, looser spacing, drawn
for paragraphs rather than for a 70px headline. If the licensed face is ever
wanted on the site, that distinction matters more than the name matching.

### What the site does now

`--carved` is `"Instrument Serif", Georgia, serif` and **Instrument Serif is
named first because it is the only thing that renders.** That rule is now
stated in the stylesheet, because naming a family nothing serves is exactly
what let `"IvyPresto Display"` sit at the front of this token for eight
sessions while looking correct.

The kit `<link>` and its two preconnects stay in all nine heads. **The site
asks for none of the kit's faces, so no font file is fetched from Adobe** —
the cost is the kit stylesheet itself, which is render blocking, plus the
`p.typekit.net` stylesheet it imports. That is the price of having the
licence embedded, and it is worth a decision rather than a default. It is
listed as an open item.

The Instrument Serif preload is back on all nine pages, because it draws the
first screen again.

### The two assertions that were asserting the wrong thing

The suite briefly checked that `ivyjournal` was loaded and that Instrument
Serif was *not* preloaded. Both now check the reverse, with the reason
written beside them, and one new one checks that **no kit family appears in
`--carved` at all**. A test that encodes a decision has to be turned around
when the decision is, which is cheaper than discovering later that the suite
was defending the wrong behaviour.

    behaviour  383 pass / 0 fail across nine pages
    analytics  141 pass / 0 fail across nine pages

### The general lesson, and it is not a small one

**Being handed a credential is not being handed a design instruction.** The
kit link arrived in a message about legality, and it was read as a brief. The
tell was available and was written down at the time and then not weighted:
§30 records that the kit contained IvyJournal rather than the IvyPresto the
entire codebase named, and it wired it in anyway on the reasoning that
`--carved` was the only serif slot. The right move on a mismatch that size is
to make the licence work and leave the appearance alone until somebody says
otherwise.


---

## 36. Session twenty-three, part four: the display scale came down

Reported as "in the heroes they are massive and on mobile especially the home
page, it doesn't flow well". Both halves are true and the second one has an
arithmetic explanation that is worth keeping.

### Why mobile was the worse half

Every size in the display scale is a `clamp(min, vw, max)`. **At 375 the vw
term is below the minimum in all 26 of them**, so every heading on the site
renders at its floor. The scale did not scale down on a phone; it collapsed
into a narrow band of large sizes with almost no hierarchy left:

    at 375, before        .ab-head h1 44.0   .rt-count b 41.6
                          .h-1 30.4   .hero-line 29.6   .c-1 27.2
                          .c-2 25.6   .h-2 24.0   .c-3 22.4   .h-3 18.4

Fourteen of those sit within 8px of each other. **The About hero was 44px on
a 375px screen**, which is the single largest thing on the site at the width
where there is least room for it.

### One factor set, applied to all 26 at once

    min x 0.82      vw x 0.93      max x 0.90

Doing it uniformly is the point. **Every relationship in the scale is
preserved by construction** rather than by twenty-six separate judgements,
including the one the file already documented: `.c-1` is deliberately larger
than `.h-2` because the carved face has the smaller x-height and needs the
extra size to read optically level. That ratio is identical after.

The minimum took the largest cut because the minimum is what mobile actually
uses. The maximum came down 10% because "in the heroes they are massive"
is a desktop observation as well.

    at 375, after         .ab-head h1 36.0   .rt-count b 34.1
                          .h-1 24.9   .hero-line 24.3   .c-1 22.3
                          .c-2 21.0   .h-2 19.7   .c-3 18.4   .h-3 17.3

    home hero at 1440     69.6 -> 62.6, still two lines
    About hero at 1440    80.0 -> 72.0

### Three minimums were floored back up

`.h-3`, `.lt-sig` and the questions list came out at **15.1px, below the 18px
body copy they sit among**. A heading smaller than its own paragraph inverts
the hierarchy rather than tightening it, so those three are floored at
1.08rem. **1.08rem is the floor for anything in this scale.**

### Verified

45 checks, nine pages at 320, 375, 390, 768 and 1440: **no horizontal
overflow anywhere, and no heading spilling its container**. Suites unchanged
at 383 and 141, both green.

The About head rule clearance — the measurement §29 was written about and
which once rendered at **-13px** — is **55px at 375, up from 46**. Smaller
headings mean a shorter copy block, and the clearance is whatever is left
after the copy takes its height, so it moved the right way.

Three unclassed `<h3>` elements measure 12px and were deliberately left
alone: they are the footer column labels, small caps by design, and never
part of this scale.

### What this did NOT fix, and it is the actual "flow" complaint

**The home hero is still 982px tall in an 812px viewport at 375.** The type
reduction took 17px off it. The other 170 is structural: `.hero-copy` is
518px and `.hero-path` — the Resurface / Reclaim / Build list that sits to
the right on a desktop — **stacks underneath it on a phone and adds 238px**.
So the fold lands inside that list and a reader sees it truncated.

No type change closes a 170px gap. The options are to lay the path out
horizontally under the copy, to drop it from the hero on mobile (it is
repeated further down the page), or to let the hero be taller than a screen
on purpose. **All three are composition decisions, so none was taken.**


---

## 37. Session twenty-three, part five: four corrections, one of them mine

Reported together: the mobile hero is now too small, all headers are too
small, there is a massive dark gap between the hero and the next section, and
"everyone who needed you" blends into the page.

### The scale was over-cut, and that was an overcorrection

§36 took the minimums down by 0.82. That was too far — it read as "massive"
before and "too small" after, so the honest answer is that the type was never
the main problem and the cut absorbed blame that belonged to the gap below.

Rebalanced **from the original values, not from the over-cut ones**, so two
rounds of rounding do not compound:

    min x 0.95      vw x 0.98      max x 0.93

    at 375   hero-line 29.6 -> 24.3 -> 28.1     .c-1 27.2 -> 22.3 -> 25.8
             ab-head h1 44.0 -> 36.0 -> 41.8    .h-2 24.0 -> 19.7 -> 22.8

The maximum keeps the larger cut, because "in the heroes they are massive"
was a desktop observation and remains true there: the About hero is 74.4px at
1440 rather than 80.

### The dark gap was never the type

Measured at 375: the last hero content ended at **918**, the hero at 982, and
**the first text of the next section did not appear until 1238**. A 320px run
of empty dark ground, which is most of half a screen.

Three things stacked into it. The `.cond` stage is `100svh` with
`align-items: center`, so on a phone about 320px of content was centred in
650px of remaining stage and pushed a further 165px down. The hero carried a
desktop-sized 64px floor under its last line. And the header clearance
padding sat on top of both.

On a phone the stage is `align-items: flex-start` now with tighter padding,
and the hero's bottom padding drops to `--s-5`. **320px -> 153px.**

**`--cond-run` was NOT touched.** The note above it says not below about
30svh, because a step shorter than one thumb flick can be skipped unread and
the five recognitions ARE the argument of that section. That reasoning still
holds. This shortened the approach, not the steps, and the section is still
2330px because that length is deliberate.

### --accent failed as text on a dark ground for the third time

`.head em, .carved em` used `var(--accent)`. On Fathom and Deepwater that
resolves to **Meniscus #2F5A61, which is a rules colour**, and "everyone who
needed you." in the home turn heading measured **2.02:1** against its ground.
Reported as "it blends in with the page overall", which is exactly what
2.02:1 looks like to a reader.

It is `var(--label)` now — the ground-aware token that already existed for
this: Breath on the dark grounds, Deepwater on the light ones. **2.02 -> 8.76
across all five instances at all five widths.** The italic was never the
problem and is untouched.

This is the third instance of the same mistake, and §0 already lists the
pattern. **The suite now asserts the measured contrast of every `em` inside a
heading rather than asserting the token name**, because naming the right
token is not the same as the result being readable.

    behaviour  384 pass / 0 fail across nine pages
    analytics  141 pass / 0 fail across nine pages
    45 layout checks at 320, 375, 390, 768, 1440: no overflow, no spill


---

## 38. iCloud took a production deploy down, and there was no bad commit

The deploy after §37 failed with:

    ENOENT: no such file or directory, scandir '.../dist/privacy-policy 2'

**This project lives on the Desktop and the Desktop is synced to iCloud
Drive.** `build.py` does `shutil.rmtree(DIST)` and recreates the whole tree on
every run, and iCloud reads a wipe-and-recreate as a conflict, so it writes
duplicates beside the real thing:

    dist/about 2   dist/assets 2   dist/assets 3   dist/privacy-policy 2
    dist/the-build 2   dist/sounding-popup 2.js   dist/.vercel/README 2.txt

`vercel deploy` listed the directory, began walking `privacy-policy 2`, and
iCloud removed it mid-scan. **A failed production deploy with no bad commit
behind it**, which is the worst kind to debug from the error text alone.

Even when they survive the scan they are stale part-copies of real routes,
and they would be uploaded. `dist/assets 2` had in fact been sitting there
since §31, where it was noticed, assumed to be Finder cruft, and not
explained. It was this.

### The fix, in two places on purpose

`build.py` sweeps them at the end of every build, and **`ship.sh` sweeps
again immediately before the upload**, because iCloud can write a fresh one
in the seconds between the build finishing and the deploy starting. Belt and
braces is right here: the single-sweep version would have passed every local
test and still failed at the same point.

Nothing legitimate in `dist/` is named `<something> <digit>` — every byte of
it is generated by `build.py` — so the shape is safe to delete on sight.

**If this project ever moves off a synced folder, both sweeps can go.** Until
then they are load-bearing, and the deploy is the only place the failure
shows.


---

## 39. Session twenty-three, part six: the void was the pin, not its placement

Two rounds were spent moving the empty space around the story scroll before
the actual answer turned up, and the failed attempts are the useful part.

### The arithmetic that made it unwinnable

The pinned block on `#condition` is about **355px on an 812px screen**, so
roughly **330px of viewport is unused no matter where it sits**. Leading gap
plus trailing gap is a constant. Every arrangement only moved the void:

| | leading | trailing | |
|---|---|---|---|
| centred, as built | 320 | 327 | reported as a massive dark gap |
| `align-items: flex-start` | **153** | 327 | fixed the approach, created the exit |
| centred, inner gap 18vh | 259 | 147 | leading went straight back up |
| centred, inner gap 26vh | 228 | 116 | and a **208px hole in the middle**, between the ticks and the recognition, which read worse than either end had |

The third and fourth rows are the ones worth keeping. Opening the inner gap
is the only change that alters the constant at all, because it is the only
one that makes the content taller — and pushed far enough it just relocates
the void into the middle of the composition.

### The fix: a pin needs a screen with room for one

`roomy()` in `initCondition` tested `innerHeight >= 520` and nothing else,
and **height was never the binding constraint**. A 375x812 phone passes that
comfortably and then pins a 355px block in an 812px viewport.

It now also requires **`innerWidth >= 768`**. Below that the five
recognitions render as the plain stacked list this component was always
built to fall back to — the note at the top of the function has said so from
the first build.

    at 375   section height  2330 -> 1249     2.87 screens -> 1.54
             leading gap      320 -> 104
             trailing gap     327 ->  40      ordinary section spacing
             home page       17489 -> 16581

Verified the gate flips at exactly 768: stepped at 768, 1024, 1440; list at
320, 375, 390, 767. **The stepped reading is untouched from 768 up**, which
is where the stage is wide enough for the pinned block to be a composition
rather than an island.

### And the section padding floor, which was the same bug as the type scale

Surveyed across **78 sections on nine pages at 375**: the median distance
from a section's top edge to its first line of text was **40px, and so was
the minimum**. `.section` is `clamp(2.5rem, 7vw, var(--s-9))` and the vw term
is below the minimum on a phone, so every section sat on its floor — 40px
between a colour band changing and a small caps eyebrow, against **128px of
the same space on a desktop**. A 3.2x difference, on the device that got the
floor.

This is the third component found with the same shape this session: the type
scale, the story scroll, and now the section rhythm. **On this site, if
something feels wrong on a phone, check whether its `clamp()` minimum is
doing all the work before changing anything else.**

    .section        clamp(2.5rem,  7vw, --s-9)  ->  clamp(3.5rem, 7vw, --s-9)
    .section--tight clamp(--s-5,   5vw, --s-7)  ->  clamp(2.75rem, 5vw, --s-7)

    median top-to-first-text at 375   40 -> 56,  minimum 52, none under 50

It also buys back headroom the seam was short of. `[data-zone]::before` is
32px at this width and is painted from the top of the section, so it had 8px
of clearance before the first line and now has 24px. Checked across all 75
zoned sections: **no seam is taller than its section's padding.**

    behaviour  384 pass / 0 fail
    analytics  141 pass / 0 fail


---

## 40. Session twenty-three, part seven: I removed an interaction nobody asked me to

§39 closed the spacing around the story scroll by gating the pin to 768 and
up, which turned the whole component into a static list on every phone.
**That was not asked for and it was the wrong trade.** The instruction was
about spacing. The interaction is the component.

Reverted. `roomy()` is back to `!reduce.matches && innerHeight >= 520`, and
the pin runs at every width again.

### What actually closes the gap, and why the earlier reasoning missed it

**A sticky element releases when its own bottom reaches its container's
bottom.** With `.cond-stage` at exactly `100svh` it releases at the same
instant the next section enters the screen, so the two then scroll together
with the whole unused ~330px locked between them, permanently. That is why
every attempt to *place* the leftover space failed: the space was not
misplaced, it was pinned in.

Make the stage its own content's height and it stays stuck for another
`viewport - stage` of scroll, so **the next section rises to meet the pinned
block instead of travelling beside it**, and the gap closes as you scroll.

    .cond.is-stepped .cond-stage  { height: auto; min-height: 32rem; }
    .cond.is-stepped .cond-track  { height: calc(32rem + span * run); }

Step pacing is untouched: `progress()` already divides by
`stage.offsetHeight`, and the track's base term moves with it, so `run` comes
out identical and each recognition is worth the same scroll it always was.

    at 375   leading gap 153            (was 320 as built)
             trailing 188 -> closes to 41 as the next section rises
             section 2330 -> 2030,      2.87 screens -> 2.50
             all five recognitions light, in order, at 320, 375 and 390
             desktop stage still exactly one viewport at 768 and 1440

### Two assertions, and a lesson about where they run

The suite only ever ran at 1280, so **deleting a mobile interaction was
invisible to it**. It now builds a second 375x812 frame and asserts the
component still steps there, and that the stage is content sized.

The first version of that guard did not count. It created the frame at
assertion time and read it on a 1400ms timeout, which fired after `done()`
had rendered the log — two assertions that always passed because they never
ran. The frame is created on load now, gets the same six seconds as the main
one, and is read synchronously. **If a guard is not in the tally it is not a
guard.**

The second version was also wrong, in a more ordinary way: it asserted the
stage was well under the viewport, which is true on the home page and false
on Greece, whose recognitions are longer copy and whose stage is legitimately
787 of an 812 screen. The property that matters is not that the stage is
short, it is that it has **zero slack** — the height IS the content plus the
padding. That holds on both.

    behaviour  386 pass / 0 fail
    analytics  141 pass / 0 fail


---

## 41. The stylesheet was duplicated for two commits, and nobody could see it

`site.css` went from **4641 lines to 6976** in §39 and stayed there through
§40. About 2,300 lines were duplicated, and both commits shipped that way.

### How

A scripted edit computed its own splice bounds:

    start = s.index("  /* SECOND PASS.")
    end   = s.index("  }\n", s.index(".cond.is-stepped .cond-in {"))

`s.index(".cond.is-stepped .cond-in {")` matched the **first** occurrence in
the file — `.cond.is-stepped .cond-in { width: 100%; }` at line 1266, which
is thousands of lines ABOVE the block being edited. So `end` came out smaller
than `start`, and `s[:start] + new + s[end:]` did not cut anything out. It
**re-inserted everything between the two points.**

### Why nothing caught it

CSS is forgiving: duplicate rules are legal and the later copy wins. So the
build passed, the suite passed 384/0, the deploy succeeded, and the site
rendered — **using the stale copies**, because they came last in the file.
That is why the story scroll kept showing the 26vh inner gap and the
`align-items` value from an experiment that had supposedly been removed two
commits earlier. The rules had been removed. Their duplicates had not.

**The tell was visible and was misread.** §39 recorded `cond-stage-rules=3`
in a grep before committing. Three rules for a component with two is the
whole story, and it went past as noise.

### The rule that comes out of it

**Never compute a splice bound from an unanchored `str.index` in a 4,000 line
stylesheet.** Two selectors in this file differ only by which media block
they sit in, and `index` cannot tell them apart. Either match a string that
is unique in the whole file, or slice the media block first and edit inside
it.

**And check the line count after any scripted CSS edit.** A 50% jump is not
subtle once anyone looks; nothing in the build, the suite or the deploy looks.

### The repair

Restored from `26ea8cb`, the last clean version, and re-applied the two
intended changes by hand: the section padding floor and the stage padding
trim. Verified afterwards that every rule from the intervening work is
present exactly once — the carved token, the rebalanced type scale, the
`--label` emphasis fix, `--focus`, the ruled inline links, the inert gauge,
the section floor — and that four structural sentinels each appear once.

    4641 clean  ->  6976 corrupt  ->  4669 repaired

---

## 42. And the condition block is centred, which is where it started

Four passes were spent trying to place the leftover viewport around the
pinned block, and every one was worse than leaving it alone:

    centred, as built        leading 320   trailing 327
    align-items: flex-start  leading 153   trailing 327
    inner gap 18vh           leading 259   trailing 147
    inner gap 26vh           leading 228   trailing 116, and a 208px hole
                             between the numbers and the recognition
    content sized stage      block at 103 above / 354 below, top heavy

The block is one short statement on a dark field and it belongs in the
optical middle of the screen. It is `align-items: center` again, at 253
above and 204 below — the extra on top is the fixed header's own space, so
that reads as centred rather than measuring as it.

**`.cond-in` is not a dial for section spacing.** The gap between the numbers
and the recognition is the component's own `--s-6`, 32px, and using it to
absorb section rhythm is what put a hole through the middle of the
composition. Two assertions now hold both facts: the block is centred at 375,
and that inner gap is under 72px.

What survives from the four passes is the part that cost nothing: the stage's
padding came down from 105/57 to 89/41 and the hero stopped holding a
desktop-sized floor under its last line. **68px off the approach with nothing
moved and nothing stretched.**

    behaviour  388 pass / 0 fail
    analytics  141 pass / 0 fail


---

## 43. Three asks: the kit out, the Greece images down, and real consent

### The Adobe kit is gone

Measured on production before removal: **render blocking, pulling a second
blocking stylesheet from `p.typekit.net`, and 243 to 323ms of DNS, TLS and
transfer for 6.2KB that drew nothing.** It was the only third party on the
critical path of a site that self hosts its type precisely to avoid one.

Nothing on any page asked for `ivyjournal` or `ivypresto-text` — that was
verified live before it came out. **An Adobe Fonts licence is not conditional
on the kit being linked from a page that does not use it.** The two
preconnects went with it, and the typekit origins came out of `style-src` and
`font-src`. The suite now asserts the ABSENCE of any typekit link or face,
because a link added back "for the licence" would be invisible in every other
check.

### The Greece images were a page problem, not one image

The flagged 213KB photograph turned out to be one of nine. **Every candidate
set on that page jumped 600w to 1200w, and a 375px screen at 2x needs 750** —
so a phone took the 1200 every time. A full scroll-through downloaded
**1,947KB**.

900w is already the convention on that page: eight images had one. The nine
that did not now do. Each was encoded to match **its own 1200w file's bytes
per pixel** rather than one blanket quality, by binary searching the WebP
quality per image, and checked with SSIM against a LANCZOS reference:

    the nine files       2008KB -> 1141KB   (-43%)
    SSIM                 0.9601 to 0.9826   (0.95 is the floor this repo uses)
    the page on a phone  1947KB -> 1479KB

### Consent, done the strict way

`gtag.js` is no longer in any page head. `assets/js/consent.js` injects it,
and **only after a reader accepts**.

**The choice that matters is which of the two implementations this is.** The
common one is Google's Consent Mode alone: load the tag immediately, declare
`analytics_storage: denied`, send cookieless pings until the reader agrees.
No cookie is set, which satisfies most cookie rules — but the reader's IP and
the page they are on still reach Google before they agreed to anything. This
site does the other thing: **before consent there is no `gtag`, no
`dataLayer`, and no request to any Google domain at all.** Consent Mode
defaults are set as well, as a second lock for any future change that loads
the tag earlier.

`analytics.js` needed no special case. It already guarded every send with
`typeof gtag !== "function"` and returned silently — written for ad blockers,
exactly the right shape for this. **That is also why `gtag` is deliberately
not defined as a `dataLayer` stub before consent:** a stub would let events
pile up and be flushed the moment the tag loaded.

Two things the first version got wrong, both found by testing rather than
review:

1. **Declining did not remove what was already there.** Analytics ran
   unconditionally on this site for days, so a returning reader arrives
   already carrying `_ga` and `_ga_KDB3GWPNHC`. A decline that stores "no"
   and leaves those in place changes nothing. Decline now clears them, across
   the bare host, the dot-prefixed domain and the registrable parent, because
   a delete only lands when domain and path match what set it.
2. **Escape dismissed the banner from anywhere on the page.** The Greece
   lightbox closes on Escape, so shutting a photograph silently answered a
   consent prompt two components away. Escape now only reaches the banner
   when focus is inside it.

The policy copy changed with it: implied consent ("continuing to use the site
means you accept them") is gone, replaced with what actually happens, plus a
**Change your cookie choice** control that any `[data-cookie-settings]`
element on the site gets wired to.

### The suite

The old assertions checked `gtag.js` was in the head, which is now exactly
the wrong thing. They assert the negative instead — banner shown, no gtag, no
`dataLayer`, no googletagmanager script — and then, **last**, that accepting
injects the tag. Order matters: run the accept first and every "nothing
before consent" assertion passes for the wrong reason. That happened once.

`runsuite.sh` reuses `--user-data-dir` between runs, so one early run that
clicked Accept left the choice stored and the banner never appeared again.
The harness clears the key before loading the page under test.

    behaviour  439 pass / 0 fail across nine pages
    analytics  141 pass / 0 fail

---

## 44. Session twenty-four: the brief, the contact page, and a deploy that had been lying

**Written at the end of session twenty-four, 29 August 2026, to hand over cleanly.**
Everything below is committed, pushed and deployed. Verified, not assumed:

    git status --short          empty
    main vs origin/main         0 ahead, 0 behind
    all ten pages               byte identical to dist/, over plain curl
    suite                       456 pass / 0 fail, nine pages
    tools/seams.py              0 mismatches

### Read this first: production was serving the source, not the build

For an unknown number of deploys, `vercel deploy` from inside `dist/` uploaded
the **repository root**. Every page went out as its source: 38,362 bytes
against 26,731 built on /about/, 43% more on the wire, with all 25 HTML
comments per page shipped to readers. `tools/build.py` was being defeated at
the last step and nothing said so.

The cause is the race section 38 already describes. iCloud writes conflict
copies into `dist/` after `build.py` recreates it, and a stray `assets 3` was
sitting there when the upload ran. The existing sweep runs **before** the
upload; iCloud wrote after it.

`ship.sh` now has two guards and both are load bearing:

  * before deploying, it **refuses outright** if a conflict copy is still in
    `dist/`, and prints which one. An aborted ship is cheap.
  * after deploying, it counts HTML comments on the live /about/ and compares
    against `dist/`. `build.py` removes every comment, so any comment on
    production means the wrong directory went up. It says so and does not
    call it shipped.

**How this went unnoticed for so long:** every verification used
`vercel curl`, which routes through Vercel's own network, and compared
*markers* rather than whole files. Source and build carry the same words, so
every marker matched. Use plain `curl` and compare a checksum against `dist/`.
Nothing else is proof.

### What shipped, against Cydnie's brief

The brief arrived as `claude-code-brief.md` with two reference files. Phases 1
through 4 are done and live. **Phase 5 is not started.**

  * **Phase 1**, all eleven text tasks on the home page. Headline is now
    "Nothing is wrong with you. Something is on top of you." No price in the
    hero: all three buttons read "Book one conversation", on Cydnie's call.
  * **Phase 2**, the restructure. New section order, the one Deepwater band,
    the contact block, the ladder reversed so A Sounding leads, the thesis
    image swapped, Why me cut to two paragraphs.
  * **Phase 3**, `/contact/`, new. Built from this site's own header, footer,
    stylesheet and type, not forked from the reference file.
  * **Phase 4**, the nav button is **Contact** on all ten pages, and the
    footer Contact points at `/contact/`.
  * Plus, after the brief: the proof carousel reordered to lead with a
    consulting voice and alternate the two businesses, with SRS and Angela
    added.

### The brief was written against an older site

Six of Phase 1's sixteen find-and-replace targets no longer existed. Three
were already done; three had been changed to something different. **Check
before running any remaining instruction from that file.** Two more:

  * It names a **Client work** section at position ten of the new order. This
    home page does not have one. Nothing filled that slot.
  * It omits two sections that do exist, the Fifteen ring and the "If I don't
    fit into a box" statement. Both kept.

### Task 13 is half done, deliberately

The band is the only Deepwater section, verified. The other half asks that
nothing sit on **Fathom** either, and four sections still do: the hero, the
thesis, the condition and Why me. The reference file only makes that work
because Phase 5 rebuilds the hero as two columns with the image in a frame.
Flipping it before that breaks a full bleed photograph for no gain. **It goes
with Phase 5.**

### HoneyBook, and the CSP

The form was blocked outright: the CSP allowed scripts from this domain, Tag
Manager and Flodesk only. Four directives are widened, **on Cydnie's explicit
approval**, because it lets a third party run code on this site:
`script-src`, `img-src`, `connect-src`, `frame-src`.

**Task 23 is answered.** HoneyBook **injects into the document**, no iframe,
observed during testing. So the token styling in the brief is possible. It is
**not applied**: the form arrives in HoneyBook's own typeface and their own
copy, "Your Next Chapter Starts Here". How much to override is Cydnie's call.

### Two template inheritance bugs, both caught before deploy

The contact page was built from `/the-letters/` so it would inherit the real
header and footer. It also inherited:

  * **that page's Flodesk popup**, which fired an overlay asking for an email
    address on the one page whose whole argument is that you do not have to
    sign up or pay to reach her. The Letters page's own comment says the popup
    is scoped to it and nowhere else.
  * **`aria-current="page"` on The Letters**, so the contact page underlined
    the wrong nav item and told a screen reader the wrong location.

If any page is ever templated from another again, check for both.

### I deleted the condition stepper's controls, and the suite caught it

The Why me rewrite used line numbers from a read taken **before** other edits
shifted them. It wrote two paragraphs into the middle of the condition section
and removed all five tick buttons.

`_test.html` caught it on the assertion generalised earlier the same session
to tie item count to tick count. The file was reverted to the last good commit
and the phase redone with **string matching, never line indices**, plus a
guard that refuses to reorder if any content would fall between the blocks.

**Never edit this codebase by line number.** Match on the string.

### Two new tools, both written because the same thing went wrong twice

  * **`tools/seams.py`.** Every section names the ground of the section above
    it by hand in `--from`. Change a zone, reorder, or delete a section and the
    one below it fades from a colour that is no longer there. Ten seams broke
    this way in one change, and four more in another. Run it after any zone or
    order change. Zero is the only acceptable number.
  * **`tools/shot.sh`.** Screenshots that actually show the page. Three things
    break a naive capture and all three are documented in the file: the reveals
    never fire, the home page's relative asset paths 404 from any subdirectory,
    and Chrome does not exit. It drives `tools/preview/_shot.html`, which
    already solved the first.

### Assertions changed this session, and why each one was wrong

Five failed correctly, because they asserted behaviour the brief changes. Each
was updated to the **new rule**, not loosened:

  * two hardcoded "five recognitions"; they now tie the count to the number of
    ticks, so a stepper with more buttons than moments fails
  * the footer's pinned eleven-link list, for the Contact target
  * A Sounding's nav button, which asserted it scrolls rather than leaves
  * the retreats FAQ count, hardcoded at seven; it now asserts the page and its
    FAQPage schema carry the same number
  * back-to-top, which asked only whether a link and a target existed. Both did.
    It now asserts the target **can be scrolled to**, and is verified red
    against the old markup.

### Open, and waiting on Cydnie

1. **Phase 5.** Two column hero, booking card over the image, sticky bar,
   scroll progress, hover lifts. The Fathom sections flip in the same pass.
2. **Angela appears twice**, in the home proof and as the only quote on the
   contact page rail, where she is doing specific work. Keep both, drop one,
   or find a different quote for the rail.
3. **Angela's source line** reads "Client, Alchemy with A" while Tamara's and
   Spencer's name the engagement. Her quote mentions a first coaching call,
   which matches nothing currently sold, so it claims nothing. Needs the fact.
4. **The HoneyBook form styling**, above.
5. **Task 26 is a report, not a fix, by instruction.** Sixteen links labelled
   "opens my scheduling page" point at honeybook.com rather than the scheduling
   subdomain. Not two, as the brief expected. They are not broken; the label is
   what is wrong.
6. **Two pages contradict their own schema.** Home shows 4 questions against 7
   in its FAQPage; Greece shows 16 against 10. Reconciling means deciding which
   set is true.

### The About page copy freeze, partially lifted

Sections 03 and 04 of `about/index.html` carry **COPY FREEZE** notices. On
29 August Cydnie lifted the **register** half: "I am a person, not depressed."
Three clauses that dwell are gone and no event went with them.

**The structural half still stands** and the file says so: do not split the
"Then life smacked me in the face" paragraph, do not tighten run-on clauses
joined with "and", do not add subheads or bullets inside the account.

That page also runs a single light ground now with one Deepwater close, and
the five "Also true" facts are cards that fill with Breath on hover.

## 45. Session twenty-five: Phase 5, and four tasks that asked for things already removed

**Written at the end of session twenty-five, 29 August 2026.**
Phase 5 of the home page brief is worked through. Most of it is NOT built,
and every one of those is a decision with evidence, not an omission.
Verified, not assumed:

    suite                       453 pass / 0 fail, nine pages
    tools/seams.py              0 mismatches
    tools/build.py              clean, dist/ rebuilt
    locked pages                changed by the cache stamp ONLY, diffed

### Where the brief is

`claude-code-brief.md` is **not in this repo and never was**. It is in
`~/Downloads/`, with `home-page-v8.html` and `contact-page.html`. Section 44
cited its phases by number without saying where to find it, which cost the
first part of this session.

### What shipped

  * **Task 33.** The one Deepwater band runs a 168deg gradient into Fathom.
  * **Task 34, the wash.** A soft Held gradient on the contact rail.
  * **The hero, one stop brighter.** Not a brief task. Cydnie asked for the
    photograph lighter, "not drastically, but not as dark". `.hero--lit`
    lifts the SCRIM rather than the image: nothing is filtered and the water
    keeps its own contrast. Measured on the built page, the ground under the
    headline went rgb(55,71,73) to rgb(88,101,101), and contrast went
    **8.13:1 to 5.07:1 for the headline and 8.16:1 to 6.66:1 for the sub**.
    Both still clear AA. Home only: `.hero-scrim` is shared with both retreat
    heroes, which are darker photographs and are locked.

### Tasks 27 and 28 were built, reviewed, and rejected

The two column hero and the booking card were built in full, published as an
artifact, and **Cydnie kept the full bleed photograph**. Worth recording,
because the reference file will ask for the two column version again:
making the hero two columns turns the waterline from the thing the reader is
standing in into a picture beside some text, and the photograph is the
argument of the page.

Three things were found while it was up, and they are the reason it is worth
having built:

  * **A light hero renders the headline invisible.** `.hero-line` and
    `.hero-call` at section 9 hardcode `var(--surface)` because that hero was
    only ever dark. On a light ground the first sentence was Surface on
    Surface: present, holding its space, unreadable. `.hero-sub` at `#A8C4C0`
    measured about 1.5:1. **Anyone lighting this hero again hits all three.**
  * **`.hero-down` is 110px tall and anchored to the hero's bottom.** Any
    layout that puts content along that edge collides with it, measured at
    14px of overlap.
  * **`onload` cannot work on this site.** The CSP is `script-src 'self'`
    plus hashes with no `'unsafe-hashes'`, so an inline handler is blocked.

There is a fourth, still live, that the artifact exposed: the reference file
is desktop first. Stacking its two columns on a phone put the photograph
under a full screen of type. At 375x812 the frame began at y=688 and 124px
of a 251px image cleared the fold, most of it under the cookie banner.

### Four tasks asked for things this site had already removed

Reported with file and line numbers rather than resolved, which is the
brief's own conflict rule. **Cydnie left all three decidable ones out.** The
notes are in the code, at `site.js` section 7-8-9 and beside `.door`, so the
next brief does not reopen them from scratch:

  * **Task 29, the sticky bar.** Forbidden by the guide, recorded twice in
    `site.css`. It is also fixed to the same edge as the cookie consent
    banner `.cc` and would cover the one control a reader has to answer.
  * **Task 30, the scroll progress bar.** Built and removed once already, on
    the ground that a thin rule at the top that changes length reads as a
    waterline that moves. **The brief's own constraints forbid exactly
    that**, and the site already has a scroll indicator: the depth gauge.
  * **Task 31, smooth scroll.** Already done and better: `site.css` does it
    in CSS with `scroll-padding-top: 6rem`. The brief's JS would drop every
    anchor target under the fixed header. No decision needed.
  * **Task 32, hover lifts.** `.door` says it in words: no lift, no shadow,
    no scale.

### Task 13's second half is still not done, and now cannot be

The brief asks that the band be the only Deepwater or Fathom ground. The
thesis, the condition and Why me were flipped to light in this session and
are still light. **The hero is Fathom again**, so the audit does not pass and
will not while the photograph is the hero. That is the trade Cydnie chose.
`tools/seams.py` caught the seam this left behind the moment the hero went
back, which is exactly why it exists.

### tools/build_artifact.py was broken and is repaired

It had not been run since 27 August and had three faults, all fixed:

  * it read the Google Fonts `<link>` out of the page to carry the
    typefaces. **The site self hosts its faces now**, so the regex matched
    nothing and the build died with an AttributeError. All eight woff2 files
    are inlined as data URIs; the artifact reaches no external origin.
  * it opened every image in `PICK` eagerly and died on one that no page
    renders any more. Stale entries are skipped; anything the page actually
    needs and cannot find is a hard failure rather than a blank photograph.
  * **it only inlined images referenced from the markup.** The ink wordmark
    is a `background-image`, so it published with an empty space where the
    logo goes. Stylesheet `url(../img/...)` references are inlined too now.

### Still open, unchanged from section 44

Items 2, 3, 4, 5 and 6 of section 44's list: Angela appearing twice, Angela's
source line, the HoneyBook form styling, the sixteen mislabelled scheduling
links, and the two pages that contradict their own FAQPage schema.


## 46. Session twenty-five, shipped: and production had never served the build

**Everything below is committed, pushed and LIVE.** Five commits on main,
`383ff37..a7d81c0`. Verified in a real browser on www, not by curl: the home
page returns **zero HTML comments**, `hero--lit` is present, and the hero
eyebrow measures 0px from the headline's left edge.

### Read this first: the deploy path was the bug, and it was a second one

Sections 32, 38 and 44 each investigated production serving the SOURCE
instead of `dist/`, and each blamed something real: `vercel deploy --cwd`
uploading the wrong directory, an iCloud conflict copy landing after the
sweep. Both were fixed and `ship.sh` guards both.

**None of that was this.** There is a Vercel git integration on this repo.
`vercel.json` carried no `buildCommand` and no `outputDirectory`, so **every
push to main published the repository root** and silently overwrote whatever
`ship.sh` had deployed. Every guard in `ship.sh` is irrelevant on that path,
because `ship.sh` never runs. Two deploy paths, and the quiet one won.

Measured on the live site before the fix:

    /            69,654 bytes, 39 HTML comments      built: 55,931 and none
    /about/      39,642 bytes, 28 HTML comments      built: 27,028 and none
    site.css     72,538 bytes over the wire          built: 16,588

A first visit cost 99,693 bytes of compressed text against 39,942 built.
Sixty per cent larger, on every reader. 13,365 bytes of internal build
commentary were public on the home page and 12,354 on About, including
Cydnie's own words back to her inside the page they describe.

`vercel.json` now sets `buildCommand` and `outputDirectory`, so a push builds
and serves `dist/`. **There is one deploy path again and it is correct.**

### Three failed deploys getting there, and what each taught

  * **A `_why_build` key in vercel.json.** JSON has no comments so an
    explanation was put in a key. Vercel validates that file strictly and
    rejects unknown top-level properties, so the whole config was discarded
    and the build never ran: 0ms, twice. **Explanations go in the commit
    message, never in vercel.json.** `vercel build --prod` reproduces this
    locally and is the check to run before pushing a config change.
  * **`.vercelignore` excluded `tools/`,** the folder holding the build
    script. Correct before, wrong the moment the build needed it. Safe to
    include now only because `outputDirectory` means nothing outside `dist/`
    is served.
  * **`build.py` fails the build on drift** between its `EXCLUDE_DIRS` and
    `.vercelignore`, which is exactly what it should do and did.

**A failed build leaves the previous deployment serving.** The site stayed up
throughout. That is the safe direction and it is why this was iterable in
production.

### PLAIN CURL IS NO LONGER SUFFICIENT ON ITS OWN

Polling during verification tripped Vercel's bot protection, which answered
**403 with `x-vercel-mitigated: challenge`** and a 33,830 byte challenge page
for every path. **That page contains no HTML comments.** So the comment count
that section 44 recommends read it as a clean build, and a checksum against
dist said it did not match. A success was nearly reported that was not one.

Check `vercel ls` for deployment status first, then read one page in a real
browser. Do not poll. Section 44's advice was right about `vercel curl` and
is now incomplete.

### What shipped

  * **The hero photograph, one stop brighter.** `.hero--lit` lifts the SCRIM,
    not the image, so the water keeps its own contrast. Ground under the
    headline rgb(55,71,73) to rgb(88,101,101); contrast 8.13:1 to 5.07:1 on
    the headline, 8.16:1 to 6.66:1 on the sub. Both clear AA. **The sub runs
    out first if this is ever lifted further.** Home only: `.hero-scrim` is
    shared with both retreat heroes.
  * **The About heading off the rule.** It overlapped by 27-38px at 320px and
    sat within 1px at 360 and 375. Cause: the job title line was added to
    that copy block after 80svh was measured, and under 390px it wraps to
    two. `min-height` 80svh to 94svh. **Third time this fails if another line
    is added, and it fails silently.**
  * **The hero eyebrow aligned.** Its text sat 40px (390px) to 64px (1440px)
    right of the headline, the call and the sub, which all shared one edge.
    The rule now hangs in the margin via `.eyebrow--hang`. 85rem, measured:
    the rule plus gap is 64px and the space to the content edge is 64.0px at
    1280 and 88px at 1360. **A first pass at 62rem put the rule 6px off
    screen from 992 to 1200 and the 1440 screenshot looked perfect.**
  * **`.vercelignore`**: "April Retreat Gatlinburg April 13th - 18th " added
    the day it landed. 48 screenshots, 145MB, unreleased location photography
    for an unannounced retreat. **The folder name has a trailing space.**
  * **`tools/build_artifact.py` repaired**, three faults, see section 45.

### Phase 5 of the brief is closed, and almost none of it was built

Tasks 27 and 28 built, published for review and rejected: the full bleed
photograph stays. Tasks 29, 30 and 32 declined, each asking for something
this site removed deliberately, with the evidence now in `site.js` section
7-8-9 and beside `.door`. Task 31 was already done in CSS and better. Tasks
33 and 34 built and reverted with the rest of the colour work, because the
colouring is right as it is. **Section 45 has the reasoning. Read it before
acting on that brief again.**

### The security and speed pass, 30 August

Security is strong apart from what the deploy was leaking. CSP with per
script hashes and no `unsafe-inline` for script, HSTS, `frame-ancestors
none`, `X-Frame-Options DENY`, nosniff, Referrer-Policy, Permissions-Policy,
COOP same-origin. **Consent gating verified: zero GTM or gtag references in
the served HTML**, injected only after a choice. 57 of 57 `target="_blank"`
carry `rel="noopener"`. No secrets; every "token" hit is a CSS design token.

Soft spots, none urgent: `style-src` needs `'unsafe-inline'` for the inline
`--d:` delays; HSTS is 63072000 on the apex and 31536000 on www with no
`includeSubDomains`; `mark-horiz-light-1200.webp` is **55KB for a wordmark**
in the header of every page, the one real image win left.

Speed: TTFB 204ms, all edge hits, network is not the problem. Local A/B
source against built: **FCP 100ms to 72ms, 622KB to 449KB.** Images are all
WebP with responsive srcset, fonts self hosted at 120K with two preloaded.

### Open

1. **Nothing asserts the About heading clears the rule.** It has broken twice
   and will break silently a third time. An assertion at 320 and 375 was
   offered and not yet taken.
2. Viewers of the home page artifact are pinned to an earlier version. Fixed
   from that page's share menu, not from here.
3. Items 2 to 6 of section 44 are untouched: Angela twice, Angela's source
   line, the HoneyBook form styling, the sixteen mislabelled scheduling
   links, and the two pages contradicting their own FAQPage schema.

## 47. Two more, after section 46 was written

Both committed, pushed and live. Section 46 stops at the eyebrow; these came
after it.

### The About head is no longer positioned by percentage

`4d0de96`. Section 46 records the heading being lifted off the rule by
raising `min-height` to 94svh. **That fix caused the next complaint**, a big
gap between the navigation and the hero on mobile and desktop both: the copy
is bottom aligned, so every pixel of the new height landed above it and about
300px of the top of the page was empty at 1440x900.

**Both faults were one construction.** A rule pinned at a PERCENTAGE of the
section with the copy pinned to the BOTTOM ties clearance and void together.
Raise the height and the emptiness grows; lower it and the heading walks back
onto the rule. It had been hand tuned three times, 68svh then 80svh then
94svh, each fixing the last one's damage. No percentage can serve both ends
of the range: the copy block is 376px tall at 320px and 312px at 1440px.

So the percentage is gone. `--ab-rule` puts the rule a fixed distance below
the header, the top padding is written as `--ab-rule` plus a gap, and the
section takes its height from its content. **Overlap is now structurally
impossible rather than tuned**: the copy cannot reach the rule because the
padding between them is defined in terms of where the rule is. Add a line to
that copy block, which is exactly what broke it before, and the section grows
downward instead.

Measured on the built page at ten sizes, 320x812 to 1920x1080: header to rule
46 to 68px, rule to heading 72 to 96px, section 597 to 661px. No tight case
and no void anywhere, and the numbers barely move across the range.

**This closes open item 1 of section 46.** The assertion offered there was to
catch a silent recurrence of the overlap. That failure mode no longer exists
by construction, so the assertion is now nice to have rather than needed.

### April 2027 has a date, a partner and a reason to join the list

`9ca2838`. Cydnie's copy, used as written, split across the block's existing
two paragraphs at the sentence break. April is now 13 to 18 April 2027, in
the United States, five days, fifteen seats, with **Kayla Freeman** named for
movement. Doors open in the autumn and the list gets early bird pricing.

Two things on the page contradicted it and were fixed with it: the comment
justifying no Event schema said April had no date, and the `Retreat dates`
ItemList named it "April 2027, location to be announced". The Event decision
still stands for the right reason, schema.org requires a location and there
is not one yet; when the property is named, put the Event on that retreat's
own page the way Greece does, not here.

The status line and the FAQ answer about pricing both still read true and
were left alone.

**ONE THING IS WAITING ON CYDNIE.** Her copy dates it "April 13-18, 2027".
The Greece card directly beneath reads "13-20 August 2027", which is the
format the rest of the site uses. The April card is internally consistent,
its date line matches its paragraph, but the two cards do not match each
other. Her words were used as given rather than reformatted. Ask before
changing either.

### State at close

    suite                 453 pass / 0 fail, nine pages
    tools/seams.py        0 mismatches
    deploys               Ready, 3 to 4s, building dist/ correctly
    production            zero HTML comments, verified in a real browser
    git                   main, level with origin, working tree clean

One untracked folder is deliberately not committed: "April Retreat Gatlinburg
April 13th - 18th ", 48 screenshots, 145MB. It is excluded from deploys in
both `.vercelignore` and `build.py`. **Decide whether it belongs in this repo
at all before adding it**; 145MB of location photography in git is permanent.

Still open, unchanged: item 2 of section 46, the home page artifact viewers
being pinned to an earlier version, and items 2 to 6 of section 44.

## 48. START HERE. The state of the site at the end of session twenty-five

**Written to hand over to a new session. If you read one section, read this
one, then 46 for the deploy path and 45 for the brief.**

Everything is committed, pushed, deployed and verified. Twelve commits,
`383ff37..1341c60`. Verified in a real browser on www, not by curl:

    git                   main, level with origin, working tree clean
    suite                 455 pass / 0 fail, nine pages
    tools/seams.py        0 mismatches
    deploys               Ready, 3 to 5s, building dist/ correctly
    production            zero HTML comments, i.e. the BUILT output

### The five things a new session most needs to know

**1. A PUSH IS A DEPLOY.** There is a Vercel git integration. Since
`15b46c5` it runs `python3 tools/build.py` and serves `dist/`, so a push to
main builds and goes live in about four seconds. `ship.sh` still exists and
still works, but it is no longer the only path and no longer the usual one.
Do not push anything you are not willing to have live.

**2. PLAIN CURL CANNOT PROVE A DEPLOY ANY MORE.** Polling tripped Vercel's
bot protection, which answers **403 with `x-vercel-mitigated: challenge`**
and an identical 33,830 byte challenge page for every path. **That page has
no HTML comments**, so the comment-count check section 44 recommends read it
as a clean build, and a checksum against dist said it did not match. A
success was nearly reported that was not one. Use `vercel ls` for status,
then read one page in a real browser. Do not poll.

**3. THE HOME PAGE FAQ SCHEMA IS GENERATED FROM THE MARKUP.** Ten questions
on the page, ten in the FAQPage, word for word. `_test.html` now asserts both
the count AND that every schema question is findable on the page, because
counting alone would not have caught the failure that actually happened.

**4. NOTHING IS WAITING ON A DECISION** except the small list at the bottom.

**5. `tools/build_artifact.py` works again** and is how Cydnie reviews
things. `python3 tools/build_artifact.py home` folds the whole page into one
self-contained file; publish it as an artifact. She reviews from that, not
from descriptions, and not from screenshots when the real page will do.

### Search Console, and what was actually wrong

Cydnie forwarded a Search Console email: one non-critical Events issue,
`Missing field "validFrom" in "offers"`. Fixed in `8bab4e2`. The Greece Event
carries two offers and they were mirror images: the early rate had
`validThrough` and no start, the standard rate had `validFrom` and no end,
which is correct because it is open ended. The Event is restated on the home
page under the same `@id`, so both files were short the same field and both
were fixed.

**`validFrom` is `2026-08-25` and that is the weakest fact in the repo.**
`git log -S3265` puts the early rate in the first commit on 25 August 2026,
so it is the earliest date this site is KNOWN to have published it. If the
rate opened earlier, through HoneyBook or anywhere else, this is wrong and
should be corrected. Both offers are SoldOut so nothing is being sold on it.
**Cydnie was asked and has not answered.**

**THE REAL PROBLEM WAS NOT THE ONE REPORTED.** While in there: the home
page's FAQPage declared **seven questions and seven answers, and not one word
of any of them was on the page**. The four a reader could open were different
questions on different subjects. Google requires FAQ content to be visible,
so that is a policy problem that can draw a manual action, where the missing
`validFrom` could not. It was never reported by Search Console.

Search Console reports what it checks, not everything that is wrong. **Audit
structured data against the rendered page, not against the warning list.**

Greece looked similar and mostly is not: its schema uses expanded labels for
questions that ARE on the page, "Is there a single occupancy option in
Crete?" against a visible "Is there a single room?". Same substance,
different wording. Worth tidying, not urgent, and NOT the same fault.

### Google Analytics is set up correctly, verified end to end

Asked for and checked on the live site rather than read out of the code:

  * **Before consent there is no `gtag` and no `dataLayer`, and zero requests
    reach Google.** That is better than the usual Consent Mode setup, which
    loads the tag immediately and merely tells it not to store.
  * After Accept the tag loads as **G-KDB3GWPNHC** and a real GA4 hit reaches
    `google-analytics.com/g/collect?v=2&tid=G-KDB3GWPNHC...&gcs=G101`.
  * Custom events work. `faq_open` fired with `question_text`,
    `question_position`, `question_count` and `page_path`. GA4 batches, so a
    single event does not appear as its own request immediately: check
    `dataLayer` rather than the network if verifying one.

**One thing only Cydnie can confirm:** that G-KDB3GWPNHC is the right
property. Hits are provably arriving there; whether that is the GA property
she reads is not something this repo can answer.

### The home FAQ now, and why it is built the way it is

Ten questions, up from four. Cydnie chose to put the seven onto the page
rather than delete them from the schema, because they are the SEO content.

**"Is this coaching or therapy?" was added and then removed on her
instruction.** Its answer had been rewritten to say plainly that this is not
therapy and not a substitute for one, which the old answer never actually
said. She removed the question entirely: naming it invites the association
even while denying it. **The word appears nowhere on the home page.** It
remains in the privacy policy, where it is a disclaimer doing the opposite
job, and it should stay there.

The list scrolls inside a fixed window, `.faq--window`, because ten stacked
summaries measured 1,094px on a 390px phone:

    phone    1,094px  1.30 screens  ->  650px  0.77 screens
    desktop    954px  1.06 screens  ->  670px  0.74 screens

Four things about it that are not obvious and should not be "simplified":

  * **It has its own IntersectionObserver.** The site's reveal system is
    keyed to the viewport, and from the viewport's position every row inside
    the box is on screen the moment the section is, so all ten would light at
    once. Passing the box as `root` is the whole difference.
  * **`tabindex="0"` is load bearing.** A scrollable box that answers only a
    mouse wheel cannot be reached by keyboard at all.
  * Opening a question near the foot of the box scrolls it into view, or the
    answer opens below the box's own fold and reads as nothing happening.
  * It degrades twice: the box still scrolls without JavaScript because that
    is the browser, and the rows are only hidden under `.js-motion`.

Scoped with a modifier. `.faq` is the same component on /retreats/ and
/the-build/ and neither is touched.

### Design decisions made this session that should not be reopened casually

  * **The hero is the full bleed photograph.** The two column version from
    the brief was built, published for review and rejected. It turns the
    waterline from the thing the reader stands in into a picture beside some
    text. `.hero--lit` lifts the SCRIM, not the image.
  * **The colouring does not move.** The light version was built and
    reverted. Tasks 33 and 34 of the brief went with it.
  * **Sticky bar, scroll progress bar and hover lifts are all declined**,
    with evidence in `site.js` section 7-8-9 and beside `.door`.
  * **The About head is positioned by a fixed offset, not a percentage.**
    Three hand tunings preceded that. Do not put a percentage back.

### Open, in the order worth doing them

1. **The `validFrom` date above.** One line, needs a fact only Cydnie has.
2. **April's date format.** Her copy reads "April 13-18, 2027"; the Greece
   card beneath reads "13-20 August 2027", the house style. The April card is
   internally consistent; the two cards are not consistent with each other.
   Her words were used as given. Ask before changing either.
3. **The Gatlinburg folder**, untracked, 48 screenshots, 145MB, excluded from
   deploys in both `.vercelignore` and `build.py`. **Decide whether it
   belongs in git at all before adding it.** 145MB there is permanent. NOTE
   THE TRAILING SPACE in the folder name; it is real and both exclusion lists
   depend on it.
4. **Viewers of the home page artifact are pinned to an earlier version.**
   Fixed from that page's share menu, not from here.
5. **Greece's FAQ labels**, above. Cosmetic.
6. Items 2 to 6 of section 44 are still untouched: Angela appearing twice,
   Angela's source line, the HoneyBook form styling, the sixteen mislabelled
   scheduling links, and the two pages contradicting their own FAQPage.

### The tools, and when to run them

    python3 tools/build.py              always, before looking at dist/
    python3 tools/seams.py              after ANY zone or section order change
    sh tools/preview/sync.sh            SP=<scratchpad>, mirrors the site
    sh tools/preview/runsuite.sh        SP, port, [/page/]  -> 455 / 0
    sh tools/shot.sh                    screenshots that actually show the page
    python3 tools/build_artifact.py     fold a page into one file for review
    vercel ls                           deployment status, the only reliable one

**If the suite fails on a page you did not touch, delete `$SP/cr-*` and run
it again before believing it.** Those are per-page Chrome profiles and they
cache. That produced one phantom failure this session, after the file under
test had already been restored.

## 49. Session twenty-six: the Gatlinburg page, built and not pushed

**Nothing in this session has been pushed or committed. A push is a deploy.**
The artifact is published for review and the working tree is where the work
is.

    suite            527 pass / 0 fail, TEN pages
    tools/seams.py   0 mismatches
    build            clean
    git              NOT pushed, NOT committed

`/retreats/gatlinburg/`. Wide Open: The Gatlinburg Edition, 13 to 18 April
2027. Ported from `gatlinburg-v5.html` in the untracked April folder, then
revised three times against Cydnie's review on 31 August.

**Pre-launch and noindex in three places on purpose:** two robots tags, an
`X-Robots-Tag` on the route in `vercel.json`, and omission from
`sitemap.xml` with a comment there saying so. The header is the one that
survives an edit to the head. The visible pre-launch band was built and
then removed on her instruction; it was only restating the noindex.

### The rule that produced most of the good decisions here

**Look for the component before writing one.** Nine were written for this
page and seven were then deleted, because the site already had them:

| written | what it actually was |
|---|---|
| `.gb-days` | `.cond`, the pinned stepped story bar |
| `.gb-hosts` | `.rt-person` with `--flip` |
| `.gb-pair` | `.pair pair--calm` |
| `.gb-facts` / `.gb-n` | `.stats` and `.drop`, Greece's Crete layout |
| `.gb-incl` scroll window | `.grid-12--hold`, the About page's sticky head |

**What survives is four rules:** `.gb-rail`, `.gb-rooms` with `.gb-room`,
`.gb-act` and `.gb-strip`, plus the colour block. Everything else on the
page is the site's own, which is why a revision that changed five sections
cost almost no new CSS.

### The one new interaction, and it is opt in

`data-loop` on `.gal`, asked for by name: "it should be a carousel that
keeps relooping." It drives the rail's own arrows on a timer and wraps, so
drag, keyboard, snapping and the progress rule all still work. It stops on
hover, on focus, off screen and under `prefers-reduced-motion`, and once a
reader has touched it it does not start again. **Greece does not declare
the attribute, so that gallery is unchanged.** Verified advancing one tile
per 3.6s in a browser, not assumed.

**The sticky booking bar and the scroll progress rule are still out.** The
wireframe carried both; site.js section 7-8-9 records them asked for and
declined twice. They were not built and were not asked for again.

### The photography

Twenty-two photographs to WebP in `assets/img/gatlinburg/`, 5MB. The 145MB
source folder stays out of git and is now excluded in `sync.sh` as well as
`.vercelignore` and `build.py`.

**Four frames were held back for the alcohol rule and then put back.**
Two deck frames and both hot tub frames have glasses of red wine in them.
The first reading was that the brief's "alcohol appears in the not-included
list and nowhere else" covers photographs too, because a photograph puts a
thing on a page as surely as a sentence does. **Cydnie overruled that on 31
August: they are the property's own listing frames, they are aesthetics and
not an offer.** They are in the carousel; the not-included line is
unchanged and is the claim that actually matters. Recorded because the
first reading was reasonable and somebody will make it again.

The hero is still cropped to 84% width to remove the name plaque beside the
front steps. **That one is not aesthetic**: the property is not named on
this page and a legible plaque names it.

No photograph of the town or the park exists. Both figures the wireframe
wanted there were dropped and the facts are prose, which is what Greece had
to do about Chania and Kera.

### The ring, and the guest count question that was raised and closed

`.fifteen-fig` is fifteen dots, fourteen filling and one open, and a reader
can count them. The brief for this page says no guest count is published,
so the two instructions collided and it was put to Cydnie rather than
guessed at. **Her answer, 31 August 2026: "Keep the community circle,
nobody needs to know the guest count on this one."** It stays, and the
no-guest-count rule still holds for the words: nothing on the page states a
number of seats. Do not reopen this on the strength of the brief alone.

The open circle was Held, the warm note, which read as a red ring on a page
of blues. It is Meniscus now, on her instruction, so it reads as the one
that is not filled rather than as an alert.

### The colour, added on review

"The page is quite dull and sad." Every value is a palette token and all of
it hangs off `.gb` on `<main>`, which exists only here: Held on the strip
heading, Breath and Held on the two halves of the included list, Breath on
the ring with a Held open circle, and a Breath fill on button hover which
gains contrast rather than losing it. The hero was `hero--bright`, which is
the DARKER modifier; it is `hero--lit` now, which is the one that lifts the
scrim rather than the image.

**The ring needed six classes of specificity.** `.z-silt .fifteen-fig
.is-counting .dot.is-filled` is five and paints it Meniscus. The fill came
back `rgb(47,90,97)` when measured in the browser, which is how it was
caught; naming the figure's own two classes puts the page's rule in front.

### Three review fixes to the hero and the buttons

**The phone hero was a strip of wall.** The file is 1.47:1 and a phone hero
is about 0.46:1, so `cover` showed a 46% wide column of it: timber and one
window, no house and no ridge. **No `object-position` fixes that**, because
no single column of a landscape photograph contains both. A `<picture>`
serves a second CROP of the same frame below 46rem, 3:4, taken from the
left half where the ridge, the sunset and the three tiers of balcony all
are. `srcset` was never the tool: it picks a different SIZE of one crop.

**The Greece hero eyebrow had the same defect and is fixed too**, on
instruction, after the Gatlinburg one was. Measured before: eyebrow text at
60px against a headline, sub, calls and facts row all at 20px. Forty out,
which is the number the note beside `.eyebrow--hang` records for the home
hero. It is `--plain` rather than `--hang` so the two retreat pages open the
same way; the home hero keeps `--hang`, which aligns the text and hangs the
rule in the margin instead. **Every other eyebrow on the site still has this
defect**, in section heads rather than heroes, where it is a smaller thing
because the eyebrow is not sitting directly above a headline on a shared
edge. Worth a sweep, not urgent.

**The hero eyebrow did not line up.** `.eyebrow` is a flex row and its
`::before` rule pushed the TEXT inward while the headline, the sub and the
buttons all sat on the wrap's edge. `.eyebrow--hang` is the site's measured
fix and was tried first; Cydnie then asked for the rule gone entirely, so it
is `.eyebrow--plain`. Measured after: eyebrow text, h1, sub and first button
all report a left edge of 20px.

**The button hover was unreadable, and it took three passes.** `.btn` fills
with a `::before` that slides up, and the text recolours at the same moment,
so the fill and the text are ONE decision. Pass one set `background` on the
element, which the `::before` covers, and `color`, which landed: Meniscus
fill with near-black text, 1.8:1. Pass two recoloured the fill per variant
and set Fathom text on each; the quiet variant still measured 2.36:1 in the
browser, so something in the cascade was still taking the colour.

**Pass three removed the variants from the question.** Every button on this
page hovers to a Fathom fill with Surface text, 14.93:1 on every ground.
There is no combination left that can put dark text on a dark fill.
Verified by pinning the hover state in the preview mirror and
screenshotting it at 1440, not by computing it and hoping.

### Five page-specific guards in _test.html were coincidences, not guards

Every one failed on a correct page and every one was gated on structure
that stopped meaning what it used to once a second retreat page existed:

  * five Greece assertions gated on `#ask` and `#booking`. Now on Greece's
    path.
  * two home FAQPage assertions gated on `.hero--lit`, a scrim modifier.
    Now on `/`.
  * two lightbox assertions pinned to the filename `bath-`. Now derived
    from the tile's own `data-full`, which is better on any page.
  * the off-site link assertion accepted "scheduling page" but not
    "booking page", and a payment link is not a scheduling page.

**A COMMENTED-OUT SCRIPT SHIPS TO PRODUCTION.** The launch JSON-LD was
wrapped in `<!-- -->` with its script tags intact, and it went out in the
built page while every other page serves zero HTML comments. `strip_html`
in build.py splits on script and style regions BEFORE it strips comments,
because a `<!--` inside a script is JavaScript, so a comment that wraps a
script is cut in half and neither half is a complete comment. The stripper
was right and the markup was wrong.

The JSON sits in the comment unwrapped now, to be wrapped at launch. **And
the comment must not name the tag in angle brackets either**: writing
`<script type="application/ld+json">` as prose inside the comment opened a
script region that ran to the next real `</script>` and left twenty two
comments in the built page. Zero is the number; check it after any edit to
that head.

**TWO CAROUSEL TILES SHIPPED AS ALT TEXT, and nothing caught it.** The
helper that wrote the twenty four tiles hardcoded `-1000.webp`, and
`deck-view` and `house-dusk` had been made at 600/900/1200/1600 for a
full-bleed band and had no 1000. `build.py` warns about image FILES nothing
references, which costs disk; it had no check in the other direction, which
costs a broken picture on a live page. **It does now, and it fails the
build rather than warning**, srcset included, because a missing width in a
srcset only breaks on the screens that ask for it. Proved by deleting a
file and watching the build refuse.

**`build_artifact.py` never swapped `data-full`**, so every gallery tile in
every artifact ever published opened a broken picture. Greece has had it
all along. Fixed; twenty tiles made it obvious.

**The suite ran green against a stale server for one whole run.** A
`python3 -m http.server` left from a previous session was serving that
session's scratchpad, so the new page 404'd and the suite reported 16 pass
/ 15 fail on a document that was not the page. Check the root first:

    lsof -p $(lsof -nP -iTCP:8814 -sTCP:LISTEN -t) | awk '$4=="cwd"'

### Five hand-maintained registries, four of which needed the page

`tools/seams.py` PAGES, `tools/stamp.py` PAGES, `tools/preview/runsuite.sh`,
and `tools/build_artifact.py` PAGES and PICK. `sitemap.xml` is the fifth and
is the one it must NOT be added to yet. `build.py` walks the tree.

### Open, in the order worth doing them

1. **The story bar is on the five days, not the questions.** She asked for
   it on the questions. `.cond` pins a stage and walks a small fixed number
   of steps; nine questions is not that shape and a disclosure list is right
   for questions. The five days are exactly five. Moveable.
3. **Still open from the brief and deliberately not on the page as
   placeholders**: the forms of movement, the second workshop subject, and
   which two outings.
4. **The per-day figures expire on 1 November 2026.** $558 and $298 hold at
   the early rate only; after that it is $580 and $320. Updated that day or
   removed that day.
5. **The four HoneyBook records must be checked against the page.** The
   links are live and wired. Nobody has confirmed the figures inside them
   match $2,790, $2,900, $1,490 and $1,600, and their four ids are not in
   the FORMS map in `_test.html`, which pins every other id on the site.
6. **The og:image is the house at dusk**, real and honest, not a
   purpose-built 1200x630.
7. Section 48's open list is untouched.

## 50. START HERE. End of session twenty-six, and the launch runbook

**Everything is committed, pushed, deployed and verified in a real browser
on www.** Seven commits, `d2c8907..df74adb`.

    git                   main, level with origin, working tree clean
    suite                 527 pass / 0 fail, TEN pages
    tools/seams.py        0 mismatches
    build                 clean, no missing and no unreferenced assets
    production            /retreats/gatlinburg/ 200, zero HTML comments
    noindex               meta + X-Robots-Tag, both confirmed on the route
    booking               all four links 200

### What is live tonight

`/retreats/gatlinburg/` is live, and **it is deliberately a page nobody can
find.** Nothing on the site links to it, it is absent from the sitemap, and
it is `noindex, nofollow, noarchive` in two independent places. That is the
prelaunch Cydnie asked for: she sends the URL to specific people, they can
book, and search engines never see it.

**Do not "fix" any of the four things above by accident.** Each one is load
bearing until she says otherwise, and three of them are invisible.

### THE LAUNCH RUNBOOK, in order, one commit each

Nothing here should be done until Cydnie says the page is public.

**1. Take the noindex off, all four places in one commit.**

    retreats/gatlinburg/index.html   delete both robots meta tags
    vercel.json                      delete the X-Robots-Tag block
    retreats/gatlinburg/index.html   uncomment the canonical
    sitemap.xml                      add the URL, delete the comment

**2. The JSON-LD, and read this before pasting it.** It is parked in a
comment in the head, and it is stored WITHOUT its script tags on purpose.
`strip_html` in build.py splits on script regions before stripping
comments, so a commented-out script SHIPS to production, and so does a
comment that merely writes the tag name in angle brackets. Wrap the JSON in
a script element of type application/ld+json, then check the built page:

    grep -c '<!--' dist/retreats/gatlinburg/index.html      must be 0

**3. Validate the structured data** against the RENDERED page, not against
the warning list. Section 48 is the reason: the home page shipped a FAQPage
whose seven questions appeared nowhere in the markup, Search Console never
reported it, and it is the kind of thing that draws a manual action. **This
page has nine questions on it and no FAQPage node.** If one is ever added,
every question in it has to be one of those nine, word for word.

**4. Add the Gatlinburg card to the Retreats index, above Greece.** April is
asserted in SEVEN places on that page and they move together:

    retreats/index.html   the #april card, its status and its copy
    retreats/index.html   the ItemList schema, currently "location to be announced"
    retreats/index.html   the FAQ answer that says April is not priced yet
    retreats/index.html   the two meta descriptions
    retreats/index.html   the closing CTA
    tools/us_map.py       the unplaced pin, if the card keeps the map

**5. Add the four HoneyBook ids to the FORMS map in `_test.html`.** Every
other id on the site is pinned there. Rewriting a block once swapped
`69fa33ac` for `69fa372c` and pointed a private retreat inquiry at the
general contact mailbox; the link still worked, still returned 200 and
still looked right. That assertion is what catches it next time.

**6. Then run the three, and only then push.**

    python3 tools/build.py
    python3 tools/seams.py                      0
    sh tools/preview/runsuite.sh "$SP" 8814     527 / 0

### Two dated things that will go wrong on their own

**1 November 2026.** The per-day figures on the room cards hold at the early
rate only. $2,790 is $558 a day and $1,490 is $298 a day; after that date it
is $580 and $320. Those two lines are updated that day or removed that day.
Nothing on the page enforces it.

**31 October 2026.** The early rate closes. The page says so in four places
and they all have to agree with HoneyBook.

### Still open, in the order worth doing them

1. **Nobody has checked the four HoneyBook service records against the
   page.** The links resolve and people can pay through them. The figures
   inside them have never been compared to $2,790, $2,900, $1,490 and
   $1,600. **This is the highest risk item on the list** and it is five
   minutes of looking.
2. **The og:image is the house at dusk**, which is a real photograph of the
   real place and is honest, but it is not a purpose-built 1200x630.
3. **Three things from the brief are still unwritten and are deliberately
   not on the page as placeholders**: the forms of movement across the
   week, the second workshop subject, and which two outings.
4. **Every eyebrow on the site except three still sits 40px right of the
   thing it labels.** `.eyebrow` is a flex row and its rule pushes the text
   in. The home hero has `--hang`, and the two retreat heroes now have
   `--plain`. The rest are section heads, where it matters less because the
   eyebrow is not directly above a headline on a shared edge. One class
   each. Worth a sweep, not urgent.
5. Section 48's list is otherwise untouched: the Greece `validFrom` date,
   Greece's FAQ labels, and items 2 to 6 of section 44.

### Three traps this session found the hard way

**The suite can run green against the wrong server.** A `python3 -m
http.server` left from a previous session was serving that session's
scratchpad. The new page 404'd and the suite reported a page that was not
the page. Check the root before believing a result:

    lsof -p $(lsof -nP -iTCP:8814 -sTCP:LISTEN -t) | awk '$4=="cwd"'

**A guard gated on structure is a coincidence waiting to expire.** Five
assertions were gated on `#ask` and `#booking` being present, two on the
`.hero--lit` class, two on the filename `bath-`. All nine passed for a year
and all nine failed the moment a second retreat page existed. Gate on the
path, or derive the expectation from the element under test.

**Setting half of a two-part rule is worse than setting neither.** `.btn`
fills with a `::before` and recolours its text at the same moment. Three
passes were spent on that hover, and the first two each left a real page
with dark text on a dark fill. Measure the result in a browser; do not
compute it and assume.

## 51. A database exists, switched off, on purpose

Added 10 September 2026. **Every form on the site is exactly where it was.**
HoneyBook takes all 28 links and the Flodesk popup stays on `/the-letters/`.
Cydnie confirmed on the day that both are right. No page markup was touched.

    db suite       30 pass / 0 fail
    site suite     527 pass / 0 fail, ten pages, unaffected
    seams          0 mismatches
    build          clean, and now refuses to ship a secret

### Read this before you get excited about api/

**The endpoints are switched off at the deploy boundary and that is the
decision, not an oversight.** `api/` is listed in `.vercelignore`. Vercel
turns every file in `api/` into a live serverless function the moment it is
uploaded, and on this repo a push is a deploy, so without that line
committing this would have put four public write endpoints on the live domain
the same minute, with nothing on the site calling them. An endpoint nobody
uses is still an endpoint somebody can find.

**Deleting `api/` from `.vercelignore` is what makes them live.** Before
doing it: confirm `SITE_DATABASE_URL` and `IP_SALT` are set in the Vercel
project, and have a page that actually calls one, or you have opened a door
onto an empty room.

`check_vercelignore()` only fails when `.vercelignore` excludes something
`build.py` does not, so `api` being in both lists is fine and intended.

### Why it exists at all

Asked for, kept "just in case". It was originally built on the reading that
the site would capture its own signups instead of HoneyBook and Flodesk.
**That reading was wrong** and the correction came before anything was wired
or deployed, which is the only reason it cost nothing. The three POST
endpoints duplicate things that already work.

**HONEYBOOK AND FLODESK ARE THE CRM. They are not a stopgap.** Cydnie said
so plainly on 10 September, and a future session should treat replacing them
as out of scope unless she reopens it. They hold the clients, the bookings,
the payments and the list. This database holds nothing and is not a rival to
them.

One idea was raised and she has parked it, so it is recorded here as a note
and not as a recommendation: webhook endpoints that RECEIVE from HoneyBook
and Flodesk rather than replace them, because the comment on
`/the-letters/` already names the cost of two systems that do not know about
each other. **She said she will worry about that.** Do not start it.

### The near miss, which is the most useful thing in this section

`tools/build.py` copies the tree into `dist/` and skips EXCLUDE_DIRS and
EXCLUDE_FILES. Those lists knew about working documents and photography.
They had never had to know about a secret, because there had never been one.
**The first build after this landed copied `.env.local` into `dist/`**, so a
push at that moment would have served the database password at
`https://cydniejocelyn.com/.env.local`, along with `api/`, `db/` and 777
files of `.venv`.

The exclude lists are fixed. The thing that matters is the second fix:
`check_no_secrets()` greps the BUILT output for connection strings, key
prefixes and private key headers and **exits 1**. It was proved by planting a
file and watching the build refuse. Excluding by name only stops what
somebody thought of; the next leak will be a connection string pasted into a
page, not a file called `.env`.

**If it ever fires, nothing deployed, and whatever it names still has to be
rotated, because it was written to disk.**

### What exists in Neon

A SECOND project, separate from Cydnie Ops deliberately:

    project   Cydnie Jocelyn Site, id old-shape-52826022
    org       Cydnie Jocelyn, org-quiet-math-76263929
    region    aws-us-east-2, Postgres 18
    branch main   empty, 0 rows
    branch check  a throwaway, wiped and rebuilt by db/check.py

**It is not the Ops database and must not become it.** Ops holds the whole
client book and its own handoff says authentication there is still open. A
credential that sits on a public endpoint must not be able to read that.

Two tables. `submissions` and `subscribers`. Both empty.

Vercel already has `SITE_DATABASE_URL` and `IP_SALT`, with production
pointing at `main` and preview and development at the `check` branch, because
a preview URL is public. They are inert while `api/` is ignored.

### Decisions worth keeping if this is picked up

**The site does not run as the owner.** It runs as `site_api`, which can
INSERT and **cannot read a submission back**. Column level SELECT on exactly
`ip_hash` and `created_at`, so rate limiting can count and nothing else.
Eleven of the thirty checks are that role being refused.

That caught a real bug rather than theoretically preventing one.
`subscribe.py` used `returning (xmax = 0)` to tell a new signup from a
repeat; `xmax` is a system column, column level grants do not cover it, and
Postgres refused the statement. It now answers the same either way, which
also closes an enumeration oracle.

**`sslmode=verify-full`, CA resolved in code.** Neon hands out `require`,
which encrypts and verifies nothing. `sslrootcert=system` is right on
Vercel's Linux and FAILS on this Mac, because OpenSSL does not read the
Keychain. Both were tried. `api/_lib/db.py` resolves it once, certifi first,
so nobody hits the local failure and "fixes" it by weakening production too.

**The raw IP is never stored**, and `hash_ip` fails closed without the salt,
because an unsalted hash of an IPv4 address is reversible in seconds.

**`setup_role.py` reuses the password by default.** `check.py` drops the
schema and so must re-apply grants every run; an earlier version issued a
fresh password each time and silently invalidated `.env.local` and Vercel.
`--rotate` is how you ask.

### Commands

    .venv/bin/python db/migrate.py            apply migrations to main
    .venv/bin/python db/migrate.py --check    and to the throwaway
    .venv/bin/python db/setup_role.py         re-apply grants, reuse password
    .venv/bin/python db/check.py              30 pass / 0 fail

Run `setup_role.py` after any migration that adds a table. A new table is not
covered by grants already applied.

## 52. START HERE. End of the night, 10 September 2026

**Everything is committed, pushed, deployed and verified on www.** Two
commits tonight, `0c5b8c7` and `ef30cfd`. Both repos clean.

    git                main, level with origin, working tree clean
    site suite         527 pass / 0 fail, ten pages
    db suite           30 pass / 0 fail
    tools/seams.py     0 mismatches
    production         site 200, every /api/ route 404, no secret served
    cydnie-ops         untouched tonight, still at 5221f33

### The one thing that decides everything else

**HoneyBook and Flodesk are the CRM.** Every form on the site goes to one of
them and that is correct and settled. The Flodesk popup on `/the-letters/`
stays alongside the HoneyBook buttons; her own comment on that page records
why. Nothing about the site's capture points changed tonight and nothing
should change without her asking.

### What actually happened tonight

**Two small design fixes to the home hero, live.** The path now stands 96px
off the ask line on a phone instead of 32, which is the same distance it sits
from the heading below it, and "The path" took the `.eyebrow` class so it
carries the same rule "The difference" does. Desktop untouched: above 62rem
the hero is two columns and the two sit side by side.

**A Neon database for the site, built and then switched off.** Section 51 has
the whole of it. The short version: it was built on a wrong reading of what
was wanted, the correction arrived before anything was wired or deployed, and
Cydnie asked to keep it "just in case". `api/` is in `.vercelignore` so the
four endpoints do not exist in production. Deleting that line is what makes
them live.

**A build guard that is worth more than the database.** `.env.local` was
copied into `dist/` by the first build after the backend landed. A push then
would have served the database password at `cydniejocelyn.com/.env.local`.
`check_no_secrets()` now fails the build on a connection string, a key
prefix or a private key header anywhere in the built output.

### If you pick this up tomorrow

Nothing is half done and nothing is waiting on a decision except the list
below. The site is in the same shape it was at the end of section 50, plus
two hero fixes, plus a dormant database.

**The Gatlinburg launch runbook is still section 50** and is still the real
next piece of work whenever she says go. It has not moved.

### Open, in the order worth doing them

1. **Nobody has checked the four HoneyBook service records against the
   Gatlinburg page.** The links resolve and people can pay through them.
   Nobody has confirmed the figures inside them read $2,790, $2,900, $1,490
   and $1,600. Highest risk item on the list and five minutes of looking.
2. **The per day figures expire on 1 November 2026.** $558 and $298 hold at
   the early rate only; after that it is $580 and $320. Updated that day or
   removed that day.
3. **The Gatlinburg page is still prelaunch**: noindex in two places, absent
   from the sitemap, linked from nowhere. Section 50 for how to undo that.
4. **Every eyebrow on the site except three still sits 40px right of the
   thing it labels.** Home hero has `--hang`; both retreat heroes now have
   `--plain`. The rest are section heads, where it matters less. One class
   each, worth a sweep, not urgent.
5. Section 48's list is otherwise untouched: the Greece `validFrom` date,
   Greece's FAQ labels, and items 2 to 6 of section 44.

## 53. START HERE. End of session twenty-seven, 11 September 2026

**Everything is committed, pushed, deployed and verified on www.** One
commit, `9546fe5`. Working tree clean.

    git                main, level with origin, clean
    site suite         527 pass / 0 fail, ten pages
    tools/seams.py     0 mismatches
    production         home 200, hero plate live, both new section ids live
    gatlinburg         still noindex, still linked from nowhere
    api/               still switched off in .vercelignore

### The three things that changed, and why

**1. The audience is founders and leaders, not women.** Thirteen strings on
five pages. **This was never a new position.** The home page FAQ has said
"the brand strategy work is for founders and leaders of any gender" the whole
time, while every headline, meta description and schema said women. The meta
description is what Google shows and what every shared link renders as a
card, so the contradiction was doing real damage. The FAQ was right; the
headlines were stale.

**Retreats are untouched and stay women only**, labelled that way on their
own pages. That is the other half of the same FAQ answer and it is a real
product boundary, not positioning drift. Do not "tidy" it.

The prompt for this was an audit: her own three case studies include
**Spencer Scott, SRS Performance**, a man, quoted on The Build, while the
site said the work was for women.

**2. The home page now says what the work is, in its own section.** The
definitions of brand, operations and business development lived only on The
Build, below the fold, where a first time visitor never reaches them. They
are on the home page now, same `.triad` component and the same words so the
two pages cannot drift.

Then the section was split, because it had grown to three jobs. `#method`
is "The work", what the work IS. `#offers` is "What it leads to", what you
can BUY. Different questions from different readers; mixed together the
first reader had to scroll past prices to learn what the work is. The seam
below `#offers` was repointed from Surface to `#DCE4E1`.

**3. The hero is a different plate.** Cydnie chose it by pointing at the
rise band further down the page, the photograph the bubbles come up
through, `layer-surface`. Cropped to its water it is `hero-rise-*`.

    old plate  hero-line        saturation 0.114
    new plate  hero-rise        saturation 0.361

**That number is the whole story.** The hero read grey because it was
desaturated, not because it was dark. She said several times she wanted it
brighter and every attempt to lighten the scrim made both the greyness and
the contrast worse. The complaint was never darkness. `hero-line` is retired
to `assets/_unused/`.

It has its own `.hero--open` modifier. `hero--lit` is shared with
/retreats/gatlinburg/ and that page is settled.

### How to measure this site's heroes, because three attempts got it wrong

**Do not sample screenshots.** `tools/shot.sh` gives different contrast
answers run to run, and one of those false passes was reported to Cydnie as
a success. Three separate attempts at this hero shipped wrong numbers that
way.

The method that works, and that every current scrim value came from: in a
real browser, draw the hero image to a canvas using its actual object-fit
cover mapping and `object-position`, apply each gradient layer per pixel,
and score the single worst pixel under each run of text against that run's
ink. Then try candidate gradients and take the lightest with nothing under
threshold. It is deterministic and it takes one `javascript_tool` call.

Thresholds used: 4.5:1 for body and small caps, 3.0:1 for the large
headline. Inks: Surface `#E7ECE8` and Muted `#A8C4C0`.

### Two audits exist and are published

Both are artifacts, both were built from the site's own copy and markup.

  * **Who The Site Says You Serve.** Six findings on positioning.
  * **Five Changes And A Position.** Conversion fixes ranked, plus the
    category position: *the consultant who tells you the price and the
    answer before you commit to anything.* Published pricing with no
    discovery call is genuinely rare and the site treats it as a pricing
    detail rather than a position.

**Three of those five conversion fixes are still undone**, below.

### Open, in the order worth doing them

1. **The free offer has no buttons and the $300 offer has three.** On the
   home page: "Book one conversation" has three `.btn`, The Letters has zero
   and five text links. The lowest friction thing, the one that feeds the
   retreats and new work first, is the only offer never given a button. One
   button at the close. This is the highest value item on this list.
2. **Every paid action leaves the domain.** The contact form is embedded, so
   questions stay on site. Every booking opens `clients.cydniejocelyn.com`
   at the moment somebody decided to pay. Embed the Sounding booking on
   `/a-sounding/` the way contact already embeds its form. Leave the retreat
   payments outbound.
3. **Three case studies, zero outcomes.** "Narrowed from general fitness to
   former competitive athletes" is a judgement most consultants could not
   defend, and none of the three says what happened next. Needs one
   defensible number each, **and only Cydnie has them.**
4. **A stray `</div>` in index.html**, around line 738, in the section with
   the reaching hand photograph. Pre-existing, committed, live. Browsers
   ignore an unmatched end tag so nothing looks broken. Three closing divs
   sit together there and removing the wrong one changes the nesting, so it
   needs a careful read rather than a guess.
5. **`reaching-water-*.webp` is unreferenced**, three files, 132KB. The
   build warns about it every time. Either use it or move it to
   `assets/_unused/`.
6. **Nobody has checked the four Gatlinburg HoneyBook records against the
   page.** People can pay through them. Highest risk item across the whole
   project and five minutes of looking.
7. Sections 50 and 52 still stand: the Gatlinburg launch runbook, the
   1 November per-day figures, and the eyebrow sweep.

### What this session did NOT do, on purpose

  * **Did not touch the retreats.** Three pages, unchanged.
  * **Did not turn the database on.** `api/` is still in `.vercelignore`.
  * **Did not change HoneyBook or Flodesk.** They are the CRM. Section 51.
  * **Did not fix the stray `</div>`**, for the reason above.

---

## 54. START HERE. Session twenty-eight, 12 September 2026. NOTHING SHIPPED.

**Read this before section 53. Everything below is uncommitted and unpushed,
and that is deliberate: Cydnie ended the session with "nothing is allowed to
be pushed or published."**

    git            HEAD f8cbf95, level with origin, 14 files modified
    production     still f8cbf95, which is the header portrait and the
                   Greece early rate removal. None of the work below is live.
    site suite     529 pass / 0 fail, ten pages
    tools/seams.py 0 mismatches
    gatlinburg     still noindex, still linked from nowhere
    api/           still switched off in .vercelignore

### The one thing that is broken and was not fixed

**THE FLIP CARDS IN SECTION 3 DO NOT WORK.** Cydnie has reported this three
times. Two causes were found and fixed and it still does not work for her, so
there is a third and I did not find it.

Fixed, and verified in a headless browser each time:

  1. `perspective` was on `.flips`, the list. The property applies to an
     element's DIRECT children only, and the rotating element `.flip-in` is a
     grandchild, so it turned with no perspective: a flat mirror flip with no
     depth. Moved onto `.flip`.
  2. The whole flip was behind `@media (hover: hover) and (pointer: fine)`.
     That does not match on a touchscreen laptop or in some embedded viewers,
     and in those the cards never turned at all. Regated on `.js-motion`, and
     a tap and keyboard toggle were added in `initFlips`, site.js section 19.

What is verified working in headless Chrome at 1140px: click flips and
unflips, Enter flips, real pointer hover flips, the halo paints, and with
`.js-motion` removed both faces stack and stay readable.

**So the next session should not start by re-reading the CSS.** Start by
finding out what Cydnie is actually looking at and on what, because the
component passes every test that can be run from here:

  * Is she reviewing the ARTIFACT or a local build? The artifact is a folded
    single file in a sandboxed frame and is the most likely differing
    environment.
  * What browser and what device? Safari needs `-webkit-backface-visibility`,
    which is set, but Safari also flattens `preserve-3d` when an ancestor has
    `overflow` other than visible, and `.proof` and `.wrap` above it have not
    been checked for that.
  * Does the card move AT ALL for her, or is it that the back is unreadable,
    or that the halo is the part that does not show? "Does not work" has
    covered three different things so far.

`overflow` on an ancestor flattening the 3D context is the strongest
remaining candidate and is the first thing to check.

### What is in the working tree, none of it live

**Phases 1 and 2 of the home restructure brief, built together.** Phase 1
deletes three sections that Phase 2 relocates, so shipping Phase 1 alone
would take that content off the site entirely.

Seventeen blocks to seven: hero, the condition, what I actually do, proof,
start here, retreats, the close. Deleted outright: The difference, What it
leads to, Before any of it, the box statement, the mid-page city band, and
the hero path rail. Relocated: the refusals to /the-build/ above the prices
and cut from four items to three, The room I build to /retreats/ as copy only
because that page already draws the fifteen ring and `initFifteen` finds it
with `querySelector`, singular. Five FAQ questions split off the home page
onto /the-build/, /retreats/ and /a-sounding/, markup and FAQPage schema
together. "I was the client" was deleted without relocating because /about/
already carries that narrative in fuller form.

**Motion lost, per standing rule 1:** both parallax elements, so the home
page now has none; the four-door stagger; one of the two waterline rules;
four split headlines. The reversal interaction was NOT lost: the brief asked
for the three objections as inline lines, which would have deleted it, so the
component moved intact and only its container tightened.

**The hero, after a long and mostly wasted argument.** The plate is
`layer-surface`, the full frame, unedited and restored from git byte for
byte. No scrim was the instruction at one point and it is not survivable:
measured on the bare plate the ground under the headline runs 0.006 to 0.976
relative luminance because the words cross the waterline, and no single ink
colour survives that range. The scrim is back, shaped to the photograph
rather than flat over it: real weight across the top where the sky is near
white, nothing at all at the right hand edge where the shafts are. Every run
measured against the glyph runs, not the element boxes.

    eyebrow 5.89   H1 5.97   category 4.91   CTA 7.60   clients 6.64

**MEASURE THE GLYPH RUNS, NOT THE ELEMENT BOXES.** A block level `<p>` is as
wide as its column and its letters are not, so scoring the box scores empty
ground and reports failures that are not there. Two "failures" were reported
to Cydnie that way before it was caught. Use `Range.getClientRects()`.

### Decisions Cydnie made this session, so they are not reopened

  * The depth gauge stays. No alternative was wanted.
  * The Greece early rate is removed. Gatlinburg's runs to 31 October and is
    untouched.
  * Header portrait: frame 48 from the branding shoot, chosen on measured
    separation against both bar colours. Frame 20 lost at 1.88:1 on the dark
    bar. Seven cropped portraits are in `assets/img/` lineage if wanted.
  * The Letters go to HONEYBOOK, not Flodesk, cf_id
    `6a19d46a5cb4c5d7f86446a9`, the same record the two buttons on
    /the-letters/ use. Flodesk was tried inline and measured out: that
    account's only form is built as `fd-modal fd-is-open`, `position: fixed`,
    `z-index: 1040`. It is a popup, and this brand does not use modals. An
    inline capture needs a form created as an INLINE form in Flodesk and a
    new id, which does not exist yet.
  * Section 7 lost its "Start here" eyebrow and its booking button, because
    section 5 is the same ask thirty lines up. Its eyebrow is "Before you go".
  * Melissa's video STAYS. It was removed once by misreading "I don't like
    the layout" as "remove it". It is on its third layout: quote leading at
    full size, video at 24rem beside it, soft edges into the page. It plays
    in place and never navigates.
  * The CTA describes the Sounding rather than naming it. "A written page,
    two days later" was rejected as something nobody registers for.

### Open, and none of it started

  1. **The flip cards.** Above.
  2. **Phase 3**, the client work showcase. `#work` on the home page is an
     empty placeholder. The three thumbnails already exist in
     `assets/img/work/`, eighteen files, and /the-build/#work renders them.
  3. **Phase 4**, canonical, schema and performance. The canonical mismatch
     is sitewide: production serves www, and all 190 absolute references in
     source point at the apex, which 308s. Not one line of Phase 4 is done.
  4. **Phase 5**, the Gatlinburg swap, held for 16 September.
  5. `Salon &middot; Chisago Lakes MN` on /the-build/ now says salon twice,
     since the name was corrected to Mane Alchemist Salon.
  6. The stray `</div>` in index.html, still there, still harmless.
  7. `reaching-water-*.webp` and `cydnie-reading-600.webp` are unreferenced
     and the build warns about them every time.

### How to resume

    python3 tools/build.py
    python3 tools/seams.py                      0
    sh tools/preview/runsuite.sh "$SP" 8814     529 / 0, ten pages

If pages report `0 pass / 0 fail`, a stale headless Chrome is holding its
profile directories and the cleanup silently failed. `pkill -f 'Google
Chrome.*--headless'`, delete `$SP/cr-*`, run it again. That happened once
this session and looked like four pages failing.

## 55. START HERE. Session twenty-nine, 12 September 2026. Still nothing shipped.

**Section 54 still holds for everything except the flip cards.** Nothing was
committed, pushed or published this session either.

    git            HEAD f8cbf95, working tree now 14 files modified + this
    site suite     529 pass / 0 fail, ten pages
    tools/seams.py 0 mismatches

### The flip cards: the third cause, found and fixed

It was never the 3D. Every ancestor was checked for `overflow`, `opacity`,
`transform`, `filter` and `contain`; the only hit is `body { overflow-x:
hidden }`, which cannot flatten `.flip-in`. The overflow theory is dead.

**The cards got stuck.** The turn answered three states at once, `:hover`,
`:focus-within` and `.is-flipped`. A click focuses the card, because it
carries `tabindex="0"`, so `:focus-within` held it turned. Measured with real
pointer events in the Browser pane before the fix:

    hover            turned
    click            turned, focused
    click again      STILL turned (class off, focus and hover hold it)
    mouse away       STILL turned (focus holds it)

On a phone it was worse: `:hover` sticks after a tap, so a tapped card never
came back at all. Every test in section 54 flipped a card once and stopped,
which is why they all passed.

**Fix.** `.is-flipped` is the one state that turns a card. `:hover` turns it
only inside `@media (hover: hover)`. Keyboard focus draws the halo through
`:focus-visible` and does not turn. `initFlips` gained a `focusout` that
clears the class. Verified after, each with real input:

    mouse    hover turns, away returns, click then away returns, hover again turns
    phone    375px touch emulation, hover:none. Tap turns, tap returns,
             tap elsewhere returns
    keyboard Enter turns, Enter returns, Tab away returns

**The review artifact was stale.** Cydnie reported "it doesn't work based off
the artifact": that artifact (50fca51a) was folded in session twenty-eight,
before this fix, and still carried `:focus-within`. The fold was re-run and
tested with storage throwing, the way the sandboxed viewer behaves; boot
survives and the flips work. Republished to the same URL on her word,
version label "Flip cards no longer stick". The site itself is still not
pushed.

Not verified: real Safari and a real phone. If Cydnie still sees a problem,
ask what browser and device before touching the code again.

### Also noticed

`sounding-popup.js` fires after 45 seconds on the home page and covered the
cards mid test. That is the popup wired on 26 August (section 10, the
`sounding-popup.js` notes), not a regression, but it is a modal on a brand that forbids modals and
anyone testing for more than 45 seconds will meet it.

### Later the same session: THE FLIP CARDS ARE GONE

Cydnie tested the fixed artifact and the flips "still don't work", and asked
for a different interactive section instead. So the fix above is superseded:
`.flips`, `.flip-*` and `initFlips` are deleted, not patched again.

**Replaced by "the three, held"**: `.held` in index.html, 11b-i in site.css,
`initHeld` at section 19 of site.js. Same three names, teasers and detail
copy, word for word (the build script asserted it).

  * Three panels in a row, ONE ALWAYS OPEN. The open one widens to 2.3fr, a
    Meniscus waterline draws across its top, Breath light rises from its
    floor, and the detail surfaces 260ms later. Under 62rem the same thing
    stacks as an accordion, one open.
  * No 3D anywhere. No `preserve-3d`, no `backface-visibility`, no hidden
    face, and no "turn back" state to get stuck in: choosing a panel is the
    only action.
  * Hover opens a panel only under `(hover: hover) and (min-width: 62rem)`,
    with a 110ms intent delay. A click or tap anywhere on a panel opens it.
    Enter, Space, arrows, Home and End on the heading buttons. Stacked, the
    tapped heading is scrolled back under the header if closing the panel
    above carried it off.
  * Fails open: nothing collapses until JS adds `.is-live`. Reduced motion
    drops every transition and keeps the interaction.

Measured at 1280: section height 368px whichever panel is open, so nothing
below it shifts. Detail text worst glyph run 4.97:1 on the risen light.
Tested with real clicks, taps and keys at 446px and synthetic events at
1280, and in the folded artifact with storage throwing. Suite 529 / 0,
seams 0. Artifact 50fca51a republished, label "Three panels replace the
flip cards". Still nothing pushed.

### Melissa's video was leaving the page

Cydnie: "the video of melissa gets pulled offsite." Real, and reproduced:
`initVideo` emptied the `<a href="youtube.com/watch...">` and put the iframe
INSIDE it, with `target` stripped. A click that reached the anchor rather
than the frame navigated the whole tab to YouTube; the test click in the
Browser pane did exactly that. Fixed in site.js section 15: on play the
anchor is replaced by a `<div>` carrying the same classes, so no link is
left. Verified: plays in place, no `<a>` left in `.melissa`, a click on the
box stays on the page. Also fixes /retreats/, same component. Suite 529 / 0.

**Two things this cannot fix, both because it is YouTube:**
  * YouTube's own logo and title inside the player still link to YouTube.
    That is YouTube's player and cannot be switched off.
  * The artifact viewer blocks frames from every outside host, so in the
    review link the YouTube player cannot play at all.
The complete fix is to host the file on the site and use a native
`<video>` (CSP already has `media-src 'self'`). Waiting on the original file
from Cydnie; nothing named Melissa exists locally and there is no ffmpeg.
Not pushed, and the artifact was not republished for this.

### Alignment, the offer section, and the video (same session, later)

**Alignment, measured at 1440 on glyph runs.** Every section's heading,
eyebrow rule and first block now start at x=132, the wrap's inner edge.
Before: /proof header on `col-c` (233), the carousel CENTRED its front quote
(384), `.melissa` a 60rem block centred in the wrap (240), and every
`<figure class="quote">` carried the UA 40px margin. Fixed: header on
`col-d`; `xFor()` in initQuotes now left-anchors the front slide (desktop
drag mode only; the touch scroller still centres); `.melissa` spans the wrap
with the video on the right edge (1308); `.quote { margin: 0 }`. The
carousel change also applies on /retreats/, same component.

**#band rebuilt as "the offer as a decision"** (site.css 11d). Left: eyebrow,
H2, two numbered steps (the conversation, what arrives) on a drawn rule,
then the reversal, intact. Right: one card with the price, "comes off The
Build", a full width "Book one conversation" and the ask line. Phone order
is head, card, steps, objections. Not sticky. No new copy; every string
was asserted against the previous build. `.band-mid`, `.band-facts`,
`.band-ask` and `.actions--mid` are gone from the CSS and were used nowhere
else.

**Melissa.** The link Cydnie pointed to is in
`CydnieJocelyn-Site/Website Links.pdf` and is the same YouTube URL the page
already uses. The site now plays it in place, but the artifact viewer blocks
all outside frames, so the review link can never play a YouTube embed.
`initVideo` now takes `data-src` on the anchor and builds a native `<video>`
from a self hosted file instead; tested with a stand-in clip (not committed).
The file itself is still missing: nothing local matches, no ffmpeg or
yt-dlp. Once `assets/video/melissa.mp4` exists, add
`data-src="assets/video/melissa.mp4"` to the anchor on / and /retreats/ and
fold the file into the artifact.

Suite 529 / 0, seams 0. Artifact republished, label "Aligned proof, new
offer layout". Nothing pushed.

### PHASE 3 BUILT, AT GATE 3 (not approved yet, nothing pushed)

Cydnie said "lets move onto the next phases". Phase 3 of
`home-restructure-claude-code-brief.md` (in the repo root) is built. The
brief's standing rule 7 makes every phase end at an approval gate, so
Phase 4 has NOT been started. Phase 5 stays held for 16 September.

**3.1 home `#work`**: `<ul class="work-showcase" id="work">`, top of
#proof. Mane Alchemist Salon, SRS Performance, SolyRey, in that order,
brief copy verbatim (asserted against the brief file), each with the
mark and phone pair from /the-build/ (same `.case-show`, `.case-mark`,
`.case-screen`, same `--mark-x`), and the live site by its domain in a new
tab, `rel="noopener"`. CSS `.ws*` beside the old `.work-showcase:empty`
note. Three columns from 62rem; nothing overflows its Silt stage at 1000
or 1440. Images are the existing `assets/img/work/*-mark-*` and
`*-screen-*` files, already descriptive filenames, lazy, with width and
height.

**3.2 /the-build/#work**: each case gains `.case-scope` (the same brief
copy) and `.case-live` (the same link). Nothing existing was rewritten.

**Waiting on Cydnie at the gate:**
  1. Alt text. The brief says submit, not publish. The six alts are the
     ones already live on /the-build/, reused.
  2. "Built to stand." and its three `.cards` still sit under Melissa and
     now name the same three clients as the showcase. Recommended to
     remove; not removed, because it is copy the brief does not name and
     it carries a 60ms stagger reveal (motion lock).
  3. Melissa video file, still.

Suite 529 / 0, seams 0. Artifacts republished: home 50fca51a ("Phase 3:
client work showcase"), The Build 6384d178 ("Phase 3.2: work parity").

### PHASE 3 APPROVED. PHASE 4 BUILT, AT GATE 4 (nothing pushed)

Cydnie approved Gate 3 with "approved". "Built to stand." was not decided
in that reply and is still on the page.

**4.1 hostname: www.** Production already 308s the apex to www. Every
absolute `https://cydniejocelyn.com` in the 11 pages (canonical, og:url,
og:image, every schema @id and url), sitemap.xml, robots.txt, llms.txt,
tools/build_artifact.py and api/unsubscribe.py is now www: 179 in pages, 0
apex left. The redirect is 308, not the 301 the brief names; both are
permanent and Google treats them the same. Changing the code means the
Vercel dashboard domain setting, which is Cydnie's account.

**4.2 FAQ.** Home 5, /a-sounding/ carries its two, /the-build/ its one,
/retreats/ its two, all with matching FAQPage schema (checked visible
summaries against schema names). One duplicate existed across pages, "Do I
need travel insurance?" on /retreats/ and /retreats/greece/; dropped from
the GREECE schema only. The visible copy on both pages is unchanged.

**4.3 schema.** Home: the Greece Event node REMOVED (it lives on
/retreats/greece/ only now). Person sameAs is the four socials on every
page that has a Person. LocalBusiness areaServed gained Stillwater and
Woodbury on every page (the footer names them now). /the-build/ Service
gained `offers`: three AggregateOffer with lowPrice 4000, 3600, 15000 USD.
/contact/ had no schema at all; it now has ContactPage with a
BreadcrumbList. Breadcrumbs already existed, nested in WebPage, on every
other indexable non-home page. Gatlinburg is Phase 5 and untouched.
NOT DONE: Google's Rich Results Test. It needs a live URL or pasting the
code into Google's form; left for after deploy.

**4.4 on-page.** One H1 on every page. No H2 to H4 skip anywhere. One skip
of another kind, reported and not changed: /contact/ goes H1 straight to
the footer's H3 column headings because the page has no H2. The home hero
section gained `id="hero"`; every other home section already had one.
Footer area line cut to the brief's six places, "and remotely anywhere"
kept. Footer descriptor is now "Brand, operations and business development
for founders and leaders." Footer links read "The Build, brand and website
work" and "The Letters, free weekly". The phone menu shows the same
descriptors through `.nav-desc`, which is `display: none` at 56rem and up,
so the desktop nav is byte-for-byte unchanged on screen. Internal links
added on home: under the showcase "The positioning behind each of the
three" to /the-build/#work, in the offer card "What happens in a Sounding"
to /a-sounding/, under Greece "How the retreats work" to /retreats/.
Section 3 already linked /the-build/. The test's CITIES list is now the
six and checked as a subset of areaServed.

**4.4b alt text.** Every home image has alt text. The one empty alt is the
second `layer-surface-1800` in the rise band, inside an `aria-hidden`
figure: decorative on purpose, so a screen reader does not hear the hero
description twice. Two instances remain (hero and band), not one as the
brief expected. No alt text was written.

**4.5 performance.** Home now preloads the hero image with the same
srcset and sizes as the `<img>` (one request confirmed, no double
download). Width and height are on every image sitewide. Lazy loading
audited at 375x812 in headless Chrome on ten pages: nothing lazy in the
first screen, nothing eager below it. Every @font-face is swap.
NOT DONE: Core Web Vitals before and after on mobile. PageSpeed Insights'
keyless daily quota was exhausted, Lighthouse is not installed, and the
Browser pane is hidden so it records no paint timings. Run PSI on the live
URL before and after the push, or install Lighthouse with her OK.

**4.6 cleanup.** No broken in-page or cross-page anchors on 11 pages. All
three Letters buttons use cf_id 6a19d46a5cb4c5d7f86446a9. sitemap.xml is
www with lastmod 2026-09-12, still WITHOUT gatlinburg and thequestions;
robots.txt points at it. Gatlinburg noindex untouched in all three places.

Suite 529 / 0, seams 0. Artifacts republished, label "Phase 4: SEO and
schema". Nothing pushed.

### Melissa's video is self hosted. The Build page reordered for conversion.

**Video.** On Cydnie's go-ahead, downloaded from YouTube with yt-dlp in a
scratchpad venv (android client; every other client refused). YouTube only
serves this video as format 18, 360x640 H.264 with AAC, 6.85MB. Remuxed
with faststart to `assets/video/melissa.mp4` (7.25MB). Both anchors (home
and /retreats/) carry `data-src`, start at 3s via `#t=3`, and their no-JS
href is the file itself, so nothing on the page points at YouTube now.
VideoObject `contentUrl` on /retreats/ is the file. Verified: plays in a
native `<video>`, no iframe, no link left. The home artifact publishes the
file as a supporting file at `assets/video/melissa.mp4`.

**TWO THINGS SHE HAS NOT SEEN YET:**
  * The video is 3:10 long. The caption on the home page says "Forty
    seconds, filmed on her phone." One of the two is wrong.
  * 360 wide is soft at 24rem on a retina screen. If she has the original
    phone file, it should replace this one.

**/the-build/ order**, 12 sections, moved intact:
  head, where this starts, what it covers, WHAT I WON'T DO, WORK, SOUNDING,
  The Build, FULL ENGAGEMENT, PRODUCTION, what I do not do, FAQ, close.
Was: ... what it covers, work, what I won't do, sounding, build,
production, full, ... . The refusals no longer sit between the proof and the
first price (still above the prices, as brief 2.1 wants), and the price
ladder climbs once: $300, $1,500 / $6,000, $15,000, then a la carte.
Work changed ground silt to light so grounds alternate; five `--from`
values repointed; seams 0. The hero gained "Book a Sounding, $300" and a
"See every price" link to #sounding: the first button used to be six
sections down. Suite 529 / 0. Artifact 6384d178 republished.

### Melissa: original file in, caption fixed. Build page copy review given.

Cydnie put the original in `CydnieJocelyn-Site/IMG_3670.mov` (256MB,
1080x1920, 3:10; that folder is gitignored and vercelignored). Encoded with
the imageio-ffmpeg binary in the scratchpad venv to 720x1280, H.264 CRF 31,
AAC 96k, faststart: 13.9MB at `assets/video/melissa.mp4`, replacing the
360p YouTube copy. CRF 30 was 15.5MB, over the artifact's 15MB per binary
file. Caption on home is now "Three minutes, filmed on her phone. It plays
here." on her instruction. Home artifact republished with the new file.

**/the-build/ copy review (recommendations only, nothing changed):**
1,785 words in the main content, more than the home page (1,596), in 12
sections. Findings given to Cydnie:
  * The same point is made 2 to 3 times: logo not sold alone (full
    engagement, What I do not do, FAQ), not coaching (What I do not do,
    FAQ), no call needed to see prices (hero, two FAQs), nothing to prepare
    (Sounding, FAQ), monthly care (production, FAQ), every price (the FAQ
    "What does an engagement cost?" restates nine prices already shown).
  * Two "no" sections, 238 words: "Here is what I won't do" and "What I do
    not do".
  * Prices spread over four sections in paragraphs.
  * "Do you publish your pricing?" (moved verbatim by brief 2.1) says custom
    work cannot carry a number; the hero says every price is published.
    They contradict each other.
  * The Sounding section repeats /a-sounding/, which exists to explain it.
Recommended target roughly 850 to 950 words. Awaiting her choice.

### /the-build/ REWRITTEN, on Cydnie's instruction (not pushed)

"Move forward with the changes and provide proper copy." All six
recommendations built. 1,785 words in 12 sections is now 773 in 7:

  hero (93)          H1 kept; lead cut to two sentences; the old "Where
                     this usually starts" section folded in as `.bd-signs`,
                     four short lines; CTA + "See every price" -> #pricing
  What it covers(52) three items, one sentence each
  #refusals (89)     the two refusal sections merged into ONE list of six:
                     bold refusal + short reason (`.refuse-plain--lead`)
  #work (116)        case-body and case-scope paragraphs replaced by
                     `.case-tags`; Tamara's quote removed here (it is on
                     home), Spencer's kept whole; "Salon · Chisago Lakes MN"
                     is "Chisago Lakes MN" (closes open item 5)
  #pricing (212)     NEW. `.tiers`: Sounding (z-deep card, the only button,
                     keeps id="sounding"), one day $1,500, season from
                     $6,000, full engagement from $15,000. Website, Content
                     and Site care as `.alacarte` rows underneath
  #faq (178)         11 questions to 5, FAQPage schema rebuilt from the
                     visible markup. "Do you publish your pricing?" now says
                     yes, matching the closed decision "floors, published"
  close (33)         location line dropped (footer has it), retreats line
                     shortened

Grounds now light, silt, light, silt, light, silt, deepwater; seams 0. No
em dashes. No invented numbers: every price and fact is one the page
already carried.

**A collision fixed on the way.** The home offer section (11d) used
`.offer` and `.offer-price`, names already owned by the old Build price
cards, which put a grid template on those cards. Home's are now `.decide`
and `.offer-cost`. The old Build-only rules (`.offers`, `.offer`, `.shapes`,
`.phases`, `.crows`, `.refuse`, `.bd-only`, `.case-body`, `.case-scope`)
are now unused and still in site.css.

On a 375x812 phone the hero button sits at y=800, right at the fold.
Suite 529 / 0. Artifacts republished: Build 6384d178, home 50fca51a.

### Alignment pass: one page grid, Build prices aligned (not pushed)

Cydnie liked the new Build page and asked for the "sold on its own" prices
aligned, alignment checked throughout, and the Sounding button on one line.

**Measured at 1440 on nine pages.** Every heading, eyebrow rule and lead
already started at the wrap edge (132). Right columns did not agree:
`.grid-12` puts col-e at 837, but `.refuse-plain--lead` 752, `.case` 784,
`.ab-split` (about) 806, `.retreat-grid` (home) 846, `.decide` (home) 866,
`.lt-pair` (letters) 752, and home's closing FAQ used col-a/col-b (635).
Thirds drifted 532 / 538 / 540. A block at the END of site.css, "ONE PAGE
GRID", puts all of them on the `.grid-12` tracks (12 columns, 2rem gutter,
halves at 1-6 and 8-12). Home FAQ markup moved to col-d/col-e. After: every
two column text layout starts its right column at 837, thirds at 535 / 937,
the four price cards at 132 / 434 / 736 / 1038.

Left as they are, and reported: /retreats/ and /retreats/greece/ media
splits `.rt-video` (600) and `.rt-date` (656) are picture-plus-text modules
with their own proportions; `.pair` (736) and `.rt-person` (937) already sit
on grid lines. Home hero eyebrow hangs its rule into the gutter on purpose.

**Build prices.** Qualifiers ("Flat", "Starting at", "Per quarter", "Per
month, starting at") now sit ABOVE every figure, so the four tier figures
share one top and the three a la carte figures share one right edge (fixed
11rem column, right aligned). Checked level at 1280 to 2560. The table goes
four across from 80rem (it was 75rem): at 1200 the step labels wrapped and
knocked two figures 16px lower. Tier names hold two lines of height at four
across.

**Sounding button** in the tier is sized to its label: nowrap, .8125rem,
.75rem by 1.1rem padding, 44px minimum. 206px, fits its card from 375 to
2560.

Suite 529 / 0, seams 0. Artifacts republished: Build and home. /about/ and
/the-letters/ changed too (one component each) and have no current artifact.

### READ THIS: the suite had been testing a stale copy all session

**Every "529 / 0" earlier in section 55 was run against the WRONG SERVER.**
Port 8814 was held by `tools/preview/serve.py` from a previous session,
serving that session's scratchpad `preview/` as synced at 10:54 on 12
September, before any of this session's work. The trap in section 50 ("the
suite can run green against the wrong server") happened again. It was found
at 20:00, the old server was killed, `sync.sh` re-run into this session's
scratchpad, and a fresh server started on 8814 from it.

Run against the real tree, the suite was 521 / 8. All eight were the four
video assertions on / and /retreats/ still expecting the YouTube iframe.
They now assert the self hosted player (link to the file with no JS, no
YouTube link anywhere, native `<video>` in place, anchor gone on play,
`#t=3`). **Real result: 531 / 0, ten pages.** Before trusting any run:

    lsof -p $(lsof -nP -iTCP:8814 -sTCP:LISTEN -t) | awk '$4=="cwd"'
    ps -o command= -p $(lsof -nP -iTCP:8814 -sTCP:LISTEN -t)   # names the root
    curl -s http://127.0.0.1:8814/the-build/ | grep -c 'Every price, before you book'

and re-run `SP=... sh tools/preview/sync.sh` after every edit, because the
suite reads the synced copy, not the working tree.

### Retreats lined up

`.rt-date` is on the page grid from 56rem: picture cols 1-6, words cols
8-12 (837 at 1440), mirrored on `--flip`. `.rt-video` puts the video in
cols 1-4 and the words from col 5 (535), not col-e: its text column holds a
quote carousel that needs the width. `.q-slide` is now `min(42rem, 80vw,
100%)`; in a column narrower than 42rem the review in front used to run
past the right edge. The /retreats/ caption said "two minutes long"; it is
3:10 and now says three. Retreats artifact b71b2da8 republished.

### PHASE 5 PREPARED, NOT APPLIED

Cydnie said "move to the next phase". Phase 5 is the Gatlinburg swap, which
the brief holds for 16 September and says "prepare only". It is prepared as
`tools/launch_gatlinburg.py` and is NOT applied to the working tree, because
Phases 1-4 are uncommitted in the same files and the swap links the
unfindable page from the home page. Run it only on her word:

    python3 tools/launch_gatlinburg.py --check     "Not launched yet"
    python3 tools/launch_gatlinburg.py             applies it, or stops and writes nothing

It does the section 50 runbook and the brief in one pass: robots tags and the
vercel.json X-Robots-Tag off, canonical on, the parked Event JSON-LD wrapped
in a @graph with the organisation node copied from the Greece page (the suite
requires it once the page is indexable), sitemap entry; home section 6 becomes
Gatlinburg (both room rates, $500 deposit, Knoxville TYS, "Prices rise on 1
November" as the one scarcity line, Greece as one line with the waitlist
link); the Retreats index April card, ItemList, both descriptions, the price
FAQ answer (visible and schema), the facts row and the closing button; and
llms.txt. No popup, per the brief.

Tested on a copy in the scratchpad: applies cleanly, refuses a second run,
build clean, seams 0, zero HTML comments in the built Gatlinburg page, the
Event carries 4 offers, suite 527 / 0 on a separate server (8815; /retreats/
loses its four map assertions because the map card is replaced). Preview
artifacts from that copy: home b895b7fb, retreats 8a605cf1.

**Not doable from here, and required before launch:** open the four HoneyBook
service records and confirm $2,790 / $2,900 king, $1,490 / $1,600 shared,
$500 deposit. **Flagged, not changed:** the Gatlinburg page describes
Cydnie's consulting as "for women building something real", which the
11 September founders-and-leaders decision replaced everywhere else.
`armonia-arch` images become unreferenced after the swap (build warns).

## 56. START HERE. End of session twenty-nine, 12 September 2026. PUSHED.

**Read this first; section 55 is the long record of how it got here.**
Cydnie paused the Retreats page mid-fix and asked for everything to be pushed
and for notes to start a new chat from. Everything in the working tree at the
end of this session was committed and pushed to `main` (a live deploy).

    what shipped   Phases 1-4 of home-restructure-claude-code-brief.md, the
                   rewritten /the-build/, the one page grid, Melissa's video
                   self hosted, and the shared hero scrim restored
    NOT shipped    Phase 5 (Gatlinburg). tools/launch_gatlinburg.py exists and
                   has NOT been run. Gatlinburg is still noindex in both
                   places, absent from the sitemap, linked from nowhere.
    suite          531 / 0, ten pages, against a fresh sync (see below)
    seams          0

### THE RETREATS PAGE: where it was paused

Cydnie's two notes, verbatim: "Gatlinburg is not linked to the retreats page
yet." and "the hero on the retreats page doesn't work with the text."

**1. The hero.** Found and fixed ONE cause, not yet confirmed as the whole
answer. The base `.hero-scrim` gradient had been deleted during the home
hero rework (session 28); home moved to `.hero--open`, Greece has
`.hero--bright`, Gatlinburg `.hero--lit`, and /retreats/ is the only hero
with no modifier, so its Surface type sat directly on the pale sky of
`cr-horizon`. Production still had the scrim, so pushing without restoring it
would have broken the live page. It is restored byte for byte from HEAD
(site.css, "THE SHARED SCRIM, RESTORED").

**Still to do, in this order:**
  a. Measure the /retreats/ hero with the composite method in section 53:
     canvas, the real object-fit mapping (`.hero-water img` is 112% wide and
     tall at -6%, `object-position: 50% 22%`), both scrim gradients per
     pixel, the WORST pixel under each glyph run (`Range.getClientRects()`),
     at 1440 and 390. Never from a screenshot.
  b. If anything is under 4.5:1, give /retreats/ its own modifier shaped to
     this photograph, the way `.hero--open` is shaped to the home plate.
     Do not edit the shared `.hero-scrim`; three other heroes do not use it
     but any future one would.
  c. Ask Cydnie what "doesn't work with the text" means before redesigning.
     It may be legibility (above), or it may be the copy: `.hero-sub` is 70
     words and "Two dates" / "The two dates" will be wrong after launch.

**2. Gatlinburg and the Retreats page.** Not linked, ON PURPOSE: the page is
in prelaunch (section 50) and linking it is part of the launch. The launch
swap is prepared in `tools/launch_gatlinburg.py` (section 55) and replaces
the April card with a Gatlinburg card that links the page. Two things to
settle with Cydnie before touching it:
  * Does she want the Retreats page to link Gatlinburg NOW, ahead of the
    16 September launch? That makes it findable. If yes, the cheapest honest
    version keeps the noindex and only swaps the card; say so explicitly.
  * The launch preview artifacts (home b895b7fb, retreats 8a605cf1) show the
    Gatlinburg links as dead, because `tools/build_artifact.py` rewrites
    cross page hrefs only for pages it knows. It has no rule for
    `/retreats/gatlinburg/` (add one BEFORE the `/retreats/#` replace, which
    would otherwise eat it), and its ARTIFACT map is stale. Current review
    artifacts: home 50fca51a, The Build 6384d178, Retreats b71b2da8, Greece
    e3dd4a3d. `/contact/` is still rewritten to `#start`; contact exists now.

### Other open items, none started

  1. HoneyBook: confirm the four Gatlinburg service records charge $2,790 /
     $2,900, $1,490 / $1,600, $500 deposit. Cydnie's to do. Required by the
     brief before the Phase 5 launch.
  2. /retreats/gatlinburg/ calls the consulting "for women building something
     real"; the 11 September decision widened that everywhere else. Asked,
     not answered.
  3. "Built to stand." on home repeats the showcase's three clients. Asked
     twice, not answered. Still on the page.
  4. Core Web Vitals before/after were never measured (PSI quota, no
     Lighthouse). Run PageSpeed Insights on www now that it is live.
  5. Rich Results Test on the live URLs, now possible.
  6. The apex redirect is 308, not the 301 the brief names; a Vercel
     dashboard setting.
  7. Unused CSS left behind by the Build rewrite: `.offers`, `.offer`,
     `.shapes`, `.phases`, `.crows`, `.refuse`, `.bd-only`, `.case-body`,
     `.case-scope`.
  8. /contact/ skips from H1 to the footer's H3s.
  9. On a 375x812 phone the Build hero button sits at the fold (y=800).

### THE SUITE TRAP, AGAIN. Do this before trusting any run.

For most of this session port 8814 was a leftover server from an earlier
session serving files synced before the session began, and every run came
back green against them. The suite reads `$SP/preview`, never the working
tree. Every time:

    SP=<this session's scratchpad> sh tools/preview/sync.sh
    ps -o command= -p $(lsof -nP -iTCP:8814 -sTCP:LISTEN -t)   # must name $SP
    sh tools/preview/runsuite.sh "$SP" 8814

**Deploy verified, 12 September.** Commit `dab01aa` pushed; `vercel ls`
showed Production Ready in 7s. Read in a real browser on www: /the-build/
has `#pricing` with four tiers and a www canonical; home has the three item
showcase and `data-src` on Melissa; /retreats/ links Gatlinburg zero times;
/retreats/gatlinburg/ still serves `noindex, nofollow, noarchive`; zero HTML
comments on all three; the live site.css carries the restored shared scrim;
`/assets/video/melissa.mp4` answers 200 `video/mp4`, 13,883,035 bytes.

## 57. START HERE. Session thirty, 12 September 2026. One push, one draft held.

**Pushed (c32c9d6), verified live in a browser:** the home client boxes.
`.work-showcase { margin: 0 }` beat `.stack-lg` and left 0px under the Proof
heading; now 48px. `.ws-stage` gained `border: 1px solid var(--rule)`, the
`.sd-panel` pairing, because Silt alone read as a smudge. Suite 531/0.

**PUSHED 12 September after Cydnie approved it: the /retreats/ rewrite.** (Was:
before she approves it, and remember any push ships the working tree.
Review artifact: https://claude.ai/code/artifact/a478bcca-86b9-4e4b-8846-87afb5068051
(the old page is still b71b2da8 for comparison).

    before   11 sections, ~1,865 words, 14 screens at 1440, first HoneyBook button at 3.5 screens
    after     9 sections,   ~986 words, 11.1 screens at 1440, first button at 1.8 screens

  * Dates moved to second, directly under the hero.
  * Format and "The room I build" merged into one "Fifteen." section; the
    15/2/0 stat row (a copy of the hero facts) removed. `.rt-count` CSS now unused.
  * Costa Rica: three quotes (Kristi, Carol "No waiting", BJB), not five;
    ends on a "See the dates" button.
  * "Who this is not for" and "Built for the week after" became one `#fit`
    section of two `.rt-incl` lists. The general "Included" list is gone.
  * FAQ: terms block removed (its "six monthly payments" was wrong for
    Gatlinburg's five month plan); 7 questions; Kris Krause no longer named
    as leading all movement; "women only?" now answers Yes, per section 53.
    FAQPage schema regenerated from the markup.
  * The April card, the pricing answer and the close button are byte for
    byte unchanged, so `tools/launch_gatlinburg.py` still applies (tested on
    a throwaway copy).
  * `_test.html`: the three-movement FAQ assertion replaced with "questions
    only, no hub-wide terms" and "dates straight after the hero". Suite 532/0, seams 0.

Defaults taken without her answer, to confirm: the "extraction" paragraph
cut, the line "Nobody will need anything from you. Nobody will leave you
either." kept; which three quotes; Gatlinburg still NOT linked (prelaunch).
The browser pane reports `visibilityState: hidden` this session, so visual
checks used `tools/shot.sh` on port 8816.

**Second round, same session, pushed with the rewrite:**
  * `#fit` ("Read this part"): heading above, the two lists side by side at
    48rem and up (`.rt-fit-head`, `.rt-fit` grid).
  * `#private` ("By inquiry"): `.rt-aside` is now a Surface panel on Silt
    with a hairline, heading (now h-2) left, copy and button right at 56rem.
    Lost `section--tight` so the dark-to-light seam clears the panel's edge.
  * Hero: `.hero--rt` widens `.hero-copy` to 48rem and drops the H1 floor to
    1.5rem. Two lines measured at 1440, 1280, 1024, 768 and 390; three only
    at 320. Count lines from TEXT NODES: the split-word `<i>` wrappers carry
    transforms and a Range over the whole h1 reports false extra lines.
    Hero contrast NOT re-measured after the widening (section 56 item a).
  * Home: `.ws-stage` takes a Breath halo on `.ws:hover` (hover devices) and
    `:focus-within`. Review artifact 50fca51a republished with it.
  Suite 532/0, seams 0.

**Pre-push hero measurement, same session.** `tools/hero_composite.js` is the
section 53 method as one script. The rewrite's shorter copy lifted the phone
text into the sky and failed at 390 (h1 2.84, sub 4.43, links 4.34; the live
page had passed at 4.69 / 4.55 / 6.23). Fixed with a phone-only
`.hero--rt .hero-scrim` under 47.99rem, shared scrim untouched. After: every
run passes at 320, 360, 375, 390, 430, 600, 767, 768, 1024, 1280, 1440, 1920;
tightest are links 4.87 at 360 and h1 3.77 at 1024.

## 58. Session thirty, continued: the About page rebuild. NOT PUSHED.

Cydnie asked for an audit ("I am the brand. I must be sold."), then said
"yes, to all" to: cutting her story using only her own sentences, pulling
photos from the branding shoot, and using every client and guest quote.

**Uncommitted in the working tree. Do not push before she approves it.**
Review artifact: https://claude.ai/code/artifact/22daed8f-7d02-4fad-ac49-41b81414747a

  * Head: portrait (shoot frame -54, denim and laptop) beside the copy,
    a real `.btn--solid` booking button, client names under it. Rule and
    Held tick kept (`.ab-head--face`, `.ab-head-grid`).
  * "Before I tell you about me" removed (repeated the head sentence).
  * Account and "What held" cut, not rewritten: every sentence left is
    hers verbatim. The old freeze's no-bullets rule still holds.
  * What held: photo (frame -99) in the held column, baptism line as
    `.ab-pull` (Meniscus rule, not Held: the tick is the page's one Held).
  * New `#words` section on Silt: all 11 quotes in the home carousel
    component plus the Melissa facade, then a booking button. BJB's "I
    walked in carrying fear" came from the home page's Review schema.
  * The rest of me: five lines unchanged, as `.ab-rest-list` beside three
    frames (-46 singing, -68 mug, -31 journal). `.ab-true` CSS now unused.
  * "The work goes in an order" section removed; each Where to start card
    carries its line; the Questions line (which pointed at /#faq) removed.
  * New images: assets/img/cydnie-{hero,sing,mug,journal,window}-*.webp.
    build_artifact.py PICK updated.

    her own copy   1,358 -> 914 words
    page length    9.2 -> 9.4 screens at 1440, 12.6 -> 13.1 at 390 (six
                   photographs and the proof section added the length back)
    photos of her  1 -> 6
    suite          538 / 0 (about 40 -> 46: the carousel and video checks
                   now apply to it), seams 0

The 15 shoot videos are 4 to 34 second behind the scenes clips with the
photographer in frame; none is Cydnie speaking to camera.

**About, second pass (same session, still NOT pushed).** Cydnie: the section
under the head "with back to back images from the hero doesn't flow", copy
still heavy, wants trending but converting layouts.
  * Story is now five moments on a rail (`#story`, `.ab-time`), no photo.
    Veil portrait no longer used on the page. Beats are her phrasing
    COMPRESSED, not verbatim: say so if she asks.
  * Images alternate: head right, story none, faith left (`.ab-faith`),
    rise band moved to after faith, Melissa right (`.ab-proof`, side by
    side with the carousel), rest of me photos left (`.ab-rest--flip`).
  * Faith copy compressed again; "Days before, I almost backed out." kept.
  * Her own copy 1,358 -> 937 (first pass) -> 733. Page 9.2 -> 8.3 screens
    at 1440. Booking buttons at 0.7, 5.0, 6.5, 7.3 screens.
  * Suite 536/0 (about 44; it was 46 with the veil portrait's parallax), seams 0.

## 59. START HERE. End of session thirty, 12 September 2026. PAUSED FOR THE EVENING.

**Read this first.** Sections 57 and 58 are the detail behind it.

### What is live (all pushed, all verified in a real browser on www)

    c32c9d6  home     client boxes: 48px under the Proof heading, hairline panels
    251a06a  retreats rewrite (11 -> 9 sections, ~1,865 -> ~1,014 words),
             two line hero, phone-only hero scrim, fit lists side by side,
             private inquiry as a panel; home client boxes get a Breath halo
    5ad6b1e  about    rebuilt (8 -> 7 sections, her copy 1,358 -> 733 words):
             portrait in the head, story as five moments, faith with photo,
             all 11 quotes + Melissa, rest of me with three shoot photos

    suite  536 / 0 on a fresh sync (port 8816 this session, see below)
    seams  0
    Gatlinburg: still noindex, still not in the sitemap, still linked from
    nowhere. tools/launch_gatlinburg.py still applies cleanly (tested on a
    throwaway copy after the retreats rewrite). NOT RUN.

### How Cydnie wants pages worked, learned this session

  * Audit first: sections, words, screens, where the buttons fall, then
    recommendations. She answers, then build and publish a review artifact.
  * Her goals, in her words: not copy heavy, do not lose the story,
    authenticity and conversion, "I am the brand. I must be sold."
  * She notices back to back images and repeated frames. Alternate photo
    sides; never put two pictures in a row.
  * She approved compressing her own copy in her own phrasing. Say plainly
    when copy is compressed rather than verbatim.
  * Quotes: she approved using every client and retreat guest quote.
  * Branding shoot: 77 unique photos in `CydnieJocelyn-Site/Branding copy/`
    (the `Branding 2/` folder duplicates them). Contact sheets numbered 1 to
    77 were sent to her; the numbering is sort order by the number in the
    filename. The 15 videos are behind the scenes clips, not to camera.
    Used so far: frame -54 (about head), -99 (what held), -46 singing,
    -68 mug, -31 journal.

### Pages still to audit, in the order worth doing them

| # | Page | Now | Why this order |
|---|---|---|---|
| 1 | **/a-sounding/** | 9 sections, 1,109 words | The $300 offer every page's main button points at. Most conversion critical page not yet audited. |
| 2 | **/retreats/gatlinburg/** | 16 sections, 2,393 words | Launches 16 September. Audit BEFORE the launch script runs. Open: "for women building something real" wording; HoneyBook prices ($2,790 / $2,900 / $1,490 / $1,600, $500 deposit) are hers to confirm. |
| 3 | **/retreats/greece/** | 16 sections, 2,436 words | Heaviest page on the site. Full, waitlist only, so the job is the waitlist and trust, not selling seats. |
| 4 | **/the-letters/** | 6 sections, 320 words | Short already. Check the Flodesk popup and the one ask. |
| 5 | **/contact/** | 1 section, 97 words | Quick: skips from H1 to the footer's H3s. |
| 6 | **/thequestions/** | 6 sections, 309 words, noindex, not in sitemap | Decide keep, fold into pages, or remove. /about/ no longer links it. |
| - | /privacy-policy/ | legal | Not a conversion page. Skip unless asked. |

### Still open from section 56 (none started)

  1. HoneyBook Gatlinburg service records: Cydnie confirms prices.
  2. Core Web Vitals / PageSpeed Insights on www (never measured).
  3. Rich Results Test on live URLs.
  4. Apex redirect is 308, brief says 301 (Vercel dashboard).
  5. Unused CSS: `.offers`, `.offer`, `.shapes`, `.phases`, `.crows`,
     `.refuse`, `.bd-only`, `.case-body`, `.case-scope`; now also
     `.rt-count`, `.ab-true`, `.triad` block on about, `.ways-questions`.
  6. /the-build/ hero button sits at the fold on a 375x812 phone.
  7. build_artifact.py ARTIFACT map is stale and has no /retreats/gatlinburg/
     rewrite rule (section 56).

### Tools and traps from this session

  * `tools/hero_composite.js`: the section 53 contrast method as one script.
    In a hidden preview pane `setTimeout` never fires; it uses none.
  * Count heading lines from TEXT NODES; the split-word `<i>` wrappers make
    a Range over the whole h1 report false extra lines.
  * The preview pane reports `visibilityState: hidden`: screenshots come back
    blank. Use `sh tools/shot.sh <port> <path> <out> <w> <h> <scrollY|anchor>`.
    A very tall shot.sh capture inflates vh-based heights (about head).
  * Port 8814 was again a leftover server from an older scratchpad. This
    session ran the suite on 8816 (`suite-s30` in .claude/launch.json),
    served from its own scratchpad. Sync, check the process, then run.
  * Review artifacts this session: retreats a478bcca, about 22daed8f,
    home 50fca51a (republished with the halo).

**Addendum to 59, same evening. PUSHED on her approval.** She asked
for new layouts for "Also true" and the closing "Come up" band on /about/.
  * Also true is a bento (`.ab-bento`, `.ab-tile--photo/--word`): singing
    frame tall on the left, mug, journal and two word tiles as a
    checkerboard, each photo carrying its own line on a Surface chip.
  * THE BREATH HOVER IS RESTORED. The original `.ab-true` cards filled to
    Breath on hover (her request); the first rebuild (5ad6b1e, live) dropped
    it. Word tiles and photo chips fill again. Live until this ships: no hover.
  * Close is a sign-off (`.ab-close--sign`): line, one sentence, button, and
    her beside it writing (shoot frame -78, `cydnie-writing-*.webp`), with
    "Cydnie" under the photo.
  * Suite 536/0, seams 0. Review artifact 22daed8f republished.

**Correction from Cydnie, same evening:** home and /the-build/ are already
audited ("We already did the home and the build page"). They are off the
list. Remaining order: A Sounding, Gatlinburg (before 16 Sept), Greece, The
Letters, Contact, The Questions. Still worth raising with her separately:
"Built to stand." repeating the home showcase, and the Sounding popup modal.

**Mobile regression on /about/, found by Cydnie, fixed the same evening.**
From 5ad6b1e to the fix, the About page was 10,085px wide on a phone: the
single column of `.ab-proof` had no `grid-template-columns`, so its implicit
track sized to the carousel's native scroll track (eleven slides). Every new
About grid now declares `minmax(0, 1fr)` as its base. Also: the edge fade on
the carousel is wide screens only, and below 48rem that carousel shows
"back, 01 / 11, forward" instead of eleven wrapping dots. All eleven pages
measured 390px wide at 390 afterwards.

THE SUITE DID NOT CATCH IT and cannot as written: it runs at 1280, where the
desktop rule already set the columns. A phone width overflow check
(documentElement.scrollWidth <= innerWidth at 390) is worth adding.

## 60. START HERE. End of the night, 12 September 2026. Everything pushed.

**Read this first; 57 to 59 are the detail.** The working tree is clean after
this commit. Nothing is waiting for approval.

### Live tonight (every push verified on www in a real browser)

    c32c9d6  home      client boxes: gap under the heading, hairline panels
    251a06a  retreats  rewrite, two line hero, phone scrim; home box halo
    5ad6b1e  about     rebuild: portrait head, story, faith, all 11 quotes
    704f070  about     rest of me as a bento (Breath hover restored),
                       close as a sign-off with her photo
    6d89b66  about     PHONE FIX: the page was 10,085px wide (see 59 addendum)
    this     about     close photo on phones: spans the column, square;
                       from 42rem up it sits beside the copy as on desktop

    suite 536 / 0 (port 8816, fresh sync), seams 0
    all eleven pages measured 390px wide at a 390 viewport

### Next session, in this order

  1. **Add a phone width check to the suite** before auditing anything else:
     `documentElement.scrollWidth <= innerWidth` at 390 on every page. The
     suite runs at 1280 and passed straight through the About overflow.
  2. **Audit /a-sounding/** (9 sections, 1,109 words): the $300 offer every
     page's main button points at. Same method as retreats and about:
     sections, words, screens, button positions, recommendations, her
     answers, build, review artifact, push on her word.
  3. **Audit /retreats/gatlinburg/** before the 16 September launch, then
     run `tools/launch_gatlinburg.py` only when she says go (section 50).
  4. Then /retreats/greece/, /the-letters/, /contact/, /thequestions/.
     Home and /the-build/ are DONE; do not re-audit them.

### Open questions for Cydnie, carried forward

  * HoneyBook Gatlinburg prices ($2,790 / $2,900 / $1,490 / $1,600, $500).
  * "for women building something real" on /retreats/gatlinburg/.
  * "Built to stand." repeating the home showcase clients.
  * The Sounding popup (`sounding-popup.js`) is a modal; the brand guide
    forbids modals.

### Check on every About change

  * Every grid on a phone needs `grid-template-columns: minmax(0, 1fr)` as
    its base when it can hold a carousel, a scroll track or a long word.
  * Image sides alternate: head right, story none, faith left, Melissa
    right, bento mixed, close right (full width on a phone).

## 61. START HERE. Session thirty one, 14 September 2026. PUSHED ON HER WORD.

Cydnie, end of session: "both can be push to github then vercel ... We will
pick up tomorrow on more edits to these two pages and get ready for the
launch on the 16th." Both pages below are live; the commit is the one that
added this section.

### Tomorrow, 15 September, in this order

  1. **Her edits to /retreats/gatlinburg/ and /the-build/.** She reviews from
     the artifacts (Gatlinburg S3YW3q4Zyfp9crbujmDFuR, Build
     2fDqqChjFryBdVYxDSPnXC). Republish the same files after each change:
     `python3 tools/build_artifact.py gatlinburg` / `build`, then publish
     `tools/cydnie-jocelyn-gatlinburg.html` / `-build.html`. A new session
     must pass the artifact URL to update rather than create a new one.
  2. **Decisions still open with her:**
       * Countdown in the booking band, or only the plain line? (Delete
         `.gb-count` for the plain line; nothing else changes.)
       * Monthly amounts under "Hold my room, $500"? Only if she confirms the
         HoneyBook split. Arithmetic if it is even: king (2790-500)/5 = $458,
         shared (1490-500)/5 = $198; from 1 November $480 and $220.
       * A sticky booking bar: she declined it twice before; only if she asks.
       * Original, full resolution house photographs from the host or the
         listing, for a truly sharp hero and deck band.
  3. **Launch prep for 16 September (section 50 is the runbook).**
       * `python3 tools/launch_gatlinburg.py --check`, then run it ONLY when
         she says go. It touches the page head, vercel.json, sitemap.xml, the
         home and Retreats cards, site.css and llms.txt; it was re-tested on a
         throwaway copy after this rebuild and applies cleanly.
       * After: build, seams 0, suite, `grep -c '<!--' dist/retreats/gatlinburg/index.html` = 0,
         push, `vercel ls`, read the page in a real browser (curl can be
         challenged; section 60), then Search Console URL Inspection on the
         live URL and a Rich Results test for the Event JSON-LD.
       * Consider at launch: an FAQPage node generated from the six questions
         on the page (every question must be on the page word for word), and
         a purpose-made 1200x630 og:image.
  4. **Carried, not started:** the phone width check in the suite (section 60
     item 1; checked by hand this session with a 390px probe: every page
     390 wide); llms.txt line 18 still says "women"; home and Gatlinburg meta
     descriptions over 160 characters; unused CSS now also `.gb-strip`,
     `.gb-rail`, `.prelaunch`, and on /the-build/ `.triad--flat` and
     `.refuse-plain--lead`; the A Sounding, Greece, Letters, Contact and
     Questions audits (section 60).

### Session setup that worked this time
  * Preview copy for screenshots and measuring: `SP=$SP/s2 sh tools/preview/sync.sh`
    served on its own port. Run the suite from a copy nothing else syncs
    into; syncing during a run spoiled two runs today.
  * `tools/shot.sh` in parallel pairs only; four at once returned blank frames.
  * Hero contrast: open the page in the browser pane, `resize_window`, then
    `await eval(await (await fetch('/_hc.js')).text())` with
    `tools/hero_composite.js` copied into the served root as `_hc.js`.

### What was built (the detail)

The detail below was written before the push; "uncommitted" in it means
"at the time". Gatlinburg is still noindex, still out of the sitemap, still
linked from nowhere; `tools/launch_gatlinburg.py` was re-tested on a throwaway
copy after the rebuild and applies cleanly (it only touches the head of the
page). NOT RUN.

### Her answers this session (saved to memory)
  * HoneyBook is covered, prices are right, $500 holds the spot. Stop asking.
  * "Gatlinburg is for all women." The bio line "for women building
    something real" is gone.
  * "brand guide isn't always right." Do not raise the Sounding popup again;
    when an ask conflicts with the guide, build the ask.
  * Costa Rica quotes and Melissa's video on Gatlinburg: yes.
  * Kayla (her own bio, sent in chat): Minnesota National Guard nearly 20
    years, currently in her 13th year of active duty. Wife, mom of two, 6 and 4.
  * Host photo: from the branding shoot (used `cydnie-window`).
  * Park trivia cut to three numbers.
  * Countdown: "can we see an example of it or maybe we just do the plain
    line". The example is built; the plain line is always under it.

### /retreats/gatlinburg/ rebuilt
Review artifact: https://claude.ai/artifact/S3YW3q4Zyfp9crbujmDFuR
(the old page is XkGkenbSEuPinTfwjjeGFn, 31 August).

    before  16 sections, 2,409 words, 18.9 screens at 1440, 24.7 at 390
            first HoneyBook button at 10.7 screens (12.3 at 390)
    after   11 sections, 1,522 words (about 250 of them the quotes),
            15.0 screens at 1440, 19.1 at 390
            first HoneyBook button at 8.5 screens (7.8 at 390)
            the five-day step-through alone is 3.5 screens of scroll

Order and grounds: hero (deep) / statement (deep) / deck band (deep) / five
days `.cond` (light) / In their words `.ab-proof` (silt) / house: room cards
then the 24 tile rail (light) / included checklist (silt) / where you are
(deep) / hosts side by side (light) / FAQ, six questions with the ask line
(silt) / book (deepwater), page ends there. Removed: the "Register today"
strip and the close band (both only linked back up the page), the rockers
band, What to expect (repeated the premise and the FAQ), the park dropdowns
and stats.

New motion, all in site.css "GATLINBURG, THE REBUILD" and site.js section 20:
  * `.gb-push`: hero photo `scale` 1 to 1.07 over 24s, once. `scale`, not
    `transform`, so initHero's inline parallax transform still applies.
  * `[data-wordlight]`: statement words brighten with scroll (`.gb-w`).
  * `.par[data-max]`: per-image lift of the 12px parallax cap (deck band 40).
  * `.gb-checks`: ticks draw in (stroke-dashoffset) with the reveal.
  * `[data-count]`: numbers count from 0 once; zeroed on the first frame
    only, so no frames means the real figure stays.
  * `.gb-host .r-img`: portraits unveil upward (clip-path) and lean in on hover.
  * Room cards and booking picks lift with a Breath glow (`translate`, so the
    reveal transform is not fought).
  * `[data-countdown]`: to 2026-11-01T00:00:00-05:00 (midnight Central after
    31 Oct), ships `hidden`, removes itself at zero. IF SHE PICKS THE PLAIN
    LINE, delete `.gb-count` from the page and nothing else changes.

Copy compressed rather than verbatim: the statement's lead, the five day
lines, both host bios (now first person), the where-you-are panels.

### /the-build/: What it covers and What I won't do
Review artifact: https://claude.ai/artifact/2fDqqChjFryBdVYxDSPnXC
Her note: both sections were "the same layout and don't make anything stand
out". What it covers is `.bd-areas`, three panels that fill Breath on hover.
What I won't do is `.bd-nots`: sticky heading left, one column of large lines
right, a Held-warm rule drawn through each (`<s>`) as it arrives. `.triad
--flat` and `.refuse-plain--lead` are now unused on this page.

### Crawlability (she asked mid-session)
Checked read-only: nothing blocks crawlers. Live pages, robots.txt and the
sitemap return 200; no custom firewall rules; Attack Mode off; Bot Protection
and AI Bots rulesets at defaults. Verified bots are exempt from Vercel's bot
protection, but a custom rule or AI Bots set to Deny would block them. Fixed:
  * `home-restructure-claude-code-brief.md` was LIVE at its path (phase plan
    and launch date). Now in `.vercelignore` and build.py EXCLUDE_FILES.
  * llms.txt said there is no /contact/ page. There is.
  * sitemap lastmod for /the-build/ to 2026-09-14.
Not changed, worth raising: llms.txt line 18 USP still says "women"; home and
Gatlinburg meta descriptions run 173 and 183 characters.

### Second round, same session: photos, type, conversion

**Photos.** "Can the hero image and the deck porch image not be so blurry?"
Mostly the review artifact, whose PICK used the 600px files; now 1632/1654.
On the page: the sources are listing screenshots (hero 1944x1112, cropped to
1632 to lose the plaque; deck 1654x1112), so the old 1600 files were already
near native. Re-exported at native width, q86, UnsharpMask(1.4, 70, 2) as
`house-dusk-1632.webp` and `deck-view-1654.webp`; hero image 104% instead of
112% on this page, push-in 1.035. Truly sharp needs the original photographs.

**Build type.** "verify the font sizes for the what I won't do section".
Measured: the struck lines were 40px under a 33.4px h-2 at 1440 (23.2 vs 22.7
at 390), and the area titles (c-2) were 35.7px under the same h-2. Now
clamp(1.25rem, 1.8vw, 1.625rem) = 26px / 20px, and the titles are c-3 (23.8 /
21.3). Every level sits under its heading at every width.

**Conversion.** Cydnie: the five month plan starts with the $500 deposit, the
first of five payments is the month after; "Make the right changes to drum up
conversion and sales."
  * "Hold my room, $500" is now the PRIMARY button on both room cards and both
    booking picks and links the five month plan record; "Pay in full" is the
    quiet one. A note under each card says how the plan runs. Hero button:
    "Hold your room for $500" (to #rooms).
  * Hero facts are six: Dates, Where, Group (Fifteen women, the cap every
    retreat page states), With (both faces, new `kayla-face-72/144.webp`),
    From $1,490, To hold a room $500. Two columns on phones.
  * `.gb-rate-strip` above the room cards: "Early rate through 31 October"
    plus `[data-daysleft]` ("47 days left", hidden until JS has a number).
  * `.gb-list` in the FAQ's left column and `.gb-later` under the booking
    band: "Not ready to decide? Join the Gatlinburg list", HoneyBook
    69fa3c69 (April 2027 pre-registration, already pinned in _test.html).
  * NOT DONE, on purpose: per-month dollar amounts (HoneyBook's split is not
    confirmed), a sticky booking bar (she declined it twice, and the consent
    banner owns the bottom edge).

**Hero contrast, measured with tools/hero_composite.js in the browser pane.**
The COMMITTED page already failed on phones and tablets: 390 h1 2.46, eyebrow
2.28, sub 4.22; 768 eyebrow 3.17, sub 3.28; 1024x768 sub 3.65, link 4.43.
Fixed with page-scoped scrims: one under 47.99rem, a stronger across-fade from
48 to 84.99rem, and the lit scrim kept above that (wide screens keep the lit
house) with the eyebrow ink lifted to #C9DCD9 (was 4.49 at 1440). After:
passes at 360, 390, 430, 768, 1024, 1152, 1280, 1366, 1440 and 1920. Tightest:
h1 3.04 at 1920, sub 4.52 at 1366. The "SPAN" row the script reports is the
solid button's own label on its Breath fill, not text on the photograph.

### Checks
    build, 0 comments in dist for both pages, seams 0,
    launch script applies on a throwaway copy with valid JSON-LD
    suite 544 pass / 0 fail on ten pages (gatlinburg 80, build 39), fresh
    sync, run from `$SP/s2` on a threaded server
    every page checked 390px wide at a 390 viewport (by hand, not in the suite)

**THE SUITE HUNG ON GATLINBURG, AND IT WAS THE SERVER, NOT THE PAGE.**
`tools/preview/serve.py` was a single-threaded TCPServer. Headless Chrome's
virtual clock stops while any request is outstanding, and the rebuilt page
plus the 375px probe iframe open enough connections that one idle keep-alive
socket held the queue: an empty dump for 12+ minutes, reproducible, and it
bisected to "page length" rather than to any one section. The browser pane
ran the same test to completion. `serve.py` is now a ThreadingTCPServer and
the page finishes in 4 seconds. If a suite run ever hangs with `dom-<page>.html`
at 0 bytes, check the server first.

`_test.html` changed twice, both deliberately: the parallax cap is now each
target's own `data-max` (12px when none is declared), and "opens a short form"
counts as an off-site link that says so.

## 62. START HERE. Launch day, 16 September 2026. GATLINBURG IS PUBLIC.

Cydnie: "Its september 16th and we need to link gatlinburg to the retreats
page. I also want to do a popup that invites people to go register since
it's finally here." Taken as the go for the section 50 launch.

### What changed
  * `tools/launch_gatlinburg.py` RUN. Gatlinburg: robots meta gone, canonical
    live, Event + LocalBusiness JSON-LD live; vercel.json X-Robots-Tag gone;
    sitemap lists it (lastmod 2026-09-16); home section 6 is Gatlinburg
    ("Booking open · April 2027", Greece one line under it); the Retreats
    April card is Gatlinburg with the house photo (the US map is gone from
    the page); Retreats schema, FAQ price answer, meta descriptions, closing
    CTA ("Choose your Gatlinburg room") and llms.txt all name it. The script
    now refuses to run again ("Already launched").
  * Retreats: title now "Retreats for Women | Gatlinburg and Crete 2027 |
    Cydnie Jocelyn"; the card button is solid, "See Gatlinburg and book".
  * **`gatlinburg-popup.js`, new, at the root.** A launch dialog: house
    photograph, "Wide Open is finally here.", fifteen women, $500 holds a
    room, early rate line, one button to /retreats/gatlinburg/, "Maybe later".
      - Pages: home, /retreats/, /retreats/greece/, /the-letters/ (ONLY_PATHS),
        with the rest excluded by name as well (SKIP_PATHS).
      - Opens after 12s of VISIBLE time, or at 35% of the page read after 4s.
      - Dismissal remembered 14 days (`gb_pop_dismissed`); stops itself on
        13 April 2027.
      - ONE POPUP A VISIT: it writes `cj_pop_shown` to sessionStorage, and
        `sounding-popup.js` now reads and writes the same key, so a reader
        never gets both. On home, Retreats and Letters, Gatlinburg fires first.
      - Skipped inside a same-origin frame whose parent path starts with `/_`
        (the suite and shot harnesses), so tests are unaffected; a
        cross-origin frame still shows it. `gbPopPreview()` in the console
        opens it (it is only defined if the script did not return early:
        clear `gb_pop_dismissed` and reload first).
      - Brand guide conflict (it forbids modals) named to her; her call.
  * Local preview in this session: `.claude/launch.json` config `gb-launch`
    serves `$SP/preview` on 8830 with a scratchpad copy of serve.py (the
    pane cannot run files from ~/Desktop).

### Checks before push
    build clean, seams 0, 0 comments in the three launched pages
    suite 540 pass / 0 fail (retreats 65 -> 61: the map assertions no
    longer apply now the card carries a photograph)
    390px wide: home, /retreats/, /retreats/gatlinburg/
    popup verified in the browser: opens on scroll, focus lands on the
    button, Escape closes it and restores scroll, dismissal stored, the
    Sounding popup stands down in the same session

### After the push (do these)
  1. `vercel ls` Ready, then read /retreats/gatlinburg/ in a browser: no
     robots meta, canonical present.
  2. Search Console: URL Inspection on the Gatlinburg URL, Request Indexing;
     resubmit sitemap.xml. Rich Results Test on the URL (Event).
  3. 31 October: early rate ends. Room cards, booking band line, rate strip,
     popup NOTE, home card, Retreats card and FAQ answer all say it; after 1
     November the prices are $2,900 and $1,600 and the popup NOTE, the
     `data-daysleft` strip and the countdown all need changing or removing
     that day (the countdown and strip remove themselves).
  4. Still open from 61: monthly amounts, original photos, the phone-width
     check in the suite, the remaining page audits.

**Addendum to 62, same day.** Cydnie: "Remove the 15 women ... on the popup.
and the cap 15 guests on the hero of the retreats page." Both removed and
pushed. "Fifteen" still appears elsewhere and was NOT touched, because she
named only those two: the Gatlinburg hero fact "Group: Fifteen women", the
rooms lead and the booking band lead on that page; on /retreats/ the
"Fifteen." section and its ring, "Bring your own fifteen.", the closing
"Fifteen seats" heading, the FAQ answer and the og/twitter titles; and the
home page's retreat schema description. Ask her whether the cap should go
from those too.
