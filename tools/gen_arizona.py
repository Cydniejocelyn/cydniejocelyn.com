"""Wild Canvas: The Arizona Edition (/retreats/arizona/), rebuilt 25 September
2026 on the luxury system.

LIVE BUT HIDDEN until Cydnie says launch (HANDOFF 68): two robots tags, a
commented canonical and the parked Event JSON-LD, all in the exact form
tools/launch_arizona.py matches. This generator reads the page it is about
to overwrite: if the launch has already run (the noindex tag is gone), it
writes the launched head instead, so re-running it can never re-hide the
page. The parked block is kept verbatim in tools/arizona_parked_jsonld.html.

Every price and link is the live page's: $1,675 early rate through 30
November 2026, $1,800 from 1 December, $500 hold, five monthly payments, the
two HoneyBook records (6ab58825... hold, 6ab58836... pay in full) and the
list (cf_id/69fa3c69...). Photographs: never the LUXE AURA wall frames or
the street view; they name the house (HANDOFF 68).

    cd tools && python3 gen_arizona.py
"""
import os
import lux_page as L

URL = L.SITE + "/retreats/arizona/"
ARW = L.ARW
HOLD = "https://clients.cydniejocelyn.com/public/6ab58825015882f2ae403595"
FULL = "https://clients.cydniejocelyn.com/public/6ab588362524c9043b35b461"
LIST = "https://www.honeybook.com/widget/cydnie_jocelyn_collective_299013/cf_id/69fa3c69e63a7a4c9bb354f1"
A = "../../assets/img/arizona/"
R = "../../assets/img/retreats/"
GALLERY = open(os.path.join(L.ROOT, "tools", "arizona_gallery.html"), encoding="utf-8").read().strip()
PARKED = open(os.path.join(L.ROOT, "tools", "arizona_parked_jsonld.html"), encoding="utf-8").read()

_current = open(os.path.join(L.ROOT, "retreats", "arizona", "index.html"), encoding="utf-8").read()
LAUNCHED = '<meta name="robots" content="noindex, nofollow, noarchive">' not in _current

FAQ = [
    ("Do I need any art experience?", "None. Every session is built so anyone can begin. If you have never called yourself an artist, you are exactly who this is for."),
    ("Do I need to know anyone going?", "No. Most women come on their own. That is the normal way to arrive at one of these."),
    ("Can I come with a friend?", "Yes. Every room is shared by two, so coming as a pair is easy. You each book separately."),
    ("When should I land?", "By 3 pm on 5 May, so the shuttles can be grouped. Book your flight into PHX with that in mind."),
    ("Do I bring my own supplies?", "No. Every art supply you need is included and waiting for you. Bring yourself."),
    ("What happens after I book?", "$500 holds your room, or you pay in full. Your invoice, payment terms and contract arrive by email, and from there Cydnie handles the details until you land in Phoenix."),
    ("What is the cancellation policy?", "It is in your contract, and you see it before you pay anything."),
]

S = lambda quote, who: ('<figure class="hv-slide" data-slide><blockquote><p>&ldquo;%s&rdquo;</p></blockquote>'
                        '<figcaption>%s &middot; Retreat guest, Costa Rica</figcaption></figure>' % (quote, who))

