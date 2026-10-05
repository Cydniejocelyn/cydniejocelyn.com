"""The five retreat guide pages (/womens-retreats/<slug>/), 5 October 2026.

Copy in retreat_places.py; this is the shared frame. Order on every page:

    hero (label as H1, the big line as styled text, per HANDOFF 80),
    why this place, the retreats that fit, what every retreat includes
    (or, on the leadership page, how a private retreat works), guests'
    words, questions, the other guides, close.

`guides_html()` is imported by gen_retreats.py, gen_gatlinburg.py and
gen_arizona.py, so the event pages and the hub link to every guide.

    python3 tools/gen_retreat_places.py
"""
import os
import lux_page as L
from retreat_places import PLACES, RETREATS, QUOTES, PRIVATE, GREECE_WAIT, url

ARW = L.ARW
PRE = "../../"

INCLUDED = [
    ("Everything handled", "Lodging, every meal and the plan for each day. You pack; the rest is done."),
    ("A small group", "Small enough to know everyone by the second night, and nobody asks you to share."),
    ("Your own pace", "Daily movement and sessions, every one optional. Rest counts."),
    ("$500 holds your room", "The balance can be spread out, and each retreat page lists exactly what is included."),
]
PRIVATE_STEPS = [
    ("Inquiry", "Tell me about your group, the dates you have in mind and where you would like to go."),
    ("Proposal", "I come back with the shape of the week, the location and the price, in writing."),
    ("Planning", "I book the house, plan the days and handle every meal and room."),
    ("The week", "Your group arrives. I host; you lead, or rest, or both."),
]


def guides_html(exclude=None, pre="/", head=True):
    """The row of guide links, for the guide pages, the hub and the event pages."""
    items = "\n".join('      <li><a href="%s"><span>%s</span><b>%s</b>%s</a></li>' % (url(p), p["short"], p["label"], ARW)
                      for p in PLACES if p["slug"] != exclude)
    return """<section class="hv-sec ct-net-sec" aria-labelledby="wr-guides">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Find your retreat</span>
      <h2 class="hv-h2" id="wr-guides">Women&rsquo;s retreats, <em>by place and purpose.</em></h2>
    </div>
    <ul class="ct-net" role="list">
%s
    </ul>
  </div>
</section>
""" % items


def card(k):
    r = RETREATS[k]
    btn = ('<a class="hv-btn hv-btn--ink" href="%s#rooms">Choose your room %s</a>' % (r["href"], ARW)) if k != "gr" else \
          ('<a class="hv-btn hv-btn--ink" href="%s">Join the waitlist %s</a>' % (GREECE_WAIT, ARW))
    note = '<p class="wr-note">%s</p>' % r["note"] if r["note"] else ""
    return """      <li class="wr-card">
        <span class="hv-label">%(tag)s</span>
        <p class="wr-when">%(when)s &middot; %(where)s</p>
        <h3><a href="%(href)s">%(name)s</a></h3>
        <p>%(text)s</p>
        <p class="wr-price">%(price)s</p>
        %(note)s
        <div class="hv-btns">%(btn)s<a class="hv-btn hv-btn--line" href="%(href)s">See the retreat</a></div>
      </li>""" % dict(r, btn=btn, note=note)


