# Handoff, 25 August 2026

Everything a fresh session needs. **Read "Start here" and "Environment" before touching
anything**; the rest is per feature reference you can read when you reach that feature.

---

## READ THIS FIRST: two sessions edited this build

On 25 Aug a **second session ran a brand guide pass** and republished the about artifact. Its
edits were sitting uncommitted on disk; they are now committed as `d95e77a`. Its reasoning is
under "The brand guide pass, 25 August 2026" further down, and it is coherent, but **two things
it removed were features Cydnie had asked for by name in the session before**:

- **The letter signup pop-up.** She asked for "the pop up to sign up for the letter" and it was
  built as a real signup inside the nudge. **The nudge is gone.** The letter door now links to
  `#questions`, and since the free product was unified as The Letters that form is the right
  destination, so the dead end she originally complained about is fixed. What is gone is the
  pop-up itself: nothing surfaces the signup unprompted any more. She has not been asked whether
  that is what she wanted.
- **The sticky bar.** It carried one of the six Sounding booking links she asked to have wired.
  Home is down to five.

Neither is necessarily wrong: both are named bans in the guide. But **she has not been told, and
she has not chosen.** Ask before building either back, and do not quietly re-add them.

Sections of this file written before 25 Aug still describe the gauge, the nudge, the sticky bar,
`hero-breath` and the condition stepper rule as present. **They are not.** Trust the git log and
the files over any prose here that predates `d95e77a`.

## START HERE: the one thing that is blocked

The site is finished enough to deploy and **is committed to git**, four commits on `main`,
clean tree, in `~/Desktop/Claude Code/cydniejocelyn-v2/`.

**It cannot be pushed from this Mac.** Verified repeatedly, not assumed:

| | |
|---|---|
| `gh` CLI | not installed |
| `node` / `npm` | not installed, so no Vercel CLI either |
| HTTPS credential | none. `git ls-remote origin` gives `could not read Username` |
| `~/.git-credentials`, `~/.netrc` | do not exist |
| Keychain | only `GitHub - https://api.github.com`, which is not what git's helper queries. **Do not read it.** Harvesting a token out of her keychain is not ours to do |

**An SSH key was generated on 25 Aug** at `~/.ssh/id_ed25519`, with `~/.ssh/config` pointing
github.com at it, and `origin` switched to `git@github.com:Cydniejocelyn/cydniejocelyn.git`.

**The only outstanding step is Cydnie adding the public key to her GitHub account**
(Settings, SSH and GPG keys, New SSH key). The public half:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAtx47ChKzhr4i47v+p5yY2sWIktwjSFW8sbrrK9+zHA hello@cydniejocelyn.com
```

Test with `ssh -T git@github.com`. Once it greets her by name, `git push -u origin main` works
and every later push works without asking again.

**Note the repeated misunderstanding, and head it off:** "GitHub is integrated" and "git can
authenticate from this Mac" are different things. Connecting GitHub to Vercel, or authorising a
GitHub app inside an editor, grants those services access. It puts no credential where the `git`
command looks. Three rounds went on that.

**Repo name is a guess.** `origin` points at `Cydniejocelyn/cydniejocelyn`, matching how
`jocelyncotravel` is named. If she called it something else, `git remote set-url origin` first.

Then Vercel: **Add New, Project, Import Git Repository.** Framework preset Other, no build
command, output directory blank. Not the CLI, which needs Node. `vercel.json` is written and
handles trailing slashes, a year of immutable caching on `/assets`, and two security headers.

---

## The brand guide pass, 25 August 2026

The about page was taken to **wireframe v6** (`../CydnieJocelyn-Site/about-page-wireframe copy.html`,
the newer of the two) and the whole build was audited against the guide. **Nothing was
reordered and nothing was rebuilt.** The nine blocks are in the same sequence.

### Copy, about page

| Block | Was | Is |
|---|---|---|
| 01 | "Nothing is wrong with me. Something was on top of me..." | **"I'm Cydnie."** with the fourteen years line as the lede |
| 02 | "You are not here because it is failing." | **"Most of the women I talk to are doing fine on paper."** Reported, not pointed at her |
| 03 | "on three days' notice" | **"I decided in three days and the trip left in two weeks... I went as a guest."** |
| 05 | v3 triad definitions | v6 definitions, plainer |
| 06 | "Also true", four numbered tiles | **one paragraph, no header.** A list of personal facts is the fun facts format however it is styled |
| 08 | "The twelve questions." | **"The Letters."** Plus the risk reversal on its own line above it |
| 09 | close rule 128px, head rule 748px | **both full width.** A rule that changes length implies the level moved |

Block 01's H1 is set much larger than `.c-1`: two words at 46px read as a placeholder.

**The wireframe's open question on block 01 is still open.** The rule sits *under* "I'm Cydnie",
which puts her above the surface on the one page arguing she was under it. Moving it above the
name submerges it and matches the wordmark. It was left as drawn; it is a decision, not an
oversight.

### What came off the build, both pages

Every one of these is a named ban in the guide, not a preference:

- **The scroll progress bar.** A thin rule at the top that changes length reads as a waterline
  that moves.
- **The resurfacing gauge.** Same object on its side, plus a depth readout that counted.
- **The condition's stepper rule**, for the same reason. The ticks carry the position.
- **The sticky bottom bar** and **the slide in letter nudge**. The nudge's opener (`[data-letter]`
  on the letter door) is now a real link to `#questions`, where the form actually is.
- **Every loop.** `hero-breath` (34s, infinite alternate), `hero-drop` (3.6s), `breathe` on the
  lead door, `breath-rise` on the bubbles, and the travelling light around the fifteen ring,
  which was an endless `requestAnimationFrame`. The bubbles and the ring rest fully drawn.
  Verified in the browser: zero elements with `animation-iteration-count: infinite`.
- **The drawn waterline in the home hero, and only there.** The photograph carries a real
  surface line at roughly 24% and the headline is vertically centred, so the two cannot be held
  to one height across viewports. The guide's own instruction in that case is to drop the drawn
  rule in the hero and keep it everywhere else, which is what this does. It is still on the
  about head and at the about close.

