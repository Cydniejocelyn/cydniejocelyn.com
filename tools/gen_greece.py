"""Rise Into Her: The Greece Edition (/retreats/greece/), rebuilt 25 September
2026 on the luxury system. FULL: every seat is taken and the list is open.

The page has two jobs, in this order: fill the waitlist, and hand anyone
who will not wait to Gatlinburg. Every fact, figure and link is from the
live page: $3,450, the $500 deposit, pay in full or six monthly payments,
both waitlist records (6a21d07b... pay in full, 6a21d63a... six month plan),
the question form (cf_id/69fa372c...), the 16-photo gallery (verbatim,
tools/greece_gallery.html), the village and property figures, both hosts,
the four objections and the FAQ. Cut for length and tone: "Who this is not
for" (its lines read as reasons to leave), "Still not answered" (folded into
the FAQ intro), the closing band (folded into the seat section).

    cd tools && python3 gen_greece.py
"""
import os
import lux_page as L

URL = L.SITE + "/retreats/greece/"
ARW = L.ARW
WAIT_FULL = "https://clients.cydniejocelyn.com/public/6a21d07b6dcfbe3d85c663b6"
WAIT_FULL_FORM = WAIT_FULL + "/1-Contact_Information"
WAIT_PLAN = "https://clients.cydniejocelyn.com/public/6a21d63a1b6caddcac951777/1-Contact_Information"
QUESTION = "https://www.honeybook.com/widget/cydnie_jocelyn_collective_299013/cf_id/69fa372ccd31fefc073c5d28"
G = "../../assets/img/greece/"
R = "../../assets/img/retreats/"
GALLERY = open(os.path.join(L.ROOT, "tools", "greece_gallery.html"), encoding="utf-8").read().strip()

FAQ = [
    ("Which airport, and how do I get to the house?", "Chania International, CHQ, about 33 km away; most cities connect through Athens. Fly in on 12 August, a day early on purpose, and be at the airport by 3:00 PM on the 13th for the group transfer. Ground transport is included both ways, and everyone holding a seat gets the full pre-travel guide."),
    ("Is there a single room?", "No. Every room is shared, two to a room, twin beds, each with its own bathroom. There is no single room and no supplement to buy one, so the price on this page is the price whoever you come with."),
    ("Can I come with a friend?", "Yes, and you will be roomed together. Say so when you book. It does not change the price either way."),
    ("Can you accommodate how I eat?", "Yes. List anything when you book and it gets to the kitchen well before you land. Meals are cooked on site with Cretan ingredients, so most things are straightforward."),
    ("Do I need travel insurance?", "It is not required and I would buy it anyway, on the day you book. The deposit is non-refundable and your flight will be booked months out. Insurance is the only thing covering either of those."),
    ("What is the phone signal like?", "Fine. There is wifi in the house and you will have service in the village. Nobody is taking your phone off you; Crete is nine hours ahead of Minnesota and the distance does most of the work on its own."),
]

S = lambda quote, who: ('<figure class="hv-slide" data-slide><blockquote><p>&ldquo;%s&rdquo;</p></blockquote>'
                        '<figcaption>%s &middot; Retreat guest, Costa Rica</figcaption></figure>' % (quote, who))

