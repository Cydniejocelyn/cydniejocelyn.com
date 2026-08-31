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
    "build": ("the-build/index.html", "cydnie-jocelyn-build.html", "The Build"),
    "retreats": ("retreats/index.html", "cydnie-jocelyn-retreats.html", "Retreats"),
    # two levels down, so its asset paths are ../../assets rather than ../assets
    "greece":   ("retreats/greece/index.html", "cydnie-jocelyn-greece.html",
                 "Rise Into Her: The Greece Edition"),
    "gatlinburg": ("retreats/gatlinburg/index.html", "cydnie-jocelyn-gatlinburg.html",
                 "Wide Open: The Gatlinburg Edition"),
    "sounding": ("a-sounding/index.html", "cydnie-jocelyn-sounding.html", "A Sounding"),
    "letters":  ("the-letters/index.html", "cydnie-jocelyn-letters.html", "The Letters"),
}
if PAGE not in PAGES:
    raise SystemExit("unknown page %r, expected one of %s" % (PAGE, ", ".join(PAGES)))
SRCFILE, OUTFILE, TITLE = PAGES[PAGE]
OUT = os.path.join(SRC, "tools", OUTFILE)

html = open(os.path.join(SRC, SRCFILE), encoding="utf-8").read()
# ../../ first: replacing ../assets/ on the Greece page would leave a stray
# ../ in front of every path it just rewrote.
html = html.replace("../../assets/", "assets/").replace("../assets/", "assets/")
css  = open(os.path.join(SRC, "assets/css/site.css"), encoding="utf-8").read()
js   = open(os.path.join(SRC, "assets/js/site.js"), encoding="utf-8").read()

body   = html[html.index("<body>") + 6:html.index("</body>")]
# A PAGE MAY LEGITIMATELY HAVE NO JSON-LD, and this used to die on one.
# Same shape as the Google Fonts crash written up below: `.group(0)` on a
# regex that matched nothing. /retreats/gatlinburg/ is pre-launch, so its
# structured data is parked in a comment until booking opens, and there is
# no script to find. An artifact of a page with no schema is a correct
# artifact of that page, not an error.
_schema = re.search(r'<script type="application/ld\+json">.*?</script>', html, re.S)
schema = _schema.group(0) if _schema else ""

# THE FACES ARE SELF HOSTED NOW, AND THIS USED TO CRASH.
# This read the Google Fonts <link> out of the page. The site stopped having
# one: the faces were self hosted in session, and `_test.html` asserts that no
# third party font stylesheet is on the critical path. So the regex matched
# nothing, `.group(0)` raised AttributeError, and the artifact build died
# outright rather than falling back to anything.
#
# The woff2 files are inlined into the folded stylesheet instead. They have to
# be: `url(../fonts/...)` resolves to nothing inside an artifact, and the
# viewer's CSP admits no host but Google Fonts, so there is nowhere to fetch
# them from. About 107KB of font becomes about 143KB of base64, which is
# nothing against the images.
#
# Every face the stylesheet names is inlined, including latin-ext and the
# serif italic. Dropping the ext faces would silently lose the accented
# characters that `unicode-range` exists to serve.
FONTDIR = os.path.join(SRC, "assets/fonts")
def inline_font(m):
    name = m.group(1)
    path = os.path.join(FONTDIR, name)
    if not os.path.exists(path):
        raise SystemExit("artifact: stylesheet names a font that is not there: " + name)
    with open(path, "rb") as fh:
        return "url(data:font/woff2;base64,%s) format('woff2')" % base64.b64encode(fh.read()).decode()
fontcount = len(re.findall(r"url\(\.\./fonts/([^)]+\.woff2)\) format\('woff2'\)", css))
css = re.sub(r"url\(\.\./fonts/([^)]+\.woff2)\) format\('woff2'\)", inline_font, css)
if not fontcount:
    raise SystemExit("artifact: no self hosted @font-face found; has the stylesheet moved?")