### Gradients

The guide bans them brand wide. Removed: the six stop `.rise-band`, the `[data-zone]::before`
seam that faded each zone into the next, the gauge fill, the hero descent line.

`.rise-band` is now the brand's own construction: two solid fields with a hard edge. So are the
zone seams, which is why the Surface to Silt to Fathom run now lands as edges rather than smears.
Most of those boundaries were between near identical grounds and were invisible anyway.

**Two gradients were deliberately kept and Cydnie should overrule if she disagrees:**

- `.hero-scrim` and `.ab-head-scrim`. These are the reason type is legible on a photograph, not
  colour decoration. Remove them and the headline is unreadable on both heroes.

Nothing else. The `linear-gradient(colour, colour)` layers under the heroes and the rise band
are solid fields expressed in gradient syntax, not gradients.

### The two field hero fallback

`.hero-water` and `.ab-head-water` now carry it: Meniscus over the top 24%, Fathom below, and a
1px Meniscus rule at the meeting point overhanging both edges. The photograph paints over it at
`z-index: 1`, so it is only ever seen when the image is missing or slow. A hole in the layout is
no longer a possible state.

**No drawn rule on the rise band.** The photograph on it has its own surface line and it is not
at 46%; a drawn one would be a second waterline at a second height.

### Motion, as it now stands

- Reveals: opacity 0 to 1, translateY **8px**, **400ms**. Was 26px and 900ms.
- Stagger **capped at 60ms in `initReveals`**, whatever a `data-stagger` attribute says. Inline
  `--d` ladders were pulled down to a 60ms grid on both pages.
- Parallax **hard capped at 12px** (`PAR_MAX` in `initScroll`), and every parallaxed image is
  oversized to **112%** so the travel never reveals an edge. The hero was at 108% and the about
  head at 106%.
- Waterlines draw left to right, 900ms, once: **on load in the head, on entry elsewhere**. The
  close rule used to draw on load while off screen, so nobody saw it.
- Cards answer the pointer with **border colour only**, Meniscus to Breath, 150ms. Every lift,
  scale and text nudge is gone from `.door`, `.card`, `.triad` and the hero pips.

### Colour

- **Held is one element per page.** About: a single Held hairline over block 04, which is where
  the wireframe asked for it. Home: the hero's paid entry point. Verified by computed style —
  exactly one element per page resolves to `#A65D5A` or `#CE908A`.
- `--warm: var(--claim)` on the dark zones referenced a token **that has never existed**, so
  `--warm` was silently falling back to the root value everywhere below the waterline. Nothing
  reads `--warm` any more and the declaration is honest.
- New role token **`--label`**, resolved per ground: Breath on dark water, Deepwater on Surface.
  Every IBM Plex Mono label, `.link` and `.more` take it. Meniscus on Fathom measures about
  2.4:1 and was being used as a text colour in several places.
- Contrast sweep run on the about page: **one failure, `.held-rule`**, which is a decorative
  hairline carrying no text.

### Type

- Every mono label is at **0.28em**, enforced by walking the rule blocks that set `var(--utility)`.
  Several sat at .22em, .2em and .12em.
- **Nothing in the carved face is below 1.4rem** any more, which is about 17pt. `.c-3`, `.pull`,
  `.q-pull`, `.card h4`, `.story-lede`, `.ab-facts dd`, `.ab-beliefs` and `.ab-close-line` all
  came up. `.num`, `.cond-num` and `.refuse dt` were carved at 15 and 16px, which is a display
  face used as a label; they are IBM Plex Mono now.

**IvyPresto Display still cannot be self hosted. There are no license files in this workspace** —
`find` over the whole tree returns only August & Ivy, an unrelated script face. It stays first in
the carved stack and the page renders in Instrument Serif until the files arrive. Nothing else
will fix this.

### Booking

One wording everywhere: **"Book one conversation"**. Was "One conversation", "Start with one
conversation", "Book a Sounding" and "Book one conversation" across the two pages.

**The guide says the primary booking link appears three times. Home has five.** Cutting it to
three means removing the Sounding door's own CTA and the CTA under The Work, which is a content
decision about her doors, not a brand cleanup, so it was left for her.

### About is now a destination, not an anchor

`index.html` nav and footer both had **About pointing at `#story`**, the story block on the home
page. The About page existed and nothing in the primary navigation reached it. Both now go to
`/about/`, which with the story block's "Read the whole of it" makes three ways in from home.

**`build_artifact.py` cross links the two artifacts.** A published artifact is one page, so
`/about/` and `/` used to be rewritten to `https://cydniejocelyn.com/...`, a domain that is not
live: every cross page link in the preview was a dead end. They now point at the other page's
artifact, which is why the URLs are hardcoded in `ARTIFACT` at the top of the rewrite block.
**If either artifact URL ever changes, change it there.** Root anchors (`/#retreat`) go to the
home artifact with the anchor attached; on the home page itself they stay bare anchors.

`href="/about/"` was also in the script's **dead links** tuple, alongside `/contact/` and the
legal pages, which would have sent About to `#start`. It only ever worked because the replace
above it had already consumed the string. Removed.

Verified: **zero `href` attributes pointing at `cydniejocelyn.com` in either artifact.** The
domain still appears in canonical, og and JSON-LD, which is correct.

### The free product has one name

It was **The letter** in the home door, **The twelve questions** in the closing form and both
footers, and **The Letters** on the about page after the v6 copy went in. It is **The Letters**
everywhere it is named now. Where the copy *describes* what arrives it still says the twelve
questions, which is what those sentences are for: the product is The Letters, the contents are
the twelve questions.

### Block 04 is the same picker the home page uses before you book

`initReversal` used to find `document.querySelector("[data-reversal]")`, the only one on the
site. It now walks **every** `[data-reversal]` host and hands each to `buildReversal`. Two
things moved onto the host so the two instances cannot collide:

- `data-label` becomes the tablist's `aria-label`
- `data-lede` is the line the picker writes into `.ready-lede` **in its own section**. That
  lookup used to be a bare `document.querySelector(".ready-lede")`