MAIN = """<main id="main">

<section class="ww-hero" aria-labelledby="az-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <span class="hv-label">Wild Canvas &middot; The Arizona Edition</span>
      <h1 id="az-h">Five days in the desert, <em>making something of your own.</em></h1>
      <p class="hv-lede">A small creative retreat for women, led by abstract artist Dr. Clarissa Castillo-Ramsey. You land in Phoenix and somebody is already waiting on you. Everything after that is handled. No art experience needed.</p>
      <div class="hv-btns">
        <a class="hv-btn hv-btn--ink" href="#rooms" data-cta="arizona-hero-rooms">Hold your room for $500 %(ARW)s</a>
        <a class="hv-btn hv-btn--line" href="#week">See the week</a>
      </div>
      <dl class="gt-facts">
        <div><dt>Dates</dt><dd>5&ndash;9 May 2027</dd></div>
        <div><dt>Where</dt><dd>Peoria, Arizona</dd></div>
        <div><dt>Group</dt><dd>Nine women</dd></div>
        <div><dt>With</dt><dd>Clarissa and Cydnie</dd></div>
        <div><dt>From</dt><dd>$1,675</dd></div>
        <div><dt>To hold a room</dt><dd>$500</dd></div>
      </dl>
    </div>
    <figure class="ww-arch">
      <img src="%(A)stable-set-portrait-848.webp" srcset="%(A)stable-set-portrait-600.webp 600w, %(A)stable-set-portrait-848.webp 848w" sizes="(min-width: 64rem) 30rem, 90vw" width="848" height="1130" alt="A long table set for dinner under a covered patio at dusk, small bonsai trees down the middle." fetchpriority="high">
      <figcaption><span>Early rate through</span><b>30 November</b></figcaption>
    </figure>
  </div>
</section>

<section class="hv-proof rx-proofstrip" aria-label="What guests said">
  <div class="hv-wrap rx-proofstrip-in">
    <span class="hv-label">The last retreat &middot; Costa Rica</span>
    <blockquote>&ldquo;The fact that you&rsquo;re even considering it should tell you that you should go.&rdquo;<cite>Kristi, retreat guest</cite></blockquote>
    <blockquote>&ldquo;No waiting, no rushing.&rdquo;<cite>Carol, retreat guest</cite></blockquote>
  </div>
</section>

<section class="hv-sec" aria-labelledby="az-why">
  <div class="hv-wrap au-row">
    <figure class="rx-wide gt-deck"><img src="%(A)sclarissa-piece-1000.webp" srcset="%(A)sclarissa-piece-600.webp 600w, %(A)sclarissa-piece-1000.webp 1000w, %(A)sclarissa-piece-1450.webp 1450w" sizes="(min-width: 60rem) 30rem, 92vw" width="1000" height="667" alt="Clarissa holding one of her small paintings in front of her face. It reads: be happy, be bright." loading="lazy"><figcaption>Clarissa, and one of hers.</figcaption></figure>
    <div>
      <span class="hv-label">Why this exists</span>
      <h2 class="hv-h2" id="az-why">You did not stop being creative. <em>You stopped having room for it.</em></h2>
      <p class="hv-lede">We spend most of our lives thinking, planning, producing and responding. Five days will not change that. It gets you far enough from it to pick up a brush, or a pen, and find out what has been waiting underneath.</p>
      <p class="rx-format-copy">This is not a sip and paint. Nobody copies the same picture, and nobody is grading what you make.</p>
    </div>
  </div>
</section>

<!-- CLARISSA, and her line. -->
<section class="hv-sec ww-standards az-maker" aria-labelledby="az-maker">
  <div class="hv-wrap au-row">
    <div>
      <span class="hv-label">Who leads the making</span>
      <h2 class="hv-h2" id="az-maker">Dr. Clarissa <em>Castillo-Ramsey.</em></h2>
      <p class="sd-truth-copy">An internationally collected abstract artist, and the one guiding every session across the five days. Watercolor, ink, words and intuitive mark-making, built so anyone can begin.</p>
    </div>
    <blockquote class="az-say"><p>&ldquo;Wild does not have to mean loud. It can mean a little less edited. A little more curious. More willing to follow what wants to emerge than to worry about doing it right.&rdquo;</p><cite>Clarissa, on what Wild Canvas is for</cite></blockquote>
  </div>
</section>

<section class="hv-sec ww-path gt-week" id="week" aria-labelledby="az-week">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">The five days</span>
      <h2 class="hv-h2" id="az-week">Room to make. <em>Room to breathe.</em></h2>
    </div>
    <ol class="ww-steps gt-days" role="list">
      <li><h3>Guided sessions</h3><p>With Clarissa. Watercolor, ink, words and intuitive mark-making, built so anyone can begin.</p></li>
      <li><h3>Nothing to get right</h3><p>The point is the process of making, noticing and saying something you could not put into words. What you make comes home with you.</p></li>
      <li><h3>The desert</h3><p>Part of the material. Color, texture and light from the landscape find their way onto the page.</p></li>
      <li><h3>Every meal</h3><p>Included and eaten together. Homemade, and nobody has to plan it.</p></li>
      <li><h3>One or two more</h3><p>Workshops co-led by Cydnie and Clarissa, still in the works. Registered guests hear about them first.</p></li>
    </ol>
  </div>
</section>

<section class="hv-sec gt-house" id="rooms" aria-labelledby="az-house">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Where you stay</span>
      <h2 class="hv-h2" id="az-house">Nine women, <em>one house.</em></h2>
      <p class="hv-lede">You sleep, eat and make here. The house is painted top to bottom by hand, which is either a coincidence or the reason we booked it. Nine places. That is the whole retreat.</p>
      <p class="gt-rate"><span>Early rate through 30 November</span> <b data-daysleft="2026-12-01T00:00:00-07:00" hidden></b></p>
    </div>
    <article class="gt-room az-room">
      <figure><img src="%(A)sroom-moon-1000.webp" srcset="%(A)sroom-moon-600.webp 600w, %(A)sroom-moon-1000.webp 1000w, %(A)sroom-moon-1702.webp 1702w" sizes="(min-width: 60rem) 40rem, 92vw" width="1000" height="664" alt="A bedroom with two beds under a hand painted mural of purple mountains, saguaros and a full moon." loading="lazy"></figure>
      <div class="gt-room-body">
        <h3>Shared room</h3>
        <p class="gt-room-price"><b>$1,675 <s>$1,800</s></b><span>Early rate through 30 November 2026, then $1,800.</span></p>
        <ul role="list"><li>Two women to a room, with a king or queen bed</li><li>The natural fit if you are coming with a friend</li><li>Every art supply, every meal and both airport shuttles included</li></ul>
        <div class="gt-room-cta">
          <a class="hv-btn hv-btn--ink" href="%(HOLD)s" data-cta="arizona-hold">Hold my room, $500 %(ARW)s<span class="hv-vh"> (opens my booking page)</span></a>
          <a class="hv-btn hv-btn--line" href="%(FULL)s" data-cta="arizona-full">Pay in full<span class="hv-vh"> (opens my booking page)</span></a>
        </div>
        <p class="gt-room-note">$500 today holds it. The balance is five monthly payments, starting the month after.</p>
      </div>
    </article>
    %(GALLERY)s
    <div class="az-play">
      <figure><img src="%(A)sminigolf-1000.webp" srcset="%(A)sminigolf-600.webp 600w, %(A)sminigolf-1000.webp 1000w" sizes="(min-width: 60rem) 24rem, 92vw" width="1000" height="664" alt="A putting green on artificial turf with three flags, against a painted desert wall." loading="lazy"><figcaption>A putting green under the desert sky</figcaption></figure>
      <figure><img src="%(A)sbowling-1000.webp" srcset="%(A)sbowling-600.webp 600w, %(A)sbowling-1000.webp 1000w" sizes="(min-width: 60rem) 24rem, 92vw" width="1000" height="664" alt="A bowling lane laid on turf beside the garden wall at dusk, pins set and string lights above." loading="lazy"><figcaption>A lawn bowling lane, lit at dusk</figcaption></figure>
      <div><span class="hv-label">For the hours between sessions</span><p>Inside, a billiards room painted wall to wall, a wooden sauna for two and a small gym. The evenings belong to the pool, the hot tub and a long table under the string lights.</p></div>
    </div>
  </div>
</section>

<section class="hv-sec" id="included" aria-labelledby="az-inc">
  <div class="hv-wrap au-row">
    <div>
      <span class="hv-label">What the price covers</span>
      <h2 class="hv-h2" id="az-inc">You land. <em>We handle the rest.</em></h2>
      <p class="az-day"><b>$335 a day</b>with the room, every meal, every supply and both shuttles already in it.</p>
      <p class="gt-not"><b>Not included:</b> your flight into Phoenix (usually $200 to $500, depending on where you fly from) and travel insurance.</p>
    </div>
    <ul class="au-facts gt-inc" role="list">
      <li>Four nights in a shared room</li>
      <li>Every meal, arrival to departure</li>
      <li>Guided creative sessions with Clarissa</li>
      <li>Airport shuttles to and from PHX</li>
      <li>Every art supply you will need</li>
      <li>Everything you make, to take home</li>
    </ul>
  </div>
</section>

<section class="hv-sec ww-standards gt-place" aria-labelledby="az-place">
  <div class="hv-wrap">
    <span class="hv-label">Where you are</span>
    <h2 class="hv-h2" id="az-place">Peoria, on the edge of <em>the Sonoran desert.</em></h2>
    <dl class="gt-legs">
      <div><dt>Getting there</dt><dd>Fly into Phoenix Sky Harbor (PHX) on 5 May and land by 3 pm, so the shuttles can be grouped. You will know who is on your flight before you board.</dd></div>
      <div><dt>Getting home</dt><dd>Depart any time after 10 am on 9 May. Book the return flight with that in mind, and the shuttles are grouped the same way they were on the way in.</dd></div>
      <div><dt>May weather</dt><dd>Warm, dry and sunny. Days in the high 80s to low 90s, evenings in the 60s, and almost never rain. Pack light layers, a hat, sunscreen and a water bottle.</dd></div>
    </dl>
  </div>
</section>

<section class="hv-sec" id="hosts" aria-labelledby="az-hosts">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Who you are with</span>
      <h2 class="hv-h2" id="az-hosts">The artist, and <em>the one holding the details.</em></h2>
    </div>
    <div class="gt-hosts">
      <article class="gt-host">
        <figure class="au-photo"><img src="%(A)sclarissa-600.webp" srcset="%(A)sclarissa-600.webp 600w, %(A)sclarissa-1000.webp 1000w" sizes="(min-width: 60rem) 16rem, 60vw" width="600" height="750" alt="Clarissa Castillo-Ramsey at a table, pencil in hand, a blue abstract painting drying in front of her." loading="lazy"></figure>
        <div><h3>Dr. Clarissa Castillo-Ramsey</h3><p class="gt-role">Artist and guide &middot; Painting Your Path&trade;</p>
          <p>Clarissa&rsquo;s turning point came through spasmodic dysphonia, a condition that challenged her ability to speak just as she was building her creativity and coaching business. She turned it into a catalyst, and found art and wellness as tools for healing and self-expression.</p>
          <p>She is an international best-selling author, an award-winning transformational coach and an internationally collected abstract artist. Her programs, including The Creative Care Summit, Painting Your Path to Self-Expression and The Art of Becoming, have helped more than 5,000 creatives and professionals get their art into the world. Through her podcast, Painting Your Path&trade;, she helps women in midlife and beyond move past imposter syndrome, perfectionism and self-doubt, and back to their creativity.</p></div>
      </article>
      <article class="gt-host">
        <figure class="au-photo"><img src="../../assets/img/cydnie-writing-600.webp" srcset="../../assets/img/cydnie-writing-600.webp 600w, ../../assets/img/cydnie-writing-1000.webp 1000w" sizes="(min-width: 60rem) 16rem, 60vw" width="600" height="900" alt="Cydnie Jocelyn sitting with an open notebook on her lap, writing." loading="lazy"></figure>
        <div><h3>Cydnie Jocelyn</h3><p class="gt-role">Host &middot; Forest Lake, Minnesota</p>
          <p>I went on a retreat before I ever ran one, and came home with my head clear for the first time in a long stretch. I&rsquo;m a wife and a mom, and a rare genetic mutation runs through my husband and both of my kids, so I know how fast a woman ends up last on her own list. These five days are for making something that is only yours. The longer version is on the <a class="hv-inline" href="/about/">About page</a>.</p></div>
      </article>
    </div>
  </div>
</section>

<section class="hv-sec gt-words" aria-labelledby="az-words">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">The last retreat, Costa Rica</span>
      <h2 class="hv-h2" id="az-words">In <em>their words.</em></h2>
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

<section class="hv-sec ww-standards gt-book" id="booking" aria-labelledby="az-book">
  <div class="hv-wrap gt-book-grid">
    <div>
      <span class="hv-label">5&ndash;9 May 2027 &middot; Peoria</span>
      <h2 class="hv-h2" id="az-book">Come make something <em>in the desert.</em></h2>
      <p class="sd-truth-copy">Nine women, five days, and everything you make comes home with you. $500 holds your room today, and the balance is five monthly payments starting the month after. Or pay in full.</p>
      <p class="gt-rate-line">The early rate holds through 30 November 2026. From 1 December the room is $1,800.</p>
    </div>
    <div class="gt-picks">
      <div class="gt-pick"><p class="gt-pick-name">Shared room</p><p class="gt-pick-price">$1,675</p>
        <div class="gt-pick-cta"><a class="hv-btn rx-btn-light" href="%(HOLD)s" data-cta="arizona-book-hold">Hold my room, $500<span class="hv-vh"> (opens my booking page)</span></a><a class="gt-full" href="%(FULL)s" data-cta="arizona-book-full">Pay in full, $1,675<span class="hv-vh"> (opens my booking page)</span></a></div></div>
      <p class="gt-pick-note">Your invoice, payment terms and contract come straight to your inbox.</p>
    </div>
  </div>
</section>

<section class="hv-sec" id="faq" aria-labelledby="faq-h">
  <div class="hv-wrap hv-faq ww-faq">
    <div>
      <span class="hv-label">Before you book</span>
      <h2 class="hv-h2" id="faq-h">The practical <em>answers.</em></h2>
      <p class="hv-lede">Still sitting on something? <a class="hv-inline" href="/contact/">Ask me</a>, or email hello@cydniejocelyn.com. I would rather you booked knowing than booked hoping.</p>
      <div class="gt-list"><p><b>Not ready to decide?</b> Join the Wild Canvas list. No payment, and nothing is held against you if you never book.</p><a class="hv-link" href="%(LIST)s">Join the list<span class="hv-vh"> (opens a short form)</span></a></div>
    </div>
    <div class="hv-faq-list">
%(FAQ)s
    </div>
  </div>
</section>

</main>
""" % {
    "ARW": ARW, "A": A, "R": R, "GALLERY": GALLERY, "HOLD": HOLD, "FULL": FULL, "LIST": LIST, "FAQ": L.faq_html(FAQ),
    "S1": S("I walked in carrying fear that the experience would take more from me than I had to give. I left being able to breathe, with old and new friends who cared about me.", "BJB"),
    "S2": S("Intimate group size, and leaders able to make us think, laugh and cry without judgement. No waiting, no rushing.", "Carol"),
    "S3": S("If you are weary from life and want to reset and refresh yourself, take a chance on an experience that will not disappoint you if you attend with open hands and heart.", "Carol"),
}

