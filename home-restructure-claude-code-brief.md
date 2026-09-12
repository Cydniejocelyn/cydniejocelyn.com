# Cydnie Jocelyn — Home Page Restructure, SEO and Work Showcase
## Claude Code Build Brief

**Scope:** Restructure the home page from seventeen sections to seven. Move displaced content to the correct pages. Build a client work showcase. Implement SEO and schema corrections across the affected pages.

**Out of scope for this brief:** The Gatlinburg launch swap, which happens Wednesday 16 September and is handled separately in Phase 5.

**On copy:** all copy in this brief is approved and final. Blockquoted copy is set verbatim and must be implemented exactly as written, including punctuation. Do not rewrite it, tighten it, expand it, or add to it. If something appears to be missing, report it rather than filling the gap. Four non-copy items remain outstanding and are listed at the end.

---

## STANDING RULES — read before every phase

1. **Motion lock.** Existing site interactions, scroll behaviors, transitions and animations may not be changed, removed, re-timed or re-implemented unless Cydnie has explicitly approved that specific change. If a section is being moved, its existing motion moves with it unchanged. If a section is being deleted, report what motion is being lost before deleting it.
2. **One Deepwater band per page, used once, marking the single action on that page.** Do not add a second.
3. **No em dashes anywhere in any copy written or edited.** Use periods, commas or colons.
4. **Do not rewrite copy that is not named in this brief.** Move it intact.
5. **Do not fill a TK.** If content is missing, leave the placeholder visible and report it.
6. **Voice rules apply to any new microcopy:** first person, plain, spoken. No coaching or wellness language. No sentences arriving in threes. No wordplay substituting for meaning. No invented statistics, seat counts or scarcity.
7. **Every phase ends at an approval gate.** Do not begin the next phase without explicit approval.

---

## PHASE 0 — Report only. No edits.

Produce a written report. Change nothing.

### 0.1 Inventory
- List every section on the home page in document order with its wrapper element, ID, class, and approximate line range.
- List every animation, scroll trigger, transition and interactive behavior currently attached to the home page, and which section each belongs to.
- List every internal anchor link on the site that targets a home page ID, including `#sounding`, `#fifteen`, `#condition` and any others.
- Confirm which Deepwater band instance exists on the home page and where.

### 0.2 Known items to verify
- **Canonical mismatch.** The page serves at `https://www.cydniejocelyn.com/` but the canonical tag and `og:url` both point to `https://cydniejocelyn.com/`. Report which hostname is canonical in production, whether a 301 exists between them, and which direction it runs. Do not fix yet.
- **The Letters button.** Confirm where the button on the home page and on `/the-letters/` currently points. It has previously pointed to an old Collective form. Report the live destination.
- **Retreat price anchor.** The path module currently reads "Retreats, from $3,265." Report every location on the site where a retreat "from" price appears.
- **The `40m` element** at the top of the page. Report what it is, what renders it, and whether anything depends on it.
- **Existing work section.** `/the-build/#work` is linked as "Client work." Report what that section currently contains and whether it holds images.
- **Existing schema.** Report all structured data currently present sitewide, by page and type.

### 0.3 Report back
Do not proceed. Deliver the report and wait.

**GATE 0 — Cydnie approves before Phase 1 begins.**

---

## PHASE 1 — Home page section consolidation

Target state is seven sections in this order. Section numbering below is the new order.

### Section 1 — Hero
**Action: modify in place. Do not rebuild.**
- H1 stays exactly as written. Do not touch it.
- Promote the category line ("Brand, operations and business development for founders and leaders who are successful on paper and depleted underneath. Forest Lake, Minnesota.") to sit directly beneath the H1 at meaningful visual weight. It is currently the smallest text in the hero. It should be the second thing read, not the fourth.
- Add this line beneath it, approved copy, set verbatim:
  > Logos, brand guides, websites, social strategy and launch plans, scoped to what the business in front of me actually needs.