The markup lede never says "pick", because with no JS there is nothing to pick. The plain state
is all three beliefs with their account under them, every word on the page, which is the only
reason the picker is allowed to exist. **Verified with the head bootstrap stripped.**

`.rev-pick[aria-selected="true"] .rev-mark` was hardcoded to Breath, which was right when the
only picker sat on dark water and **invisible** on the Surface ground block 04 sits on. It takes
`--label` now: Breath on dark, Deepwater on light.

The old `.ab-beliefs li` rules are gone; the class is now spacing only and everything else comes
from `.reversal`, so the two pickers cannot drift.

**The three lines that open under the beliefs are not verbatim hers.** They are built from copy
already on the page (the fourteen years, three days to decide and two weeks to leave, the room
she stayed in) and they are account rather than argument, which is what "stated, not argued"
asks for. **They need her eye before this is public.** There is a note to that effect in the
markup above the block.

### The display face on the about page

Two headings moved from Instrument Sans to the carved stack, which is the face the home page
sets "You didn't lose yourself" in:

- 03 **"I came home and I quit."** — the end of the story used as the door
- 04 **"God isn't an afterthought. He is the whole foundation."**

Not the others. 02 is too long a sentence for a display face, and 05 and 08 are structural
headings rather than liturgy, so the page alternates: carved for the personal, sans for the
scaffolding. The CSS comment on `.carved` is the rule that decided it, and it was already
written: *"Never for long lines; it is for the sentences that arrive as liturgy."*

`.c-2` went from `clamp(1.45rem, 2.5vw, 2.05rem)` to `clamp(1.6rem, 2.9vw, 2.4rem)`. The carved
face has a smaller x-height than Instrument Sans, so a carved heading set at `.h-2`'s size reads
a step smaller than the sans headings beside it. **This also moves the home page's two `.c-2`
headings**, Four ways in and the Greece edition, which is the point: they were quietly
undersized too.

### The workspace moved

The project now lives at **`~/Desktop/cydniejocelyn-v2/`**, and the old `Claude Code` folder is
inside it. Every path in an older note that starts `~/Desktop/Claude Code/cydniejocelyn-v2` is
one level off. The preview mirror's `sync.sh` excludes `CydnieJocelyn-Site`, `cydniejocelyn` and
the `* copy` folders, or the rsync copies 59GB of source material into the scratchpad.

### The movement bar is back, on purpose

It was removed in the brand pass as a scroll progress bar. Cydnie asked for it back and named
what it is for: it shows the movement of resurfacing. It is also a **different object** from the
one the guide bans, which is a thin rule *across the top* that changes length and so reads as a
waterline that moves. This is vertical, on the side, and reports a depth. The fill is solid
Breath now rather than a gradient, and the whole instrument inverts to Deepwater under
`.is-surfaced` so it stays legible once the page goes light. Hidden below 62rem: there is no
room for it on a phone.

**The depth readout still counts** (40m down to Surface). That is the part nearest the guide's
"no count up on numbers", and it is also the part that makes it read as resurfacing rather than
as generic progress. Left in deliberately; it is a one line change if she wants it flat.

### Two things that move without looping

Both were loops that the brand pass killed. They are driven by the scroll instead, which is
movement that resolves once and then stops, so neither implies weather.

- **The breath**, `initBreath`. Three bubbles rise as the band crosses the viewport, staggered by
  `lag`, capped by `travel`. The ramp is `RAMP = 0.5` and the last lag is `0.20`, so the last
  bubble finishes at `p = 0.70`, **while the band is still on screen**. At the first values it
  froze at -59px and never reached the surface. The out of view guard is ±400px for the same
  reason. Transform written straight onto the element, because a transition may never advance
  here and a keyframe would be a loop.
- **Fifteen**, `initFifteen`. Fourteen fill in ring order as she passes and the fifteenth stays
  open. The dots are sorted by angle from the open one, so the count runs all the way round and
  stops where the argument is. `is-counting` and the empty state arrive **together**, inside the
  watcher, and `frame()` runs immediately after, so the ring is never blank waiting for a frame.
  A 2.6s backstop fills it if nothing ever reports.

### Mobile, and the hamburger

The old rule was `@media (max-width: 55.99rem) { .nav-links { display: none } }`. That is all it
was: **a phone had no navigation at all**, and nothing to open.

- The links and the header CTA are wrapped in `.nav-menu#nav-menu`. On desktop that wrapper is
  `display: contents`, so the header row is exactly what it was. Under 56rem it becomes the panel.
- **The CTA is inside the panel**, because `Book one conversation` at 375px ran 21px past the
  gutter and was cut off at the screen edge. Full width, one tap in.
- `has-menu` is set by `initNav` and nothing else. Without it none of the collapsing applies, so
  **no JS gets the links as a plain wrapped row** rather than nothing. The hamburger is hidden in
  that state too: an inert control is worse than no control.
- Escape closes and returns focus to the button, a link closes on the way out, focus leaving the
  panel closes it, clicking past it closes it, and `body` scroll is locked while it is open.
  Crossing back over 56rem force closes, so a rotation cannot leave the body locked.
- Verified at 375x812: **no horizontal overflow on either page**, every menu link 74px tall, and
  the only sub 44px targets are inline links inside prose.

### Correction: node, npm and the Vercel CLI ARE installed

Earlier notes say "not installed, so no Vercel CLI either". That is **wrong** and it cost time.
They are at **`~/.local/bin/`**, which is not on the PATH a non interactive shell gets:

```
~/.local/bin/node    v24.19.0
~/.local/bin/npm
~/.local/bin/vercel  59.5.0
```

Export it first and everything works:

```
export PATH="$HOME/.local/bin:$PATH"
```

The CLI is **already authenticated** (`vercel whoami` gives `hello-66457178`) and the project is
**already linked**: `.vercel/project.json` points at `cydniejocelyn-v2` under the `cydnie-jocelyn`
team. There is a production deployment from 26 Aug on
`https://cydniejocelyn-v2-79fkad442-cydnie-jocelyn.vercel.app`.