def main_html(p):
    pattern, widths, w, h, alt = p["img"]
    big = max(x for x in widths if x <= 1000) if any(x <= 1000 for x in widths) else widths[0]
    src = PRE + "assets/img/" + pattern % big
    srcset = ", ".join("%sassets/img/%s %dw" % (PRE, pattern % x, x) for x in widths)
    lead = p["slug"] == "leadership"
    if lead:
        cta = '<a class="hv-btn hv-btn--ink" href="%s" data-cta="private-retreat-guide">Start a private inquiry %s</a>' % (PRIVATE, ARW)
        cta2 = '<a class="hv-btn hv-btn--line" href="/retreats/">See the open retreats</a>'
        trust = "<li>Your group</li><li>Your dates</li><li>Your location</li>"
    else:
        first = RETREATS[p["retreats"][0]]
        cta = '<a class="hv-btn hv-btn--ink" href="#retreats">See the dates %s</a>' % ARW
        cta2 = '<a class="hv-btn hv-btn--line" href="%s">%s</a>' % (first["href"], first["name"].split(":")[0])
        trust = "<li>Meals included</li><li>A small group</li><li>$500 holds a room</li>"
    why_body = "\n".join("        <p>%s</p>" % x for x in p["why_p"])
    why_items = "\n".join('      <li><h3>%s</h3><p>%s</p></li>' % x for x in p["why_items"])
    if lead:
        middle = """<section class="hv-sec ww-path" id="how" aria-labelledby="wr-how">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">How it works</span>
      <h2 class="hv-h2" id="wr-how">From inquiry <em>to the week.</em></h2>
    </div>
    <ol class="ww-steps" role="list">
%s
    </ol>
    <p class="ww-menu-note"><a class="hv-link" href="%s">Start a private inquiry</a></p>
  </div>
</section>""" % ("\n".join('      <li><h3>%s</h3><p>%s</p></li>' % s for s in PRIVATE_STEPS), PRIVATE)
    else:
        middle = """<section class="hv-sec ww-path" id="retreats" aria-labelledby="wr-dates">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">The retreats</span>
      <h2 class="hv-h2" id="wr-dates">Where you <em>could be.</em></h2>
    </div>
    <ul class="wr-cards" role="list">
%s
    </ul>
  </div>
</section>

<section class="hv-sec" aria-labelledby="wr-inc">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Every retreat</span>
      <h2 class="hv-h2" id="wr-inc">What you can <em>count on.</em></h2>
    </div>
    <ul class="ww-profiles wr-inc" role="list">
%s
    </ul>
  </div>
</section>""" % ("\n".join(card(k) for k in p["retreats"]),
                 "\n".join('      <li><h3>%s</h3><p>%s</p></li>' % x for x in INCLUDED))
    quotes = "\n".join('      <li><figure class="hv-q"><blockquote><p>&ldquo;%s&rdquo;</p></blockquote><figcaption>%s &middot; Retreat guest, Costa Rica</figcaption></figure></li>'
                       % QUOTES[q] for q in p["quotes"])
    close_btn = cta if lead else '<a class="hv-btn hv-btn--ink" href="#retreats">Choose your retreat %s</a>' % ARW
    return """<main id="main">

<section class="ww-hero" aria-labelledby="wr-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <h1 class="hv-label" id="wr-h">%(label)s</h1>
      <p class="ww-display">%(display)s</p>
      <p class="hv-lede">%(lede)s</p>
      <div class="hv-btns">
        %(cta)s
        %(cta2)s
      </div>
      <ul class="ww-trust" role="list">%(trust)s</ul>
    </div>
    <figure class="ww-arch">
      <img src="%(src)s" srcset="%(srcset)s" sizes="(min-width: 64rem) 30rem, 90vw" width="%(w)d" height="%(h)d" alt="%(alt)s" fetchpriority="high">
      <figcaption><span>%(cap0)s</span><b>%(cap1)s</b></figcaption>
    </figure>
  </div>
</section>

<section class="hv-sec ct-local" aria-labelledby="wr-why">
  <div class="hv-wrap">
    <div class="ct-local-grid">
      <div>
        <span class="hv-label">%(why_label)s</span>
        <h2 class="hv-h2" id="wr-why">%(why_h2)s</h2>
      </div>
      <div class="hv-body">
%(why_body)s
      </div>
    </div>
    <ul class="ww-profiles" role="list">
%(why_items)s
    </ul>
  </div>
</section>

%(middle)s

<section class="hv-sec" aria-labelledby="wr-words">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Guest reviews</span>
      <h2 class="hv-h2" id="wr-words">In their <em>words.</em></h2>
      <p class="hv-lede">From the women at the last retreat, in Costa Rica. <a class="hv-inline" href="/retreats/">Watch Melissa&rsquo;s video</a> on the retreats page.</p>
    </div>
    <ul class="hv-quotes sd-quotes" role="list">
%(quotes)s
    </ul>
  </div>
</section>

<section class="hv-sec" id="faq" aria-labelledby="faq-h">
  <div class="hv-wrap hv-faq ww-faq">
    <div>
      <span class="hv-label">Questions</span>
      <h2 class="hv-h2" id="faq-h">Before you <em>book.</em></h2>
      <p class="hv-lede">Something not here? <a class="hv-inline" href="/contact/">Ask me directly</a>, or write to hello@cydniejocelyn.com.</p>
    </div>
    <div class="hv-faq-list">
%(faq)s
    </div>
  </div>
</section>

%(guides)s
<section class="hv-close" aria-labelledby="close-h">
  <div class="hv-wrap">
    <span class="hv-label hv-label--c">Your week away</span>
    <h2 class="hv-h2" id="close-h">%(close_h2)s</h2>
    <p class="hv-lede">Not ready to choose? <a class="hv-inline" href="/newsletter/">The Letters</a> hear about every new retreat first.</p>
    <div class="hv-btns">%(close_btn)s</div>
  </div>
</section>

</main>
""" % dict(p, cta=cta, cta2=cta2, trust=trust, src=src, srcset=srcset, w=w, h=h, alt=alt, cap0=p["cap"][0], cap1=p["cap"][1],
           why_body=why_body, why_items=why_items, middle=middle, quotes=quotes, faq=L.faq_html(p["faq"]),
           guides=guides_html(exclude=p["slug"]), close_btn=close_btn)


