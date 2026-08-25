"""Fold the site into one self-contained file for the Artifact viewer.

The viewer's CSP allows no external hosts except Google Fonts, so images are
inlined as data URIs and the typefaces are linked from Google. A published
fragment carries no <meta charset>, so the output is pure ASCII: markup uses
numeric entities, and the stylesheet and script are folded, since entities are
not parsed inside <style> or <script>.

Nothing here changes a design decision. site.css and site.js go through whole.
"""
import base64, os, re, sys

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# `python3 build_artifact.py about` folds the about page instead of the home
# page. Asset paths there are ../assets, so they are normalised on the way in.
PAGE = (sys.argv[1] if len(sys.argv) > 1 else "home").lower()
PAGES = {
    "home":  ("index.html",       "cydnie-jocelyn.html",       "The Resurfacing Business"),
    "about": ("about/index.html", "cydnie-jocelyn-about.html", "About Cydnie Jocelyn"),
}
if PAGE not in PAGES:
    raise SystemExit("unknown page %r, expected one of %s" % (PAGE, ", ".join(PAGES)))
SRCFILE, OUTFILE, TITLE = PAGES[PAGE]
OUT = os.path.join(SRC, "tools", OUTFILE)

html = open(os.path.join(SRC, SRCFILE), encoding="utf-8").read()
html = html.replace("../assets/", "assets/")
css  = open(os.path.join(SRC, "assets/css/site.css"), encoding="utf-8").read()
js   = open(os.path.join(SRC, "assets/js/site.js"), encoding="utf-8").read()

body   = html[html.index("<body>") + 6:html.index("</body>")]
schema = re.search(r'<script type="application/ld\+json">.*?</script>', html, re.S).group(0)

# Read the font link out of the page rather than restating it here. The last
# build hardcoded Cinzel and DM Sans and kept shipping them long after the
# stacks moved to Instrument and Plex, so the artifact was set in the wrong
# faces with no error anywhere.
fonts = re.search(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^"]*">', html).group(0)

# Every image the page actually renders. Keys are matched as substrings of the
# src path, so they have to stay distinct from one another.
PICK = {
    "reaching-shadow":    "reaching-shadow-632.webp",
    "cydnie-reading":     "cydnie-reading-1000.webp",
    "hero-line":          "hero-line-1717.webp",
    "cydnie-veil":        "cydnie-veil-1100.webp",
    "cydnie-hero":        "cydnie-hero-1400.webp",
    "layer-surface":      "layer-surface-1200.webp",
    "cydnie-reading":     "cydnie-reading-1000.webp",
    "armonia-arch":       "armonia-arch-900.webp",
    "mark-horiz-light":   "mark-horiz-light-800.webp",
    "mark-horiz-dark":    "mark-horiz-dark-800.webp",
}
data = {}
for stem, name in PICK.items():
    with open(os.path.join(SRC, "assets/img", name), "rb") as fh:
        data[stem] = "data:image/webp;base64," + base64.b64encode(fh.read()).decode()

# One resolution each, so srcset and sizes have nothing left to choose between.
# A <source> stripped of its srcset is ignored, and the <img> fallback stands.
body = re.sub(r'\s+srcset="[^"]*"', "", body)
body = re.sub(r'\s+sizes="[^"]*"', "", body)

missing = []
def swap(m):
    for stem, uri in data.items():
        if stem in m.group(1):
            return 'src="%s"' % uri
    missing.append(m.group(1))
    return 'src=""'

body = re.sub(r'src="(assets/img/[^"]+)"', swap, body)
body = body.replace('<script src="assets/js/site.js" defer></script>', "")
# An artifact is one page, so a link to another page of the site has nothing
# to reach. Rewriting `/#retreat` to `#retreat` made twelve dead anchors that
# swallowed the click silently; absolute URLs at least say where they go.
SITE = "https://cydniejocelyn.com"
body = body.replace('href="/#', 'href="%s/#' % SITE)
body = body.replace('href="/about/"', 'href="%s/about/"' % SITE)
body = body.replace('href="/"', 'href="%s/"' % SITE)

# pages that do not exist yet resolve to the on-page CTA
for dead in ('href="/contact/"', 'href="/legal/privacy/"', 'href="/legal/terms/"', 'href="/about/"'):
    body = body.replace(dead, 'href="#start"')
body = body.replace('href="/"', 'href="#main"')

entities = lambda t: "".join(c if ord(c) < 128 else "&#%d;" % ord(c) for c in t)
FOLD = {"—": "--", "–": "-", "’": "'", "‘": "'",
        "“": '"', "”": '"', "…": "...", "é": "e"}
def fold(t):
    for k, v in FOLD.items():
        t = t.replace(k, v)
    return "".join(c for c in t if ord(c) < 128)

body, schema = entities(body), entities(schema)
css, js = fold(css), fold(js)

out = (
    "<title>" + TITLE + "</title>\n"
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    + fonts + "\n" + schema
    + "\n<style>\n" + css + "\n</style>\n"
    # the head script the body slice leaves behind. Without it .js-motion is
    # never set and every reveal rule sits inert, so the page arrives finished
    # rather than arriving.
    + '<script>document.documentElement.className += " js-motion";</script>\n'
    + body + "\n<script>\n" + js + "\n</script>\n"
)

open(OUT, "w", encoding="ascii").write(out)
print("built   %s  (%s)" % (OUT, PAGE))
print("size    %.2f MB" % (os.path.getsize(OUT) / 1024 / 1024))
print("ascii   %s" % all(ord(c) < 128 for c in out))
print("fonts   %s" % fonts[fonts.index("family="):][:72])
print("missing %s" % (missing or "none"))
