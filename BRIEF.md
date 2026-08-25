# The brief, as issued 24 August 2026

Cydnie's own words, kept verbatim in substance. This is the current spec.

## The job

Refine the site that already exists. Do not rebuild it, do not restructure the sections, do not
rewrite the positioning copy. This is a pass for conversion and life: keep every existing
section and its order, and improve what is already there. One self-contained HTML file.

## Who it is for

The resurfacing business: brand, operations and business development for women who are
successful on paper and depleted underneath. The thesis of the identity is a waterline. There
is an above and a below, and she is under it. Nothing is wrong with her, something is on top of
her, and the second diagnosis is survivable.

Register: direct, warm, chiselled, unhurried. Restraint is the aesthetic. Positioned explicitly
against wellness visual language and against the coaching category. The reader can smell a
funnel from the top of the page, so every conversion mechanic has to survive that.

## The offers, in selling order

1. **The letter.** A Sunday night letter. No offers in them, ever. Free entry point, and the
   primary CTA on most of the page. Flodesk.
2. **A Sounding. $300.** One honest conversation, and a written page two days later: what she
   said, in the order it actually goes, and one clear next thing to do. Paid entry point, and
   what the sticky bar sells.
3. **Fifteen.** The retreat, fifteen seats. Booking opens September, getaway in April.
   Waitlist link only, never a CTA.
4. **Somewhere to Stand.** The longer build engagements.

Only two CTAs exist on the page: the letter and A Sounding. Never two different CTAs in one
section.

## Palette, exact values, nothing else

| Token | Hex | Use |
|---|---|---|
| Fathom | `#071A1F` | Primary dark ground, and the only ink |
| Deepwater | `#0C2830` | Panels, cards, form fields, alternating bands |
| Meniscus | `#2F5A61` | Hairline rules and small caps labels only, never body text |
| Breath | `#9FCCC6` | Accent only, small elements, never a large fill |
| Surface | `#E7ECE8` | The light ground. Never pure white anywhere |
| Held | `#A65D5A` | The warm note. One element per section, maximum |
| Held Lift | `#CE908A` | Hover state for Held only |

Roughly 70/30 dark to light across the page.

## Type

```css
--carved:  "IvyPresto Display","Instrument Serif",Georgia,serif;
--level:   "Instrument Sans",-apple-system,"Segoe UI",Helvetica,sans-serif;
--utility: "IBM Plex Mono",ui-monospace,Menlo,monospace;
```

IvyPresto is licensed and self-hosted, so it stays first and Instrument Serif carries it.
Display type is regular weight only, never bold, never below 17px. Body is Instrument Sans at
1.6 line height. IBM Plex Mono is labels and eyebrows only: uppercase, 0.28em letterspacing.

## Banned outright

- No em dashes, in copy or in code comments.
- No drawn waves, droplets, ripples or swimmers. Every rule on the page is level; a tilted or
  curved rule reads as a mistake. This governs illustration and CSS shapes. The hero photograph
  is a real water surface and is approved.
- No decorative gradients, glossy surfaces, soft focus, glow, shadow bloom, rounded pill buttons.
- No sparkles, confetti, emoji, icon clipart, checkmark glyphs.
- No countdown timers, fake stock counters, "only 3 left", discount energy. She does not
  discount. Honest scarcity is allowed, because Fifteen genuinely has fifteen seats.
- No stat that is not a real number. Cut it rather than invent it.

## Hero

The image is chosen: `Home page hero image.png`, underwater looking up at the surface, no person
in frame. It is the brand thesis as a photograph, and the point of view is the client's. Do not
substitute stock, do not crop to another subject.

- Export 1600 and 800 in WebP and JPEG, `<picture>` and `srcset`, explicit width and height,
  `object-fit: cover`, `fetchpriority="high"`, no lazy loading.
- Do not duotone it, it already sits in the palette. Measured: `#1A3133` near the top,
  `#32494A` through the rays, `#000E16` at the bottom.