# IMAGES REFERENCED FROM THE STYLESHEET, which the swap below never sees.
# `swap` only rewrites `src="assets/img/..."` in the markup. The ink wordmark
# is not an <img>: it is a `background-image` on `.brand-mark--ink`, so it was
# left as `url(../img/...)`, resolved to nothing in the artifact, and the
# header published with an empty space where the logo goes.
#
# It went unnoticed until the home hero became light. The ink mark only shows
# once `.hdr.is-surfaced` is set, which used to mean "scrolled past a dark
# hero"; now the top of the page is light and the header is surfaced from the
# first pixel, so the missing asset is the first thing on the page.
def inline_css_img(m):
    name = m.group(1)
    path = os.path.join(SRC, "assets/img", name)
    if not os.path.exists(path):
        raise SystemExit("artifact: stylesheet names an image that is not there: " + name)
    with open(path, "rb") as fh:
        return "url(data:image/webp;base64,%s)" % base64.b64encode(fh.read()).decode()

cssimg = len(re.findall(r"url\(\.\./img/([^)]+)\)", css))
css = re.sub(r"url\(\.\./img/([^)]+)\)", inline_css_img, css)


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
    # the ink wordmark, for once the reader has surfaced. mark-horiz-dark is
    # the half submerged drawing and is no longer referenced by any page.
    "mark-horiz-ink":     "mark-horiz-ink-800.webp",
    # The Build's work block. Unused stems cost nothing: `data` is only ever
    # consumed by `swap`, which matches against the src actually in the markup.
    "mane-alchemist-mark":     "work/mane-alchemist-mark-900.webp",
    "mane-alchemist-screen":   "work/mane-alchemist-screen-500.webp",
    "srs-performance-mark":    "work/srs-performance-mark-900.webp",
    "srs-performance-screen":  "work/srs-performance-screen-500.webp",
    "solyrey-mark":            "work/solyrey-mark-900.webp",
    "solyrey-screen":          "work/solyrey-screen-500.webp",
    # The retreat pages. One resolution each, the 600 wide variant, because
    # these two pages carry twenty photographs between them and the artifact
    # inlines every one of them as base64. This list is exactly what the two
    # pages render: a stem here that no page uses keeps a file alive that
    # nothing needs, which is how 3.5MB of dead assets accumulated once.
    "retreat-steps":      "retreat-steps-1200.webp",
    "retreats/cr-horizon": "retreats/cr-horizon-600.webp",
    "retreats/cr-dusk":    "retreats/cr-dusk-600.webp",
    "retreats/cr-room":    "retreats/cr-room-600.webp",
    "retreats/cr-floor":   "retreats/cr-floor-600.webp",
    "retreats/cr-surf":    "retreats/cr-surf-600.webp",
    "retreats/kris":       "retreats/kris-600.webp",
    "cydnie-greece":       "retreats/cydnie-greece-600.webp",
    "melissa-poster":     "retreats/melissa-poster-405.webp",
    "greece/house":       "greece/house-600.webp",
    "greece/drive":       "greece/drive-600.webp",
    "greece/olive":       "greece/olive-600.webp",
    "greece/path":        "greece/path-600.webp",
    "greece/deck":        "greece/deck-600.webp",
    "greece/studio":      "greece/studio-600.webp",
    "greece/room":        "greece/room-600.webp",
    "greece/bath":        "greece/bath-600.webp",
    "greece/lounge":      "greece/lounge-600.webp",
    "greece/dining":      "greece/dining-600.webp",
    "greece/sauna":       "greece/sauna-600.webp",
    "greece/barrel":      "greece/barrel-600.webp",
    "greece/grounds":     "greece/grounds-600.webp",
    "greece/lawn":        "greece/lawn-600.webp",
    "greece/pool-view":   "greece/pool-view-600.webp",
    "greece/pool-":       "greece/pool-600.webp",
    "greece/dinner":      "greece/dinner-600.webp",
    "greece/table":       "greece/table-600.webp",
    "greece/kitchen":     "greece/kitchen-600.webp",
    "greece/pergola":     "greece/pergola-600.webp",
    # Gatlinburg. Ten photographs of the house plus Kayla; Cydnie reuses the
    # standing retreat portrait the Greece page already folds.
    "gatlinburg/house-dusk":  "gatlinburg/house-dusk-600.webp",
    "gatlinburg/deck-view":   "gatlinburg/deck-view-600.webp",
    "gatlinburg/porch-swing": "gatlinburg/porch-swing-600.webp",
    "gatlinburg/porch-":      "gatlinburg/porch-600.webp",
    "gatlinburg/great-room":  "gatlinburg/great-room-600.webp",
    "gatlinburg/bar":         "gatlinburg/bar-600.webp",
    "gatlinburg/kitchen":     "gatlinburg/kitchen-600.webp",
    "gatlinburg/gym":         "gatlinburg/gym-600.webp",
    "gatlinburg/king-suite":  "gatlinburg/king-suite-600.webp",
    "gatlinburg/bunk-room":   "gatlinburg/bunk-room-600.webp",
    "gatlinburg/kayla":       "gatlinburg/kayla-600.webp",
    "gatlinburg/ridge":       "gatlinburg/ridge-600.webp",
    "gatlinburg/hot-tub-stone":   "gatlinburg/hot-tub-stone-600.webp",
    "gatlinburg/hot-tub":         "gatlinburg/hot-tub-600.webp",
    "gatlinburg/sunset":          "gatlinburg/sunset-600.webp",
    "gatlinburg/deck-table":      "gatlinburg/deck-table-600.webp",
    "gatlinburg/living":          "gatlinburg/living-600.webp",
    "gatlinburg/kitchen-wide":    "gatlinburg/kitchen-wide-600.webp",
    "gatlinburg/king-balcony":    "gatlinburg/king-balcony-600.webp",
    "gatlinburg/bedroom-ridge":   "gatlinburg/bedroom-ridge-600.webp",
    "gatlinburg/bunks-blue":      "gatlinburg/bunks-blue-600.webp",
    "gatlinburg/bath-round":      "gatlinburg/bath-round-600.webp",
    "gatlinburg/bath-double":     "gatlinburg/bath-double-600.webp",
    "gatlinburg/shower":          "gatlinburg/shower-600.webp",
    "gatlinburg/gym-wide":        "gatlinburg/gym-wide-600.webp",
    "gatlinburg/theater":         "gatlinburg/theater-600.webp",
    "gatlinburg/games":           "gatlinburg/games-600.webp",
}
# PICK covers every page this tool can fold, so most of it is irrelevant to
# whichever one is being built, and it goes stale as the site's assets move.
# It used to open all of them eagerly: on 29 August that made the whole build
# die on `reaching-shadow-632.webp`, an image no page renders any more.
#
# A stem whose file is gone is skipped rather than fatal. That is safe because
# `swap` records anything the page actually asks for and cannot find, and the
# check below turns that into a hard failure. A review artifact with a blank
# photograph in it is worse than one that refuses to build.
data, absent = {}, []
for stem, name in PICK.items():
    path = os.path.join(SRC, "assets/img", name)
    if not os.path.exists(path):
        absent.append(name)
        continue
    with open(path, "rb") as fh:
        data[stem] = "data:image/webp;base64," + base64.b64encode(fh.read()).decode()

