#!/usr/bin/env python3
"""Draw the contiguous United States as one SVG path, for the April 2027 card.

April is real, it is in the United States, and the location is not announced.
A stock photograph of somewhere it is not would be a lie, and an empty grey
box is a hole in the layout. So the card carries a map with nothing marked on
it: the country, drawn as a hairline in the brand's own ink, and a single open
ring where the pin would go.

The open ring is the site's own motif. The Fifteen mark on the home page fills
fourteen circles and leaves the fifteenth open, and that open one is the whole
argument. Here it is the same shape doing the same job: the thing that has not
been decided yet is drawn, not hidden.

The outline is the national border traced clockwise from Cape Flattery in
about ninety points, projected with a Lambert conformal conic, which is what a
US map is normally drawn on and is why the northern border curves rather than
running flat. It is deliberately coarse: the card renders it about 520px wide
and softens it, so anything finer would be thrown away.

    python3 tools/us_map.py            # writes assets/img/us-outline.svg
"""

import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "us-outline.svg")

# (lat, lon), clockwise from Cape Flattery. Coarse on purpose.
BORDER = [
    # --- the 49th parallel, west to east
    (48.39, -124.73), (49.00, -123.10), (49.00, -117.03), (49.00, -110.00),
    (49.00, -104.05), (49.00, -100.00), (49.00, -97.23), (49.38, -95.15),
    # --- the boundary waters and Lake Superior
    (48.62, -93.35), (48.35, -92.50), (48.10, -90.85), (48.00, -89.60),
    (47.20, -88.20), (46.75, -85.50), (46.50, -84.40),
    # --- Lake Huron
    (45.85, -84.72), (45.35, -82.55), (43.60, -82.10), (42.95, -82.42),
    # --- Lake Erie
    (41.70, -83.47), (41.95, -81.00), (42.55, -79.75), (42.90, -79.05),
    # --- Lake Ontario and the St Lawrence
    (43.28, -79.07), (43.60, -76.60), (44.10, -76.30), (44.55, -75.30),
    (45.01, -74.72),
    # --- the 45th parallel across Vermont and New Hampshire, then Maine
    (45.01, -71.50), (45.30, -71.10), (46.20, -70.25), (47.35, -69.22),
    (47.20, -68.00), (46.20, -67.79), (45.15, -67.05),
    # --- the Atlantic, north to south
    (44.50, -68.00), (43.70, -70.20), (42.90, -70.80), (42.05, -70.19),
    (41.35, -71.85), (40.63, -73.90), (39.40, -74.42), (38.80, -75.05),
    (37.90, -75.30), (36.93, -76.00), (35.90, -75.55), (35.22, -75.53),
    (34.60, -76.55), (33.85, -78.00), (32.75, -79.85), (32.03, -80.85),
    (30.70, -81.45), (29.20, -80.90), (28.40, -80.52), (26.60, -80.03),
    # --- Florida and the Gulf, east to west
    (25.15, -80.40), (25.85, -81.55), (27.90, -82.85), (29.15, -83.03),
    (29.70, -84.90), (30.15, -85.60), (30.40, -88.00), (30.25, -89.30),
    (29.15, -89.02), (29.30, -90.10), (29.70, -93.95), (28.95, -95.40),
    (27.80, -97.40), (25.95, -97.15),
    # --- the southern border, east to west
    (26.40, -99.10), (28.50, -100.40), (29.40, -101.00), (29.20, -103.00),
    (29.80, -104.70), (31.78, -106.48), (31.78, -108.21), (31.33, -108.21),
    (31.33, -111.07), (32.72, -114.72),
    # --- the Pacific, south to north
    (32.53, -117.12), (33.72, -118.25), (34.45, -120.47), (35.45, -120.90),
    (36.60, -121.90), (37.80, -122.52), (38.95, -123.73), (40.44, -124.41),
    (42.00, -124.40), (43.30, -124.40), (44.60, -124.07), (46.25, -124.05),
    (47.00, -124.20),
]

# Lake Michigan, traced as a hole. Without it the national border runs
# straight down the Ontario side and Michigan has no Lower Peninsula, which is
# the one omission a reader in Minnesota would notice immediately. The other
# Great Lakes need no hole: their northern shores are the border already.
LAKE_MICHIGAN = [
    (45.85, -84.85), (45.10, -86.20), (44.00, -86.25), (42.80, -86.20),
    (41.70, -86.90), (41.70, -87.60), (43.10, -87.90), (44.55, -87.35),
    (45.15, -87.10), (45.60, -86.30),
]

