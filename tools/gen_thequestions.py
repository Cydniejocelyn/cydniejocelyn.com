"""The Questions (/thequestions/), restyled 26 September 2026.

The QR destination from the GATHER table (Erickson Farmstead, Isanti, MN;
was The Journey, Minneapolis until 21 October 2026). Her
answer of 26 September: restyle it, keep it. It stays noindex and out of
the sitemap, because it only makes sense to someone holding a card.

The twelve questions are verbatim and numbered 01 to 12 to match the cards.
The hero and "why" lines are hers. Changed: "Who's asking" speaks to
founders and leaders like the rest of the site (BRIDGE lines, mine), and
the ask is now the Letters first (a gentle next step for someone who has
just met her) with the free call second, instead of the $300 Sounding. No
popups here, as before.

14 November 2026 (GATHER night): a holiday section between the questions
and "Who's asking": "Give yourself the gift this holiday season", with
the two open retreats as the /retreats/ cards (.rx-date). Her facts:
$250 off Gatlinburg for GATHER guests, and Arizona's early rate. How the
$250 is claimed with the HoneyBook code GATHER (her yes) through 30 November,
as on her flyers: $1,350 shared, $2,650 king. Same night: the offer also sits
in the hero (rx-next), and an ink band like the flyers'. Pine cut from the
flyers was tried and removed on her word ("doesn't work one bit").
"Who's asking" turns porcelain so two white sections don't touch.

    cd tools && python3 gen_thequestions.py
"""
import os
import lux_page as L

URL = L.SITE + "/thequestions/"
CALL, ARW = L.CALL, L.ARW
I = "../assets/img/"

QUESTIONS = [
    "What made you laugh this week?",
    "What&rsquo;s a compliment you&rsquo;ve never forgotten?",
    "Where were you the last time you felt completely at ease?",
    "What&rsquo;s one small thing that made this week better?",
    "What do people come to you for?",
    "What are you better at now than you were a year ago?",
    "What did you love doing when you were ten?",
    "Who would be proud of where you are right now?",
    "What are you building that no one has seen yet?",
    "What would you do this year if it didn&rsquo;t have to be impressive?",
    "What would you say yes to if you knew it would work?",
    "Where do you want to go that you haven&rsquo;t been?",
]
LIST = "\n".join('      <li><span>%02d</span><p>%s</p></li>' % (i + 1, q) for i, q in enumerate(QUESTIONS))