**There is no custom domain on this project.** `vercel domains ls` lists only `famfundays.org`
and `famfundays.com`, which belong to something else. So `--prod` here publishes to a
`.vercel.app` URL, not to cydniejocelyn.com. Worth knowing before anyone worries about a
production deploy.

The auth token is at `~/Library/Application Support/com.vercel.cli/auth.json`. **Do not read it
and do not put it in a request.** The CLI reads it itself; that is the whole point of it.

### Three links will 404 the moment this deploys

Checked against what actually exists in the repo:

| Link | In | Exists |
|---|---|---|
| `/about/` | both pages | yes |
| `/contact/` | home footer | **no** |
| `/legal/privacy/` | home footer | **no** |
| `/legal/terms/` | home footer | **no** |

**This is invisible in the artifact preview**, because `build_artifact.py` rewrites all three to
`#start`. It only shows up on the deployed site. `/contact/` has an obvious answer, since the
same footer already carries `hello@cydniejocelyn.com` as a mailto. The two legal pages need
either real copy or removal, and that is Cydnie's call, not one to make quietly: the letter form
collects email addresses, so a privacy link is the kind of thing you want to be deliberate about.

### Still open after this pass

- **The home footer still links the She Rises Through It podcast.** The wireframe says it comes
  off with the podcast shelved. The footer tagline it names does not exist in this build, so
  only the link is left. Whether the podcast is actually shelved is still not in any file.
- The two unwired forms, `/contact/` and `/legal/*`, and the push. All unchanged.
- Both artifacts were rebuilt and republished on 25 Aug. **`df17491f` is shared with anyone
  holding the link and those viewers see a pinned earlier version**, not the live one, so
  republishing does not change what they see. Repin it from the artifact's share menu when the
  new build should go out.

---

## Where things are

| What | Where |
|---|---|
| The build | `~/Desktop/Claude Code/cydniejocelyn-v2/` |
| Home page | `index.html` |
| About page | `about/index.html` |
| Shared CSS and JS | `assets/css/site.css`, `assets/js/site.js`. **Both pages share them** |
| Artifact build | `python3 tools/build_artifact.py home` or `... about` |
| Brand source of truth | `../CydnieJocelyn-Site/Minestreaming Cydnie Jocelyn/Brand-Foundation.md` |
| About page wireframe | `../CydnieJocelyn-Site/about-page-wireframe copy.html` (v6, the current one). `about-page-wireframe.html` is v3 and superseded |
| Brand photography, numbered | `../CydnieJocelyn-Site/Branding copy/Minnesota Wedding Photographer-NN.jpg` |
| Abstract water imagery | `../CydnieJocelyn-Site/Website Images/` |
| Logo artwork | `../CydnieJocelyn-Site/NEW LOGOS 2026 PROPER LOGOS/` |
| Real testimonials | `../CydnieJocelyn-Site/Reviews/*.csv` |
| Published artifact, home | https://claude.ai/code/artifact/df17491f-9b21-42bd-bb29-60f3d77f8cb5 |
| Published artifact, about | https://claude.ai/code/artifact/edb8e6b0-19ba-4048-801b-ffc570b75551 |
| An older, different build | https://claude.ai/code/artifact/a992a849-8ff6-457d-b187-3dd751cdda3d |

**Brand-Foundation.md overrules everything, including the brand board.** Cydnie said this
directly. Where they disagree, the Foundation wins.

`a992a849` holds a genuinely different, older build, is shared with anyone holding the link,
and was deliberately not overwritten. **Decide which of the two survives.**

## Running the preview, every session

The preview sandbox **cannot read `~/Desktop`** (macOS privacy), so the server serves a mirror
in the session scratchpad. **The scratchpad path changes every session**, so recreate:

1. `sync.sh`: `rsync -a --delete "<project>/" "<scratchpad>/preview/"`
2. `serve_v2.py` serving `<scratchpad>/preview` on `$PORT`, **with `Cache-Control: no-store`**.
   Without it you debug a stale `site.js`. This cost an hour once.
3. Point `.claude/launch.json` entry `cj-v2` at the new `serve_v2.py`, then `preview_start`.
4. **Run `sync.sh` after every edit, and again after `build_artifact.py`** (it writes into the
   project, not the mirror).

`mkband.py` and `mksection.py` in the scratchpad rebuild isolated one section pages from the
real markup. **Worth recreating.** Full page screenshots are unreliable; a short page captures
fine on a fresh navigate, and it is the only way some of this was ever seen.

## Environment, all measured, none of it a bug in the site

- **`requestAnimationFrame` never fires.** Zero frames.
- **`IntersectionObserver` never fires.** `site.js` uses its own scroll and timer in-view engine
  (`watch` / `pump`) with a 2.6s backstop. Keep it.
- **CSS transitions never advance.** A 200ms transition still reports `currentTime 0` after
  1200ms. **CSS keyframe animations do advance**, and direct style writes apply instantly. So:
  transitions dead, animations alive, style writes alive.
  - `initTweenProbe()` runs one probe at boot and sets `no-tween` on the root if transitions are
    inert, which drops them all so everything lands finished. **Keep the probe.** Without it
    sixteen of twenty four revealed elements on the about page sat at `opacity: 0`.
  - **Never animate content opacity up from zero.** A stuck keyframe applies its first frame
    forever, fill mode or not. Animate transform and let the resting state be visible.
- **`window.scrollTo(x, y)` silently does nothing**, because `html` has `scroll-behavior:
  smooth` and smooth scrolling needs rAF. Use `scrollTo({top, behavior: "instant"})`.
- **Screenshots go stale or blank after a programmatic scroll**, and often fire before an image
  decodes. Take a second shot, or measure the DOM. **Measure, do not look.**
- **`document.timeline.currentTime` sometimes freezes at 0 entirely.** When it does, no
  animation on the page is running and nothing is verifiable. Check it before concluding a
  piece of motion is broken.

## What is built

**Home**: hero, condition, re-diagnosis, rise band, the work, differentiator band, before you
book, fifteen, proof, story, retreat, refusals, statement, questions, close, footer.

**About**: nine blocks to the wireframe, plus the rise band between 03 and 04.

