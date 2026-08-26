# Claude Code: build one page

Scope is a single page: `/the-build`. Attached: `the-build-page-FINAL.html`,
a working wireframe with copy, structure, motion, and schema already in place.

---

## Scope lock. Read this first.

**Only `/the-build` may be created or modified. Every other file in this
repository is off limits.**

Specifically off limits:

- **All brand client work.** Mane Alchemist, SRS Performance, SolyRey. Their
  layouts, components, styles, and assets stay exactly as they are. Do not
  refactor them, do not reuse their components here, do not "align" them with
  this page, do not touch their files for any reason.
- **Home and About.** Already built. Do not modify.
- **Any shared or global stylesheet, layout, template, or component that other
  pages consume.**

**Do not extract shared components.** Do not create a global nav component, a
global footer component, a shared token file, or a shared type scale. Anything
this page needs, it defines locally, scoped to itself.

If a change appears to require touching a file outside `/the-build`, **stop and
say so.** Do not work around it.

Before finishing, list every file created or modified. If anything outside
`/the-build` appears on that list, it is a mistake.

---

## Rules for this page

1. **No em dashes.** Periods, commas, or colons.
2. **Do not rewrite the copy.** It is final. Fix typos and markup errors only.
3. **No coaching language.** No "empower," "journey," "potential," "go deep."
4. **No wellness visual conventions.** No gradients, no stock imagery, no
   countdown timers, no invented statistics, no sparkles, no curved rules.
5. **The waterline is always level.** It fills once, left to right, and holds.
   Never animated in a loop. Never a wave, never a ripple.
6. **One Deepwater band on this page**, on the A Sounding block. Nowhere else.
7. **Do not invent prices, dates, testimonials, or client names.**
8. **Do not add a testimonial.** The slot at the close is deliberately empty.

---

## What to do

Convert `the-build-page-FINAL.html` into the project's stack, as a self contained
page.

**Keep:**
- All copy, exactly as written.
- Block order and structure.
- All motion behaviour: rise and settle, the waterline fill, the sticky bar,
  hover states.
- The `prefers-reduced-motion` block.
- The JSON-LD graph, with `@id` values unchanged.

**Strip:**
- The annotation layer: every `.note` block, the `.toggle` button, and the
  toggle script. Review scaffolding, not production.

---

## Replace before shipping

| Item | Current state | Needed |
|---|---|---|
| Palette hex values | Placeholders | Real tokens: Fathom, Deepwater, Meniscus, Breath, Surface, Held, Held Lift, Silt |
| Display typeface | Bodoni Moda proxy | IvyPresto Display, licensed via Adobe Creative Cloud |
| Body and mono | Instrument Sans, IBM Plex Mono | Correct as-is |
| Client images | `/work/*.webp`, do not exist | Export at 1400px WebP from the 6250px originals. Do not ship originals. |
| `sameAs` in schema | Contains `REPLACE` | Real Instagram and LinkedIn URLs |
| OG image | `og/the-build.jpg`, does not exist | Every social share renders blank until it exists |
| Postal code | 55025 | Confirm |

Define the palette tokens **locally on this page**. Do not add them to a global
stylesheet.

---

## Page structure, for reference

1. Hero
2. The condition
3. Three areas: brand, operations, business development
4. Proof: three client brand boards, captioned by positioning decision
5. A Sounding, phase zero. $300. The one Deepwater band. The only button.
6. The Build: one day $1,500, a season from $6,000
7. Production: website from $4,000, content $3,600 per quarter
8. Full engagement from $15,000
9. Refusals
10. Questions, then the close

### The triad in the hero

Resurface, Reclaim, Build. Settled and live:

- Resurface links to `/a-sounding`. It means the conversation.
- Reclaim links to `/retreats`. It means the retreats.
- Build is the current page. Static, with `aria-current="page"`.

The triad carries brand language. The nav bar carries plain labels people search
for. Same destinations, different jobs. Do not unify the two vocabularies and do
not relabel either one.

**The only call to action on this page is A Sounding.** No other block gets a
button. The retreats line at the close is body text and a link, not a button.
Do not promote it.

---

## Consistency

The visible figures and the JSON-LD figures must match exactly. If one changes,
both change in the same commit.

---

## Do not resolve. Flag and stop.

1. Testimonials from brand clients have not been requested yet.
2. Nothing else. The triad is settled and linked. See below.
