"""The Sounding (/a-sounding/), rebuilt 25 September 2026 on the luxury system.

Her answers: the free call comes first and every client then does the
Sounding before any Build ("every client starts here" stays true); keep the
name that converts best, so it stays "The Sounding" with the plain subtitle
"a 90-minute strategy session" used on every page. Kept from the old page,
because it was the best writing on it: the Felt / Found pairs, the one-page
deliverable, and "Sometimes the answer is that you don't need me". Cut: the
water language ("You are not lacking anything. You are under something"),
"no discovery call" (there is one now), and the price said three times.

    python3 tools/gen_a_sounding.py
"""
import lux_page as L

URL = L.SITE + "/a-sounding/"
CALL, SOUND, ARW = L.CALL, L.SOUND, L.ARW

FAQ = [
    ("Do I need the free call first?",
     "It is the recommended first step: thirty minutes to make sure the Sounding is right for you. If you already know it is, book the Sounding directly."),
    ("Is this a coaching call?",
     "No. There is no goal setting and nothing to work on between sessions. It is a strategy session: you describe how the business currently runs, and you leave with the pressure located and a written report of what to address first."),
    ("Does the $300 count toward a larger project?",
     "Yes. If you go on to a Build, the $300 comes off it. The Sounding is still complete on its own: the report is yours either way, and whether to continue is a decision you make after it is in your hands."),
    ("What if I do not know what my problem is?",
     "That is the usual starting point. Finding it is the work of the ninety minutes, and it is why the conversation covers the whole business rather than the part you think is broken."),
    ("What is in the written report?",
     "My full take on the business: what I heard, what is load bearing, and my recommendations in the order I would take them. If the honest answer is that you do not need outside help, the report says so and explains why."),
    ("How soon can I book?",
     "Usually two to three weeks out. Open times are on the booking page, remote or in person around the Twin Cities."),
]