- Primary CTA stays as is.
- **Remove** the line "Or ask me a question first. I answer those myself." from the hero. It moves to Section 5.
- Add a client name strip beneath the CTA: Mane Alchemist, SolyRey, SRS Performance. Small type, no logos required for this phase.
- **Decision required from Cydnie, do not implement either option without it.** Cydnie's photo currently appears only at position eleven, inside the "Why me" section that moves to About in Phase 2. That means the restructured home page has no image of her at all. This is a solo practice where she is the product, and her face raises trust. Two options: place `cydnie-reading-1000.webp` in the sticky header at small scale, or place it immediately below the hero as a bridge into Section 2. The underwater hero image stays either way. Report both options with mockups and wait.

### Section 2 — The condition
**Action: keep intact, move into position 2.**
- The 11:40pm section with its four numbered items. No copy changes. Motion preserved exactly.

### Section 3 — What I actually do
**Action: rebuild from the existing "The work" section. All copy below is approved and set verbatim.**

The section leads with the structural claim, proves scope, then lists deliverables. Do not reorder these four blocks.

**3.1 Section lead**
> **Brand, operations and business development. One person, held at once.**
>
> Most businesses solve this with three vendors who never speak to each other, or three hires they cannot carry. I am the partnership instead. You get the scope your business actually needs, without a salary attached to it.
>
> Every engagement is built for the business in front of me. A full brand audit if that is what is needed. A full build if that is what is needed. Nothing templated and no version of you I have already sold to someone else.

**3.2 The three pillars**, as cards beneath the lead. Headings stay as they are.

Brand
> A logo, a brand guide, and a website of five to eight pages. The guide covers your colors, your voice, and how the brand gets used and how it does not. Then the social strategy, the content plan, and the launch plan that puts it in front of people. Ongoing support after launch runs two reels and one static a week, with captions, hashtags, posting and analytics.

Operations
> We look at how the work actually moves, intake through handoff, and find the parts held together by you remembering to do them. Then we decide what changes and where the money is better spent.

Business development
> I come out of business development, so we start with the industries you are in and the people you want in front of. I build the vetting database that sorts who is hot, warm and cold. Then a 90 day plan covering where to pitch and what to say when you get there.

**3.3 Range proof**, its own line beneath the cards, visually distinct from them.
> Currently building five websites and the dashboard that runs them, for one client.

**3.4 Pricing**
- **Remove** the `$1,500 to $15,000` range wherever it appears on the home page.
- Publish three floors, styled as anchors, not as a table:
  - Website, from $4,000
  - Social and content, from $3,600 a quarter
  - Full brand launch, from $15,000
- The $1,500 day build does **not** appear on the home page. It stays on `/the-build/`. A $1,500 figure next to $15,000 anchors visitors down.
- Retain, relocated from the deleted "What it leads to" card: "Every price is published, and your Sounding fee comes off it."

**3.5 Section close**
- Close with the existing line "I lead with heart and close with operations," relocated from the "Why me" section.

### Section 4 — Proof
**Action: merge two existing sections into one.**
- Top half: the client work showcase. Built in Phase 3. Leave a placeholder container in this phase.
- Bottom half: testimonials, reduced from eight to five.
  - Keep five, in this exact order, with these attributions:
    1. Tamara · Mane Alchemist Salon
    2. Spencer Scott · SRS Performance
    3. Angela · Consulting client
    4. Carol · Retreat guest, Costa Rica
    5. Kristi · Retreat guest, Costa Rica
  - Tamara and Spencer are reattributed to their projects so their quotes and their showcase entries reinforce each other. **Hold Tamara's reattribution until Cydnie confirms she has cleared it with Tamara.** If unconfirmed at build time, leave her as "Consulting client" and flag it.
  - Angela's attribution changes from "Client · Alchemy with A" to "Consulting client." The quote itself is unchanged.
  - **Delete:** the "Anonymous" testimonial and the "BJB" testimonial. Both are unattributed or initialed and reduce credibility rather than adding it.
  - **Delete:** the Kris testimonial.
- Melissa's video: replace the trailing text link with a visible thumbnail and play affordance. YouTube ID `DrrP4hdw0lo`. Thumbnail asset TK. Do not autoplay. Do not embed a tracking iframe on load, use a click-to-load facade so it does not cost Largest Contentful Paint.

