"""The six city pages (/brand-strategy/<city>/), 5 October 2026.

Every page sells the Strategy Day ($1,500) and leads into a website or a
Full Brand Launch. What each page says about its place lives in cities.py;
this file is the frame they share. Order on every page:

    hero, the place, the Strategy Day, the price, after the day,
    proof (a case on Minneapolis and Chisago, quotes elsewhere),
    local questions, the other cities, close.

The city pages are linked from the home page (#cities) and from each other,
never from the navigation (her brief).

    python3 tools/gen_cities.py
"""
import os
import lux_page as L
from cities import CITIES, url

CALL, SOUND, ARW = L.CALL, L.SOUND, L.ARW
PRE = "../../"

STEPS = [
    ("Audit", "What is working, what is not, and why: your website, your offers, your reviews and how you describe the business today."),
    ("Discovery", "Who you serve best, who you want more of, and what they are choosing between when they find you."),
    ("Positioning", "The one clear decision: who the business is for and what it should be known for."),
    ("Message", "The words to say it, on your website, in a conversation and in a search result."),
]

QUOTES = """    <ul class="hv-quotes sd-quotes" role="list">
      <li><figure class="hv-q"><blockquote><p>&ldquo;She listens with intention, quickly understands your vision, and brings it to life with ease.&rdquo;</p><p>As a new business owner, she has lifted so much off my plate.</p></blockquote><figcaption>Tamara &middot; Mane Alchemist Salon, Chisago City</figcaption></figure></li>
      <li><figure class="hv-q"><blockquote><p>&ldquo;She helped redesign how I operate.&rdquo;</p><p>Cydnie is very knowledgeable and incredibly dedicated.</p></blockquote><figcaption>Spencer Scott &middot; SRS Performance, Minneapolis</figcaption></figure></li>
    </ul>"""

CASE = {
    "srs": dict(
        label="Client work in Minneapolis", h2="Narrowed <em>on purpose.</em>",
        lede="A Minneapolis strength studio competing with every gym in the city. Instead of competing on equipment and hours, it now speaks to one person: the former competitive athlete.",
        img="srs-performance", alt="SRS Performance website home page, purple wordmark over athletes training",
        tag="Brand &amp; operations", name="SRS Performance",
        story=[("The decision", "Narrowed from general fitness to former competitive athletes."),
               ("What we built", "A half-built site rebuilt as a brand, then email funnels, offer guides, positioning and a plan for growing into the community.")],
        quote=("She helped redesign how I operate.", "Spencer Scott, SRS Performance"),
        href="https://srsperform.com"),
    "mane": dict(
        label="Client work in Chisago City", h2="A decision <em>before a design.</em>",
        lede="A new salon in Chisago City, before opening day, with a clear vision and no brand yet. The decision came first: away from the wellness salon default and toward deliberate luxury.",
        img="mane-alchemist", alt="Mane Alchemist Salon website home page, dark green with a gold art deco wordmark",
        tag="Full Brand Launch", name="Mane Alchemist Salon",
        story=[("The decision", "Positioned away from the wellness salon default and toward deliberate luxury."),
               ("What we built", "Logo, brand guide and voice, a website built to scale, then a 90-day social plan that built demand before opening day."),
               ("Where it is now", "Open, booking online, and still partnered: quarterly content and monthly strategy.")],
        quote=("She listens with intention, quickly understands your vision, and brings it to life with ease.", "Tamara, Mane Alchemist Salon"),
        href="https://manealchemistsalon.com"),
}


