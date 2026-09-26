"""Privacy policy and terms (/privacy-policy/), restyled 26 September 2026.

A RESTYLE ONLY. The legal text lives in tools/privacy_body.html, lifted
verbatim from the old page; change it there, and only with her word. Her
approved edits of 26 September, and nothing else:
  * the Fonts paragraph and "Adobe Fonts" in the tools list came out: the
    rebuilt site serves its own type (Instrument Sans / Serif), so both
    would have been false after launch;
  * Letters sign-ups are stored "in HoneyBook or Flodesk, depending on the
    form you used" (the page's form is HoneyBook, the popup is Flodesk),
    and both tool lines say so.
Every anchor is kept (#terms, #retreats and the rest are linked from the
retreat pages). No popups here, as before.

UPDATED is the "Last updated" line. Set it to the launch month in the
launch commit, not before (a future date on this page would be a lie).

    cd tools && python3 gen_privacy_policy.py
"""
import os
import lux_page as L

URL = L.SITE + "/privacy-policy/"
UPDATED = "August 2026"
raw = open(os.path.join(L.ROOT, "tools", "privacy_body.html"), encoding="utf-8").read()
TOC, BODY = raw.split("\n<!--BODY-->\n")

MAIN = """<main id="main">

<section class="lg-head" aria-labelledby="pv-h">
  <div class="hv-wrap">
    <span class="hv-label">Cydnie Jocelyn LLC</span>
    <h1 id="pv-h">Privacy Policy <em>and Terms of Use</em></h1>
    <p class="hv-lede">This page covers how Cydnie Jocelyn LLC collects and uses your information, and the terms that govern your use of this website. Where you have signed a separate agreement with Cydnie Jocelyn LLC, that agreement governs.</p>
    <p class="lg-stamp">Last updated: <b>%(UPDATED)s</b></p>
  </div>
</section>

<section class="lg-sec" aria-label="Privacy policy and terms of use">
  <div class="hv-wrap lg-doc">
%(TOC)s
    <div class="lg-body">
%(BODY)s
    </div>
  </div>
</section>

</main>
""" % {"UPDATED": UPDATED, "TOC": TOC, "BODY": BODY}

about = {n["@id"]: n for n in L.old_graph("about/index.html") if "@id" in n}
graph = [about.get(n.get("@id"), n) if n.get("@type") != "WebPage" else n
         for n in L.old_graph("privacy-policy/index.html")]

OUT = "privacy-policy/index.html"
L.render(
    out=OUT, depth=1, active=None,
    title="Privacy Policy and Terms of Use | Cydnie Jocelyn",
    description="How Cydnie Jocelyn LLC collects and uses your information, and the terms that govern your use of this website, a Sounding, a Build engagement and a retreat.",
    canonical=URL,
    og_title="Privacy Policy and Terms of Use | Cydnie Jocelyn",
    og_description="How Cydnie Jocelyn LLC collects and uses your information, and the terms that govern your use of this website.",
    graph=graph, main=MAIN, body_class="ww-page",
)
p = os.path.join(L.ROOT, OUT)
s = open(p, encoding="utf-8").read()
for tag in ('<script src="/sounding-popup.js" defer></script>\n', '<script src="/gatlinburg-popup.js" defer></script>\n'):
    assert s.count(tag) == 1, tag
    s = s.replace(tag, "")
open(p, "w", encoding="utf-8").write(s)
print("written", len(s))