### Section 5 — Start here: A Sounding
**Action: keep the existing "Start here" section, absorb one other.**
- Keep the existing copy: ninety minutes, written analysis two days later, $300, comes off The Build.
- Absorb the three objections from "Before you book" as short inline lines beneath the CTA. Keep the question-and-answer pairs intact, compress the container.
- Move the relocated line here: "Or ask me a question first. I answer those myself," with the contact link.
- **Delete** the "Before any of it / You can just ask me something" section entirely. Its function now lives here. Retain the `hello@cydniejocelyn.com` address as plain text.
- **This section carries the page's single Deepwater band.**

### Section 6 — Retreats
**Action: reduce the existing Greece block.**
- Until 16 September, Greece remains but the full specification table is cut to: sold out, waitlist open, dates, location, link to the Greece page and link to the waitlist.
- **Delete** from the home page: early rate, standard rate, deposit line. Those stay on `/retreats/greece/`.
- **Delete** the sentence "A second date lands in April 2027." It is replaced in Phase 5.
- **Delete** the retreat card line "Booking opens in September for the April getaway." It is stale and the word "getaway" is off-voice.

### Section 7 — Close
**Action: keep the existing closing CTA, add two things.**
- Existing final CTA copy and button stay.
- Add an inline email capture for The Letters. Single field, no popup. Note: the sitewide Sounding popup already runs at a 45 second delay with 30 day dismissal memory. Do not add or trigger any second popup on this page.
- Add the home FAQ beneath, as a collapsed accordion. Question set specified in Phase 4.

### Sections deleted outright in Phase 1
- **"What it leads to"** and its four offer cards. This section is dissolved, not relocated. Each card's function is now carried by a full section: the Sounding card by Section 5, the Retreats card by Section 6, The Letters card by the Section 7 capture, and The Build card by Section 3. Before deleting, confirm nothing unique is lost. Two lines in it are the only instances of their content and must be handled: the Retreats card carries "Fifteen seats, because above a certain number solitude becomes performance," which already exists in "The room I build" and is therefore safe to delete, and The Build card carries "Every price is published, and your Sounding fee comes off it," which must be preserved and moved into Section 3.
- **"The difference."** Contains a verbatim duplicate of the H1 and its follow-on sentence. The duplication is the reason for the cut.
- **"The path"** three-step jump module.
- **"Before you decide / Here is what I won't do."** Moves to The Build in Phase 2.
- **"The room I build."** Moves to Retreats in Phase 2.
- **"Why me / I was the client."** Moves to About in Phase 2. Replace on the home page with nothing. It is not needed in the new order.
- **"If I don't fit into a box, you shouldn't either."** Delete. Not relocated.
- **The mid-page "Brand strategy across Minnesota" city band.** Delete. The footer list is retained.
- **The `40m` element**, pending the Phase 0 report on what it is.

### Phase 1 reporting
- Report every deleted section and the motion lost with it.
- Report every internal anchor that is now broken and what it should point to instead.
- Report the disposition of the inter-section scroll cues, including "Read on," "Come up" and any others found in Phase 0. Several are attached to sections being deleted. Do not delete a cue that still has a valid destination and do not leave one pointing at a removed section. Propose where each surviving cue should land and wait for approval.

**GATE 1 — Cydnie approves before Phase 2 begins.**

---

## PHASE 2 — Relocate displaced content

Move intact. Do not rewrite. Preserve existing markup and motion.

### 2.1 To `/the-build/`
- **"Here is what I won't do."** Place above the pricing block, below the scope explanation.
  - Reduce from four items to three. **Delete** the fourth item, "Nobody pulls you out." It is a philosophy statement inside a list that promised refusals, and it breaks the pattern.
  - Fix the third item: the heading and the first sentence of the body are currently the identical sentence, "You will meet me where you are." Keep the heading, cut the duplicate opening from the body.
- Add the FAQ question "Do you publish your pricing?" to this page. Remove it from the home page.

### 2.2 To `/retreats/`
- **"The room I build"** section, in full, including the fifteen-circle graphic and its alt text.
- Add the FAQ questions "What does alone in a group of fifteen mean?" and "Are the retreats women only?" to this page. Remove both from the home page.

### 2.3 To `/a-sounding/`
- Add the FAQ questions "What actually happens, and when?" and "What if I am not ready to spend $300?" to this page. Remove both from the home page.

### 2.4 To `/about/`
- Confirm whether the "I was the client" narrative already appears on About. If it does, delete the home page instance without relocating. If it does not, move it in full.