# The graph is the WebPage only while hidden; the launch script adds the
# Event (with the Organization) from the parked block.
graph = [{
    "@type": "WebPage", "@id": URL + "#webpage", "url": URL,
    "name": "Wild Canvas: The Arizona Edition", "inLanguage": "en-US",
    "isPartOf": {"@id": L.SITE + "/#website"},
}]

if LAUNCHED:
    # the launch turned the parked Event on; keep it on every re-run, with
    # the organiser as the one LocalBusiness entity the Greece page carries
    import json, re
    event = json.loads(re.search(r"\n(\{\n  \"@context\".*?\n\})\n-->", PARKED, re.S).group(1))
    event.pop("@context", None)
    org = [n for n in L.old_graph("retreats/greece/index.html")
           if "LocalBusiness" in (n.get("@type") if isinstance(n.get("@type"), list) else [n.get("@type")])][0]
    event["organizer"] = {"@id": org["@id"]}
    graph = [org, event] + graph
    robots, canonical, extra = None, None, ""
else:
    robots = ('<meta name="robots" content="noindex, nofollow, noarchive">\n'
              '<meta name="googlebot" content="noindex, nofollow">')
    canonical = ('<!-- AT LAUNCH: uncomment the canonical.\n'
                 '<link rel="canonical" href="https://www.cydniejocelyn.com/retreats/arizona/">\n-->')
    extra = PARKED

