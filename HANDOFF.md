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

## START HERE: nothing is blocked any more

**It is pushed and it is deployed.** Both of the things earlier handoffs described as blocked
were blocked by the same wrong belief: that this Mac had no tooling.

### The tooling was never missing, it is just off PATH

`node`, `npm`, `vercel` and `gh` are all in **`~/.local/bin/`**, which a non interactive shell
does not inherit. Three sessions went looking for workarounds that were never needed. Always:

```
export PATH="$HOME/.local/bin:$PATH"
```

| | |
|---|---|
| `gh` | 2.98.0, logged in as `Cydniejocelyn`, scopes `read:org` and `repo` |
| `vercel` | 59.5.0, authenticated as `hello-66457178` |
| `node` | v24.19.0 |

### GitHub

**The old remote pointed at a repository that does not exist.** `Cydniejocelyn/cydniejocelyn`
was a guess by an earlier session, based on how `jocelyncotravel` is named, and `gh repo view`
resolves it to nothing. The SSH key generated on 25 Aug is also still not on her account, so
`git@github.com` still answers `Permission denied (publickey)`.

Neither mattered in the end. `gh` was already authenticated, so:

- `gh auth setup-git` wires `gh` in as the git credential helper over **HTTPS**
- the repo was created: **https://github.com/Cydniejocelyn/cydniejocelyn.com**, **private**
- `origin` is now `https://github.com/Cydniejocelyn/cydniejocelyn.com.git`

Named to match her own convention: her other site repo is `famfundays.com`. Rename in the
GitHub UI and `git remote set-url` if she wants something else.

**The SSH key is now moot.** Do not spend another session on it. If SSH is ever wanted, the
public half is in the old note below; otherwise HTTPS through `gh` works and needs nothing.

### Vercel

Deployed from the **CLI, not from Git**. The two are independent and have been conflated twice.
See "It is deployed, and it is behind a login" below.

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