Type is Instrument Serif and Instrument Sans with IBM Plex Mono for labels, all from Google
Fonts; IvyPresto Display stays first in the carved stack for when it is licensed. Palette is the
seven tokens in `BRIEF.md` and nothing else. Depth runs roughly 70/30 dark to light.

## Open, in priority order

1. **The push.** See Start here.
2. **Two forms are unwired.** `action="#"` on the letter signup in the nudge and on the twelve
   questions form in the closing section. One Flodesk endpoint, two forms.
3. **Block 03 of the about page needs a decision.** See "The block 03 problem" below. The
   wireframe describes copy that does not exist in this workspace.
4. **Never verified since the rebuilds**: full contrast sweep, keyboard reachability of the
   sticky bar and the nudge, a real no-JS pass. Do these before it goes public.
5. **`/contact/` and `/legal/*` still do not exist.** The footer links `/contact/`. The artifact
   build rewrites it, so it looks fine in preview and would 404 on the real site.
6. **Footer nav `A Sounding` points at `#start`**, which is the closing section, not the
   Sounding. Either `#sounding` or the booking link.
7. **The podcast question.** The wireframe says it is shelved and that "She Rises Through It"
   should come off the site including the footer tagline. The about page does not mention it;
   **the home footer still links it.** Whether it is actually shelved is not in any file.

## The hero, as rebuilt

Rebuilt to the reference layout Cydnie sent: the photograph is the whole hero and the words
stand in it.

- **Full bleed.** `.hero-water` is the photograph at `inset: 0`, `.hero-scrim` is two gradients
  over it, and the hero is `min-height: 100svh`. The old right hand plate and the booking card
  are gone, which also retires the waterline alignment above: nothing has to meet anything.
- **The scrim is load bearing, not decoration.** Across: near solid under the words, gone by
  the far side. Down: dark at the very top so the header holds over bright water, open through
  the middle so the surface stays luminous, and down to ground at the foot so the seam into the
  condition is not a band. Change those stops and you are changing whether the type is legible.
- **The headline is set as an inscription**, uppercase carved, the second line in Breath via the
  existing `.hero-line em` rule. Hero only. Every other carved heading on the site stays
  sentence case.
- **The paid entry point survives, reworded.** `Start with one conversation` on a Held rule,
  with `$300. Say it out loud once. Two days later a written page arrives.` under it. The old
  `A Sounding` card copy, the `The paid entry point` label and `Book a Sounding` are all gone
  from the hero. The product is still called A Sounding everywhere else; that name was not
  changed, only the hero's wording.
- **The right rail is RESURFACE / RECLAIM / BUILD**, which is hers. It is the name of the
  `hasOfferCatalog` in this page's own JSON-LD, and the FAQ block spells it out: "Resurface,
  then Reclaim, then Build: permission, a witness, and a plan, in that order." It appears
  nowhere in the visible copy, only in the structured data, which is how the first pass at this
  hero missed it and briefly shipped the four doors instead. The three stops map to the offers
  the catalogue lists against them: Resurface to `#sounding`, Reclaim to `#fifteen`, Build to
  `#build`, the last being a new id on the Somewhere to Stand door.
- **Worth saying plainly: the methodology is invisible on the page.** It is her stated
  three-part method and until now it existed only where Google can read it. The hero rail is
  the first place a human meets it.

### The build script was lying about the fonts

`tools/build_artifact.py` hardcoded a Google Fonts link for **Cinzel and DM Sans** and kept
shipping it long after the stacks moved to Instrument Serif, Instrument Sans and IBM Plex Mono.
Nothing errors when an artifact links the wrong families; it just silently sets the whole page
in the fallbacks. It now reads the `<link>` out of `index.html` instead of restating it, so it
cannot drift again. It also carries the `js-motion` bootstrap that the `<body>` slice was
dropping, without which every reveal rule sat inert. `PICK` was pointing at `hero-underwater`,
which this hero no longer uses; the build now reports any src it could not inline instead of
quietly emitting `src=""`.

### Two real bugs found while doing it

- **An orphaned `<canvas class="caustics">` was still in the markup** with no CSS. A bare canvas
  defaults to 300x150 and is a block, so it was **pushing the entire page down 150px**, and it
  is almost certainly what has been breaking screenshot capture in this preview all along. The
  notes above say canvas broke capture in earlier builds; the canvas never actually left.
  Removed, from `index.html` and from the `README` motion list.
- **The reset caps every image at `max-width: 100%`**, so the hero image's `width: 108%` was
  silently clamped to 100% while its `left: -4%` still applied, leaving the right edge 4% short.
  The old `.hero-plate img` had the same 112% and the same clamp. `.hero-water img` now sets
  `max-width: none`.

## Images, and what is not possible

- **Hero is `hero-line-*.webp`**, from `Website Images/Wavy Horizon Beneath Pale Skies.png`
  (1717x916). It has a real waterline, so the headline stands in the water under a visible
  surface. `object-position: 50% 22%` keeps the line high. **The scrim had to change with it**:
  the old plate was uniformly dark on the right, this one has bright sky exactly where the path
  rail stands, so the horizontal gradient no longer falls below .32 and the rail is set in
  Surface rather than muted.
- **About opens on a brand photograph now**, `cydnie-hero-*.webp`, image 45: her holding the
  written page, which is the thing she sells. The home page opens on water, this one opens on
  her. **The wireframe said no photograph in block 01** and held the portrait until 03 so it
  would read as evidence; Cydnie overrode that. There are two images of her on the page now.
  - **She is left of centre in the frame and cannot be moved.** The box is a wider ratio than
    the source, so `object-fit: cover` crops vertically and `object-position` X does nothing.
    The copy moved to the right of her instead, which also gives the page a different opening
    shape from the home hero.
  - **The scrim is a different animal from the water one.** Carrying the home scrim over reduced
    her to a silhouette. It is near solid where the words are and falls off a cliff by 78%,
    because the point of a photograph of a person is that you can see the person.
  - **Narrow widths flip it entirely**: she takes the top of the frame, the copy sits in the
    dark under her, and the scrim turns vertical. Full width copy beside her is not possible and
    on top of her is not acceptable.