MAIN = """<main id="main">

<section class="ww-hero" aria-labelledby="gr-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <span class="hv-label">Rise Into Her &middot; The Greece Edition</span>
      <h1 id="gr-h">Eight days <em>in Crete.</em></h1>
      <p class="hv-lede">A small-group retreat for women in Douliana, a hillside village in western Crete with about forty houses in it. Fifteen seats, one property, and eight days that ask nothing of you.</p>
      <div class="hv-btns">
        <a class="hv-btn hv-btn--ink" href="#seat" data-cta="greece-hero-wait">Join the waitlist %(ARW)s</a>
        <a class="hv-btn hv-btn--line" href="/retreats/gatlinburg/" data-cta="greece-hero-gatlinburg">Gatlinburg is open</a>
      </div>
      <dl class="gt-facts">
        <div><dt>Dates</dt><dd>13&ndash;20 August 2027</dd></div>
        <div><dt>Where</dt><dd>Douliana, Crete</dd></div>
        <div><dt>Seats</dt><dd>Fifteen, all taken</dd></div>
        <div><dt>With</dt><dd>Cydnie and Kris</dd></div>
        <div><dt>Price</dt><dd>$3,450</dd></div>
        <div><dt>Waitlist</dt><dd>Open, no payment</dd></div>
      </dl>
    </div>
    <figure class="ww-arch">
      <img src="%(G)shouse-1200.webp" srcset="%(G)shouse-600.webp 600w, %(G)shouse-900.webp 900w, %(G)shouse-1200.webp 1200w" sizes="(min-width: 64rem) 30rem, 90vw" width="1200" height="1200" alt="The stone house at Armonia Retreat Center at dusk, a vine pergola across its front." fetchpriority="high">
      <figcaption><span>All fifteen seats taken</span><b>Waitlist open</b></figcaption>
    </figure>
  </div>
</section>

<section class="hv-proof rx-proofstrip" aria-label="What guests said">
  <div class="hv-wrap rx-proofstrip-in">
    <span class="hv-label">The last retreat &middot; Costa Rica</span>
    <blockquote>&ldquo;The fact that you&rsquo;re even considering it should tell you that you should go.&rdquo;<cite>Kristi, retreat guest</cite></blockquote>
    <blockquote>&ldquo;It greatly surpassed all my expectations.&rdquo;<cite>Alice, retreat guest</cite></blockquote>
  </div>
</section>

<section class="hv-sec" aria-labelledby="gr-why">
  <div class="hv-wrap au-row">
    <figure class="rx-wide gt-deck"><img src="%(G)sdrive-1200.webp" srcset="%(G)sdrive-600.webp 600w, %(G)sdrive-1200.webp 1200w, %(G)sdrive-1800.webp 1800w" sizes="(min-width: 60rem) 30rem, 92vw" width="1200" height="800" alt="A stone-paved lane through olive trees leading to the houses of Douliana." loading="lazy"><figcaption>The lane into Douliana.</figcaption></figure>
    <div>
      <span class="hv-label">Why this exists</span>
      <h2 class="hv-h2" id="gr-why">You are the one <em>everything runs through.</em></h2>
      <p class="hv-lede">It works because you are holding it, and holding it is the part nobody sees.</p>
      <p class="rx-format-copy">Eight days will not fix that. What it does is put you somewhere the weight is not yours for a week, with women in the same position, and let you find out what you think when nothing is asking for you.</p>
    </div>
  </div>
</section>

<section class="hv-sec ww-path gt-week" id="week" aria-labelledby="gr-week">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">The week</span>
      <h2 class="hv-h2" id="gr-week">Eight days, and only two of them <em>ask anything of you.</em></h2>
    </div>
    <ol class="ww-steps gt-days" role="list">
      <li><h3>Mornings</h3><p>Movement, led by Kris. Strength, mobility, and whatever your body will actually do that day. There is nothing to be behind in.</p></li>
      <li><h3>Crete, or nothing</h3><p>One day is Crete: the gorge trails, the harbour at Chania, villages from the eighteenth century. The next has nothing on it at all.</p></li>
      <li><h3>Two sittings</h3><p>Twice in the week the group sits down together. No workbook, no binder, and no round the room where everyone has to say something.</p></li>
      <li><h3>Evenings</h3><p>Dinner, cooked on site. The first night and the last are the full group; in between, you eat when you are hungry and go to bed early if you like.</p></li>
      <li><h3>The Tuesday after</h3><p>The point is the phone call you take at home a fortnight later, and how differently you answer it.</p></li>
    </ol>
    <p class="gr-aside">The excursion lineup is still being finalised. Everyone holding a seat gets the full schedule as it lands.</p>
  </div>
</section>

<section class="hv-sec ww-standards gt-place" aria-labelledby="gr-place">
  <div class="hv-wrap">
    <span class="hv-label">The place</span>
    <h2 class="hv-h2" id="gr-place">Douliana, <em>Crete.</em></h2>
    <p class="sd-truth-copy">About forty houses on a hilltop above Souda Bay, in the Apokoronas region of western Crete. Stone streets, and an architecture largely unchanged since the eighteenth century. A village people live in rather than a resort town, which is the whole reason it was chosen.</p>
    <div class="gt-nums gr-nums">
      <div><b><span data-count="40">40</span></b><span>Houses in the village</span></div>
      <div><b><span data-count="100">100</span><small>m</small></b><span>Above the sea</span></div>
      <div><b><span data-count="15">15</span><small>min</small></b><span>To the nearest water</span></div>
      <div><b><span data-count="33">33</span><small>km</small></b><span>From Chania airport</span></div>
    </div>
    <dl class="gt-legs">
      <div><dt>The sea</dt><dd>Almirida, Kalyves and Kera are all about fifteen minutes away. Kera stays quiet because the last stretch is a forty minute walk in.</dd></div>
      <div><dt>Walking</dt><dd>Trails leave from the village itself, through gorges and woodland to Agios Ioannis, a church built into a cave.</dd></div>
      <div><dt>Chania</dt><dd>The old town and the Venetian harbour, half an hour away and on the schedule at least once.</dd></div>
    </dl>
  </div>
</section>

<section class="hv-sec gt-house" id="stay" aria-labelledby="gr-stay">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Where you stay</span>
      <h2 class="hv-h2" id="gr-stay">Armonia <em>Retreat Center.</em></h2>
      <p class="hv-lede">One house, in the middle of the village, and for eight days it is only ours. Fifteen guests, two to a room, twin beds, and every room has its own bathroom. Kris and I are in the house too.</p>
    </div>
    <dl class="gr-stats">
      <div><dt>Of grounds</dt><dd>4,000 m&sup2;</dd></div>
      <div><dt>Women on the property</dt><dd>17</dd></div>
      <div><dt>Room type, one price</dt><dd>1</dd></div>
      <div><dt>Nights, all yours</dt><dd>7</dd></div>
    </dl>
    %(GALLERY)s
    <dl class="gt-legs gr-onsite">
      <div><dt>On site</dt><dd>A pool and a deck, a sauna indoors and a barrel sauna out in the olive grove, a gym, an indoor studio for the morning it rains, a lounge, a full kitchen, and outdoor dining under vine.</dd></div>
      <div><dt>Grounds</dt><dd>Olive, palm and stone paths, a lawn with an old stone oven on it, and the circular deck the mornings happen on. The village is on the other side of the wall.</dd></div>
    </dl>
    <p class="gr-credit">Photography by Armonia Retreat Center.</p>
  </div>
</section>

<section class="hv-sec" id="hosts" aria-labelledby="gr-hosts">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Who is running it</span>
      <h2 class="hv-h2" id="gr-hosts">Two of us, and <em>neither of us is a guru.</em></h2>
    </div>
    <div class="gt-hosts">
      <article class="gt-host">
        <figure class="au-photo"><img src="%(R)scydnie-greece-600.webp" srcset="%(R)scydnie-greece-600.webp 600w, %(R)scydnie-greece-1000.webp 1000w" sizes="(min-width: 60rem) 16rem, 60vw" width="1000" height="1407" alt="Cydnie Jocelyn, standing, hands together, in a white shirt against a warm wall." loading="lazy"></figure>
        <div><h3>Cydnie Jocelyn</h3><p class="gt-role">Host &middot; Brand and business strategist</p>
          <p>Fourteen years in corporate marketing, then a retreat that turned out to be the thing that ended that chapter. I left, I got baptised, and I built this out of obedience rather than a plan. Here I am the person who booked the property, chose the village, and will make sure the week actually works, so that nobody in the room has to be the one holding it. The longer version is on the <a class="hv-inline" href="/about/">About page</a>.</p></div>
      </article>
      <article class="gt-host">
        <figure class="au-photo"><img src="%(R)skris-600.webp" srcset="%(R)skris-600.webp 600w, %(R)skris-1000.webp 1000w" sizes="(min-width: 60rem) 16rem, 60vw" width="1000" height="1500" alt="Kris Krause outdoors in a Your Time Fitness vest, looking off to one side." loading="lazy"></figure>
        <div><h3>Kris Krause</h3><p class="gt-role">Movement &middot; Your Time Fitness, Minnesota</p>
          <p>Fifteen years working with women on strength and mobility, mostly women who had written off both. She was diagnosed with rheumatoid arthritis in her twenties and built her practice around what she learned doing it. She leads the morning movement in Crete, and she meets you where your body is that morning, which on day four is a different place than it was on day one.</p></div>
      </article>
    </div>
  </div>
</section>

<section class="hv-sec gt-house" id="included" aria-labelledby="gr-inc">
  <div class="hv-wrap au-row">
    <div>
      <span class="hv-label">What the price covers</span>
      <h2 class="hv-h2" id="gr-inc">Everything <em>once you land.</em></h2>
      <p class="gt-not">Your flight is the only thing you book yourself, and I will sit down with the routes with you once you have a seat. Airlines have not opened August 2027 schedules yet; when they do, budget $1,000 to $2,000 round trip from Minneapolis.</p>
      <p class="gt-not"><b>Not included:</b> airfare, travel insurance, and personal spending or anything outside the schedule.</p>
    </div>
    <ul class="au-facts gt-inc" role="list">
      <li>Seven nights at Armonia, shared room, en-suite</li>
      <li>Breakfast, lunch and dinner, every day</li>
      <li>Daily movement sessions with Kris</li>
      <li>All group sessions and excursions</li>
      <li>Pool and sauna, all week</li>
      <li>Round trip ground transport from CHQ</li>
    </ul>
  </div>
</section>

<!-- BEFORE THE NUMBER: her four objections, kept, because they are the
     conversion work on this page. -->
<section class="hv-sec" aria-labelledby="gr-stop">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Before the number</span>
      <h2 class="hv-h2" id="gr-stop">What is actually <em>stopping you.</em></h2>
      <p class="hv-lede">Four things women say to me before they book. All four are reasonable.</p>
    </div>
    <ul class="ww-profiles gr-objs" role="list">
      <li><h3>&ldquo;I cannot be away that long.&rdquo;</h3><p>Eight days once, against the fifty-one weeks you spend being the one everything runs through. The week is built so that nothing needs you in it.</p></li>
      <li><h3>&ldquo;I would not know anyone.&rdquo;</h3><p>Most women come alone. That is the normal way to do this, and fifteen is small enough that by the second day you are not on the edge of anything.</p></li>
      <li><h3>&ldquo;I am not fit enough for it.&rdquo;</h3><p>There is nothing to be fit enough for. Kris designs the movement around who is in the room. If stairs and hills are a real concern, tell me before you book.</p></li>
      <li><h3>&ldquo;It is a lot of money.&rdquo;</h3><p>It is, and the figure is below rather than after a call. What you are actually buying is eight days in which nobody needs anything from you.</p></li>
    </ul>
  </div>
</section>

<section class="hv-sec gt-words" aria-labelledby="gr-words">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Costa Rica, April 2026</span>
      <h2 class="hv-h2" id="gr-words">What the last group <em>said.</em></h2>
    </div>
    <div class="rx-proof">
      <figure class="au-vid rx-vid">
        <a class="rt-play melissa-play" data-video="DrrP4hdw0lo" data-src="../../assets/video/melissa.mp4" data-start="3" data-title="Melissa on the Costa Rica retreat" href="../../assets/video/melissa.mp4#t=3">
          <img src="%(R)smelissa-poster-405.webp" srcset="%(R)smelissa-poster-300.webp 300w, %(R)smelissa-poster-405.webp 405w" sizes="(min-width: 60rem) 20rem, 74vw" width="405" height="720" loading="lazy" decoding="async" alt="Melissa, speaking to her phone camera in her car on the way home from the retreat.">
          <span class="au-play" aria-hidden="true"><svg width="18" height="20" viewBox="0 0 18 20" fill="currentColor"><path d="M0 0l18 10L0 20z"/></svg></span>
          <span class="hv-vh">Play Melissa&rsquo;s video about the Costa Rica retreat</span></a>
        <figcaption><b>&ldquo;I learned that I matter too.&rdquo;</b> Melissa, on the drive home from Costa Rica.</figcaption>
      </figure>
      <div class="hv-slides" data-slides aria-roledescription="carousel" aria-label="What guests said">
        <div class="hv-slides-track" aria-live="off">
          %(S1)s
          %(S2)s
          %(S3)s
          %(S4)s
        </div>
        <div class="hv-slides-nav" hidden>
          <button type="button" class="hv-slides-prev" aria-label="Previous review"><svg viewBox="0 0 16 10" fill="none" aria-hidden="true"><path d="M5 1L1 5l4 4M1 5h15" stroke="currentColor" stroke-width="1.2"/></svg></button>
          <div class="hv-slides-dots" role="group" aria-label="Choose a review"></div>
          <button type="button" class="hv-slides-next" aria-label="Next review"><svg viewBox="0 0 16 10" fill="none" aria-hidden="true"><path d="M11 1l4 4-4 4M15 5H0" stroke="currentColor" stroke-width="1.2"/></svg></button>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- THE SEAT: the price anyway, the two waitlist records, the terms, and
     Gatlinburg for anyone who will not wait. -->
<section class="hv-sec ww-standards gt-book" id="seat" aria-labelledby="gr-seat">
  <div class="hv-wrap gt-book-grid">
    <div>
      <span class="hv-label">Full &middot; Waitlist open</span>
      <h2 class="hv-h2" id="gr-seat">All fifteen seats <em>are taken.</em></h2>
      <p class="sd-truth-copy">The price is here anyway, because you should be able to see what a thing costs before you decide whether to wait for it. Choose how you would pay and you go on the list. When a seat opens I call the list in order.</p>
      <dl class="gt-legs gr-terms">
        <div><dt>Deposit</dt><dd>$500 holds your seat. It comes off the total, and it is not refundable.</dd></div>
        <div><dt>Balance</dt><dd>Pay in full, or six monthly payments. If neither works, tell me and we will talk about it.</dd></div>
        <div><dt>Travel insurance</dt><dd>Buy it the day you book. Your deposit and your flights are both committed early.</dd></div>
      </dl>
    </div>
    <div class="gt-picks">
      <div class="gt-pick"><p class="gt-pick-name">The seat &middot; shared room, twin beds, private bathroom</p><p class="gt-pick-price">$3,450</p>
        <div class="gt-pick-cta gr-pick-cta">
          <a class="hv-btn rx-btn-light" href="%(WAIT_FULL_FORM)s" data-cta="greece-wait-full">Waitlist, paying in full<span class="hv-vh"> (opens my scheduling page)</span></a>
          <a class="hv-btn rx-btn-light" href="%(WAIT_PLAN)s" data-cta="greece-wait-plan">Waitlist, six month plan<span class="hv-vh"> (opens my scheduling page)</span></a>
        </div></div>
      <p class="gt-pick-note">No payment is taken to join the list. Picking a plan only tells me how you would pay if a seat comes up, and it is the same list either way.</p>
      <div class="gr-alt"><p><b>Not willing to wait on a seat?</b> Gatlinburg is open: five days in the Smokies, 13 to 18 April 2027, booking now.</p><a class="gt-full" href="/retreats/gatlinburg/" data-cta="greece-seat-gatlinburg">See Gatlinburg</a></div>
    </div>
  </div>
</section>

<section class="hv-sec" id="faq" aria-labelledby="faq-h">
  <div class="hv-wrap hv-faq ww-faq">
    <div>
      <span class="hv-label">Before you ask</span>
      <h2 class="hv-h2" id="faq-h">The practical <em>answers.</em></h2>
      <p class="hv-lede">If yours is the quieter question, about the money, or the flight, or whether you would be the wrong person in that room, send it. I answer it myself, usually the same day.</p>
      <div class="gt-list"><a class="hv-link" href="%(QUESTION)s">Send a question<span class="hv-vh"> (opens my scheduling page)</span></a></div>
    </div>
    <div class="hv-faq-list">
%(FAQ)s
    </div>
  </div>
</section>

</main>
""" % {
    "ARW": ARW, "G": G, "R": R, "GALLERY": GALLERY, "WAIT_FULL_FORM": WAIT_FULL_FORM, "WAIT_PLAN": WAIT_PLAN,
    "QUESTION": QUESTION, "FAQ": L.faq_html(FAQ),
    "S1": S("I walked in carrying fear that the experience would take more from me than I had to give. I left being able to breathe, with old and new friends who cared about me.", "BJB"),
    "S2": S("If you are weary from life and want to reset and refresh yourself, take a chance on an experience that will not disappoint you if you attend with open hands and heart.", "Carol"),
    "S3": S("I was burnt out and struggling to figure out why I always felt behind. My need to be perfect and always reliable had become the reason I failed to show up for myself when I needed it the most.", "Kristi"),
    "S4": S("The friends you meet will be there for you if you are willing to reach out and share yourself. Costa Rica will remain in my heart forever.", "BJB"),
}

