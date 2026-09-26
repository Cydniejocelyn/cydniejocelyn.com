"""Retreats hub (/retreats/), rebuilt 25 September 2026 on the luxury system.

Kept, because it was right: the headline, the three dates and every fact on
them, "Alone in a group of fifteen", the Costa Rica voices and Melissa's
video (moved here from About), "Bring your own fifteen", the FAQ. Fixed:
"Twice a year" beside three dates; "A Sounding / The Build" -> the site's
names; "Carol Poedel" -> "Carol" as everywhere else; "Not for you if" ->
"What it isn't" (qualifies without pushing away). Arizona stays unnamed on
this page: it is live but unlinked until she says launch (HANDOFF 68).
Retreats stay women only (HANDOFF 53).

    cd tools && python3 gen_retreats.py
"""
import lux_page as L

URL = L.SITE + "/retreats/"
ARW = L.ARW
GREECE_WAIT = "https://clients.cydniejocelyn.com/public/6a21d07b6dcfbe3d85c663b6"
MAY_LIST = "https://www.honeybook.com/widget/cydnie_jocelyn_collective_299013/cf_id/69fa3c69e63a7a4c9bb354f1"
PRIVATE = "https://www.honeybook.com/widget/cydnie_jocelyn_collective_299013/cf_id/69fa33ac59c6a6842e88b725"

FAQ = [
    ("Do I have to own a business to come?",
     "No. Some women who come run companies and some do not, and it has never once mattered in the room. The consulting is separate: <a class=\"hv-inline\" href=\"/the-build/\">Work with me</a>."),
    ("Do I have to come with someone?",
     "Most women come alone. That is the normal way to do this, not the brave version of it. Fifteen is small enough that by the second day you are not on the edge of anything."),
    ("What fitness level does this require?",
     "None in particular. Movement is led every day and shaped around who is in the room, not around who is fittest. If stairs and trails are a real concern, tell me before you book and I will be straight with you."),
    ("Can you accommodate how I eat?",
     "Yes. List anything when you book and it reaches the kitchen well before you land."),
    ("What is included?",
     "In Gatlinburg: lodging, every meal, daily movement, two workshops and two outings. Airfare is not included; fly into Knoxville and from the airport forward the logistics are ours. Each retreat lists exactly what is included on its own page."),
    ("What does it cost and how do I hold a seat?",
     "Gatlinburg is $1,490 for a shared room and $2,790 for the private king suite at the early rate, through 31 October 2026, and $500 holds your room. Greece is $3,450, with a $500 non-refundable deposit. Every figure is published on the retreat&rsquo;s own page."),
    ("Do I need travel insurance?",
     "It is not required, and I would buy it the day you book. The deposit is non-refundable and your flight will be booked months out."),
    ("Are the retreats women only?",
     "Yes. Each retreat says so on its own page. The consulting is for founders and leaders of any gender."),
]

S = lambda quote, who, where: (
    '<figure class="hv-slide" data-slide><blockquote><p>&ldquo;%s&rdquo;</p></blockquote>'
    '<figcaption>%s &middot; %s</figcaption></figure>' % (quote, who, where))

Q = lambda quote, body, who, where: (
    '<li><figure class="hv-q"><blockquote><p>&ldquo;%s&rdquo;</p><p>%s</p></blockquote>'
    '<figcaption>%s &middot; %s</figcaption></figure></li>' % (quote, body, who, where))

