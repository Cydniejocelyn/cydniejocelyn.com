"""The Wild Canvas launch, as one run.

    python3 tools/launch_arizona.py            apply it to this tree
    python3 tools/launch_arizona.py --check    say whether it would apply

DO NOT RUN THIS UNTIL CYDNIE SAYS THE PAGE IS PUBLIC. Until then the page is
live at its URL and unfindable on purpose: noindex in the head, an
X-Robots-Tag on the route, absent from sitemap.xml, and linked from nowhere.
Every change here makes it findable.

IT REFUSES TO RUN WHILE A TODO IS LEFT ON THE PAGE. That is the point of the
yellow markers: each one is a fact Cydnie still owes the page (the three
HoneyBook links, the bathroom setup, the supplies, the departure timing, the
add-on workshops, what else is not included). A launch that ships one of them
is worse than no launch, and nothing else in the repo would catch it.

Every replacement matches on an exact string and asserts how many times it
occurs, per the rule in CLAUDE.md, and the script stops before writing
anything if one of them does not match. It writes nothing on a partial match.

After it runs, and before any push:

    python3 tools/build.py
    python3 tools/seams.py                      0
    sh tools/preview/runsuite.sh "$SP" <port>   all pass
    grep -c '<!--' dist/retreats/arizona/index.html     must be 0

THE ONE THING THIS CANNOT CHECK: that the HoneyBook records charge $1,675 and
$1,800 with a $500 deposit and five monthly payments. Cydnie looks.

Written 24 September 2026.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

edits = {}   # path -> text, written only when every step has matched


def load(path):
    if path not in edits:
        edits[path] = io.open(os.path.join(ROOT, path), encoding="utf-8").read()
    return edits[path]


def sub(path, old, new, count=1):
    s = load(path)
    n = s.count(old)
    if n != count:
        raise SystemExit("STOP: %s expected %d of %r, found %d. Nothing written."
                         % (path, count, old[:90], n))
    edits[path] = s.replace(old, new)


A = "retreats/arizona/index.html"
page = load(A)

if '<meta name="robots" content="noindex, nofollow, noarchive">' not in page:
    raise SystemExit("Already launched: the Arizona robots tag is gone. Nothing to do.")

# ---------------------------------------------- the TODO gate
todos = re.findall(r'class="az-todo[^"]*"[^>]*>(.*?)<', page, re.S)
if todos:
    print("STOP: %d TODO marker(s) are still on the page:" % len(todos))
    for t in todos:
        print("   -", re.sub(r"\s+", " ", t).strip()[:90])
    print("Fill them in first. Nothing written.")
    sys.exit(1)

parked_tk = re.findall(r'href="#tk-[a-z]+"', page)
if parked_tk:
    raise SystemExit("STOP: %d parked booking link(s) still point at #tk-. "
                     "Nothing written." % len(parked_tk))

if "--check" in sys.argv:
    print("Not launched yet, and no TODO markers left. "
          "Running without --check applies the launch.")
    sys.exit(0)

# ---------------------------------------------- 1. the locks come off
sub(A, '<meta name="robots" content="noindex, nofollow, noarchive">\n', "")
sub(A, '<meta name="googlebot" content="noindex, nofollow">\n', "")
sub(A, '<!-- AT LAUNCH: uncomment the canonical.\n'
       '<link rel="canonical" href="https://www.cydniejocelyn.com/retreats/arizona/">\n-->',
       '<link rel="canonical" href="https://www.cydniejocelyn.com/retreats/arizona/">')

# the pre-launch band
s = load(A)
# Already gone since 24 September: the page went live that evening as an
# unlinked, noindex landing page on Cydnie's word, and the band had to go
# first. Removed here only if some later edit put it back.
m = re.search(r'<!-- THE PRE-LAUNCH BAND\..*?</section>\n\n', s, re.S)
if m:
    edits[A] = s[:m.start()] + s[m.end():]

# ---------------------------------------------- 2. the JSON-LD, wrapped
s = load(A)
m = re.search(r'<!-- AT LAUNCH: uncomment, then validate before pushing\..*?\n(\{\n  "@context": "https://schema\.org",\n  "@type": "Event".*?\n\})\n-->', s, re.S)
if not m:
    raise SystemExit("STOP: the parked Arizona JSON-LD was not found. Nothing written.")
import json
event = json.loads(m.group(1))
# reuse the LocalBusiness node the Greece page carries, so the organiser is
# one entity across the site rather than three copies of a name
gr = load("retreats/greece/index.html")
org = None
for blk in re.findall(r'<script type="application/ld\+json">\n?(.*?)</script>', gr, re.S):
    for node in json.loads(blk).get("@graph", []):
        t = node.get("@type"); t = t if isinstance(t, list) else [t]
        if "LocalBusiness" in t:
            org = node
if not org:
    raise SystemExit("STOP: no LocalBusiness node on /retreats/greece/ to copy. Nothing written.")
event.pop("@context", None)
event["organizer"] = {"@id": org["@id"]}
graph = {"@context": "https://schema.org", "@graph": [org, event]}
edits[A] = (s[:m.start()] + '<script type="application/ld+json">\n'
            + json.dumps(graph, indent=2, ensure_ascii=False) + '\n</script>' + s[m.end():])

# ---------------------------------------------- 3. the route header
sub("vercel.json", '''    {
      "source": "/retreats/arizona/(.*)",
      "headers": [
        {
          "key": "X-Robots-Tag",
          "value": "noindex, nofollow, noarchive"
        }
      ]
    },
''', "")

# ---------------------------------------------- 4. the sitemap
s = load("sitemap.xml")
m = re.search(r'  <!-- /retreats/arizona/ is deliberately absent.*?-->\n', s, re.S)
if not m:
    raise SystemExit("STOP: the sitemap's Arizona comment was not found. Nothing written.")
edits["sitemap.xml"] = s[:m.start()] + '''  <url>
    <loc>https://www.cydniejocelyn.com/retreats/arizona/</loc>
    <lastmod>%s</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
''' % os.environ.get("LAUNCH_DATE", "2026-10-01") + s[m.end():]

# ---------------------------------------------- 5. the Retreats index card
#
# The "A third date is coming" card becomes the real one. Everything the
# mystery card withheld is named here: the retreat, the place, the price and
# the artist. The map figure goes with it, because there is a photograph now.
R = "retreats/index.html"
s = load(R)
start = s.index('      <!-- THE THIRD DATE')
end = s.index('      </article>\n', start) + len('      </article>\n')
ARROW = ('<svg class="arw" width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true">'
         '<path d="M9 1l4 4-4 4M13 5H0" stroke="currentColor" stroke-width="1.2"/></svg>')
edits[R] = s[:start] + '''      <!-- WILD CANVAS, launched. This card replaced the unnamed "A third
           date is coming" one, which carried the US map with no pin on it
           while the location was a secret. -->
      <article class="rt-date rt-date--flip r-up" id="may" aria-labelledby="may-h">
        <figure class="rt-date-fig">
          <img src="../assets/img/arizona/great-room-1000.webp"
               srcset="../assets/img/arizona/great-room-600.webp 600w, ../assets/img/arizona/great-room-1000.webp 1000w, ../assets/img/arizona/great-room-1450.webp 1450w"
               sizes="(min-width: 56rem) 45vw, 100vw" width="1450" height="992"
               loading="lazy" decoding="async"
               alt="A long open room with a hand painted desert sunset covering the far wall, a stone island with stools, and deep green sofas.">
        </figure>
        <div>
          <p class="rt-status">Booking open</p>
          <p class="rt-date-when">5&ndash;9 May 2027 &middot; Peoria, Arizona</p>
          <h3 class="head h-3" id="may-h">Wild Canvas: The Arizona Edition</h3>
          <p>Five days in a painted house on the edge of the Sonoran desert, with guided creative sessions led by abstract artist Dr. Clarissa Castillo-Ramsey. Lodging, every meal and the airport shuttles are included. No art experience needed.</p>
          <p>A shared room is $1,675 at the early rate. $500 holds your room.</p>
          <div class="actions">
            <a class="btn btn--solid" href="/retreats/arizona/"><span>See Wild Canvas and book</span>
              %s</a>
            <span class="note-under">The early rate holds through 30 November. Prices rise on 1 December.</span>
          </div>
        </div>
      </article>
''' % ARROW + s[end:]

# ---------------------------------------------- 6. write, only now
for path, text in edits.items():
    io.open(os.path.join(ROOT, path), "w", encoding="utf-8").write(text)
    print("wrote", path)

print("\nLaunch applied. Build, run seams and the suite, check the HoneyBook "
      "records, and read the page in a real browser before any push.")