def proof(c):
    if c["proof"] == "quotes":
        return """<section class="hv-sec" aria-labelledby="ct-proof">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">%s</span>
      <h2 class="hv-h2" id="ct-proof">%s</h2>
      <p class="hv-lede">%s</p>
    </div>
%s
  </div>
</section>""" % (c["proof_label"], c["proof_h2"], c["proof_lede"], QUOTES)
    k = CASE[c["proof"]]
    phone = ('\n        <div class="hv-phone"><div><img src="%sassets/img/work/%s-screen-500.webp" width="500" height="1095" '
             'alt="%s website on a phone" loading="lazy"></div></div>' % (PRE, k["img"], k["name"]))
    story = "\n".join('          <div><dt>%s</dt><dd>%s</dd></div>' % s for s in k["story"])
    return """<section class="hv-sec" aria-labelledby="ct-proof">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">%(label)s</span>
      <h2 class="hv-h2" id="ct-proof">%(h2)s</h2>
      <p class="hv-lede">%(lede)s</p>
    </div>
    <article class="hv-feature">
      <div class="hv-feature-media">
        <div class="hv-browser"><div><img src="%(pre)sassets/img/work/%(img)s-desktop-1400.webp" srcset="%(pre)sassets/img/work/%(img)s-desktop-800.webp 800w, %(pre)sassets/img/work/%(img)s-desktop-1400.webp 1400w" sizes="(min-width: 64rem) 44rem, 92vw" width="1400" height="788" alt="%(alt)s" loading="lazy"></div></div>%(phone)s
      </div>
      <div>
        <span class="hv-label">%(tag)s</span>
        <h3>%(name)s</h3>
        <dl class="hv-story">
%(story)s
        </dl>
        <blockquote>&ldquo;%(q)s&rdquo;<cite>%(cite)s</cite></blockquote>
        <a class="hv-link" href="%(href)s" target="_blank" rel="noopener">Visit the site<span class="hv-vh"> (opens in a new tab)</span></a>
      </div>
    </article>
  </div>
</section>""" % dict(k, pre=PRE, phone=phone, story=story, q=k["quote"][0], cite=k["quote"][1])


def network(c):
    others = [o for o in CITIES if o is not c]
    links = "\n".join('      <li><a href="%s"><span>%s</span><b>%s</b>%s</a></li>' % (url(o), o["short"], o["label"], ARW) for o in others)
    return """<section class="hv-sec ct-net-sec" aria-labelledby="ct-net">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Also in person</span>
      <h2 class="hv-h2" id="ct-net">Around <em>Minnesota.</em></h2>
      <p class="hv-lede">Based in Forest Lake, working in person across the north metro and the Twin Cities, and remotely anywhere in the United States. Taking a team away? See <a class="hv-inline" href="/womens-retreats/leadership/">leadership retreats</a>.</p>
    </div>
    <ul class="ct-net" role="list">
%s
    </ul>
  </div>
</section>""" % links