- **About portrait is `cydnie-veil-*.webp`**, image 24 of the branding shoot: behind a sheer
  curtain, half obscured, looking away. It is the only frame in the set that argues the page.
- **The abstract Website Images set tops out around 760px** and most are near 300. None can
  carry a full bleed hero. The only hero sized files there are the six over 1MB.
- **`Home page hero example.png` is a mockup of this hero design**, which is where the reference
  screenshot came from.
- **A brand video hero is not buildable here.** There is no ffmpeg on this machine, the source
  is 443MB of `.MOV`, and an artifact caps at 16MB with assets inlined as data URIs. It needs
  transcoding to mp4 and webm somewhere else first, and on the real site it wants a poster
  frame and a paused state under reduced motion.

## The about page

`about/index.html`, built to the nine blocks of `about-page-wireframe.html` in the order it
sets. It shares `site.css` and `site.js` with the home page; asset paths are `../assets` and
`build_artifact.py` normalises them.

What the wireframe asked for and this honours: no photograph until block 03, the beats in 03
left unlabelled so she meets the words in 05, the foundation placed under the story it held up
rather than first or last, the triad numbered because the order is the argument, four items in
Also true and four cells in the facts, the letters attached under the doors rather than being a
fourth door, and no second CTA in the close. **The head rule is 748px and the close rule is
128px**, which is the one place a rule carries meaning through its length.

### The block 03 problem, which needs a person

The wireframe marks block 03 **"Yours, keep"** and describes it as already written: *I pressed
record anyway*, the casita floor in Costa Rica, the heavy Shure, nobody on the other side of the
recording. **That copy is not in this workspace.** It exists only as that description inside the
wireframe itself; there is no draft of it in any file.

So block 03 was built from copy that is verifiably hers: the account on `cydniejocelyn/about/`
(the fourteen years, the postpartum years, the company, Costa Rica, the question she could not
answer) and the timeline now on the home page. The headline is **"I came home and I quit."**,
her sentence, verbatim. **Either supply the recording copy or confirm this version.** Nothing on
that block was invented, which is also why the Shure and the casita floor are absent.

### Other open items on this page

- **The portrait is the same one the home story uses.** It is the only portrait in the project.
  A second frame would stop the two pages sharing a face.
- **Two wireframe placeholders were dropped rather than faked**: `Works with [business type and
  size]` and `Retreats led [number]`. The facts block carries Entity and Board instead, both
  sourced. Restore the originals when there are real values.
- **The wireframe says the podcast is shelved**, and that "the rise" and "She Rises Through It"
  should come off the site including the footer tagline. The About page does not mention them.
  **The home page footer still links She Rises Through It.** Not changed, because whether the
  podcast is actually shelved is not something the file can tell me.
- `.r-img` was deliberately not used on the portrait, for the reason in the environment notes:
  it fades from `opacity: 0` through a transition, and transitions do not advance in the preview.

`build_artifact.py` now takes a page argument: `python3 tools/build_artifact.py about`. Because
an artifact is a single page, cross page links are rewritten to absolute `cydniejocelyn.com`
URLs. The first pass rewrote them to bare anchors and produced twelve dead links that swallowed
the click silently.

## Booking

Every Sounding call to action points at the HoneyBook scheduling page:
`https://clients.cydniejocelyn.com/schedule/6a185c26693e14802690e9f6`

Six of them: the header button, the hero's paid entry point, the Sounding door's note in The
Work, the CTA under The Work, the closing Book one conversation, and the sticky banner. All
same tab, no `target="_blank"`: it is a conversion step on her own subdomain, not a reference
link. `build_artifact.py` rewrites `/contact/` and `/legal/*` to `#start`, and this URL is
absolute so it passes through untouched. Verified as six exact matches in the built artifact.

**The footer nav still has `A Sounding` pointing at `#start`**, which is the closing section,
not the Sounding. It was not on the list and it is a directory entry rather than a CTA, so it
was left alone, but it goes somewhere its label does not promise. Either `#sounding` or the
booking link would be an improvement. The footer's `Contact` also still points at `/contact/`,
which does not exist.

## The letter signup

The nudge signs you up where it stands. It used to link to `#letter`, which is a paragraph
about the letter with nothing to fill in, so the only offer on the page for the free product
went nowhere.

- **Email only**, hidden tag `letter`, `action="#"` like the twelve questions form. **Both are
  still unwired.** One Flodesk endpoint, two forms to point at it.
- **`inert` while it is down.** A form parked off screen must not be reachable by tab, and
  `aria-hidden` alone does not stop focus. Verified enforced in this browser.
- **`.nudge.is-instant` drops the transition only, never the transform.** The first version
  pinned `translateY(0)` there too, and because `is-instant` outlives `is-up` the card stayed
  on screen after being dismissed. If you touch this, re-test dismissal, not just opening.
- **Anything with `data-letter` calls it back.** Dismissing is remembered for the session, so
  without an opener the only signup for the letter would be gone for good after one click. The
  letter door's note is that opener now, in place of "Weekly", which the door's own copy
  already says as "a letter on Sunday nights".
- **`button.door-note` needs its box reset.** The site's reset gives buttons `font` but not
  padding, border or line-height, so the opener measured 24px against the other notes' 18 and
  put the row of notes back out of line.
- **Focus goes to the email field, not the first focusable**, which is the dismiss cross.



`#turn` is 55/45, copy left and one photograph right, stacking under 900px with the copy first
and the picture at 16:9. The picture is `hero-underwater-*.webp`, looking up from below the
surface with the light breaking into shafts. It sits beside "You are **under** something, and
pressure is not a character flaw", which is the whole reason it is that picture and not
another. It carries no caption: the copy next to it is the caption.

- **`.col-c` keeps `grid-column: 2 / 11`** from the twelve column system, which would punch
  implicit columns through a two column grid. `.turn-split > .col-c { grid-column: 1 }`
  overrides it rather than removing the class, so the left column's markup is untouched.