MAIN = """<main id="main">

<section class="ww-hero" aria-labelledby="rx-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <span class="hv-label">Retreats for women</span>
      <h1 id="rx-h">A week where you are not the one <em>holding it together.</em></h1>
      <p class="hv-lede">Small-group retreats for women who are the reason everything works. Lodging, every meal and the plans are handled. You don&rsquo;t need to own a business to come.</p>
      <div class="hv-btns">
        <a class="hv-btn hv-btn--ink" href="/retreats/gatlinburg/#rooms" data-cta="retreats-hero-rooms">Choose your Gatlinburg room %(ARW)s</a>
        <a class="hv-btn hv-btn--line" href="#dates">See all dates</a>
      </div>
      <div class="rx-next"><span>Next retreat</span><p><b>Gatlinburg, Tennessee &middot; 13&ndash;18 April 2027</b>From $1,490. The early rate ends 31 October, and $500 holds your room.</p></div>
    </div>
    <figure class="ww-arch">
      <img src="../assets/img/retreats/cr-floor-1000.webp" srcset="../assets/img/retreats/cr-floor-600.webp 600w, ../assets/img/retreats/cr-floor-1000.webp 1000w" sizes="(min-width: 64rem) 30rem, 90vw" width="1000" height="1613" alt="Women sitting together in a circle on the floor of an open-air pavilion in Costa Rica" fetchpriority="high">
      <figcaption><span>Costa Rica, day three</span><b>Nine in the morning</b></figcaption>
    </figure>
  </div>
</section>

<!-- PROOF, straight under the hero. -->
<section class="hv-proof rx-proofstrip" aria-label="What guests said">
  <div class="hv-wrap rx-proofstrip-in">
    <span class="hv-label">Costa Rica &middot; April 2026</span>
    <blockquote>&ldquo;The fact that you&rsquo;re even considering it should tell you that you should go.&rdquo;<cite>Kristi, retreat guest</cite></blockquote>
    <blockquote>&ldquo;I learned that I matter too.&rdquo;<cite>Melissa, retreat guest</cite></blockquote>
  </div>
</section>

<!-- THE DATES. Every fact from the old page, unchanged. Arizona unnamed. -->
<section class="hv-sec" id="dates" aria-labelledby="rx-dates">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">On the calendar</span>
      <h2 class="hv-h2" id="rx-dates">Three dates. <em>When one fills, it closes.</em></h2>
    </div>
    <ul class="rx-dates" role="list">
      <li class="rx-date">
        <figure><img src="../assets/img/gatlinburg/house-dusk-portrait-834.webp" srcset="../assets/img/gatlinburg/house-dusk-portrait-600.webp 600w, ../assets/img/gatlinburg/house-dusk-portrait-834.webp 834w" sizes="(min-width: 60rem) 24rem, 92vw" width="834" height="1112" alt="The private house in Gatlinburg lit up at dusk against the Smoky Mountains" loading="lazy"></figure>
        <div class="rx-date-body">
          <span class="hv-pill rx-pill">Booking open</span>
          <p class="rx-when">13&ndash;18 April 2027 &middot; Gatlinburg, Tennessee</p>
          <h3>Wide Open: The Gatlinburg Edition</h3>
          <p>Five days in a private house at the edge of the Smoky Mountains, with Kayla Freeman leading the morning movement. Lodging, every meal, two workshops and two outings are included.</p>
          <dl><div><dt>Shared room</dt><dd>$1,490</dd></div><div><dt>Private king suite</dt><dd>$2,790</dd></div></dl>
          <p class="rx-note">Early rate through 31 October. $500 holds your room. Fly into Knoxville; from the airport forward, the logistics are ours.</p>
          <div class="hv-btns"><a class="hv-btn hv-btn--ink" href="/retreats/gatlinburg/#rooms" data-cta="retreats-card-rooms">Choose your room %(ARW)s</a><a class="hv-link" href="/retreats/gatlinburg/">See the week</a></div>
        </div>
      </li>
      <li class="rx-date rx-date--soon">
        <figure class="rx-soon"><!-- The US map from tools/us_map.py (via the old page): the country, and an open ring where the pin would go. -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 633"
               role="img" aria-labelledby="usmap-t" class="usmap" preserveAspectRatio="xMidYMid meet">
            <title id="usmap-t">A map of the United States with no location marked on it</title>
            <defs>
              <!-- The country fades at its edges rather than stopping on a hard line,
                   which is the same seam construction the page's own sections use. -->
              <radialGradient id="usmap-veil" cx="50%%" cy="46%%" r="62%%">
                <stop offset="0%%"   stop-color="#fff" stop-opacity="1"/>
                <stop offset="62%%"  stop-color="#fff" stop-opacity="1"/>
                <stop offset="100%%" stop-color="#fff" stop-opacity="0"/>
              </radialGradient>
              <mask id="usmap-mask">
                <rect width="1000" height="633" fill="url(#usmap-veil)"/>
              </mask>
            </defs>
            <g mask="url(#usmap-mask)">
              <path class="usmap-fill" fill-rule="evenodd" d="M65.0 18.1L93.9 12.0L185.8 36.9L294.0 58.0L386.7 69.3L450.1 73.5L493.5 74.8L526.1 65.8L554.6 83.4L568.3 89.4L594.8 94.1L614.8 95.2L638.7 112.4L683.3 118.7L701.9 122.4L698.6 138.4L735.8 145.2L749.5 185.0L746.4 201.0L732.5 232.8L774.5 220.4L793.6 202.7L804.0 192.4L802.0 183.7L842.0 167.9L844.5 155.2L858.6 141.1L865.6 128.3L917.8 114.9L922.4 106.5L930.0 82.1L938.3 51.1L958.2 48.7L968.7 70.3L988.0 90.1L977.6 109.7L947.4 138.7L942.7 159.7L958.5 176.0L934.8 199.8L903.8 225.4L901.6 255.7L893.7 272.1L894.0 293.8L886.3 319.0L900.0 340.8L904.0 356.3L887.9 374.9L863.8 398.0L832.7 430.4L815.9 450.6L809.1 483.8L826.1 517.2L837.1 534.7L854.8 575.5L853.0 611.3L825.4 598.8L790.4 554.3L782.4 525.2L742.1 517.3L726.5 508.4L676.8 507.5L650.5 513.2L658.2 538.9L635.5 536.9L555.3 530.9L525.3 549.2L483.1 576.6L487.8 621.1L445.9 609.3L420.3 557.8L408.9 535.7L367.1 537.7L333.1 520.4L301.9 469.7L267.3 465.4L265.9 476.0L208.5 467.3L142.5 421.3L94.8 415.3L79.7 382.7L42.1 355.0L40.4 330.0L29.6 298.7L26.5 268.3L13.1 235.8L12.0 198.7L23.5 163.8L32.9 134.6L47.6 107.1L59.8 69.9L62.9 52.2ZM696.5 138.6L676.2 158.8L678.2 184.8L682.1 212.9L672.6 239.9L660.4 241.1L652.2 208.7L658.3 173.7L661.2 159.2L673.3 147.3Z"/>
              <path class="usmap-line" d="M65.0 18.1L93.9 12.0L185.8 36.9L294.0 58.0L386.7 69.3L450.1 73.5L493.5 74.8L526.1 65.8L554.6 83.4L568.3 89.4L594.8 94.1L614.8 95.2L638.7 112.4L683.3 118.7L701.9 122.4L698.6 138.4L735.8 145.2L749.5 185.0L746.4 201.0L732.5 232.8L774.5 220.4L793.6 202.7L804.0 192.4L802.0 183.7L842.0 167.9L844.5 155.2L858.6 141.1L865.6 128.3L917.8 114.9L922.4 106.5L930.0 82.1L938.3 51.1L958.2 48.7L968.7 70.3L988.0 90.1L977.6 109.7L947.4 138.7L942.7 159.7L958.5 176.0L934.8 199.8L903.8 225.4L901.6 255.7L893.7 272.1L894.0 293.8L886.3 319.0L900.0 340.8L904.0 356.3L887.9 374.9L863.8 398.0L832.7 430.4L815.9 450.6L809.1 483.8L826.1 517.2L837.1 534.7L854.8 575.5L853.0 611.3L825.4 598.8L790.4 554.3L782.4 525.2L742.1 517.3L726.5 508.4L676.8 507.5L650.5 513.2L658.2 538.9L635.5 536.9L555.3 530.9L525.3 549.2L483.1 576.6L487.8 621.1L445.9 609.3L420.3 557.8L408.9 535.7L367.1 537.7L333.1 520.4L301.9 469.7L267.3 465.4L265.9 476.0L208.5 467.3L142.5 421.3L94.8 415.3L79.7 382.7L42.1 355.0L40.4 330.0L29.6 298.7L26.5 268.3L13.1 235.8L12.0 198.7L23.5 163.8L32.9 134.6L47.6 107.1L59.8 69.9L62.9 52.2ZM696.5 138.6L676.2 158.8L678.2 184.8L682.1 212.9L672.6 239.9L660.4 241.1L652.2 208.7L658.3 173.7L661.2 159.2L673.3 147.3Z" pathLength="1"/>
            </g>
            <g class="usmap-pin" transform="translate(530.7 276.1)">
              <circle class="usmap-ring" r="21"/>
              <circle class="usmap-ring usmap-ring--out" r="38"/>
            </g>
          </svg>
          <figcaption><span>May</span><b>2027 &middot; Somewhere in the United States</b></figcaption></figure>
        <div class="rx-date-body">
          <span class="hv-pill rx-pill rx-pill--line">In the works</span>
          <p class="rx-when">5&ndash;9 May 2027 &middot; Location named later</p>
          <h3>A third date is coming.</h3>
          <p>Five days in the United States, co-hosted with Clarissa Castillo Ramsey, whose work I have wanted to put in a room with mine for a long time. The list hears the place, the price and the shape of the week before anyone else.</p>
          <a class="hv-btn hv-btn--line" href="%(MAY_LIST)s" data-cta="retreats-card-may">Hear about May first</a>
          <p class="rx-note">No payment. You hear the place, the price and the dates first.</p>
        </div>
      </li>
      <li class="rx-date">
        <figure><img src="../assets/img/greece/dinner-1200.webp" srcset="../assets/img/greece/dinner-600.webp 600w, ../assets/img/greece/dinner-900.webp 900w, ../assets/img/greece/dinner-1200.webp 1200w" sizes="(min-width: 60rem) 24rem, 92vw" width="1200" height="1200" alt="An outdoor dining table under a lantern-lit pergola at dusk at Armonia Retreat Center in Crete" loading="lazy"></figure>
        <div class="rx-date-body">
          <span class="hv-pill rx-pill rx-pill--ink">Full &middot; Waitlist open</span>
          <p class="rx-when">13&ndash;20 August 2027 &middot; Douliana, Crete</p>
          <h3>Rise Into Her: The Greece Edition</h3>
          <p>Eight days at Armonia Retreat Center in a hillside village of about forty houses. Water, food cooked on site, long walks, and enough quiet to hear what you actually think. Movement led by Kris Krause.</p>
          <p class="rx-note">All fifteen seats are spoken for. The list is how they get filled when one opens.</p>
          <div class="hv-btns"><a class="hv-btn hv-btn--ink" href="%(GREECE_WAIT)s" data-cta="retreats-card-greece-wait">Join the waitlist</a><a class="hv-link" href="/retreats/greece/">Everything about Greece</a></div>
        </div>
      </li>
    </ul>
  </div>
</section>

<!-- THE FORMAT, and who it is for, in one section. "What it isn't" is
     folded into the format list; the sunset band is cut for length. -->
<section class="hv-sec rx-format" aria-labelledby="rx-fifteen">
  <div class="hv-wrap au-row">
    <figure class="rx-wide"><img src="../assets/img/retreats/cr-room-1200.webp" srcset="../assets/img/retreats/cr-room-600.webp 600w, ../assets/img/retreats/cr-room-1200.webp 1200w, ../assets/img/retreats/cr-room-1800.webp 1800w" sizes="(min-width: 60rem) 30rem, 92vw" width="1200" height="675" alt="Women stretching on mats on a wooden deck beside a pool in Costa Rica" loading="lazy"><figcaption>The middle of the week, on the floor.</figcaption></figure>
    <div>
      <span class="hv-label">Who it is for</span>
      <h2 class="hv-h2" id="rx-fifteen">For the woman <em>everyone depends on.</em></h2>
      <ul class="au-facts rx-days" role="list">
        <li>You are the one everybody depends on, at work, at home, or both.</li>
        <li>You want a stretch of days where that is not the arrangement.</li>
        <li>You want to come home knowing fourteen women well enough to text them.</li>
      </ul>
      <p class="rx-format-copy">No retreat goes over fifteen women, because that is how many people can actually be known in a week. Rest, movement, food somebody else made, and long stretches of unscheduled time. No workbook, no pitch, nothing to prepare.</p>
      <p class="au-why">Nobody will need anything from you. <em>Nobody will leave you either.</em></p>
    </div>
  </div>
</section>

<!-- COSTA RICA: the proof. Melissa's video and the guests' words, moved
     here from About. -->
<section class="hv-sec" aria-labelledby="rx-cr">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Costa Rica &middot; April 2026</span>
      <h2 class="hv-h2" id="rx-cr">The last one <em>already happened.</em></h2>
      <p class="hv-lede">Rise &amp; Reground ran in Nosara in April 2026. This is what the women said afterward, in their own words.</p>
    </div>
    <div class="rx-proof">
      <figure class="au-vid rx-vid">
        <a class="rt-play melissa-play" data-video="DrrP4hdw0lo" data-src="../assets/video/melissa.mp4" data-start="3" data-title="Melissa on the Costa Rica retreat" href="../assets/video/melissa.mp4#t=3">
          <img src="../assets/img/retreats/melissa-poster-405.webp" srcset="../assets/img/retreats/melissa-poster-300.webp 300w, ../assets/img/retreats/melissa-poster-405.webp 405w" sizes="(min-width: 60rem) 20rem, 74vw" width="405" height="720" loading="lazy" decoding="async" alt="Melissa, speaking to her phone camera in her car on the way home from the retreat.">
          <span class="au-play" aria-hidden="true"><svg width="18" height="20" viewBox="0 0 18 20" fill="currentColor"><path d="M0 0l18 10L0 20z"/></svg></span>
          <span class="hv-vh">Play Melissa&rsquo;s video about the Costa Rica retreat</span></a>
        <figcaption><b>&ldquo;I learned that I matter too.&rdquo;</b> Melissa recorded this on her phone on the drive home. Three minutes, not edited.</figcaption>
      </figure>
      <div class="hv-slides" data-slides aria-roledescription="carousel" aria-label="What guests said">
        <div class="hv-slides-track" aria-live="off">
          %(S1)s
          %(S2)s
          %(S3)s
          %(S4)s
          %(S5)s
          %(S6)s
        </div>
        <div class="hv-slides-nav" hidden>
          <button type="button" class="hv-slides-prev" aria-label="Previous review"><svg viewBox="0 0 16 10" fill="none" aria-hidden="true"><path d="M5 1L1 5l4 4M1 5h15" stroke="currentColor" stroke-width="1.2"/></svg></button>
          <div class="hv-slides-dots" role="group" aria-label="Choose a review"></div>
          <button type="button" class="hv-slides-next" aria-label="Next review"><svg viewBox="0 0 16 10" fill="none" aria-hidden="true"><path d="M11 1l4 4-4 4M15 5H0" stroke="currentColor" stroke-width="1.2"/></svg></button>
        </div>
      </div>
    </div>
    <div class="rx-proof-cta"><a class="hv-btn hv-btn--ink" href="/retreats/gatlinburg/#rooms" data-cta="retreats-proof-rooms">Choose your Gatlinburg room %(ARW)s</a><span>Early rate through 31 October</span></div>
  </div>
</section>

<!-- PRIVATE RETREATS -->
<section class="hv-sec ww-standards rx-private" aria-labelledby="rx-private">
  <div class="hv-wrap au-row">
    <div>
      <span class="hv-label">By inquiry</span>
      <h2 class="hv-h2" id="rx-private">Bring your <em>own fifteen.</em></h2>
    </div>
    <div>
      <p class="sd-truth-copy">If you already have the women, I will build the week: your group, your dates, your location. Teams and communities use it too. The price depends on where and how long, so it starts with a conversation.</p>
      <div class="hv-btns" style="margin-top:2rem"><a class="hv-btn hv-btn--blue rx-btn-light" href="%(PRIVATE)s" data-cta="retreats-private">Start a private inquiry %(ARW)s</a></div>
    </div>
  </div>
</section>

<section class="hv-sec" id="faq" aria-labelledby="faq-h">
  <div class="hv-wrap hv-faq ww-faq">
    <div>
      <span class="hv-label">Before you book</span>
      <h2 class="hv-h2" id="faq-h">What people <em>ask.</em></h2>
      <p class="hv-lede">Something not here? <a class="hv-inline" href="/contact/">Ask me directly.</a></p>
    </div>
    <div class="hv-faq-list">
%(FAQ)s
    </div>
  </div>
</section>

<section class="hv-close" aria-labelledby="close-h">
  <div class="hv-wrap">
    <span class="hv-label hv-label--c">Fifteen seats</span>
    <h2 class="hv-h2" id="close-h">When they go, <em>the date closes.</em></h2>
    <p class="hv-lede">That is the number, not a tactic. Gatlinburg is booking now, and the early rate holds through 31 October.</p>
    <div class="hv-btns">
      <a class="hv-btn hv-btn--ink" href="/retreats/gatlinburg/#rooms" data-cta="retreats-close-rooms">Choose your Gatlinburg room %(ARW)s</a>
      <a class="hv-btn hv-btn--line" href="%(GREECE_WAIT)s">Greece waitlist</a>
    </div>
    <p class="au-also">Looking for the consulting instead? <a class="hv-inline" href="/the-build/">Work with me</a>, with every price published.</p>
  </div>
</section>

</main>
""" % {
    "ARW": ARW, "GREECE_WAIT": GREECE_WAIT, "MAY_LIST": MAY_LIST, "PRIVATE": PRIVATE, "FAQ": L.faq_html(FAQ),
    "S1": S('I was burnt out and struggling to figure out why I always felt behind. My need to be perfect and always reliable had become the reason I failed to show up for myself when I needed it the most.', 'Kristi', 'Rise &amp; Reground, Costa Rica'),
    "S2": S('Intimate group size, and leaders able to make us think, laugh and cry without judgement. No waiting, no rushing.', 'Carol', 'Rise &amp; Reground, Costa Rica'),
    "S3": S('I walked in carrying fear that the experience would take more from me than I had to give. I left being able to breathe, with old and new friends who cared about me.', 'BJB', 'Rise &amp; Reground, Costa Rica'),
    "S4": S('It greatly surpassed all my expectations. My only regret was that I did not pack more swim suits.', 'Alice', 'Rise &amp; Reground, Costa Rica'),
    "S5": S('If you are weary from life and want to reset and refresh yourself, take a chance on an experience that will not disappoint you if you attend with open hands and heart.', 'Carol', 'Rise &amp; Reground, Costa Rica'),
    "S6": S('The friends you meet will be there for you if you are willing to reach out and share yourself. Costa Rica will remain in my heart forever.', 'BJB', 'Rise &amp; Reground, Costa Rica'),
}

