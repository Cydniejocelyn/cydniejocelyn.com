"""Stamp the CSS and JS links with a content hash.

`vercel.json` used to mark everything under /assets/ immutable for a year,
including site.css and site.js, whose filenames never change. A returning
visitor was therefore pinned to the stylesheet they first downloaded while
the markup kept updating underneath it, which is how the hero arrived
unstyled: new HTML, year-old CSS.

The header is fixed, but `immutable` means a browser will not even
revalidate, so a changed URL is the only thing that rescues a cache that is
already poisoned. Run this after editing site.css or site.js.
"""
import hashlib, io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def h(rel):
    return hashlib.sha1(io.open(os.path.join(ROOT, rel), "rb").read()).hexdigest()[:8]

# Every file under /assets/css/ or /assets/js/, which vercel.json marks
# immutable for a year. Adding a file there and forgetting to add it here is
# how a reader gets pinned to a stale copy forever.
STAMPED = ("assets/css/site.css", "assets/js/site.js",
           "assets/js/analytics.js", "assets/js/consent.js")

def version():
    """The single definition of the ?v= hash.

    build.py imports this rather than recomputing it. It used to have its own
    copy of the arithmetic, and on 28 August 2026 adding analytics.js to this
    tuple made the two disagree: stamp.py wrote 38bd24d7 into all nine pages
    and build.py refused the build because it still expected 3a9791d6. The
    guard was right and the duplication was the bug.
    """
    return hashlib.sha1("".join(h(f) for f in STAMPED).encode()).hexdigest()[:8]

V = version()

PAGES = (
    ("index.html",                  "assets/"),
    ("about/index.html",            "../assets/"),
    ("the-build/index.html",        "../assets/"),
    ("retreats/index.html",         "../assets/"),
    ("retreats/greece/index.html",  "../../assets/"),   # two levels down
    ("retreats/gatlinburg/index.html", "../../assets/"),  # two levels down
    ("a-sounding/index.html",       "../assets/"),
    ("the-letters/index.html",      "../assets/"),
    ("privacy-policy/index.html",   "../assets/"),
    ("thequestions/index.html",     "../assets/"),
    ("contact/index.html",          "../assets/"),
)

for page, pre in PAGES:
    p = os.path.join(ROOT, page)
    s = io.open(p, encoding="utf-8").read()
    s = re.sub(r'href="' + re.escape(pre) + r'css/site\.css(\?v=[0-9a-f]+)?"',
               'href="' + pre + 'css/site.css?v=' + V + '"', s)
    s = re.sub(r'src="' + re.escape(pre) + r'js/site\.js(\?v=[0-9a-f]+)?"',
               'src="' + pre + 'js/site.js?v=' + V + '"', s)
    s = re.sub(r'src="' + re.escape(pre) + r'js/analytics\.js(\?v=[0-9a-f]+)?"',
               'src="' + pre + 'js/analytics.js?v=' + V + '"', s)
    s = re.sub(r'src="' + re.escape(pre) + r'js/consent\.js(\?v=[0-9a-f]+)?"',
               'src="' + pre + 'js/consent.js?v=' + V + '"', s)
    io.open(p, "w", encoding="utf-8").write(s)
print("stamped", V)
