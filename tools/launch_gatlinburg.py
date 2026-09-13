"""Phase 5 of the home restructure brief: the Gatlinburg launch, as one run.

    python3 tools/launch_gatlinburg.py            apply it to this tree
    python3 tools/launch_gatlinburg.py --check    say whether it would apply

DO NOT RUN THIS UNTIL CYDNIE SAYS GATLINBURG IS PUBLIC. The brief holds the
swap for Wednesday 16 September and says "prepare only". Until then the page
is live but unfindable on purpose (HANDOFF section 50), and every change here
makes it findable: the home page and the Retreats index link to it, the
noindex comes off, and it goes into the sitemap.

It is a script rather than an edit in the working tree because Phases 1 to 4
are sitting uncommitted in the same files. Putting the swap in those files
would launch Gatlinburg the next time anything else is pushed.

Every replacement matches on an exact string and asserts how many times it
occurs, per the rule in CLAUDE.md, and the script stops before writing
anything if one of them does not match. It writes nothing on a partial match.

After it runs, and before any push:

    python3 tools/build.py
    python3 tools/seams.py                      0
    sh tools/preview/runsuite.sh "$SP" 8814     all pass
    grep -c '<!--' dist/retreats/gatlinburg/index.html     must be 0

THE ONE THING THIS CANNOT CHECK: that the four HoneyBook service records
charge $2,790, $2,900, $1,490 and $1,600 with a $500 deposit. The brief
requires the page and HoneyBook to match on launch day. Cydnie looks.

Written 12 September 2026.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARROW = ('<svg class="arw" width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true">'
         '<path d="M9 1l4 4-4 4M13 5H0" stroke="currentColor" stroke-width="1.2"/></svg>')

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


def between(path, start, end, new):
    """Replace from `start` through `end` inclusive; both must occur once."""
    s = load(path)
    for marker in (start, end):
        if s.count(marker) != 1:
            raise SystemExit("STOP: %s expected one %r, found %d. Nothing written."
                             % (path, marker[:90], s.count(marker)))
    a = s.index(start)
    b = s.index(end, a) + len(end)
    edits[path] = s[:a] + new + s[b:]


# ---------------------------------------------------------------- 0. guard
G = "retreats/gatlinburg/index.html"
if '<meta name="robots" content="noindex, nofollow, noarchive">' not in load(G):
    raise SystemExit("Already launched: the Gatlinburg robots tag is gone. Nothing to do.")
if "--check" in sys.argv:
    print("Not launched yet. Running without --check applies Phase 5.")
    sys.exit(0)

# ------------------------------------------ 1. the page: indexable, with schema
sub(G, '<meta name="robots" content="noindex, nofollow, noarchive">\n', "")
sub(G, '<meta name="googlebot" content="noindex, nofollow">\n', "")
sub(G, '<!-- AT LAUNCH: uncomment the canonical.\n<link rel="canonical" href="https://www.cydniejocelyn.com/retreats/gatlinburg/">\n-->',
    '<link rel="canonical" href="https://www.cydniejocelyn.com/retreats/gatlinburg/">')
s = load(G)
m = re.search(r'<!-- AT LAUNCH: uncomment, then validate before pushing\..*?\n(\{\n  "@context": "https://schema\.org",\n  "@type": "Event".*?\n\})\n-->', s, re.S)
if not m:
    raise SystemExit("STOP: the parked Gatlinburg JSON-LD was not found. Nothing written.")
# An indexable page on this site carries the organisation node, with the same
# areaServed as every other page; the suite asserts it. It is taken from the
# Greece page so the two cannot drift, and the event points at it by @id.
import json
event = json.loads(m.group(1))
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
edits[G] = (s[:m.start()] + '<script type="application/ld+json">\n'
            + json.dumps(graph, indent=2, ensure_ascii=False) + '\n</script>' + s[m.end():])

# vercel.json: the X-Robots-Tag block scoped to the page
sub("vercel.json", '''    {
      "source": "/retreats/gatlinburg/(.*)",
      "headers": [
        {
          "key": "X-Robots-Tag",
          "value": "noindex, nofollow, noarchive"
        }
      ]
    },
''', "")

# sitemap: add the URL, drop the pre-launch comment
s = load("sitemap.xml")
m = re.search(r'  <!-- /retreats/gatlinburg/ is deliberately absent too.*?-->\n', s, re.S)
if not m:
    raise SystemExit("STOP: the sitemap's Gatlinburg comment was not found. Nothing written.")
edits["sitemap.xml"] = s[:m.start()] + '''  <url>
    <loc>https://www.cydniejocelyn.com/retreats/gatlinburg/</loc>
    <lastmod>2026-09-16</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
''' + s[m.end():]

# ------------------------------------------------- 2. home, section 6 becomes Gatlinburg
H = "index.html"
between(H, '<section class="section z-light" data-zone style="--from:var(--deepwater)" id="retreat" aria-labelledby="retreat-h">',
        '        <figcaption>Armonia Retreat Center, Douliana, Crete</figcaption>\n      </figure>\n    </div>\n  </div>\n</section>',
'''<section class="section z-light" data-zone style="--from:var(--deepwater)" id="retreat" aria-labelledby="retreat-h">
  <!-- PHASE 5, GATLINBURG. Section 6 was Greece, which is sold out; it is now
       the retreat a reader can book, and Greece is one line under it. The one
       scarcity line is the 1 November price rise, because it is the only real
       one. No popup, per the brief: the section is the announcement. -->
  <div class="wrap">
    <div class="retreat-grid">
      <div class="retreat-copy">
        <p class="eyebrow r-fade">Booking open &middot; April 2027</p>
        <h2 class="carved c-2 split" id="retreat-h">Wide Open.<br>The Gatlinburg edition.</h2>
        <div class="stack r-up" style="--d:120ms; margin-top:var(--s-5)">
          <p class="lead">Five days in a private house at the edge of the Smoky Mountains. Lodging, every meal, daily movement and two workshops are included.</p>
          <p class="muted">You fly into Knoxville, and from the airport forward the logistics are ours.</p>
        </div>
        <dl class="meta-list r-up" style="--d:180ms">
          <div><dt>Dates</dt><dd><time datetime="2027-04-13">13</time>&ndash;<time datetime="2027-04-18">18 April 2027</time></dd></div>
          <div><dt>Where</dt><dd>Gatlinburg, Tennessee</dd></div>
          <div><dt>Shared room</dt><dd>$1,490</dd></div>
          <div><dt>Private king suite</dt><dd>$2,790</dd></div>
          <div><dt>Deposit</dt><dd>$500 holds your room</dd></div>
          <div><dt>Fly into</dt><dd>Knoxville, TYS</dd></div>
        </dl>
        <p class="retreat-rise r-up" style="--d:200ms">The early rate holds through 31 October. Prices rise on 1 November.</p>
        <div class="actions r-up" style="--d:220ms; margin-top:var(--s-5)">
          <a class="btn" href="/retreats/gatlinburg/"><span>Everything about Gatlinburg</span>
            ''' + ARROW + '''</a>
          <a class="link" href="/retreats/gatlinburg/#rooms">Choose your room</a>
        </div>
        <p class="small r-up retreat-also" style="--d:240ms">Greece, August 2027, is sold out. <a class="link" href="https://clients.cydniejocelyn.com/public/6a21d07b6dcfbe3d85c663b6" rel="noopener">The waitlist is open<span class="vh"> (opens my scheduling page)</span></a>.</p>
        <p class="small r-up" style="--d:260ms; margin-top:var(--s-4)"><a class="more" href="/retreats/"><span>How the retreats work</span>
          ''' + ARROW + '''</a></p>
      </div>
      <figure class="retreat-fig r-img">
        <img src="assets/img/gatlinburg/house-dusk-portrait-834.webp"
             srcset="assets/img/gatlinburg/house-dusk-portrait-600.webp 600w, assets/img/gatlinburg/house-dusk-portrait-834.webp 834w"
             sizes="(min-width: 56rem) 40vw, 100vw" width="834" height="1112"
             loading="lazy" decoding="async"
             alt="A timber house on a wooded slope at dusk, its windows lit, with the ridgeline of the Smoky Mountains behind it.">
        <figcaption>The house, Gatlinburg, Tennessee</figcaption>
      </figure>
    </div>
  </div>
</section>''')

sub("assets/css/site.css", "/* ---------- ONE PAGE GRID, 12 September",
'''/* Phase 5: the one scarcity line under the Gatlinburg facts, and Greece as
   a single line beneath the buttons. */
.retreat-rise { margin: var(--s-4) 0 0; font-size: .9375rem; color: var(--ink); }
.retreat-also { margin-top: var(--s-5); padding-top: var(--s-4); border-top: 1px solid var(--rule); color: var(--muted); max-width: 34rem; }

/* ---------- ONE PAGE GRID, 12 September''')

# ------------------------------------------------- 3. the Retreats index
R = "retreats/index.html"
sub(R, '<meta name="description" content="Small group retreats for women, capped at fifteen. Crete in August 2027 and a US date in April 2027. From Forest Lake, Minnesota.">',
       '<meta name="description" content="Small group retreats for women. Gatlinburg, Tennessee in April 2027, booking now, and Crete in August 2027. From Forest Lake, Minnesota.">')
sub(R, '<meta name="twitter:description" content="Crete in August 2027, a second date in April 2027, and private retreats by inquiry.">',
       '<meta name="twitter:description" content="Gatlinburg in April 2027, booking now, Crete in August 2027, and private retreats by inquiry.">')
sub(R, '"description": "Small group retreats for women, capped at fifteen. Crete in August 2027, a second date in April 2027, and private retreats by inquiry.",',
       '"description": "Small group retreats for women. Gatlinburg, Tennessee in April 2027, Crete in August 2027, and private retreats by inquiry.",')
sub(R, '''          "name": "April 13–18, 2027, location to be announced"
''', '''          "name": "Wide Open: The Gatlinburg Edition",
          "url": "https://www.cydniejocelyn.com/retreats/gatlinburg/"
''')
sub(R, '      <div><dt>Greece</dt><dd>$3,450</dd></div>',
       '      <div><dt>Gatlinburg</dt><dd>From $1,490</dd></div>\n      <div><dt>Greece</dt><dd>$3,450</dd></div>')
OLD_PRICE_Q = "Greece is $3,450, with a $500 non-refundable deposit. April 2027 is not priced yet; when it is, the letters hear first. Every figure is published on the retreat’s own page."
NEW_PRICE_Q = "Gatlinburg is $1,490 for a shared room and $2,790 for the private king suite at the early rate, through 31 October 2026, and $500 holds your room. Greece is $3,450, with a $500 non-refundable deposit. Every figure is published on the retreat’s own page."
sub(R, OLD_PRICE_Q, NEW_PRICE_Q)
s = load(R)
m = re.search(r'<p>Greece is \$3,450, with a \$500 non-refundable deposit\. April 2027 is not priced yet; when it is, <a class="link" href="/the-letters/">the letters</a> hear first\.(.*?)</p>', s, re.S)
if not m:
    raise SystemExit("STOP: the visible pricing answer on /retreats/ was not found. Nothing written.")
edits[R] = s[:m.start()] + "<p>" + NEW_PRICE_Q.replace("’", "&rsquo;") + "</p>" + s[m.end():]

# the April card becomes the Gatlinburg card; id="april" stays for old links
between(R, '      <article class="rt-date r-up" id="april" aria-labelledby="april-h">',
        '''            <span class="note-under">No payment. Early rate held for the list.</span>
          </div>
        </div>
      </article>''',
'''      <article class="rt-date r-up" id="april" aria-labelledby="april-h">
        <figure class="rt-date-fig">
          <img src="../assets/img/gatlinburg/house-dusk-900.webp"
               srcset="../assets/img/gatlinburg/house-dusk-600.webp 600w, ../assets/img/gatlinburg/house-dusk-900.webp 900w, ../assets/img/gatlinburg/house-dusk-1200.webp 1200w"
               sizes="(min-width: 56rem) 45vw, 100vw" width="1600" height="1090"
               loading="lazy" decoding="async"
               alt="A timber house on a wooded slope at dusk, its windows lit, with the ridgeline of the Smoky Mountains behind it.">
        </figure>
        <div>
          <p class="rt-status">Booking open</p>
          <p class="rt-date-when">13&ndash;18 April 2027 &middot; Gatlinburg, Tennessee</p>
          <h3 class="head h-3" id="april-h">Wide Open: The Gatlinburg Edition</h3>
          <p>Five days in a private house at the edge of the Smoky Mountains, with Kayla Freeman leading the morning movement. Lodging, every meal, two workshops and two outings are included.</p>
          <p>A shared room is $1,490 and the private king suite is $2,790 at the early rate. $500 holds your room.</p>
          <div class="actions">
            <a class="btn" href="/retreats/gatlinburg/"><span>Everything about Gatlinburg</span>
              ''' + ARROW + '''</a>
            <span class="note-under">The early rate holds through 31 October. Prices rise on 1 November.</span>
          </div>
        </div>
      </article>''')

sub(R, '<p class="lead r-up" style="--d:60ms; margin-top:var(--s-5)">That is the number, not a tactic. April goes to the list before it goes anywhere else.</p>',
       '<p class="lead r-up" style="--d:60ms; margin-top:var(--s-5)">That is the number, not a tactic. Gatlinburg is booking now, and the early rate holds through 31 October.</p>')
sub(R, '''      <a class="btn btn--solid" href="https://www.honeybook.com/widget/cydnie_jocelyn_collective_299013/cf_id/69fa3c69e63a7a4c9bb354f1" rel="noopener">
        <span>Join the list for April</span>
        ''' + ARROW + '''
      <span class="vh"> (opens my scheduling page)</span></a>''',
'''      <a class="btn btn--solid" href="/retreats/gatlinburg/#rooms">
        <span>Choose your Gatlinburg room</span>
        ''' + ARROW + '''</a>''')

# ------------------------------------------------- 4. llms.txt
sub("llms.txt", '''- A second retreat runs in April 2027. Shorter, closer to home, same cap of fifteen. The date,
  location and price are not confirmed and are therefore not published. They go to the
  pre-registration list before they go anywhere else.''',
'''- Wide Open: The Gatlinburg Edition, 13 to 18 April 2027, in a private house in Gatlinburg,
  Tennessee, at the edge of the Great Smoky Mountains. With Cydnie Jocelyn and Kayla Freeman.
  Lodging, every meal, daily movement, two workshops and two outings included. Shared room
  $1,490 and private king suite $2,790 at the early rate through 31 October 2026, then $1,600
  and $2,900. $500 deposit. Fly into Knoxville (TYS); airfare is not included.
  https://www.cydniejocelyn.com/retreats/gatlinburg/''')

# ------------------------------------------------- write, only now
for path, text in edits.items():
    io.open(os.path.join(ROOT, path), "w", encoding="utf-8").write(text)
    print("wrote", path)
print("\nPhase 5 applied. Build, run seams and the suite, and check HoneyBook, before any push.")