graph = L.old_graph("retreats/greece/index.html")
for n in graph:
    if n.get("@type") == "FAQPage":
        n.update(L.faq_node(URL, FAQ))

PRELOAD = ('<link rel="preload" as="image" href="%shouse-1200.webp" imagesrcset="%shouse-600.webp 600w, '
           '%shouse-900.webp 900w, %shouse-1200.webp 1200w" imagesizes="(min-width: 64rem) 30rem, 90vw" '
           'type="image/webp" fetchpriority="high">\n') % (G, G, G, G)

n = L.render(
    out="retreats/greece/index.html", depth=2, active="/retreats/",
    title="Rise Into Her: The Greece Edition | Crete, August 2027",
    description="Rise Into Her: eight days at Armonia Retreat Center, Douliana, Crete, 13 to 20 August 2027. Fifteen women, all seats taken, waitlist open.",
    canonical=URL,
    og_title="Rise Into Her: The Greece Edition | Crete, August 2027",
    og_description="Eight days in a hillside village in western Crete, for fifteen women. All seats taken; the waitlist is open.",
    graph=graph, main=MAIN, preload=PRELOAD, body_class="ww-page",
    og_image=L.SITE + "/assets/img/greece/house-1200.webp",
    reveal=(".ww-head", ".au-row > div", ".gt-days > li", ".gt-nums > div", ".gt-legs > div", ".gr-stats > div",
            ".gt-host", ".gr-objs > li", ".hv-slides", ".gt-book-grid > div"),
    reveal_imgs=(".gt-deck",),
)
print("written", n)
