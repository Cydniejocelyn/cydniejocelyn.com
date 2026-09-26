"""Wide Open: The Gatlinburg Edition (/retreats/gatlinburg/), rebuilt 25
September 2026 on the luxury system. THIS PAGE IS LIVE AND TAKING BOOKINGS.

Nothing a guest pays against has changed: both room prices, the early rate
and its deadline (31 October 2026; $2,900 / $1,600 from 1 November), the
$500 hold, the five monthly payments, and all four HoneyBook links are the
same records the live page uses. Kept: every fact on the old page, the 24
photograph gallery (verbatim, tools/gatlinburg_gallery.html), the three park
figures (checkable, sourced in the old page's notes), both host bios, the
countdown to the real deadline (site.js [data-countdown]). Cut: the water
lines ("You are not lacking anything. You are under something"; "Come up
for air in the Smokies"). Order changed for conversion: rooms and prices
come right after the week, the guests' words sit beside the booking.

    cd tools && python3 gen_gatlinburg.py
"""
import lux_page as L

URL = L.SITE + "/retreats/gatlinburg/"
ARW = L.ARW
HB = "https://clients.cydniejocelyn.com/public/"
KING_HOLD, KING_FULL = HB + "private5monthpymtgatlinburg", HB + "gatlinburgpymtfullprivate"
SHARED_HOLD, SHARED_FULL = HB + "gatlinburgsharedroom5monthspymtplan", HB + "gatlinburgsharedpymtfull"
LIST = "https://www.honeybook.com/widget/cydnie_jocelyn_collective_299013/cf_id/69fa3c69e63a7a4c9bb354f1"
IMG = "../../assets/img/gatlinburg/"
GALLERY = open(__import__("os").path.join(L.ROOT, "tools", "gatlinburg_gallery.html"), encoding="utf-8").read()

FAQ = [
    ("Do I need to know anyone going?", "No. Most women come on their own. That is the normal way to arrive at one of these."),
    ("Can I come with a friend?", "Yes, and plenty of women do. The shared room is the natural fit if you are coming as a pair, and you each book it separately."),
    ("What is the difference between the two rooms?", "The king suite is yours alone, with your own bathroom and balcony. The shared room is bunk style with other guests. Everything else about the five days is identical."),
    ("What if I do not want to do the movement?", "Then do not. It is on the schedule every morning and it is optional every morning."),
    ("What happens after I book?", "You choose your room and how you want to pay. $500 holds it either way. Your invoice, payment terms and contract arrive by email, and from there Cydnie handles the details until you land in Knoxville."),
    ("What is the cancellation policy?", "It is in your contract, and you see it before you pay anything. The contract is where those terms are binding, so that is where they live."),
]

S = lambda quote, who, where: (
    '<figure class="hv-slide" data-slide><blockquote><p>&ldquo;%s&rdquo;</p></blockquote>'
    '<figcaption>%s &middot; %s</figcaption></figure>' % (quote, who, where))

def room(name, price, later, bullets, hold, full, img, alt, w, h):
    lis = "".join("<li>%s</li>" % b for b in bullets)
    return """<article class="gt-room">
        <figure><img src="%(img)s-1000.webp" srcset="%(img)s-600.webp 600w, %(img)s-1000.webp 1000w" sizes="(min-width: 60rem) 36rem, 92vw" width="%(w)s" height="%(h)s" alt="%(alt)s" loading="lazy"></figure>
        <div class="gt-room-body">
          <h3>%(name)s</h3>
          <p class="gt-room-price"><b>%(price)s</b><span>%(later)s</span></p>
          <ul role="list">%(lis)s</ul>
          <div class="gt-room-cta">
            <a class="hv-btn hv-btn--ink" href="%(hold)s" data-cta="gatlinburg-hold">Hold my room, $500 %(arw)s<span class="hv-vh"> (opens my booking page)</span></a>
            <a class="hv-btn hv-btn--line" href="%(full)s" data-cta="gatlinburg-full">Pay in full<span class="hv-vh"> (opens my booking page)</span></a>
          </div>
          <p class="gt-room-note">$500 today holds it. The balance is five monthly payments, starting the month after.</p>
        </div>
      </article>""" % dict(name=name, price=price, later=later, lis=lis, hold=hold, full=full, img=IMG + img, alt=alt, w=w, h=h, arw=ARW)