# One resolution each, so srcset and sizes have nothing left to choose between.
# A <source> stripped of its srcset is ignored, and the <img> fallback stands.
body = re.sub(r'\s+srcset="[^"]*"', "", body)
body = re.sub(r'\s+sizes="[^"]*"', "", body)

missing = []
def swap(m):
    # Longest stem first. These are substring matches, so `greece/pool-`
    # would otherwise claim `greece/pool-view-600.webp` and both tiles would
    # show the same photograph.
    for stem in sorted(data, key=len, reverse=True):
        uri = data[stem]
        if stem in m.group(1):
            return 'src="%s"' % uri
    missing.append(m.group(1))
    return 'src=""'

body = re.sub(r'src="(assets/img/[^"]+)"', swap, body)

# THE LIGHTBOX READS `data-full`, AND IT WAS NEVER SWAPPED. Every gallery
# tile carries the path of its full size file; inside an artifact that path
# reaches nothing, so the tiles looked right and every one of them opened a
# broken picture. Caught on the Gatlinburg page, where twenty tiles made it
# obvious; the Greece artifact has had it all along. Same swap, and the same
# `missing` list catches a stem that is not inlined.
def swap_full(m):
    for stem in sorted(data, key=len, reverse=True):
        if stem in m.group(1):
            return 'data-full="%s"' % data[stem]
    missing.append(m.group(1))
    return 'data-full=""'

body = re.sub(r'data-full="(assets/img/[^"]+)"', swap_full, body)
# the asset links now carry a ?v= build id, so match past it
body = re.sub(r'<script src="assets/js/site\.js[^"]*" defer></script>', "", body)
# An artifact is one page, so a link to another page of the site has nothing
# to reach. Rewriting `/#retreat` to `#retreat` made twelve dead anchors that
# swallowed the click silently; absolute URLs at least say where they go.
SITE = "https://cydniejocelyn.com"