graph = L.old_graph("retreats/index.html")
for n in graph:
    if n.get("@type") == "FAQPage":
        n.update(L.faq_node(URL, [(q, __import__("re").sub(r"<[^>]+>", "", a)) for q, a in FAQ]))

PRELOAD = ('<link rel="preload" as="image" href="../assets/img/retreats/cr-floor-1000.webp" '
           'imagesrcset="../assets/img/retreats/cr-floor-600.webp 600w, ../assets/img/retreats/cr-floor-1000.webp 1000w" '
           'imagesizes="(min-width: 64rem) 30rem, 90vw" type="image/webp" fetchpriority="high">\n')

n = L.render(
    out="retreats/index.html", depth=1, active="/retreats/",
    title="Retreats for Women | Gatlinburg and Crete 2027 | Cydnie Jocelyn",
    description="Small-group retreats for women, fifteen at most. Gatlinburg, Tennessee in April 2027, booking now; Crete in August 2027, waitlist open; a third date in May 2027.",
    canonical=URL,
    og_title="Retreats for Women | Cydnie Jocelyn",
    og_description="A week where you are not the one holding it together. Fifteen women at most. Gatlinburg April 2027, booking now.",
    graph=graph, main=MAIN, preload=PRELOAD, body_class="ww-page",
    reveal=(".ww-head", ".rx-date", ".au-row > div", ".hv-slides", ".rx-proof-cta"),
    reveal_imgs=(".rx-wide", ".rx-vid"),
)
print("written", n)