MAIN = """<main id="main">

<!-- HERO: what it is, what it costs, what you leave with. -->
<section class="ww-hero" aria-labelledby="sd-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <span class="hv-label">The Sounding</span>
      <h1 id="sd-h">Know exactly what to <em>fix first.</em></h1>
      <p class="hv-lede">The Sounding is a 90-minute strategy session across brand, operations and business development. Two days later you get my full take in writing: what is really going on, and what I recommend, in order. Or, if it is the honest answer, that you don&rsquo;t need me.</p>
      <div class="hv-btns">
        <a class="hv-btn hv-btn--ink" href="%(SOUND)s" data-cta="sounding-hero">Book the Sounding, $300 %(ARW)s</a>
        <a class="hv-btn hv-btn--line" href="%(CALL)s" data-cta="free-call-sounding">Not sure? Free call first</a>
      </div>
      <ul class="ww-trust" role="list"><li>$300 flat</li><li>Credited to your project</li><li>Nothing to prepare</li></ul>
    </div>
    <figure class="ww-arch">
      <img src="../assets/img/sounding/hero-1100.webp" srcset="../assets/img/sounding/hero-700.webp 700w, ../assets/img/sounding/hero-1100.webp 1100w, ../assets/img/sounding/hero-1500.webp 1500w" sizes="(min-width: 64rem) 30rem, 90vw" width="1100" height="1467" alt="Cydnie Jocelyn in a garden, one hand in her hair, smiling thoughtfully" fetchpriority="high">
      <figcaption><span>Your written report</span><b>Two days later</b></figcaption>
    </figure>
  </div>
</section>

<!-- FELT / FOUND: her two pairs from the old page, the proof of how she
     thinks. -->
<section class="hv-sec" aria-labelledby="sd-ff">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Why it works</span>
      <h2 class="hv-h2" id="sd-ff">What you feel is rarely <em>where it starts.</em></h2>
      <p class="hv-lede">Most people who book a Sounding can list everything they have built. What they cannot find is the thing making all of it heavier every month. It is almost always structural, and almost never where it is felt.</p>
    </div>
    <div class="sd-ff">
      <div class="sd-ff-row"><p><span>What you feel</span>The bookkeeping is late.</p><p><span>What we find</span><em>Because the pricing is wrong.</em></p></div>
      <div class="sd-ff-row"><p><span>What you feel</span>The work is exhausting.</p><p><span>What we find</span><em>Because you are still the only one who can do the part that matters.</em></p></div>
    </div>
  </div>
</section>

<!-- WHAT YOU WILL KNOW: the outcome, spelled out before the price. -->
<section class="hv-sec ww-who sd-know" aria-labelledby="sd-know">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">After your Sounding</span>
      <h2 class="hv-h2" id="sd-know">You will know <em>four things.</em></h2>
    </div>
    <ul class="ww-profiles sd-know-list" role="list">
      <li><h3>What is really going on</h3><p>The structural reason the business feels heavier, not just the symptom you came in with.</p></li>
      <li><h3>What to fix first</h3><p>My recommendations, in the order I would take them, so you are not guessing where to start.</p></li>
      <li><h3>Whether you need help</h3><p>Some fixes you can make yourself. I will say which, and whether you need me for any of the rest.</p></li>
      <li><h3>Where it can go</h3><p>Where the brand and the business can go from here, once the thing holding them is dealt with.</p></li>
    </ul>
  </div>
</section>

<!-- HOW IT WORKS: her four steps, shorter. -->
<section class="hv-sec ww-path" aria-labelledby="sd-how">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">How it works</span>
      <h2 class="hv-h2" id="sd-how">One conversation, <em>across everything.</em></h2>
    </div>
    <ol class="ww-steps" role="list">
      <li><h3>Book a time</h3><p>Pick a time and name your business. That is the whole form: no intake, no pre-work.</p></li>
      <li><h3>Ninety minutes</h3><p>Brand, operations and business development, because where pressure lands is rarely where it starts. You talk; I ask and take notes.</p></li>
      <li><h3>Your report</h3><p>Two days later, my full take in writing: what I heard, what is load bearing, and what I recommend, in order.</p></li>
      <li><h3>Your call</h3><p>Nothing waiting at the end. If you want to keep working together, you say so, and the $300 comes off your Build.</p></li>
    </ol>
  </div>
</section>

<!-- THE DELIVERABLE, shown as the page itself. -->
<section class="hv-sec sd-leave" aria-labelledby="sd-page">
  <div class="hv-wrap sd-leave-grid">
    <div class="sd-doc" aria-hidden="true">
      <svg class="hv-wm sd-doc-mark" viewBox="0 0 504.2 54.4"><use href="#cj-wordmark"/></svg>
      <p class="sd-doc-title">The Sounding <span>Your written report</span></p>
      <ol>
        <li><b>What I heard</b><i></i><i class="short"></i></li>
        <li><b>What is load bearing</b><i></i><i></i><i class="short"></i></li>
        <li><b>My recommendations, in order</b><i></i><i></i><i></i><i></i><i class="short"></i></li>
      </ol>
    </div>
    <div>
      <span class="hv-label">What you leave with</span>
      <h2 class="hv-h2" id="sd-page">My full take, <em>in writing.</em></h2>
      <p class="hv-lede">Not a call you have to remember. A written report of everything I saw and what I recommend, in the order I would do it. Act on it without me, or hand it to a partner. It is yours either way.</p>
      <ul class="sd-list" role="list"><li>What I heard</li><li>What is load bearing</li><li>My recommendations, in order</li><li>Or, honestly, that you don&rsquo;t need me</li></ul>
    </div>
  </div>
</section>

<!-- THE HONEST ANSWER: kept word for word in spirit, set on ink. -->
<section class="hv-sec ww-standards sd-truth" aria-labelledby="sd-truth">
  <div class="hv-wrap">
    <span class="hv-label">The part most people leave out</span>
    <h2 class="hv-h2" id="sd-truth">Sometimes the answer is that <em>you don&rsquo;t need me.</em></h2>
    <p class="sd-truth-copy">Sometimes my recommendation is a hire. Sometimes a price change, a contract already sitting unsigned, or nothing at all for a quarter while something else settles. None of that is work I would bill you for, and I will tell you when it is the answer.</p>
    <p class="sd-truth-close">Hearing it in week one is worth more than $300. The alternative is a year spent solving the wrong problem.</p>
  </div>
</section>

<!-- PROOF: the two clients who started here, with where it led. -->
<section class="hv-sec" aria-labelledby="sd-proof">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Every client starts here</span>
      <h2 class="hv-h2" id="sd-proof">In <em>their words.</em></h2>
    </div>
    <ul class="hv-quotes sd-quotes" role="list">
      <li><figure class="hv-q"><blockquote><p>&ldquo;She listens with intention, quickly understands your vision, and brings it to life with ease.&rdquo;</p><p>As a new business owner, she has lifted so much off my plate, allowing me to focus on what matters most.</p></blockquote><figcaption>Tamara &middot; Mane Alchemist Salon &middot; The Sounding, then a Full Brand Launch</figcaption></figure></li>
      <li><figure class="hv-q"><blockquote><p>&ldquo;She helped redesign how I operate.&rdquo;</p><p>Cydnie is very knowledgeable and incredibly dedicated.</p></blockquote><figcaption>Spencer Scott &middot; SRS Performance &middot; The Sounding, then brand and operations</figcaption></figure></li>
    </ul>
  </div>
</section>

<!-- BOOK: the price once, with everything it includes. -->
<section class="hv-sec sd-buy" id="book" aria-labelledby="sd-buy">
  <div class="hv-wrap sd-buy-grid">
    <div>
      <span class="hv-label">Book the Sounding</span>
      <h2 class="hv-h2" id="sd-buy">$300, <em>and it is never spent twice.</em></h2>
      <p class="hv-lede">Complete on its own, and it comes off your Build if you go on to one.</p>
    </div>
    <div class="sd-ticket">
      <p class="sd-ticket-price"><span>Flat</span>$300</p>
      <ul role="list"><li>A 90-minute strategy session on the whole business</li><li>My full take and recommendations, in writing, two days later</li><li>Credited to your Build if you continue</li><li>Remote, or in person around the Twin Cities</li></ul>
      <a class="hv-btn hv-btn--ink" href="%(SOUND)s" data-cta="sounding-book">Book the Sounding %(ARW)s</a>
      <p class="sd-ticket-note">Usually booked two to three weeks out. <a class="hv-inline" href="%(CALL)s">Or start with a free call.</a></p>
    </div>
  </div>
</section>

<section class="hv-sec" id="faq" aria-labelledby="faq-h">
  <div class="hv-wrap hv-faq ww-faq">
    <div>
      <span class="hv-label">Questions</span>
      <h2 class="hv-h2" id="faq-h">Before you <em>book.</em></h2>
      <p class="hv-lede">Not ready to spend $300? <a class="hv-inline" href="/contact/">Ask me a question</a>, or start with <a class="hv-inline" href="/the-letters/">the Letters</a>. They are free and arrive weekly.</p>
    </div>
    <div class="hv-faq-list">
%(FAQ)s
    </div>
  </div>
</section>

</main>
""" % {"CALL": CALL, "SOUND": SOUND, "ARW": ARW, "FAQ": L.faq_html(FAQ)}