# The two pages are published as two artifacts, so a cross page link inside
# one of them is pointed at the other one's artifact. Without this, About in
# the nav sent the reader to a domain that is not live yet, and the preview
# stopped being a site you could walk. On the real build these stay `/about/`
# and `/`; only the artifact is rewritten.
ARTIFACT = {
    "home":  "https://claude.ai/code/artifact/df17491f-9b21-42bd-bb29-60f3d77f8cb5",
    "about": "https://claude.ai/code/artifact/edb8e6b0-19ba-4048-801b-ffc570b75551",
    # The Build has not been published as an artifact yet. Until it is, a link
    # to it resolves to the canonical URL, which at least says where it goes.
    # Put the artifact URL here the first time it is published.
    "build": None,
    # Neither retreat page has been published as an artifact yet. Put the URL
    # here the first time one is.
    "retreats": None,
    "greece":   None,
    # Neither new page has been published as an artifact yet either.
    "sounding": None,
    "letters":  None,
}
BUILD_HREF = ARTIFACT["build"] or (SITE + "/the-build/")
body = body.replace('href="/the-build/#',
                    'href="#' if PAGE == "build" else 'href="%s#' % BUILD_HREF)
body = body.replace('href="/the-build/"',
                    'href="#main"' if PAGE == "build" else 'href="%s"' % BUILD_HREF)
# a link to the page you are already on is an anchor, not a trip out
body = body.replace('href="/about/"',
                    'href="#main"' if PAGE == "about" else 'href="%s"' % ARTIFACT["about"])
# a root anchor is a section of the home page: an anchor when you are on it,
# a trip to the home artifact when you are not
body = body.replace('href="/#', 'href="#' if PAGE == "home" else 'href="%s#' % ARTIFACT["home"])
body = body.replace('href="/"',
                    'href="#main"' if PAGE == "home" else 'href="%s"' % ARTIFACT["home"])

# The retreats pages, same rule as The Build: an anchor when you are already
# on that page, the other artifact when there is one, the canonical URL when
# there is not.
RETREATS_HREF = ARTIFACT["retreats"] or (SITE + "/retreats/")
GREECE_HREF   = ARTIFACT["greece"]   or (SITE + "/retreats/greece/")
body = body.replace('href="/retreats/greece/"',
                    'href="#main"' if PAGE == "greece" else 'href="%s"' % GREECE_HREF)
body = body.replace('href="/retreats/#',
                    'href="#' if PAGE == "retreats" else 'href="%s#' % RETREATS_HREF)
body = body.replace('href="/retreats/"',
                    'href="#main"' if PAGE == "retreats" else 'href="%s"' % RETREATS_HREF)

# A Sounding and The Letters, same rule again. Both are in the nav and the
# footer of every page now, so without this an export carries two root
# relative hrefs that resolve to nothing inside an artifact.
SOUNDING_HREF = ARTIFACT["sounding"] or (SITE + "/a-sounding/")
LETTERS_HREF  = ARTIFACT["letters"]  or (SITE + "/the-letters/")
body = body.replace('href="/a-sounding/#',
                    'href="#' if PAGE == "sounding" else 'href="%s#' % SOUNDING_HREF)
body = body.replace('href="/a-sounding/"',
                    'href="#main"' if PAGE == "sounding" else 'href="%s"' % SOUNDING_HREF)
body = body.replace('href="/the-letters/"',
                    'href="#main"' if PAGE == "letters" else 'href="%s"' % LETTERS_HREF)

# pages that do not exist yet resolve to the on-page CTA. About is not one of
# them: it exists, it is in the nav, and it was only ever in this list because
# the replace above had already consumed it.
for dead in ('href="/contact/"', 'href="/legal/privacy/"', 'href="/legal/terms/"'):
    body = body.replace(dead, 'href="#start"')

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
    # No preconnect and no font host. Every face is a data URI in the
    # stylesheet below, so the artifact reaches no external origin at all.
    + schema
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
print("fonts   %d self hosted faces inlined" % fontcount)
print("cssimg  %d stylesheet image reference(s) inlined" % cssimg)
print("missing %s" % (missing or "none"))
print("skipped %d stale PICK entries" % len(absent))
if missing:
    raise SystemExit(
        "artifact: %d image(s) on this page could not be inlined and would "
        "publish blank:\n  %s\nAdd them to PICK, or point PICK at the "
        "resolution that still exists." % (len(missing), "\n  ".join(missing)))