def main_html(c):
    stem, pattern, widths, w, h, alt = c["img"]
    src = PRE + pattern % (1000 if 1000 in widths else 1100)
    srcset = ", ".join("%s%s %dw" % (PRE, pattern % x, x) for x in widths)
    steps = "\n".join('      <li><h3>%s</h3><p>%s</p></li>' % s for s in STEPS)
    items = "\n".join('      <li><h3>%s</h3><p>%s</p></li>' % s for s in c["local_items"])
    body = "\n".join("        <p>%s</p>" % p for p in c["local_p"])
    nearby = ", ".join(c["nearby"][:-1]) + " and " + c["nearby"][-1]
    return """<main id="main">

<!-- HERO: the place in the label, the Strategy Day in the first screen. -->
<section class="ww-hero" aria-labelledby="ct-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <span class="hv-label">Brand strategy &middot; %(label)s</span>
      <h1 id="ct-h">%(h1)s</h1>
      <p class="hv-lede">%(lede)s</p>
      <div class="hv-btns">
        <a class="hv-btn hv-btn--ink" href="%(CALL)s" data-cta="free-call-city-%(slug)s">Book a free call %(ARW)s</a>
        <a class="hv-btn hv-btn--line" href="#day">What happens in the day</a>
      </div>
      <ul class="ww-trust" role="list"><li>$1,500 flat</li><li>One day, in writing</li><li>In person or remote</li></ul>
    </div>
    <figure class="ww-arch">
      <img src="%(src)s" srcset="%(srcset)s" sizes="(min-width: 64rem) 30rem, 90vw" width="%(w)d" height="%(h)d" alt="%(alt)s" fetchpriority="high">
      <figcaption><span>Strategy Day</span><b>$1,500 flat</b></figcaption>
    </figure>
  </div>
</section>

<!-- THE PLACE: written for this town only (tools/cities.py). -->
<section class="hv-sec ct-local" aria-labelledby="ct-local">
  <div class="hv-wrap">
    <div class="ct-local-grid">
      <div>
        <span class="hv-label">%(local_label)s</span>
        <h2 class="hv-h2" id="ct-local">%(local_h2)s</h2>
      </div>
      <div class="hv-body">
%(body)s
        <p class="ct-near">Also working with businesses in %(nearby)s.</p>
      </div>
    </div>
    <ul class="ww-profiles" role="list">
%(items)s
    </ul>
  </div>
</section>

<!-- THE STRATEGY DAY: the offer, the same on every city page. -->
<section class="hv-sec ww-path" id="day" aria-labelledby="ct-day">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">The Strategy Day</span>
      <h2 class="hv-h2" id="ct-day">One day to <em>decide.</em></h2>
      <p class="hv-lede">For the business that needs a decision more than a build. We work through four things in order, and by the end of the day the hardest questions about your brand have answers, in writing.</p>
    </div>
    <ol class="ww-steps" role="list">
%(steps)s
    </ol>
  </div>
</section>

<!-- THE PRICE, once, with everything it includes. -->
<section class="hv-sec sd-buy" id="book" aria-labelledby="ct-buy">
  <div class="hv-wrap sd-buy-grid">
    <div>
      <span class="hv-label">What it costs</span>
      <h2 class="hv-h2" id="ct-buy">$1,500, <em>flat.</em></h2>
      <p class="hv-lede">No hourly add-ons and no proposal to decode. Start with a free call so we can plan the day around your business.</p>
    </div>
    <div class="sd-ticket">
      <p class="sd-ticket-price"><span>Strategy Day</span>$1,500</p>
      <ul role="list"><li>A full day on your brand and business</li><li>Audit, discovery, positioning and message</li><li>Your positioning and message in writing</li><li>In person or remote, your choice</li><li>$1,500 comes off a Full Brand Launch</li></ul>
      <a class="hv-btn hv-btn--ink" href="%(CALL)s" data-cta="free-call-city-book-%(slug)s">Book a free call to plan it %(ARW)s</a>
      <p class="sd-ticket-note">Not ready for a full day? <a class="hv-inline" href="/brand-strategy/strategy-session/">The Sounding</a> is 90 minutes and a written roadmap for $300.</p>
    </div>
  </div>
</section>

<!-- AFTER THE DAY: the lead into the website or the full launch. -->
<section class="hv-sec ct-next" aria-labelledby="ct-next">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">After the day</span>
      <h2 class="hv-h2" id="ct-next">Then <em>build it.</em></h2>
      <p class="hv-lede">%(next_lede)s The decisions from your Strategy Day become the brief, and if you choose the Full Brand Launch, the $1,500 comes off it.</p>
    </div>
    <div class="ww-menu">
      <div class="ww-group">
        <div class="ww-item"><h4>Website</h4><p>A separate package when it is not part of a Full Brand Launch. Built in code and yours outright. No theme, no plugins, no platform to rent. Five to eight pages, with the copy and the search foundations done properly.</p><ul role="list"><li>Five to eight pages</li><li>Copy</li><li>SEO</li></ul><span class="hv-price">From<b>$4,000</b></span></div>
        <div class="ww-item ww-item--sig"><h4>Full Brand Launch <span class="hv-tag">Signature</span></h4><p>Logo, brand guide and voice, a website, then the social strategy and launch plan that puts it in front of the right people. The complete partnership, and your $1,500 Strategy Day comes off it.</p><ul role="list"><li>Identity &amp; logo</li><li>Website</li><li>Launch plan</li></ul><span class="hv-price">From<b>$15,000</b></span></div>
      </div>
    </div>
    <p class="ww-menu-note"><a class="hv-link" href="/brand-strategy/">Every service and price</a></p>
  </div>
</section>

%(proof)s

<section class="hv-sec" id="faq" aria-labelledby="faq-h">
  <div class="hv-wrap hv-faq ww-faq">
    <div>
      <span class="hv-label">Questions</span>
      <h2 class="hv-h2" id="faq-h">Before you <em>book.</em></h2>
      <p class="hv-lede">Something not here? <a class="hv-inline" href="/contact/">Ask me directly.</a> I answer every one myself.</p>
    </div>
    <div class="hv-faq-list">
%(faq)s
    </div>
  </div>
</section>

%(network)s

<section class="hv-close" aria-labelledby="close-h">
  <div class="hv-wrap">
    <span class="hv-label hv-label--c">Let&rsquo;s begin</span>
    <h2 class="hv-h2" id="close-h">%(close_h2)s</h2>
    <p class="hv-lede">Thirty minutes, free, to see whether a Strategy Day is the right next step for your business.</p>
    <div class="hv-btns">
      <a class="hv-btn hv-btn--ink" href="%(CALL)s" data-cta="free-call-city-close-%(slug)s">Book a free 30-min call %(ARW)s</a>
    </div>
    <small>Or write to me at <a class="hv-inline" href="mailto:hello@cydniejocelyn.com">hello@cydniejocelyn.com</a></small>
  </div>
</section>

</main>
""" % dict(c, CALL=CALL, ARW=ARW, src=src, srcset=srcset, w=w, h=h, alt=alt, steps=steps, items=items,
           body=body, nearby=nearby, proof=proof(c), faq=L.faq_html(c["faq"]), network=network(c))