KING = room("Private king suite", "$2,790", "Early rate through 31 October 2026, then $2,900.",
            ["A king bed, and the room is yours alone", "Your own bathroom", "A private balcony facing the mountains"],
            KING_HOLD, KING_FULL, "king-suite",
            "A four poster king bed with white linen, facing glass doors onto a private balcony with the mountains beyond.", 1000, 680)
SHARED = room("Shared room", "$1,490", "Early rate through 31 October 2026, then $1,600.",
              ["Bunk style, shared with other guests", "Bathrooms throughout the house, never a wait", "The natural fit if you are coming with a friend"],
              SHARED_HOLD, SHARED_FULL, "bunk-room",
              "A bunk room with white metal bunk beds made up in white and grey linen, under a pine ceiling.", 1000, 680)

MAIN = """<main id="main">

<section class="ww-hero" aria-labelledby="gt-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <span class="hv-label">Wide Open &middot; The Gatlinburg Edition</span>
      <h1 id="gt-h">Five days in <em>the Smokies.</em></h1>
      <p class="hv-lede">A small-group retreat for women, in a private house at the edge of the national park. You land in Knoxville and somebody is already waiting on you. Everything after that is handled.</p>
      <div class="hv-btns">
        <a class="hv-btn hv-btn--ink" href="#rooms" data-cta="gatlinburg-hero-rooms">Choose your room %(ARW)s</a>
        <a class="hv-btn hv-btn--line" href="#week">See the week</a>
      </div>
      <dl class="gt-facts">
        <div><dt>Dates</dt><dd>13&ndash;18 April 2027</dd></div>
        <div><dt>Where</dt><dd>Gatlinburg, Tennessee</dd></div>
        <div><dt>Group</dt><dd>Fifteen women</dd></div>
        <div><dt>With</dt><dd>Cydnie and Kayla</dd></div>
        <div><dt>From</dt><dd>$1,490</dd></div>
        <div><dt>To hold a room</dt><dd>$500</dd></div>
      </dl>
    </div>
    <figure class="ww-arch">
      <img src="%(IMG)shouse-dusk-portrait-834.webp" srcset="%(IMG)shouse-dusk-portrait-600.webp 600w, %(IMG)shouse-dusk-portrait-834.webp 834w" sizes="(min-width: 64rem) 30rem, 90vw" width="834" height="1112" alt="A timber house on a wooded slope at dusk, its windows lit, with the ridgeline of the Smoky Mountains behind it." fetchpriority="high">
      <figcaption><span>Early rate through</span><b>31 October</b></figcaption>
    </figure>
  </div>
</section>

<section class="hv-proof rx-proofstrip" aria-label="What a guest said">
  <div class="hv-wrap rx-proofstrip-in">
    <span class="hv-label">The last retreat &middot; Costa Rica</span>
    <blockquote>&ldquo;The fact that you&rsquo;re even considering it should tell you that you should go.&rdquo;<cite>Kristi, retreat guest</cite></blockquote>
    <blockquote>&ldquo;I left being able to breathe, with old and new friends who cared about me.&rdquo;<cite>BJB, retreat guest</cite></blockquote>
  </div>
</section>

<!-- WHY, beside the deck. Her paragraph, without the water line. -->
<section class="hv-sec" aria-labelledby="gt-why">
  <div class="hv-wrap au-row">
    <figure class="rx-wide gt-deck"><img src="%(IMG)sdeck-view-1200.webp" srcset="%(IMG)sdeck-view-600.webp 600w, %(IMG)sdeck-view-1200.webp 1200w, %(IMG)sdeck-view-1654.webp 1654w" sizes="(min-width: 60rem) 30rem, 92vw" width="1200" height="807" alt="A covered deck with a long table and rocking chairs, looking across bare spring woodland to the mountains." loading="lazy"><figcaption>The deck, and what it looks at.</figcaption></figure>
    <div>
      <span class="hv-label">Why this exists</span>
      <h2 class="hv-h2" id="gt-why">Room to <em>set it down.</em></h2>
      <p class="hv-lede">Five days will not remove the weight. It gets you out from under it long enough to look at it straight, next to women who will not need you to explain yourself first.</p>
    </div>
  </div>
</section>

<!-- THE FIVE DAYS: her five lines. -->
<section class="hv-sec ww-path gt-week" id="week" aria-labelledby="gt-week">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">The five days</span>
      <h2 class="hv-h2" id="gt-week">Full enough to matter. <em>Thin enough to breathe.</em></h2>
    </div>
    <ol class="ww-steps gt-days" role="list">
      <li><h3>Movement</h3><p>Every morning starts with movement, led by Kayla. Optional every morning, and nobody is counting who came.</p></li>
      <li><h3>Two workshops</h3><p>In the house, led by Cydnie and Kayla together. Goal setting is one of them. Nothing to prepare.</p></li>
      <li><h3>Two outings</h3><p>Twice in the week you leave the property. Getting there and back is arranged and inside the price.</p></li>
      <li><h3>Open time</h3><p>Long stretches with nothing on them. On purpose. The porch, the town, or sleep.</p></li>
      <li><h3>Every meal</h3><p>Included and eaten together. Except Friday dinner, which is out and on your own.</p></li>
    </ol>
  </div>
</section>

<!-- THE HOUSE AND THE ROOMS: prices, both booking links per room, then the
     gallery. The four HoneyBook links are the live records. -->
<section class="hv-sec gt-house" id="rooms" aria-labelledby="gt-house">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Where you stay</span>
      <h2 class="hv-h2" id="gt-house">A private house, and <em>all of it is ours.</em></h2>
      <p class="hv-lede">Fifteen women, one house. You sleep, eat, move and do both workshops here, with two hot tubs that belong to the house and a deck facing the mountains.</p>
      <p class="gt-rate"><span>Early rate through 31 October</span> <b data-daysleft="2026-11-01T00:00:00-05:00" hidden></b></p>
    </div>
    <div class="gt-rooms">
      %(KING)s
      %(SHARED)s
    </div>
    %(GALLERY)s
  </div>
</section>

<section class="hv-sec" id="included" aria-labelledby="gt-inc">
  <div class="hv-wrap au-row">
    <div>
      <span class="hv-label">What the price covers</span>
      <h2 class="hv-h2" id="gt-inc">You land. <em>We handle the rest.</em></h2>
      <p class="gt-not"><b>Not included:</b> your flight into Knoxville (running $400 to $600 right now), the one dinner out, alcohol, travel insurance, and anything you buy in town.</p>
    </div>
    <ul class="au-facts gt-inc" role="list">
      <li>Five nights in the room you choose</li>
      <li>Every meal but one dinner</li>
      <li>Movement every morning</li>
      <li>Both workshops</li>
      <li>Two outings, with the transport</li>
      <li>Airport shuttles both ways</li>
      <li>Two private hot tubs</li>
      <li>The resort gym</li>
    </ul>
  </div>
</section>

<!-- WHERE YOU ARE. Checkable figures (see the old page's notes): 12 million
     recreation visits in 2024, 848 miles of trail, about 71 miles of the
     Appalachian Trail inside the park. data-count animates them; the markup
     holds the real figure. -->
<section class="hv-sec ww-standards gt-place" id="place" aria-labelledby="gt-place">
  <div class="hv-wrap">
    <span class="hv-label">Where you are</span>
    <h2 class="hv-h2" id="gt-place">Gatlinburg, at the front door of <em>the Smoky Mountains.</em></h2>
    <p class="sd-truth-copy">The most visited national park in the country, and in April the wildflowers are coming up.</p>
    <div class="gt-nums">
      <div><b><span data-count="12">12</span><small>m</small></b><span>Visits to the park in 2024</span></div>
      <div><b><span data-count="848">848</span></b><span>Miles of trail</span></div>
      <div><b><span data-count="71">71</span></b><span>Miles of the Appalachian Trail</span></div>
    </div>
    <dl class="gt-legs">
      <div><dt>Getting there</dt><dd>Fly into Knoxville (TYS), about an hour out. Cydnie arranges the shuttles both ways, and you will know who is on your flight before you board.</dd></div>
      <div><dt>Getting around</dt><dd>Both outings are driven. The rest of the week, the town trolley is a fifteen minute walk from the house.</dd></div>
      <div><dt>April weather</dt><dd>Days in the 60s and low 70s, nights in the 40s, colder on the trails. Pack layers.</dd></div>
    </dl>
  </div>
</section>

<section class="hv-sec" id="hosts" aria-labelledby="gt-hosts">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Who you are with</span>
      <h2 class="hv-h2" id="gt-hosts">Two of us, and <em>neither of us is a guru.</em></h2>
    </div>
    <div class="gt-hosts">
      <article class="gt-host">
        <figure class="au-photo"><img src="%(IMG)skayla-600.webp" srcset="%(IMG)skayla-600.webp 600w, %(IMG)skayla-900.webp 900w" sizes="(min-width: 60rem) 16rem, 60vw" width="600" height="893" alt="Kayla Freeman, standing outdoors on a path, one hand in her pocket." loading="lazy"></figure>
        <div><h3>Kayla Freeman</h3><p class="gt-role">Movement &middot; Minnesota National Guard</p>
          <p>I&rsquo;m so excited to be co-hosting my very first women&rsquo;s retreat. I have served in the Minnesota National Guard for nearly 20 years and I&rsquo;m in my 13th year of active duty, which taught me a lot about resilience, balance and being intentional with self-care. I&rsquo;m a wife and a mom to two young kids, 6 and 4, so I know how easy it is to put yourself last. I lead the morning movement: realistic, sustainable, and no overhaul required.</p></div>
      </article>
      <article class="gt-host">
        <figure class="au-photo"><img src="../../assets/img/cydnie-window-600.webp" srcset="../../assets/img/cydnie-window-600.webp 600w, ../../assets/img/cydnie-window-1000.webp 1000w" sizes="(min-width: 60rem) 16rem, 60vw" width="600" height="900" alt="Cydnie Jocelyn, laughing by a window with her hand in her hair, in a white shirt." loading="lazy"></figure>
        <div><h3>Cydnie Jocelyn</h3><p class="gt-role">Host &middot; Forest Lake, Minnesota</p>
          <p>I went on a retreat before I ever ran one, and came home with my head clear for the first time in a long stretch. I&rsquo;m a wife and a mom, and a rare genetic mutation runs through my husband and both of my kids, so I know how fast a woman ends up last on her own list. These five days are for setting that down. The longer version is on the <a class="hv-inline" href="/about/">About page</a>.</p></div>
      </article>
    </div>
  </div>
</section>

<!-- THE GUESTS' WORDS beside Melissa, then straight into booking. -->
<section class="hv-sec gt-words" aria-labelledby="gt-words">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">The last retreat, Costa Rica</span>
      <h2 class="hv-h2" id="gt-words">In <em>their words.</em></h2>
    </div>
    <div class="rx-proof">
      <figure class="au-vid rx-vid">
        <a class="rt-play melissa-play" data-video="DrrP4hdw0lo" data-src="../../assets/video/melissa.mp4" data-start="3" data-title="Melissa on the Costa Rica retreat" href="../../assets/video/melissa.mp4#t=3">
          <img src="../../assets/img/retreats/melissa-poster-405.webp" srcset="../../assets/img/retreats/melissa-poster-300.webp 300w, ../../assets/img/retreats/melissa-poster-405.webp 405w" sizes="(min-width: 60rem) 20rem, 74vw" width="405" height="720" loading="lazy" decoding="async" alt="Melissa, speaking to her phone camera in her car on the way home from the retreat.">
          <span class="au-play" aria-hidden="true"><svg width="18" height="20" viewBox="0 0 18 20" fill="currentColor"><path d="M0 0l18 10L0 20z"/></svg></span>
          <span class="hv-vh">Play Melissa&rsquo;s video about the Costa Rica retreat</span></a>
        <figcaption><b>&ldquo;I learned that I matter too.&rdquo;</b> Melissa, on the drive home from Costa Rica. Three minutes, filmed on her phone.</figcaption>
      </figure>
      <div class="hv-slides" data-slides aria-roledescription="carousel" aria-label="What guests said">
        <div class="hv-slides-track" aria-live="off">
          %(S1)s
          %(S2)s
          %(S3)s
          %(S4)s
          %(S5)s
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

<!-- BOOKING: the countdown to the real early-rate deadline, and both rooms
     with both links. -->
<section class="hv-sec ww-standards gt-book" id="booking" aria-labelledby="gt-book">
  <div class="hv-wrap gt-book-grid">
    <div>
      <span class="hv-label">13 to 18 April 2027 &middot; Gatlinburg</span>
      <h2 class="hv-h2" id="gt-book">Five days to <em>breathe in the Smokies.</em></h2>
      <p class="sd-truth-copy">Fifteen women. $500 holds your room today, and the balance is five monthly payments starting the month after. Or pay in full.</p>
      <div class="gt-count" data-countdown="2026-11-01T00:00:00-05:00" hidden>
        <p class="gt-count-label">The early rate ends in</p>
        <div class="gt-count-cells" role="timer" aria-live="off">
          <span><b data-unit="d">00</b><i>Days</i></span>
          <span><b data-unit="h">00</b><i>Hours</i></span>
          <span><b data-unit="m">00</b><i>Minutes</i></span>
          <span><b data-unit="s">00</b><i>Seconds</i></span>
        </div>
      </div>
      <p class="gt-rate-line">The early rate holds through 31 October 2026. From 1 November the rooms are $2,900 and $1,600.</p>
    </div>
    <div class="gt-picks">
      <div class="gt-pick"><p class="gt-pick-name">Private king suite</p><p class="gt-pick-price">$2,790</p>
        <div class="gt-pick-cta"><a class="hv-btn rx-btn-light" href="%(KING_HOLD)s" data-cta="gatlinburg-book-king-hold">Hold my room, $500<span class="hv-vh"> (opens my booking page)</span></a><a class="gt-full" href="%(KING_FULL)s" data-cta="gatlinburg-book-king-full">Pay in full<span class="hv-vh"> (opens my booking page)</span></a></div></div>
      <div class="gt-pick"><p class="gt-pick-name">Shared room</p><p class="gt-pick-price">$1,490</p>
        <div class="gt-pick-cta"><a class="hv-btn rx-btn-light" href="%(SHARED_HOLD)s" data-cta="gatlinburg-book-shared-hold">Hold my room, $500<span class="hv-vh"> (opens my booking page)</span></a><a class="gt-full" href="%(SHARED_FULL)s" data-cta="gatlinburg-book-shared-full">Pay in full<span class="hv-vh"> (opens my booking page)</span></a></div></div>
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
      <div class="gt-list"><p><b>Not ready to decide?</b> Join the Gatlinburg list. No payment, and nothing is held against you if you never book.</p><a class="hv-link" href="%(LIST)s">Join the list<span class="hv-vh"> (opens a short form)</span></a></div>
    </div>
    <div class="hv-faq-list">
%(FAQ)s
    </div>
  </div>
</section>

</main>
""" % {
    "ARW": ARW, "IMG": IMG, "KING": KING, "SHARED": SHARED, "GALLERY": GALLERY.strip(), "LIST": LIST,
    "KING_HOLD": KING_HOLD, "KING_FULL": KING_FULL, "SHARED_HOLD": SHARED_HOLD, "SHARED_FULL": SHARED_FULL,
    "FAQ": L.faq_html(FAQ),
    "S1": S("I was burnt out and struggling to figure out why I always felt behind. My need to be perfect and always reliable had become the reason I failed to show up for myself when I needed it the most.", "Kristi", "Retreat guest, Costa Rica"),
    "S2": S("Intimate group size, and leaders able to make us think, laugh and cry without judgement. No waiting, no rushing.", "Carol", "Retreat guest, Costa Rica"),
    "S3": S("If you are weary from life and want to reset and refresh yourself, take a chance on an experience that will not disappoint you if you attend with open hands and heart.", "Carol", "Retreat guest, Costa Rica"),
    "S4": S("The friends you meet will be there for you if you are willing to reach out and share yourself. Costa Rica will remain in my heart forever.", "BJB", "Retreat guest, Costa Rica"),
    "S5": S("It greatly surpassed all my expectations. My only regret was that I did not pack more swim suits.", "Alice", "Retreat guest, Costa Rica"),
}

