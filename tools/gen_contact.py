"""Contact (/contact/), rebuilt 26 September 2026 on the luxury system.

Her answers (26 September): lead with the free call as well as the question
form. Second pass, same day, her word: the embedded HoneyBook placement
(69f9f2a0...) "doesn't work", so the form is a button to the direct link of
the same question form Greece uses (cf_id/69fa372c...); no embed script. The
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
QUESTION = "https://www.honeybook.com/widget/cydnie_jocelyn_collective_299013/cf_id/69fa372ccd31fefc073c5d28"
I = "../assets/img/"


MAIN = """<main id="main">

<section class="ww-hero" aria-labelledby="ct-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <span class="hv-label">Contact</span>
      <h1 id="ct-h">Let&rsquo;s <em>talk.</em></h1>
      <p class="hv-lede">Book a free 30-minute call, or send me a question below. Either way, you hear back from me.</p>
      <div class="hv-btns">
        <a class="hv-btn hv-btn--ink" href="%(CALL)s" data-cta="free-call-contact">Book a free 30-min call %(ARW)s</a>
        <a class="hv-btn hv-btn--line" href="#ask" data-cta="question-contact-hero">Ask a question</a>
      </div>
      <ul class="ww-trust" role="list"><li>Forest Lake, Minnesota</li><li>Partnering nationwide</li><li>Answered within a day</li></ul>
    </div>
    <figure class="ww-arch">
      <img src="%(I)scydnie-mug-1000.webp" srcset="%(I)scydnie-mug-600.webp 600w, %(I)scydnie-mug-1000.webp 1000w" sizes="(min-width: 64rem) 30rem, 90vw" width="1000" height="1500" alt="Cydnie Jocelyn laughing on a sofa with a mug in her hand" fetchpriority="high">
    </figure>
  </div>
</section>

<!-- THE QUESTION FORM. A button to the HoneyBook form's own page, which
     works everywhere; the embed did not. -->
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
    <!-- THE QUESTION FORM (26 September 2026, her word "pushed to neon"):
         /api/inquiry saves it to her Neon database and emails it to
         hello@cydniejocelyn.com. Replaces the button to the HoneyBook form,
         which stays as the no-JavaScript fallback. -->
    <form class="ct-card cj-form" data-api="inquiry" aria-labelledby="ct-form-h">
      <p class="ct-card-lab">The question form</p>
      <p class="ct-card-h" id="ct-form-h">Tell me what&rsquo;s on <em>your mind.</em></p>
      <label class="cj-f"><span>Your name</span><input name="name" type="text" autocomplete="name"></label>
      <label class="cj-f"><span>Email</span><input name="email" type="email" required autocomplete="email"></label>
      <label class="cj-f"><span>Your question</span><textarea name="message" rows="5" required maxlength="5000"></textarea></label>
      <input class="cj-hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="hv-btn hv-btn--ink" type="submit" data-cta="question-contact">Send my question %(ARW)s</button>
      <p class="cj-status" role="status" aria-live="polite"></p>
      <p class="ct-card-or">Or book a <a class="hv-inline" href="%(CALL)s" data-cta="free-call-contact-card">free 30-min call</a> instead.</p>
      <noscript><p><a class="hv-inline" href="%(QUESTION)s" rel="noopener">Use this form instead</a></p></noscript>
    </form>
  </div>
</section>

</main>
""" % {"CALL": CALL, "ARW": ARW, "I": I, "QUESTION": QUESTION}

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
    description="Book a free 30-minute call with Cydnie Jocelyn, brand and business strategist, or send a question she answers herself. Partnering nationwide.",
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
open(p, "w", encoding="utf-8").write(s)
print("written", len(s))
