# cydniejocelyn.com

Static site. No build step, no dependencies: every file here is finished output.
Home page only so far.

## Serving it locally

```bash
cd "cydniejocelyn-v2" && python3 -m http.server 8620
```

## What is here

| Path | Holds |
|---|---|
| `index.html` | The whole home page, including the JSON-LD graph |
| `assets/css/site.css` | Design system, built from Brand Guide v1.1 |
| `assets/js/site.js` | Motion layer. No dependencies |
| `assets/fonts/` | Satoshi and Fraunces, subset to Latin, variable |
| `assets/img/` | Water band, logo lockups, photography |
| `robots.txt`, `sitemap.xml`, `llms.txt` | Crawlability, including for answer engines |

## Image layers

Cut back deliberately. Every picture now has a job; the moodboard-style rows are gone.

| Where | Shape | File | The shot |
|---|---|---|---|
| The rise band, behind the Breath mark | 2.6:1 full bleed | `layer-surface` | The underside of the surface. Masked top and bottom, so the interest must sit in the middle third. |
| Beside the story | portrait | `cydnie-reading` | You, turned away, cool graded. The one portrait on the page. |
| The retreat block | 0.78:1 | `armonia-arch` | The arched opening at Armonia with the olive tree beyond, from your Crete folder. |

**Still reserved:** a wide retreat photograph, 2.6:1 at 1800px, from behind or above, no faces
to camera. Drop it in above "work that shipped".

Everything else was removed. The named brand set (`01_pressure_shadow` through
`20_reaching_shadow`) is shot in portrait at roughly 300x508, which is why it read as inserted
rather than integrated: at column width it has to be upscaled and it competes with the type.
**Re-export those at 1200px on the long edge** and they can carry full-bleed bands properly.

## The rise## The rise

The Foundation's arc is *submerged, underwater, resurface, breath, flight*, so the page starts at
depth and comes up. But a rise is not one slow fade: she surfaces **at the re-diagnosis**, and
the page has to breathe after it. The depth rhythm is:

| Zone | Sections | Ground |
|---|---|---|
| `.z-breath` | the mark | Breath `#071A1F` |
| `.z-deep` | the condition, the re-diagnosis | Fathom `#0C2830` |
| `.rise-band` | where she comes up | gradient to Surface |
| `.z-light` | the method, fifteen | Surface `#E7ECE8` |
| `.z-silt` | proof | `#DCE4E1` |
| `.z-deep` | the story | Fathom, one deliberate return to depth |
| `.z-light` / `.z-silt` | retreat, refusals, questions, the close | Surface / silt |
| `.ftr` | footer | Fathom |

Dark is about 28% of the page and the light arrives at roughly the 20% mark. Each zone
declares `--from` so its top edge fades out of the zone above it and the change never reads
as a band.

Two colourways, each measured against its actual ground:

| | Ink | Muted | Faint | Accent | Warm |
|---|---|---|---|---|---|
| deep grounds | Surface | `#A8C4C0` | `#7E9E9B` | Meniscus | Claim `#CE908A` |
| light grounds | Fathom | `#48666A` | `#456063` | Deepwater | `#8F4A47` |

`#A8C4C0`, `#7E9E9B`, `#48666A`, `#456063` and `#8F4A47` are additions, not board swatches.
The published Held is 3.2:1 on Fathom and 4.0:1 on Surface, and Claim is 2.9:1 on mid water,
all of which fail AA as type. The board's own values still do every fill, rule and ornament.

## Type

Carved set is Cinzel, an inscriptional Roman where lowercase sets as small capitals, which is
what produces "RESurFAce" on the board. It carries the short, certain lines only, per the
Foundation's "short when certain" register. Body is DM Sans, at the specified 60 to 66
characters per line.

If the carved set is IvyPresto Display, the stack already names `ivypresto-display` first: add
the Adobe kit and it takes over. Swapping it is one line, `--font-carved` in `site.css`.

## The mark

The board's misuse rules are followed exactly. The mark sits on a solid field, never over
photography, and is never animated, outlined or rotated. Clear space is set to cap height via
`.mark-hold`. Nothing in `site.js` touches it.

## Why nothing depends on IntersectionObserver

Reveals, the seal and the bubbles all run through one in-view engine in `site.js`: a rAF and
scroll check, with a hard timeout that reveals anything still hidden after 2.6s. An earlier
build used `IntersectionObserver` alone, and in any browser where it is delayed or blocked the
entire page below the fold stayed at `opacity: 0`. The seal likewise rests fully drawn and the
orbit only modulates from that resting state, so a browser that never fires an animation frame
still shows a complete, correct page.

## Motion

Everything is authored in its finished state. `site.js` adds `.js-motion` to `<html>` and only
then are the offsets applied, so no-JS and `prefers-reduced-motion` both get the complete page
immediately.

What moves, and what it means:

- **the ground** lightens continuously as the page is read
- **the depth gauge** counts up out of the water and reads "Surface" at the end
- **lines surface**: they rise and the blur clears off them
- **the meniscus dividers** sag with scroll momentum, then settle level
- **the offer rows** bend their line toward the pointer instead of lighting a box
- **the Breath mark** rises through the band where the reader comes up
- **the Fifteen seal** settles one circle at a time, the open one last

The register is the Foundation's: unhurried, and never chasing. Nothing demands attention;
it answers the reader.

## Breakpoints

480 / 672 / 896 / 992 / 1200. The 672px (42rem) layer is the tablet one: without it the twelve
column grids collapsed to a single narrow column all the way from 480px to 992px, which is what
made the page look unresponsive on an iPad.

## Ratings: there is no average anywhere, and that is deliberate

**Nothing on this site publishes an average score.** The Costa Rica feedback form got six
responses, and an average of six is not a rating: one person moves it by two tenths. It was on
the retreats page as 9.7 out of 10 and in the home page's structured data as an
`AggregateRating` of 4.8 from a `ratingCount` of 6, and Cydnie took both out on
26 August 2026. She is right. The quotations are stronger than any figure derived from them.

What stays: the individual `Review` entries in the home page's `@graph`. Each is a real,
attributed quotation the site already shows on the page, not an average.

The raw responses are first-party and live in `CydnieJocelyn-Site/Reviews/`. If a real sample
ever exists, the figure goes back in three places in the same commit: the retreats page,
`llms.txt`, and an `aggregateRating` on `#retreat-service`.

**5.0 on Google** is plain text only and is deliberately not marked up: Google's own
structured-data guidelines exclude ratings collected from Google, and a `reviewCount` that
cannot be verified is the kind of claim that gets rich results suppressed.

## Before launch: required wiring

1. **IvyPresto Display.** Create a Web Project at fonts.adobe.com containing IvyPresto Display
   and paste the `<link>` into `index.html` where the flagged comment sits. The CSS stack already
   names `ivypresto-display` first.
2. **The email form.** `action="#"` on the twelve-questions form is a placeholder. Point it at
   the Flodesk endpoint and keep the hidden `tag` field.
3. **Pages that do not exist yet.** The home page links to `/contact/`, `/legal/privacy/` and
   `/legal/terms/`. The primary CTA points at `/contact/`, so that page has to exist before this
   goes live. These are the only root-absolute paths left in the file; every asset path is
   relative, so `index.html` also opens correctly straight from the folder.
4. **Image slot 5.** Reserved and marked in the page. See the table above.
5. **The Session's price**, if it is to carry one. The layout does not break either way.

Check the flags at any time:

```bash
grep -n "WIRING REQUIRED" index.html
```