PRELOAD = ('<link rel="preload" as="image" href="%stable-set-portrait-848.webp" imagesrcset="%stable-set-portrait-600.webp 600w, '
           '%stable-set-portrait-848.webp 848w" imagesizes="(min-width: 64rem) 30rem, 90vw" type="image/webp" '
           'fetchpriority="high">\n') % (A, A, A)

n = L.render(
    out="retreats/arizona/index.html", depth=2, active="/retreats/",
    title="Wild Canvas: The Arizona Edition | Peoria, May 2027",
    description="Wild Canvas: a creative retreat for women in Peoria, Arizona, 5 to 9 May 2027. Lodging, every meal, guided creative sessions with Dr. Clarissa Castillo-Ramsey and airport shuttles included. No art experience needed.",
    canonical=URL,
    og_title="Wild Canvas: The Arizona Edition | May 2027",
    og_description="Five days in the desert making something of your own, for nine women, with artist Dr. Clarissa Castillo-Ramsey. From $1,675.",
    graph=graph, main=MAIN, preload=PRELOAD, body_class="ww-page",
    og_image=L.SITE + "/assets/img/arizona/table-set-1000.webp",
    robots_html=robots, canonical_html=canonical, head_extra=extra,
    reveal=(".ww-head", ".au-row > div", ".gt-days > li", ".gt-room", ".gt-inc", ".gt-legs > div", ".gt-host",
            ".hv-slides", ".gt-book-grid > div", ".az-play > *"),
    reveal_imgs=(".gt-deck",),
)
print("written", n, "(launched)" if LAUNCHED else "(hidden: noindex, canonical and JSON-LD parked)")