- The bottom is darker and bluer than Fathom, so either warm it toward Fathom in the lower 30%
  or end the hero on a full width Meniscus rule. Both were done.
- The brightest band is around 34% down. Keep copy in the lower left over dark water, and
  verify 4.5:1 against the actual pixels rather than the average.
- **Two waterlines must become one.** The photograph's surface is at 24% of the frame; the
  drawn rule under the H1 has to meet it, so they read as one line running the hero, drawn on
  the left and real on the right. If the alignment cannot hold across viewports, drop the drawn
  rule in the hero only and keep it everywhere else. Never ship both at different heights.
- Fallback is not a gradient. A solid two field block: Meniscus in the top 24%, Fathom below,
  1px Meniscus rule at the join overhanging both sides.
- Booking card floats over the **lower right**, breaking the edge. Lower left is where the copy
  sits and is the darkest part of the frame. Deepwater, 1px Meniscus border, radius max 2px,
  no shadow. The border is what holds its edge, so it is not optional.
- Parallax: oversize to 112%, 12px of travel at most, transform only.

## Conversion

- **Sticky bar.** Fixed bottom, hidden on load, revealed after the hero, hidden again at the
  footer so it never covers the closing CTA. Fathom, 1px Meniscus top rule, one line of
  Instrument Sans at 15px, one Held CTA. Sells A Sounding, not urgency. Collapses to CTA and
  price on mobile.
- **The band.** Replaces any discount offer. Carved face, centred, on Fathom, short Held rule
  beneath: *Sometimes the answer is that you don't need me.* Then one line explaining that a
  Sounding ends with the truth, including the version where the next move is not hiring her.
- **Risk reversal.** Four lines, each with a drawn Meniscus rule to its left. No badge, no seal,
  no shield.
- **FAQ.** Native `details` and `summary`. Four questions, 40 to 70 words each: is this coaching
  therapy or consulting; what if I cannot explain what is wrong; what actually happens and when;
  what if I am not ready to spend $300 (answer: the letter, and link the letter not the booking
  page). Summaries carved at 19px, chevron is a 1px rule that rotates, no icon font.
- **The nudge.** One slide-in, once per visit, dismissible, after the visitor passes pricing.
  Offers the letter, never a discount. Deepwater card, Meniscus hairline, real accessible close
  label. Stays dismissed for the session. Absent entirely without JavaScript.

## Life

The waterline is the signature, and every motion is that rule doing something.

- Scroll progress as a rising waterline: 1px Meniscus fixed at the top, filling left to right.
  This states the thesis, so get it exactly right.
- The page lightens as she scrolls. Contrast never dips below 4.5:1 through the transition.
- The headline rule draws left to right once on load, 900ms, ease-out, overhanging the text on
  both sides. **Build this first and judge the rest against it.**
- Hero parallax, 12px maximum.
- Card hover: `translateY(-2px)`, 200ms, border Meniscus to Breath, no shadow.
- Smooth scroll via CSS `scroll-behavior` and `scroll-padding-top`, not a JS loop.
- Nav button: a Held rule extending beneath on hover, 180ms. No pulse, no shine, no sparkle.
- No third moving thing in the hero. Restless is the feeling this site exists to relieve.

## Fast and bulletproof

Transforms and opacity only. No animated filters, no blend modes, no backdrop-filter, no
marquees. No external JS libraries. **The page must work fully with JavaScript disabled**:
every section visible, every link working, the FAQ opening and closing, all copy present. Only
external resources are Google Fonts and the hero image, both preconnected. Every scroll
animation gated behind `prefers-reduced-motion`, rendering final state immediately. Visible
keyboard focus everywhere: 2px Breath outline, 2px offset. The sticky bar, the nudge and the
FAQ all reachable and dismissible by keyboard. Responsive to 360px; the booking card stacks
under the image on mobile. Watch specificity so section padding is not cancelled.
