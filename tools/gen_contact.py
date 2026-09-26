"""Contact (/contact/), rebuilt 26 September 2026 on the luxury system.

Her answers (26 September): lead with the free call as well as the question
form. The HoneyBook placement (69f9f2a0...) is unchanged: the div, the
pixel and the controller script, re-added after the shared scripts. The
Sounding line is gone (the free call is the front door); "No sequence, no
list, no follow up you did not ask for" is cut (an exit); the location line
matches the rest of the site (nationwide). No popups on this page, as
before: both tags are stripped below, and both scripts skip /contact.

    cd tools && python3 gen_contact.py
"""
import os
import lux_page as L

URL = L.SITE + "/contact/"
CALL, ARW = L.CALL, L.ARW
PID = "69f9f2a0db6ae2c455d04434"
I = "../assets/img/"

HB = """<!-- The HoneyBook controller for placement %s. The div it looks for is
     already in the document by this point; build.py hashes this for the CSP. -->
<script>
  (function(h,b,s,n,i,p,e,t) {
    h._HB_ = h._HB_ || {};h._HB_.pid = i;;;;
    t=b.createElement(s);t.type="text/javascript";t.async=!0;t.src=n;
    e=b.getElementsByTagName(s)[0];e.parentNode.insertBefore(t,e);
})(window,document,"script","https://widget.honeybook.com/assets_users_production/websiteplacements/placement-controller.min.js","%s");
</script>
""" % (PID, PID)

MAIN = """<main id="main">

<section class="ww-hero" aria-labelledby="ct-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <span class="hv-label">Contact</span>
      <h1 id="ct-h">Let&rsquo;s <em>talk.</em></h1>
      <p class="hv-lede">Book a free 30-minute call, or send me a question below. Either way, you hear back from me.</p>
      <div class="hv-btns">
        <a class="hv-btn hv-btn--ink" href="%(CALL)s" data-cta="free-call-contact">Book a free 30-min call %(ARW)s</a>
        <a class="hv-btn hv-btn--line" href="#ask">Ask a question</a>
      </div>
      <ul class="ww-trust" role="list"><li>Forest Lake, Minnesota</li><li>Partnering nationwide</li><li>Answered within a day</li></ul>
    </div>
    <figure class="ww-arch">
      <img src="%(I)scydnie-mug-1000.webp" srcset="%(I)scydnie-mug-600.webp 600w, %(I)scydnie-mug-1000.webp 1000w" sizes="(min-width: 64rem) 30rem, 90vw" width="1000" height="1500" alt="Cydnie Jocelyn laughing on a sofa with a mug in her hand" fetchpriority="high">
    </figure>
  </div>
</section>

<!-- THE QUESTION FORM. HoneyBook placement %(PID)s. The div and the pixel
     stay together; min-height holds the space until the form lands, and the
     noscript is the only way to reach her with JavaScript off. -->
<section class="hv-sec ct-ask" id="ask" aria-labelledby="ct-ask">
  <div class="hv-wrap au-row">
    <div class="ct-side">
      <span class="hv-label">Ask me something</span>
      <h2 class="hv-h2" id="ct-ask">No question <em>too small.</em></h2>
      <p class="hv-lede">I answer these myself, usually within a day.</p>
      <blockquote class="ct-quote"><p>&ldquo;She&rsquo;s truly a breath of fresh air.&rdquo;</p><cite>Angela &middot; Alchemy with A</cite></blockquote>
      <dl class="ct-more">
        <div><dt>Email</dt><dd><a class="hv-inline" href="mailto:hello@cydniejocelyn.com">hello@cydniejocelyn.com</a></dd></div>
        <div><dt>Retreats</dt><dd>Dates, prices and answers are on <a class="hv-inline" href="/retreats/">each retreat&rsquo;s page</a>.</dd></div>
      </dl>
    </div>
    <div class="ct-embed">
      <div class="hb-p-%(PID)s-2"></div>
      <img height="1" width="1" style="display:none" src="https://www.honeybook.com/p.png?pid=%(PID)s" alt="">
      <noscript><p>The form needs JavaScript. Write to <a class="hv-inline" href="mailto:hello@cydniejocelyn.com">hello@cydniejocelyn.com</a> instead and it reaches the same inbox.</p></noscript>
    </div>
  </div>
</section>

</main>
""" % {"CALL": CALL, "ARW": ARW, "I": I, "PID": PID}

about = {n["@id"]: n for n in L.old_graph("about/index.html") if "@id" in n}
graph = [about.get(n.get("@id"), n) if n.get("@type") != "ContactPage" else n
         for n in L.old_graph("contact/index.html")]

PRELOAD = ('<link rel="preload" as="image" href="%scydnie-mug-1000.webp" '
           'imagesrcset="%scydnie-mug-600.webp 600w, %scydnie-mug-1000.webp 1000w" '
           'imagesizes="(min-width: 64rem) 30rem, 90vw" type="image/webp" fetchpriority="high">\n' % (I, I, I))

OUT = "contact/index.html"
L.render(
    out=OUT, depth=1, active="/contact/",
    title="Contact Cydnie Jocelyn | Book a Free Call or Ask a Question",
    description="Book a free 30-minute call with Cydnie Jocelyn, brand and business strategist, or send a question and she will answer it herself. Forest Lake, Minnesota, partnering nationwide.",
    canonical=URL,
    og_title="Contact Cydnie Jocelyn | Book a Free Call or Ask a Question",
    og_description="A free 30-minute call, or a question she answers herself, usually within a day.",
    graph=graph, main=MAIN, preload=PRELOAD, body_class="ww-page",
    reveal=(".au-row > .ct-side",),
)
p = os.path.join(L.ROOT, OUT)
s = open(p, encoding="utf-8").read()
for tag in ('<script src="/sounding-popup.js" defer></script>\n', '<script src="/gatlinburg-popup.js" defer></script>\n'):
    assert s.count(tag) == 1, tag
    s = s.replace(tag, "")
assert s.count("</body>") == 1
s = s.replace("</body>", HB + "</body>", 1)
open(p, "w", encoding="utf-8").write(s)
print("written", len(s))