# ---------- structured data: the old graph, updated ----------
graph = L.old_graph("a-sounding/index.html")
for n in graph:
    t = n.get("@type")
    if t == "WebPage":
        n["name"] = "The Sounding: a 90-minute strategy session"
        for it in n.get("breadcrumb", {}).get("itemListElement", []):
            if it.get("position") == 2:
                it["name"] = "The Sounding"
    if t == "Service":
        n["name"] = "The Sounding"
        n["serviceType"] = "Business strategy session"
        n["description"] = ("A 90-minute strategy session across brand, operations and business development, "
                            "with a written report of findings and recommendations two days later. $300, credited to a Build.")
    if t == "FAQPage":
        n.update(L.faq_node(URL, FAQ))
    if isinstance(t, list) and "ProfessionalService" in t:
        n["description"] = ("Brand, website, operations and business development partnership for founders and leaders, "
                            "with every price published. Based in Forest Lake, Minnesota, working with clients across the United States.")

PRELOAD = ('<link rel="preload" as="image" href="../assets/img/sounding/hero-1100.webp" '
           'imagesrcset="../assets/img/sounding/hero-700.webp 700w, ../assets/img/sounding/hero-1100.webp 1100w, '
           '../assets/img/sounding/hero-1500.webp 1500w" imagesizes="(min-width: 64rem) 30rem, 90vw" '
           'type="image/webp" fetchpriority="high">\n')

n = L.render(
    out="a-sounding/index.html", depth=1, active="/the-build/",
    title="The Sounding | 90-Minute Business Strategy Session & Written Report, $300",
    description="The Sounding: a 90-minute strategy session across brand, operations and business development, then a written report of findings and recommendations two days later. $300, credited to your project.",
    canonical=URL,
    og_title="The Sounding | A 90-minute strategy session with Cydnie Jocelyn",
    og_description="Know exactly what to fix first: 90 minutes on the whole business, then my full take and recommendations in writing. $300, credited to your project.",
    graph=graph, main=MAIN, preload=PRELOAD, body_class="ww-page",
    reveal=(".ww-head", ".sd-ff-row", ".sd-know-list > li", ".ww-steps > li", ".sd-leave-grid > div:last-child", ".sd-truth .hv-wrap > *",
            ".hv-quotes > li", ".sd-buy-grid > *"),
    reveal_imgs=(".sd-doc",),
)
print("written", n)
