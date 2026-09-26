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
    ("What does it cost and how do I hold a seat?",
     "Gatlinburg is $1,490 for a shared room and $2,790 for the private king suite at the early rate, through 31 October 2026, and $500 holds your room. Greece is $3,450, with a $500 non-refundable deposit. Every figure is published on the retreat&rsquo;s own page."),
    ("Do I need travel insurance?",
     "It is not required, and I would buy it the day you book. The deposit is non-refundable and your flight will be booked months out."),
    ("Are the retreats women only?",
     "Yes. Each retreat says so on its own page. The consulting is for founders and leaders of any gender."),
]

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
        <a class="hv-btn hv-btn--ink" href="/retreats/gatlinburg/" data-cta="retreats-hero-gatlinburg">See Gatlinburg, booking now %(ARW)s</a>
        <a class="hv-btn hv-btn--line" href="#dates">All dates</a>
      </div>
      <ul class="ww-trust" role="list"><li>Fifteen women at most</li><li>Nothing to prepare</li><li>Most come alone</li></ul>
    </div>
    <figure class="ww-arch">
      <img src="../assets/img/retreats/cr-floor-1000.webp" srcset="../assets/img/retreats/cr-floor-600.webp 600w, ../assets/img/retreats/cr-floor-1000.webp 1000w" sizes="(min-width: 64rem) 30rem, 90vw" width="1000" height="1613" alt="Women sitting together in a circle on the floor of an open-air pavilion in Costa Rica" fetchpriority="high">
      <figcaption><span>Costa Rica, day three</span><b>Nine in the morning</b></figcaption>
    </figure>
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
          <p class="rx-note">Early rate through 31 October. $500 holds your room.</p>
          <a class="hv-btn hv-btn--ink" href="/retreats/gatlinburg/" data-cta="retreats-card-gatlinburg">See Gatlinburg and book %(ARW)s</a>
        </div>
      </li>
      <li class="rx-date rx-date--soon">
        <div class="rx-soon" aria-hidden="true"><span>May</span><b>2027</b></div>
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

<!-- THE FORMAT: fifteen. -->
<section class="hv-sec rx-format" aria-labelledby="rx-fifteen">
  <div class="hv-wrap au-row">
    <figure class="rx-wide"><img src="../assets/img/retreats/cr-room-1200.webp" srcset="../assets/img/retreats/cr-room-600.webp 600w, ../assets/img/retreats/cr-room-1200.webp 1200w, ../assets/img/retreats/cr-room-1800.webp 1800w" sizes="(min-width: 60rem) 30rem, 92vw" width="1200" height="675" alt="Women stretching on mats on a wooden deck beside a pool in Costa Rica" loading="lazy"><figcaption>The middle of the week, on the floor.</figcaption></figure>
    <div>
      <span class="hv-label">The format</span>
      <h2 class="hv-h2" id="rx-fifteen">Alone in a group <em>of fifteen.</em></h2>
      <p class="hv-lede">No retreat goes over fifteen women, and some are smaller, because that is how many people can actually be known in a week.</p>
      <ul class="au-facts rx-days" role="list">
        <li>Rest, movement, and food somebody else made.</li>
        <li>Long stretches of unscheduled time.</li>
        <li>No workbook, no intention circle, nothing to prepare.</li>
      </ul>
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
      <ul class="hv-quotes rx-quotes" role="list">
        %(Q1)s
        %(Q2)s
        %(Q3)s
        %(Q4)s
      </ul>
    </div>
  </div>
</section>

<!-- A PAUSE: the low tide, her caption. -->
<figure class="rx-band">
  <img src="../assets/img/retreats/cr-dusk-1200.webp" srcset="../assets/img/retreats/cr-dusk-600.webp 600w, ../assets/img/retreats/cr-dusk-1200.webp 1200w, ../assets/img/retreats/cr-dusk-1536.webp 1536w" sizes="100vw" width="1536" height="2048" alt="The sunset sky reflected in wet sand at low tide in Costa Rica" loading="lazy">
  <figcaption><span class="hv-label">Costa Rica &middot; the last evening</span><p>Low tide, and the whole sky in the sand. <em>Nobody organised this part.</em></p></figcaption>
</figure>

<!-- WHO IT IS FOR. "Not for you if" softened to "What it isn't". -->
<section class="hv-sec ww-pf" aria-labelledby="rx-who">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Who this is for</span>
      <h2 class="hv-h2" id="rx-who">For the woman <em>everyone depends on.</em></h2>
    </div>
    <div class="ww-pf-grid">
      <div class="ww-fix rx-for">
        <h3>It is for you if</h3>
        <ul role="list">
          <li>You are the one everybody depends on, at work, at home, or both.</li>
          <li>You want a stretch of days where that is not the arrangement.</li>
          <li>You want to come home knowing fourteen women well enough to text them.</li>
        </ul>
      </div>
      <div class="ww-problem rx-isnt">
        <h3>What it isn&rsquo;t</h3>
        <ul role="list">
          <li>A mastermind. Nobody is going to pitch you.</li>
          <li>A curriculum with a binder to take home.</li>
          <li>A programme you need a measurable outcome from before the cost feels justified.</li>
        </ul>
      </div>
    </div>
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
    "Q1": Q("The fact that you&rsquo;re even considering it should tell you that you should go.", "You&rsquo;ll come out the other end with new people in your life.", "Kristi", "asked what she would say to someone afraid to come alone"),
    "Q2": Q("No waiting, no rushing.", "Intimate group size, and leaders able to make us think, laugh and cry without judgement.", "Carol", "Rise &amp; Reground, Costa Rica"),
    "Q3": Q("I left being able to breathe.", "I walked in carrying fear that the experience would take more from me than I had to give.", "BJB", "Rise &amp; Reground, Costa Rica"),
    "Q4": Q("My only regret was that I did not pack more swim suits.", "It greatly surpassed all my expectations.", "Alice", "Rise &amp; Reground, Costa Rica"),
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
    reveal=(".ww-head", ".rx-date", ".au-row > div", ".rx-quotes > li", ".ww-pf-grid > div"),
    reveal_imgs=(".rx-wide", ".rx-vid"),
)
print("written", n)
