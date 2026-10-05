"""The 404 page (/404.html), added 5 October 2026 from the SEO audit.

Vercel serves dist/404.html for any path that does not exist, at that path,
so every asset reference here has to be absolute: a relative "assets/" would
resolve under /some/old/link/ and the page would arrive unstyled. render()
writes depth-0 relative paths; they are made absolute below and asserted.

The old Showit URLs that Google still indexes 301 in vercel.json; this page
catches whatever is left (old blog posts at the root, typos, dead pins).
noindex, no canonical, no popups.

    cd tools && python3 gen_404.py
"""
import os
import re
import lux_page as L

CALL, ARW = L.CALL, L.ARW
I = "/assets/img/"

LINKS = (
    ("/brand-strategy/", "Work with me", "Services and every price"),
    ("/brand-strategy/strategy-session/", "The Sounding", "A 90-minute strategy session"),
    ("/retreats/", "Retreats", "Small-group retreats for women"),
    ("/newsletter/", "The Letters", "A free weekly newsletter"),
    ("/about/", "About", "Who I am and how I work"),
    ("/contact/", "Contact", "A free call or a question"),
)

MAIN = """<main id="main">

<section class="ww-hero" aria-labelledby="nf-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <h1 class="hv-label" id="nf-h">Page not found</h1>
      <p class="ww-display">This page has <em>moved on.</em></p>
      <p class="hv-lede">The site was rebuilt in 2026, so an older link may have brought you here. Everything still exists, it just lives somewhere new.</p>
      <div class="hv-btns">
        <a class="hv-btn hv-btn--ink" href="/" data-cta="home-404">Go to the home page %(ARW)s</a>
        <a class="hv-btn hv-btn--line" href="%(CALL)s" data-cta="free-call-404">Book a free 30-min call</a>
      </div>
    </div>
    <figure class="ww-arch">
      <img src="%(I)scydnie-direct-1000.webp" srcset="%(I)scydnie-direct-600.webp 600w, %(I)scydnie-direct-1000.webp 1000w" sizes="(min-width: 64rem) 30rem, 90vw" width="1000" height="1500" alt="Cydnie Jocelyn smiling, in a denim jacket against a warm brown wall" fetchpriority="high">
    </figure>
  </div>
</section>

<section class="hv-sec" aria-labelledby="nf-where">
  <div class="hv-wrap">
    <span class="hv-label">Where things live now</span>
    <h2 class="hv-h2" id="nf-where">Try one of <em>these.</em></h2>
    <ul class="nf-links" role="list">
%(LINKS)s
    </ul>
  </div>
</section>

</main>
""" % {"CALL": CALL, "ARW": ARW, "I": I,
       "LINKS": "\n".join('      <li><a href="%s"><b>%s</b><span>%s</span></a></li>' % l for l in LINKS)}

OUT = "404.html"
L.render(
    out=OUT, depth=0, active=None,
    title="Page not found | Cydnie Jocelyn",
    description="This page has moved. Find Cydnie Jocelyn's services, retreats, The Letters and contact details here.",
    canonical=L.SITE + "/",
    og_title="Page not found | Cydnie Jocelyn",
    og_description="This page has moved. Everything still exists, it just lives somewhere new.",
    graph=[{"@type": "WebPage", "name": "Page not found", "isPartOf": {"@id": L.SITE + "/#website"}}],
    main=MAIN, body_class="ww-page", gen="gen_404.py",
    robots_html='<meta name="robots" content="noindex, follow">', canonical_html="",
)
p = os.path.join(L.ROOT, OUT)
s = open(p, encoding="utf-8").read()
for tag in ('<script src="/sounding-popup.js" defer></script>\n', '<script src="/gatlinburg-popup.js" defer></script>\n'):
    assert s.count(tag) == 1, tag
    s = s.replace(tag, "")
s = (s.replace('src="assets/', 'src="/assets/').replace('href="assets/', 'href="/assets/')
      .replace(' assets/img', ' /assets/img'))
assert not re.search(r'(?:src|href|srcset)="(?!/|https?:|#|mailto:|data:)', s), "relative path left in 404.html"
open(p, "w", encoding="utf-8").write(s)
print("written", len(s))