ORG = [n for n in L.old_graph("index.html") if isinstance(n.get("@type"), list) and "LocalBusiness" in n["@type"]][0]


def graph(p):
    import html as _h
    u = L.SITE + url(p)
    name = _h.unescape(p["label"])
    nodes = [
        ORG,
        {"@type": "WebPage", "@id": u + "#webpage", "url": u, "name": p["title"], "description": p["description"],
         "isPartOf": {"@id": L.SITE + "/#website"}, "about": {"@id": ORG["@id"]},
         "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Home", "item": L.SITE + "/"},
             {"@type": "ListItem", "position": 2, "name": "Retreats", "item": L.SITE + "/retreats/"},
             {"@type": "ListItem", "position": 3, "name": name, "item": u}]}},
        L.faq_node(u, p["faq"]),
    ]
    if p["retreats"]:
        nodes.append({"@type": "ItemList", "@id": u + "#retreats", "name": name,
                      "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": L.SITE + RETREATS[k]["href"],
                                           "name": _h.unescape(RETREATS[k]["name"])} for i, k in enumerate(p["retreats"])]})
    else:
        nodes.append({"@type": "Service", "@id": u + "#service", "name": "Private women's leadership retreats",
                      "serviceType": "Leadership retreat", "provider": {"@id": ORG["@id"]}, "url": u,
                      "areaServed": [{"@type": "State", "name": "Minnesota"}, {"@type": "Country", "name": "United States"}],
                      "description": p["description"]})
    return nodes


if __name__ == "__main__":
    for p in PLACES:
        out = "womens-retreats/%s/index.html" % p["slug"]
        os.makedirs(os.path.join(L.ROOT, os.path.dirname(out)), exist_ok=True)
        pattern, widths, w, h, alt = p["img"]
        big = max(x for x in widths if x <= 1000)
        preload = ('<link rel="preload" as="image" href="%sassets/img/%s" imagesrcset="%s" imagesizes="(min-width: 64rem) 30rem, 90vw" '
                   'type="image/webp" fetchpriority="high">\n' % (PRE, pattern % big,
                   ", ".join("%sassets/img/%s %dw" % (PRE, pattern % x, x) for x in widths)))
        n = L.render(
            out=out, depth=2, active="/retreats/", gen="gen_retreat_places.py (copy in tools/retreat_places.py)",
            title=p["title"], description=p["description"], canonical=L.SITE + url(p),
            og_title=p["title"].split(" | ")[0], og_description=p["description"],
            graph=graph(p), main=main_html(p), preload=preload, body_class="ww-page wr-page",
            reveal=(".ww-head", ".ct-local-grid > *", ".ww-profiles > li", ".ww-steps > li", ".wr-card",
                    ".hv-quotes > li", ".ct-net > li"),
        )
        print("written", out, n)