- **The picture drifts as you scroll past it.** It carries `.par` with `data-speed="0.22"`,
  the same engine the story figure uses, so the light on the wall moves while the reader moves.
  Chosen over a drop shadow, which would have done nothing: the plate sits on near black and a
  shadow needs something to fall on.
  - The image is `height: 116%; top: -8%` inside an `overflow: hidden` frame, giving 38px of
    slack each side against a measured maximum drift of 21px. **Raise `data-speed` and you eat
    that margin**; past about 0.4 an edge appears at the top or bottom of the frame.
  - It is a direct style write, not a transition or an animation, which is why it is the one
    piece of motion in this build that can actually be verified in the preview. Reduced motion
    pins it through the existing `.par { transform: none !important }` rule.
- **No reveal class on the picture, deliberately.** `.r-img` fades in from `opacity: 0` through
  a transition, and transitions do not advance in the preview (see the environment notes), so
  the one large photograph in this section would be the thing left invisible. It is simply
  there.
- The image was already in `assets/img` at three widths and had never been used on the page.

An interactive SVG diagram lived here for one revision: a waterline that rose past a fixed
Held mark, with the light clipped to the air by a scaled clipPath that tracked the water with
no script. It was removed on request and replaced with the photograph. Nothing of it remains in
`index.html`, `site.css` or `site.js`; if it is ever wanted back, the trick worth keeping was
`scaleY = 1 + translateY/120` on the clip rect, which locks two CSS animations together at
every frame instead of only at the ends.

## Proof, one at a time

Four quotes on a carousel that can be dragged, stepped, keyed or dotted. Kris's is new; the
lede that read "Six women filled in the feedback form after Rise & Reground in Costa Rica,
April 2026. Unedited." is gone, along with the two-column header it sat in.

- **Every quote stays in the document and in the accessibility tree.** The markup is the plain
  stack of all four; `initQuotes()` only decides which is in front. A carousel that hides four
  fifths of the proof when the script fails is not proof.
- **Position is measured, never assumed.** `xFor()` reads each slide's real `offsetLeft` and
  width, so it survives a resize, a late font swap and quotes of different lengths. Do not
  replace it with index times an assumed slide width.
- **There is a landing backstop.** If a move has not landed after 700ms the carousel adds
  `q-instant` and stops using transitions at all, for the reason in the environment notes
  above: a dimmed slide that never brightens is a quote nobody can read.
- **Slides are stretched to the tallest by the flex track**, which is what stops the section
  jumping. The caption therefore does not use `margin-top: auto` in the live state, or a short
  quote would strand its attribution a screen below itself. Kris's quote is roughly twice the
  length of the others, so slide one carries visible slack on a phone. Trimming her quote is
  the fix if that ever matters; the layout is not the problem.

Seven slides now, each built as **pull, body, attribution**. The pull is her own phrase said
loudly so a slide reads from across the room; it repeats words that follow it, so it carries
`aria-hidden` rather than being read out twice. Pulls came from Cydnie for Carol, Anonymous and
Angela; the other three are contiguous phrases lifted out of those quotes rather than anything
written. Order runs the five retreat voices first and Angela's client review last, which hands
off into Built to stand.

Slides stretch to the tallest, so the short ones carry visible air. **Keep the pulls top
aligned rather than centring the content**: centring would split the slack above and below and
the pulls would then sit at six different heights across the neighbours you can see.

### Three things about the reviews that need a person to decide

- ~~Tamara, Mane Alchemist Salon.~~ Arrived and in, as slide seven.
- **Carol's pull says "how you did it" and her body says "how you did that."** Cydnie wrote the
  pull that way and it was run verbatim. One word, and a pull quote sitting directly above the
  sentence it misquotes is the kind of thing a reader notices.
- **Angela's review says "coaching call."** The FAQ says plainly that this is not life coaching
  or mindset coaching. Her words, her experience, run in full; flagged because the same
  objection was raised about Kris's "vacation business" and answered by trimming.
- **There is now a Kristi and a Kris in the carousel, two different retreat guests.** The
  source CSV itself calls one of them "The other Kris, aka Mom", so the collision is real and
  predates the site. They may need distinguishing in the captions.

Kris's quote is her second paragraph, verbatim. Her first paragraph called it a "vacation
business" and was dropped on Cydnie's instruction, because the FAQ says plainly this is not a
wellness brand and the site sells resurfacing and brand work.

The structured data was left alone. `aggregateRating` still reads `ratingCount: 6` against the
retreat Service, which is still true: six people filled the form. Kris is one of them.

## Before you book, made operable

The section used to be four reassurances you read past. It is now the objection handler it was
always describing: the reader picks the thing that is actually stopping her and gets the answer
to that one. Her four lines are the answers, verbatim; the four worries are new copy, each
derived straight from the answer it belongs to and written in the reader's voice.

- **The markup is the pairs.** Four worries, each with its answer under it, all eight readable
  with no JS at all. `initReversal()` turns them into a tablist and one panel. Strip the JS and
  the section still does its whole job, which is the only reason the picker is allowed to exist.
- **It is a tablist by the book**: one tab in the tab order, arrows to move and wrap, Home and
  End to the ends, `aria-controls` and `aria-labelledby` wired both ways.
- **The panel is held at the height of the longest answer** so choosing never moves the page
  under the reader's thumb. Note the trap: `.rev-panels` is `border-box` with 32px of padding
  and a 1px rule, so the reserved height has to carry that chrome as well as the answer. The
  first pass set the answer height alone and the fourth answer still opened the box 33px.
- **The lede is swapped by JS.** The markup says "Whichever one is actually stopping you, it is
  already answered", because with no JS there is nothing to pick. Live, it says "Pick the one
  that is actually stopping you." Do not put the instruction in the markup.
- **The selected mark is `--breath`, not `--accent`.** On this ground `--accent` resolves to
  Meniscus, which is darker than the faint rule it is supposed to beat, so the drawn mark read
  as less visible than the undrawn ones.

The old `.reversal li` hairline that drew on reveal is gone, and so is its entry in the two
reveal selector lists in `site.js`. Check both if you touch that engine.

## The four ways in, aligned

The four rows read as four accidents rather than one grid. Four separate causes, all measured,
all fixed in section 12 of `site.css`:

- **The lead row was indented out of the column by its own left border.** `.door--lead` carried
  `border-left` plus `padding-left: 2rem`, which pushed its stage label, heading, copy and note
  33px right of the other three and narrowed its measure by the same, so its paragraph wrapped
  an extra line and its row ran 29px taller. The marker is now an absolutely positioned rule in
  the gutter, `.door--lead::before`, which cannot touch the layout. It breathes on opacity now
  rather than on border-colour.
- **The notes sat at four different heights.** `align-self: center` inside rows of unequal
  height put them at 92, 106, 79 and 92px from each row's top. They are on the baseline now.
- **One note was a different size and colour from the other three.** `.door-note--link` had
  `min-height: 44px`, which made it 44px tall against the others' 18px, and `color:
  var(--breath)`, which is #9FCCC6 on the #E7ECE8 ground: **1.6:1, effectively invisible.** The
  touch target is now grown with a pseudo element instead of a height, and all four notes take
  `var(--muted)`.
- **One stage label wrapped to two lines.** `$300 - The paid entry point` needs 243px and the
  column was 14rem/224px. Column one is 16rem now.

**Do not change the fixed column widths to anything content-sized.** Each `.door` is its own
grid, so `auto` or `max-content` gives the four rows four different columns, which is the
misalignment this section just came out of. If a label ever needs more room, widen the fixed
value.

At 1280 all four rows now measure identically: stage at x64, heading at x368, note at x1024,
labels 19px tall, notes 18px, one colour. Row heights still differ, because the copy differs,
which is what a row list is for.

## The condition section, as built

Five recognitions on a pinned scroll. `.cond-track` is five and a half screens tall,
`.cond-stage` inside it is `position: sticky; top: 0`, and `initCondition()` in `site.js`
reads how far the pin has travelled and lights the recognition that belongs there.

- **No wheel is swallowed.** Nothing calls `preventDefault`, nothing retimes a scroll, the
  scrollbar keeps telling the truth. The reader can leave at any moment at their own speed.
  That is the only version of this worth shipping.
- **Progressive, in that order.** The markup is the plain list of all five. JS adds
  `is-stepped` to the section and every stepped rule hangs off that class. Remove the class
  and the plain list is back, unchanged. So no-JS, reduced motion, and short screens
  (`innerHeight < 520`) all get the list, and the gate is re-checked on every resize.
- **`--cond-run` on `.cond-track` is the dial**, currently `72svh` per recognition. The
  section costs the page about 4,300px at 860px tall; lower the run if that is too much.
  `--cond-tail` (0.5) holds the fifth one on screen instead of sweeping it away.
- **The ticks are real navigation.** Click or arrow-key one and the page scrolls to the middle
  of that step, so state never changes out from under the scroll position. `aria-current`
  follows the active one, and all five stay in the accessibility tree the whole time.
- **The stack has no natural height** once the five are laid on one another, so JS measures
  the tallest and holds it in `--cond-h`, re-measuring on resize and for 2.4s after load
  while the fonts settle.

Verified by measurement, not by eye: the walk lights 1-2-3-4-5 at even thresholds, the gauge
tops out as the fifth arrives, all five tick targets land on their own step, a 480px-tall
viewport falls back to the list and back again on resize, and nothing below the section moved.

**Screenshots after a programmatic scroll are unreliable here, as the notes above say.** One
of them showed step 01 while the DOM was on 05, and a reload-and-capture came back garbled.
Measure the DOM. Do not chase what the screenshot shows.

## The rise band, as rebuilt

`.surfacing` had no CSS at all, so the ornament SVG took its width from the wrap and stood
1152x960 on its own. The band ran **1469px, taller than the screen it sits on**, and the
bubbles were rendering black on browser defaults. Fixed:

- **The SVG is sized**, `clamp(2.5rem, 4.2vw, 3.25rem)` wide, and the 40x96 viewBox gives it
  the height it rises through. The band is now 267px at 404px wide, 459px at 1280, 520px at
  1600. About a third of what it was.
- **The drawn waterline is gone.** The photograph behind is the surface; two of them read as
  a mistake, and the drawn one sat exactly on the photographic one.
- **The bubbles have a dark rim**, `rgba(7,26,31,.5)`, over the Breath fill. Breath alone
  disappears the moment a bubble crosses the surface highlight, which is where they cross.
- **They move.** `breath-rise`, 6.4s, infinite: up 70 units, widening as the pressure comes
  off them, gone at the top. All three are drawn at the bottom of the column and pulled apart
  by negative `animation-delay`, so the loop never jumps anyone back down. Pure CSS keyframes,
  because rAF is dead in the preview and a JS loop could not be verified here.
- **Reduced motion** gets them held apart by static transforms, so it is still a column of
  three rising, just not moving. `Come up` is Plex Mono tracked caps in Surface.

## Previewing one section on its own

Screenshots of the whole page are unreliable here, but a short page that pulls in `site.css`
captures fine on a fresh navigate. `mkband.py` in the scratchpad rebuilds `_band.html` from
the real markup in `index.html`, so what it shows is what the site has, and `sync.sh` runs it
after every rsync (rsync's `--delete` wipes it otherwise). Worth copying for any other section
that is hard to see in place.

## Things deliberately not done, and why

- **Pricing tier list, featured tier, How It Works, stats count-up, nav button pulse, button
  sparkle, discount band.** The brief asks to modify or cut these. None exist on this site.
  Building them would restructure the page, which the same brief forbids. Flagged, not built.
- **Google rating in structured data.** The page shows "5.0 on Google" as plain text only.
  Google's own guidelines exclude ratings collected from Google, and an unverifiable
  `reviewCount` gets rich results suppressed. Needs the real count from her profile.
- **Aggregate rating markup** was removed with the stats row, since nothing visible backs it.

## Palette additions, and why they exist

The published warm tones fail as body text on their own grounds: Held is 3.2:1 on Fathom and
4.0:1 on Surface, Claim is 2.9:1 on mid water. Text uses `#A8C4C0`, `#48666A`, `#456063` and
`#8F4A47` instead. The board values still do every fill, rule and ornament. Documented in
`README.md`.