# The organisation node is the home page's, verbatim, so every page makes
# the same claim about who and where the business is.
ORG = [n for n in L.old_graph("index.html") if isinstance(n.get("@type"), list) and "LocalBusiness" in n["@type"]][0]
ORG_ID = ORG["@id"]


def graph(c):
    u = L.SITE + url(c)
    area = [{"@type": t, "name": n, "containedInPlace": {"@type": "State", "name": "Minnesota"}} for t, n in c["area"]]
    import html as _h
    plain = lambda s: _h.unescape(s.replace("<em>", "").replace("</em>", ""))
    return [
        ORG,
        {"@type": "WebPage", "@id": u + "#webpage", "url": u, "name": plain(c["title"]),
         "description": c["description"], "isPartOf": {"@id": L.SITE + "/#website"}, "about": {"@id": ORG_ID},
         "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Home", "item": L.SITE + "/"},
             {"@type": "ListItem", "position": 2, "name": "Brand Strategy", "item": L.SITE + "/brand-strategy/"},
             {"@type": "ListItem", "position": 3, "name": "Brand strategy in " + plain(c["label"]), "item": u}]}},
        {"@type": "Service", "@id": u + "#service", "name": "Strategy Day: brand strategy in " + plain(c["label"]),
         "serviceType": "Brand strategy", "provider": {"@id": ORG_ID}, "areaServed": area, "url": u,
         "description": "One day on audit, discovery, positioning and message, delivered in writing. "
                        "In person or remote, by preference and location. The $1,500 comes off a Full Brand Launch; a website is a separate package.",
         "offers": [
             {"@type": "Offer", "name": "Strategy Day", "price": 1500, "priceCurrency": "USD"},
             {"@type": "AggregateOffer", "name": "Website", "lowPrice": 4000, "priceCurrency": "USD"},
             {"@type": "AggregateOffer", "name": "Full Brand Launch", "lowPrice": 15000, "priceCurrency": "USD"}]},
        L.faq_node(u, c["faq"]),
    ]


for c in CITIES:
    out = "brand-strategy/%s/index.html" % c["slug"]
    os.makedirs(os.path.join(L.ROOT, os.path.dirname(out)), exist_ok=True)
    stem, pattern, widths, w, h, alt = c["img"]
    preload = ('<link rel="preload" as="image" href="%s%s" imagesrcset="%s" imagesizes="(min-width: 64rem) 30rem, 90vw" '
               'type="image/webp" fetchpriority="high">\n' % (PRE, pattern % (1000 if 1000 in widths else 1100),
                                                              ", ".join("%s%s %dw" % (PRE, pattern % x, x) for x in widths)))
    n = L.render(
        out=out, depth=2, active=None, gen="gen_cities.py (copy in tools/cities.py)",
        title=c["title"], description=c["description"], canonical=L.SITE + url(c),
        og_title=c["title"].split(" | ")[0] + " | Strategy Day, $1,500",
        og_description=c["description"],
        graph=graph(c), main=main_html(c), preload=preload, body_class="ww-page ct-page",
        reveal=(".ww-head", ".ct-local-grid > *", ".ww-profiles > li", ".ww-steps > li", ".sd-buy-grid > *",
                ".ww-item", ".hv-quotes > li", ".ct-net > li"),
    )
    print("written", out, n)