graph = L.old_graph("retreats/gatlinburg/index.html")

PRELOAD = ('<link rel="preload" as="image" href="%shouse-dusk-portrait-834.webp" '
           'imagesrcset="%shouse-dusk-portrait-600.webp 600w, %shouse-dusk-portrait-834.webp 834w" '
           'imagesizes="(min-width: 64rem) 30rem, 90vw" type="image/webp" fetchpriority="high">\n') % (IMG, IMG, IMG)

n = L.render(
    out="retreats/gatlinburg/index.html", depth=2, active="/retreats/",
    title="Wide Open: The Gatlinburg Edition | Tennessee, April 2027",
    description="Wide Open: five days in Gatlinburg, Tennessee, 13 to 18 April 2027. Lodging, every meal, daily movement, two workshops and two outings included.",
    canonical=URL,
    og_title="Wide Open: The Gatlinburg Edition | April 2027",
    og_description="Five days in a private house in the Smokies, for fifteen women. From $1,490; $500 holds your room.",
    graph=graph, main=MAIN, preload=PRELOAD, body_class="ww-page",
    og_image=L.SITE + "/assets/img/gatlinburg/house-dusk-1200.webp",
    reveal=(".ww-head", ".au-row > div", ".gt-days > li", ".gt-room", ".gt-inc", ".gt-nums > div", ".gt-legs > div",
            ".gt-host", ".hv-slides", ".gt-book-grid > div"),
    reveal_imgs=(".gt-deck",),
)
print("written", n)