**GATE 2 — Cydnie approves before Phase 3 begins.**

---

## PHASE 3 — Client work showcase

This is the highest-value addition in the brief. The site currently sells brand and web design while showing no brand or web design.

### 3.1 Home page, Section 4 top half
Build a three-item showcase in this exact order. All URLs confirmed live and reflecting her work. All copy approved and set verbatim.

**1. Mane Alchemist Salon** · https://manealchemistsalon.com
> Full brand launch. Logo, brand guide, voice, and a website built to scale. Followed by a 90 day social launch plan that built demand before opening. Now on quarterly content and monthly strategy.

**2. SRS Performance** · https://srsperform.com
> Brand and operations for a Minneapolis strength studio. Took over a half built site and rebuilt it as a brand. Then email funnels, offering guides, niche and differentiation, and a plan for getting into the community and vetting locations.

**3. SolyRey** · https://solyrey.com
> Full brand refresh for a founder with a clear vision and no capacity to execute it. New logo, brand guide, and a complete website relaunch.

- **Order is deliberate.** SRS sits second because it is the only entry proving brand and operations inside one engagement, which is the claim Section 3 opens with. Do not reorder alphabetically or by date.
- T Sharp and Alchemy with A are **not** featured. Remove both from the existing "Built to stand" list on the home page and from the parallel list on `/the-build/#work`.
- Each item carries: project name, its copy above, thumbnail, and an outbound link to the live site. Links open in a new tab with `rel="noopener"`.
- Do not add, shorten, or expand the project copy. Do not add metrics of any kind.
- Thumbnails: WebP, explicit width and height attributes to prevent layout shift, `loading="lazy"`, descriptive filenames (`work-mane-alchemist-800.webp`, not `img-01.webp`).
- Alt text describes the work shown, not the brand name alone. Example shape: "Mane Alchemist website home page, dark identity with serif wordmark." Draft alt text and submit it for approval rather than publishing it.

### 3.2 `/the-build/#work`
- Bring this section to parity with the home page showcase so the "Client work" link does not land on something thinner than what the visitor just left.

**GATE 3 — Cydnie approves before Phase 4 begins.**

---

## PHASE 4 — SEO, schema and technical visibility

### 4.1 Canonical and hostname
- Resolve the www versus non-www mismatch identified in Phase 0. Pick one hostname, make the canonical tag, `og:url` and all internal absolute links agree with it, and confirm a 301 runs from the other.

### 4.2 FAQ split and FAQPage schema
Four separate FAQ blocks, each with its own `FAQPage` schema. Do not duplicate the same question across two pages, since duplicated FAQ schema is routinely ignored.

**Home page keeps five:**
1. Is this brand strategy, or is this a conversation about how I feel?
2. What if I cannot explain what is wrong?
3. What is the resurfacing business?
4. How do I start working with Cydnie Jocelyn?
5. Where is Cydnie Jocelyn based?

**`/a-sounding/` takes two:** What actually happens, and when? / What if I am not ready to spend $300?

**`/the-build/` takes one:** Do you publish your pricing?

**`/retreats/` takes two:** What does alone in a group of fifteen mean? / Are the retreats women only?

Answers move verbatim. No rewriting.

### 4.3 Structured data to implement
- `ProfessionalService` or `LocalBusiness` on the home page, with name, address locality Forest Lake MN, geo coordinates already present in meta, email, URL, `areaServed`, and `sameAs` for Instagram, Facebook, Pinterest, YouTube.
- `Person` for Cydnie Jocelyn Brown, linked from the organization as founder, with `sameAs` to the same social profiles.
- `Service` for A Sounding, with `offers` carrying the $300 price and USD currency.
- `Service` for The Build, with `offers` carrying the three published floors as `lowPrice` entries in USD: website $4,000, quarterly social and content $3,600, full brand launch $15,000. Approved for publication.
- `Event` for each retreat on its own retreat page, not on the home page, with start and end dates, location, and offer pricing. Greece is marked `SoldOut`.
- `BreadcrumbList` on all non-home pages.
- Validate everything against Google's Rich Results Test before reporting complete.