MAIN = """<main id="main">

<section class="ww-hero" aria-labelledby="tq-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <span class="hv-label">GATHER &middot; Erickson Farmstead &middot; Isanti, MN</span>
      <h1 id="tq-h">You picked <em>one.</em></h1>
      <p class="hv-lede">There were twelve on the table. Here are the other eleven. Take them with you and use them on someone this week.</p>
      <div class="hv-btns">
        <a class="hv-btn hv-btn--ink" href="#questions">See all twelve %(ARW)s</a>
        <a class="hv-btn hv-btn--line" href="#retreats">The GATHER retreat offer</a>
      </div>
      <div class="rx-next tq-next"><span>GATHER exclusive &middot; through 30 November</span><p><b>Rest in the mountains. Make something in the desert.</b>Two women&rsquo;s retreats for 2027, with special pricing for everyone here tonight. <a class="hv-inline" href="#retreats">Give yourself the gift</a></p></div>
    </div>
    <figure class="ww-arch">
      <img src="%(I)scydnie-direct-1000.webp" srcset="%(I)scydnie-direct-600.webp 600w, %(I)scydnie-direct-1000.webp 1000w" sizes="(min-width: 64rem) 30rem, 90vw" width="1000" height="1500" alt="Cydnie Jocelyn smiling, a denim jacket slipping off one shoulder" fetchpriority="high">
    </figure>
  </div>
</section>

<!-- THE TWELVE. Numbered to match the cards: someone holding 07 has to
     find 07. Her "why" lines sit above them. -->
<section class="hv-sec tq-sec" id="questions" aria-labelledby="tq-why">
  <div class="hv-wrap">
    <div class="ww-head tq-why">
      <span class="hv-label">The questions</span>
      <h2 class="hv-h2" id="tq-why">I ask questions like these because <em>most rooms don&rsquo;t.</em></h2>
      <p class="hv-lede">We get asked what we do and where we work and how the kids are, and we answer all of it without ever saying anything true.</p>
    </div>
    <ol class="tq-list" role="list">
%(LIST)s
    </ol>
  </div>
</section>

<!-- THE GIFT. GATHER night, 14 November 2026. The two open retreats, as
     the cards on /retreats/. Women only, said in the lede, as the retreats
     are everywhere else. -->
<section class="hv-sec tq-gift" id="retreats" aria-labelledby="tq-gift">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">For everyone at GATHER &middot; Holiday 2026</span>
      <h2 class="hv-h2" id="tq-gift">Give yourself the gift <em>this holiday season.</em></h2>
      <p class="hv-lede">Two retreats. Two ways to make room for yourself. If tonight reminded you how good it feels to be asked something real, a retreat is five days of it. Both are small-group women&rsquo;s retreats in 2027.</p>
      <p class="tq-band">Special retreat pricing through 30 November</p>
    </div>
    <ul class="rx-dates" role="list">
      <li class="rx-date">
        <figure><img src="../assets/img/gatlinburg/house-dusk-portrait-834.webp" srcset="../assets/img/gatlinburg/house-dusk-portrait-600.webp 600w, ../assets/img/gatlinburg/house-dusk-portrait-834.webp 834w" sizes="(min-width: 60rem) 24rem, 92vw" width="834" height="1112" alt="The private house in Gatlinburg lit up at dusk against the Smoky Mountains" loading="lazy"></figure>
        <div class="rx-date-body">
          <span class="rx-pill">GATHER exclusive &middot; through 30 November</span>
          <p class="rx-when">13&ndash;18 April 2027 &middot; Gatlinburg, Tennessee</p>
          <h3>Wide Open: The Gatlinburg Edition</h3>
          <p>Five days in a private house at the edge of the Smoky Mountains, with Kayla Freeman leading the morning movement. Lodging, every meal, two workshops and two outings are included.</p>
          <dl><div><dt>Shared room</dt><dd>$1,350 <s>$1,600</s></dd></div><div><dt>Private king suite</dt><dd>$2,650 <s>$2,900</s></dd></div></dl>
          <p class="rx-note">Use code <b>GATHER</b> when you book for $250 off, through 30 November. $500 holds your room.</p>
          <div class="hv-btns"><a class="hv-btn hv-btn--ink" href="/retreats/gatlinburg/#rooms" data-cta="questions-gatlinburg">Choose your room %(ARW)s</a><a class="hv-link" href="/retreats/gatlinburg/">See the week</a></div>
        </div>
      </li>
      <li class="rx-date">
        <figure><img src="../assets/img/arizona/table-set-portrait-848.webp" srcset="../assets/img/arizona/table-set-portrait-600.webp 600w, ../assets/img/arizona/table-set-portrait-848.webp 848w" sizes="(min-width: 60rem) 24rem, 92vw" width="848" height="1130" alt="A long table set for dinner under a covered patio at dusk, small bonsai trees down the middle." loading="lazy"></figure>
        <div class="rx-date-body">
          <span class="rx-pill">Early rate &middot; through 30 November</span>
          <p class="rx-when">5&ndash;9 May 2027 &middot; Peoria, Arizona</p>
          <h3>Wild Canvas: The Arizona Edition</h3>
          <p>Five days in a painted house on the edge of the Sonoran desert, with guided creative sessions led by abstract artist Dr. Clarissa Castillo-Ramsey. Lodging, every meal and the airport shuttles are included. No art experience needed.</p>
          <dl><div><dt>Shared room</dt><dd>$1,675 <s>$1,800</s></dd></div></dl>
          <p class="rx-note">The early rate holds through 30 November, then the room is $1,800. $500 holds it.</p>
          <div class="hv-btns"><a class="hv-btn hv-btn--ink" href="/retreats/arizona/#rooms" data-cta="questions-arizona">Hold your room %(ARW)s</a><a class="hv-link" href="/retreats/arizona/">See the week</a></div>
        </div>
      </li>
    </ul>
    <p class="au-also tq-allret"><a class="hv-inline" href="/retreats/">Every retreat, in one place</a></p>
  </div>
</section>

<!-- WHO'S ASKING. BRIDGE: both paragraphs are mine, widened to founders
     and leaders on the site's positioning; her old lines spoke to women
     only and used the old heavy register. -->
<section class="hv-sec tq-sec" aria-labelledby="tq-who">
  <div class="hv-wrap au-row">
    <div>
      <span class="hv-label">Who&rsquo;s asking</span>
      <h2 class="hv-h2" id="tq-who">I&rsquo;m <em>Cydnie.</em></h2>
    </div>
    <div class="tq-who">
      <p class="hv-lede">A brand and business strategist in Forest Lake, Minnesota. I partner with founders and leaders on brand, website, operations and business development, start to finish.</p>
      <p>By the time someone gets to me, the business usually works. What they want is someone who sees where it could go, and builds it with them.</p>
      <p><a class="hv-inline" href="/about/">More about me</a></p>
    </div>
  </div>
</section>

<section class="hv-close" aria-labelledby="close-h">
  <div class="hv-wrap">
    <span class="hv-label hv-label--c">Keep the conversation going</span>
    <h2 class="hv-h2" id="close-h">One letter, <em>every week.</em></h2>
    <p class="hv-lede">If these questions landed, the letters will too. Free, written by me, and the first word on every retreat.</p>
    <div class="hv-btns">
      <a class="hv-btn hv-btn--ink" href="/newsletter/" data-cta="questions-letters">Get the letters %(ARW)s</a>
    </div>
    <p class="au-also">Rather talk now? <a class="hv-inline" href="%(CALL)s" data-cta="free-call-questions">Book a free 30-min call</a>.</p>
  </div>
</section>

</main>
""" % {"CALL": CALL, "ARW": ARW, "I": I, "LIST": LIST}