# Lambert conformal conic, the standard for a US map: two standard parallels
# at 33 and 45 north, origin at 39N 96W. It is why the northern border curves.
LAT0, LON0, P1, P2 = 39.0, -96.0, 33.0, 45.0
R = 1.0


def project(lat, lon):
    r1, r2 = math.radians(P1), math.radians(P2)
    n = (math.log(math.cos(r1) / math.cos(r2)) /
         math.log(math.tan(math.pi / 4 + r2 / 2) / math.tan(math.pi / 4 + r1 / 2)))
    F = math.cos(r1) * math.tan(math.pi / 4 + r1 / 2) ** n / n
    def rho(la):
        return R * F / math.tan(math.pi / 4 + math.radians(la) / 2) ** n
    theta = n * math.radians(lon - LON0)
    r, r0 = rho(lat), rho(LAT0)
    # The textbook formula gives y increasing north. Screen y increases south,
    # so this is the textbook y negated. Getting that backwards draws a map
    # that is upside down and still looks vaguely plausible, which is worse
    # than one that looks obviously wrong.
    return r * math.sin(theta), r * math.cos(theta) - r0


def build():
    pts = [project(la, lo) for la, lo in BORDER]
    lake = [project(la, lo) for la, lo in LAKE_MICHIGAN]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    W, H, PAD = 1000.0, None, 12.0
    scale = (W - PAD * 2) / (maxx - minx)
    H = (maxy - miny) * scale + PAD * 2

    def to(p):
        return (PAD + (p[0] - minx) * scale, PAD + (p[1] - miny) * scale)

    d = []
    for ring in (pts, lake):
        for i, p in enumerate(ring):
            x, y = to(p)
            d.append(("M" if i == 0 else "L") + "%.1f %.1f" % (x, y))
        d.append("Z")

    # Where the open ring sits. Not a location: it is placed in the middle of
    # the country, off the exact centre, so it reads as "somewhere here" rather
    # than as a pin in a city nobody has been told about yet.
    mx, my = to(project(40.5, -95.0))

    return ("".join(d), W, H, mx, my)


PATH, W, H, MX, MY = build()

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %(w).0f %(h).0f"
     role="img" aria-labelledby="usmap-t" class="usmap" preserveAspectRatio="xMidYMid meet">
  <title id="usmap-t">A map of the United States with no location marked on it</title>
  <defs>
    <!-- The country fades at its edges rather than stopping on a hard line,
         which is the same seam construction the page's own sections use. -->
    <radialGradient id="usmap-veil" cx="50%%" cy="46%%" r="62%%">
      <stop offset="0%%"   stop-color="#fff" stop-opacity="1"/>
      <stop offset="62%%"  stop-color="#fff" stop-opacity="1"/>
      <stop offset="100%%" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
    <mask id="usmap-mask">
      <rect width="%(w).0f" height="%(h).0f" fill="url(#usmap-veil)"/>
    </mask>
  </defs>
  <g mask="url(#usmap-mask)">
    <path class="usmap-fill" fill-rule="evenodd" d="%(d)s"/>
    <path class="usmap-line" d="%(d)s" pathLength="1"/>
  </g>
  <g class="usmap-pin" transform="translate(%(mx).1f %(my).1f)">
    <circle class="usmap-ring" r="21"/>
    <circle class="usmap-ring usmap-ring--out" r="38"/>
  </g>
</svg>
""" % {"w": W, "h": H, "d": PATH, "mx": MX, "my": MY}

# The card inlines the SVG rather than linking it, because an <img src=".svg">
# cannot be coloured or animated from the page's stylesheet and this one is
# both. Inlining means the markup holds a copy of the geometry, so the copy is
# written by this script between the markers rather than pasted by hand.
PAGE = os.path.join(ROOT, "retreats", "index.html")
START, END = "<!-- US-MAP:START -->", "<!-- US-MAP:END -->"


def inject():
    with open(PAGE, encoding="utf-8") as fh:
        html = fh.read()
    if START not in html or END not in html:
        raise SystemExit("markers missing in %s" % os.path.relpath(PAGE, ROOT))
    head = html[:html.index(START) + len(START)]
    tail = html[html.index(END):]
    body = "\n" + "\n".join("          " + ln for ln in SVG.strip().splitlines()) + "\n          "
    with open(PAGE, "w", encoding="utf-8") as fh:
        fh.write(head + body + tail)


if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(SVG)
    inject()
    print("wrote %s and inlined it into %s  (%d x %d, %d border points)"
          % (os.path.relpath(OUT, ROOT), os.path.relpath(PAGE, ROOT),
             W, H, len(BORDER)))