### 4.4 On-page SEO
- One H1 per page. Confirm the home page has exactly one after restructure.
- Heading hierarchy must not skip levels. Report any H2 followed directly by H4.
- Every section keeps or gains a stable ID so anchors survive.
- The footer city list is retained but reduced. Current list runs to thirteen towns in one paragraph and reads as keyword stuffing to a human. Reduce to the six highest-value: Forest Lake, Minneapolis, Saint Paul, Stillwater, Woodbury, White Bear Lake. Keep the "remotely anywhere" clause.
- Footer descriptor: replace "Strategic brand partner for what's next" with the hero category line, shortened. It currently contradicts the hero positioning and it is the last line a visitor reads.
- **Desktop nav stays exactly as it is.** No descriptors, no subtitles, no changes to labels. Decided: the clutter cost outweighs the comprehension gain, and Section 3 plus the work showcase carry the explanation instead.
- Short descriptors are added in two lower-pressure places only: the mobile menu and the footer link lists. Use "The Build, brand and website work" and "The Letters, free weekly."
- Internal linking: home Section 3 links to `/the-build/`, Section 4 links to `/the-build/#work`, Section 5 links to `/a-sounding/`, Section 6 links to `/retreats/`. Descriptive anchor text, never "learn more."

### 4.4b Image alt text and duplicate assets
- `layer-surface-1800.webp` is currently used twice on the home page, once in "The difference" and once in "The condition." The second instance has an empty alt attribute. After Phase 1 deletes "The difference," confirm only one instance remains and give it descriptive alt text.
- Audit every image on the home page for a missing, empty or non-descriptive alt attribute and report the list before writing any replacements.
- Alt text describes the image content, not the brand. Submit all drafted alt text for approval rather than publishing it.

### 4.5 Performance
- Preload the hero image. It is the Largest Contentful Paint element.
- Explicit width and height on every image sitewide to eliminate layout shift.
- `loading="lazy"` on everything below the first screen, and only below it.
- Fonts on `font-display: swap`.
- Report Core Web Vitals before and after on mobile.

### 4.6 Cleanup
- Fix or remove every anchor broken by Phase 1.
- Confirm The Letters button points to the current form and not the old Collective form.
- Regenerate `sitemap.xml` and confirm `robots.txt` references it.

**GATE 4 — Cydnie approves before Phase 5 begins.**

---

## PHASE 5 — Gatlinburg swap (Wednesday 16 September, held until launch)

Do not execute before Cydnie confirms launch. Prepare only.

- Section 6 becomes Gatlinburg: Wide Open, The Gatlinburg Edition. Dates 13 to 18 April 2027. Private King Suite and Shared Room, both rates. $500 deposit. Knoxville (TYS) fly-in. The 1 November price increase as the single scarcity line, since it is the only real one.
- Greece drops to one line beneath it: sold out, waitlist open, link.
- Any retreat "from" price sitewide updates to the shared room rate. Verify against live HoneyBook service records before publishing. Published page prices and HoneyBook records must match on launch day.
- **No popup for Gatlinburg.** The Sounding popup already runs sitewide. Two competing popups means one gets dismissed reflexively, and it will be the newer one. The section swap gives Gatlinburg more space than a banner would and costs nothing.
- Add `Event` schema for Gatlinburg on the retreat page.

**GATE 5 — final approval before publish.**

---

## OUTSTANDING — still needed from Cydnie

All copy is approved and written into the phases above. No copy TKs remain. Four items are open.

### Assets
1. Thumbnail image for Mane Alchemist Salon.
2. Thumbnail image for SRS Performance.
3. Thumbnail image for SolyRey.
4. Melissa video thumbnail image.

Phase 3 cannot complete without items 1 through 3. Phase 1 Section 4 cannot complete without item 4.

### Decisions
5. Hero photo placement. Sticky header, below hero, or neither. Phase 1 Section 1.
6. Tamara's testimonial reattribution to Mane Alchemist Salon, pending her confirmation. Default to "Consulting client" if unconfirmed.

### Closed decisions, recorded so they are not reopened
- Pricing is published. Floors, not ranges, not fixed prices.
- The $1,500 day build stays off the home page.
- Desktop navigation is unchanged. Descriptors in mobile menu and footer only.
- T Sharp and Alchemy with A are not featured anywhere.
- Showcase order is Mane Alchemist, SRS Performance, SolyRey, and is not alphabetical or chronological.
- No popup for Gatlinburg.