graph = [{"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": "The Questions",
          "isPartOf": {"@id": L.SITE + "/#website"}, "author": {"@id": L.SITE + "/#cydnie"}, "inLanguage": "en-US"}]

PRELOAD = ('<link rel="preload" as="image" href="%scydnie-direct-1000.webp" '
           'imagesrcset="%scydnie-direct-600.webp 600w, %scydnie-direct-1000.webp 1000w" '
           'imagesizes="(min-width: 64rem) 30rem, 90vw" type="image/webp" fetchpriority="high">\n' % (I, I, I))

OUT = "thequestions/index.html"
L.render(
    out=OUT, depth=1, active=None,
    title="The Questions | Cydnie Jocelyn",
    description="The twelve questions from the GATHER table, and the eleven you did not pick. Cydnie Jocelyn, brand and business strategist, Forest Lake, Minnesota.",
    canonical=URL,
    og_title="The Questions | Cydnie Jocelyn",
    og_description="There were twelve on the table. Here are the other eleven.",
    graph=graph, main=MAIN, preload=PRELOAD, body_class="ww-page",
    robots_html='<meta name="robots" content="noindex, follow">',
    reveal=(".ww-head", ".au-row > div"),
)
p = os.path.join(L.ROOT, OUT)
s = open(p, encoding="utf-8").read()
for tag in ('<script src="/sounding-popup.js" defer></script>\n', '<script src="/gatlinburg-popup.js" defer></script>\n'):
    assert s.count(tag) == 1, tag
    s = s.replace(tag, "")
open(p, "w", encoding="utf-8").write(s)
print("written", len(s))
