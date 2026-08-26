#!/usr/bin/env python3
"""Cut the retreat imagery out of the source libraries.

Two destinations, and they are kept apart on purpose:

  assets/img/greece/   Armonia Retreat Center and Douliana. Genuine Crete.
  assets/img/retreats/ Costa Rica, April 2026, plus Kris. Genuine Costa Rica.

The v2 drafts in `Greece Retreat/` hotlinked Showit URLs and captioned
several Costa Rica photographs as Crete -- a Costa Rica coastline as "the
coastline of western Crete", a sauna interior as "a meal at the retreat".
Every mapping below was checked against the actual pixels, and nothing
crosses from one folder to the other. If a caption cannot be honoured by a
real photograph, the figure is dropped rather than filled.

Sources are small: several Armonia files are only 1000-1075px wide, so the
emitted widths are capped at the source. No upscaling anywhere.

The tables below are exactly what the two pages render, and nothing else. The
first pass generated the whole shortlist and left 3.5MB of frames on disk that
no page ever pointed at. If a new figure is wanted, add the row here and add
the stem to PICK in `build_artifact.py` in the same commit.

Frames considered and not used are listed at the foot of this file, so the
next pass does not have to sift 296 photographs again.

    python3 tools/retreat_images.py
"""

import os
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING = os.path.join(ROOT, "CydnieJocelyn-Site", "Branding copy")
ARMONIA = os.path.join(
    ROOT,
    "CydnieJocelyn-Site",
    "08.13.2027-08.20.2027 | Crete Greece | Armonia Retreat Center copy",
    "Armonia Retreat Center",
    "wetransfer_armonia-retreat-photos_2026-06-01_1053",
)
COSTA = os.path.join(ROOT, "Costa Rica copy")

# slug -> (source file, [widths])
# The property gallery is a rail now, not five tiles, so it carries the whole
# house rather than a sample of it. Emitted at 600 and 900: a rail tile is
# about 360px wide on a desktop, so 900 covers it to 2.5x and anything larger
# is weight nobody sees.
GREECE = {
    # the rooms
    "room":      ("MK_09994en-ps.jpg",   [600, 1000]),
    "bath":      ("Bathroom 3.jpg",      [600, 900]),
    # the shared rooms
    "lounge":    ("MK_00162en.jpg",      [600, 900]),
    "dining":    ("MK_00132en.jpg",      [600, 900]),
    "kitchen":   ("MK_00197en.jpg",      [600, 900]),
    "studio":    ("studio.jpg",          [600, 1200]),
    # water and heat
    "pool":      ("NIK_5065.jpg",        [600, 1200]),
    "pool-view": ("NIK_5070.jpg",        [600, 1200, 1800]),
    "sauna":     ("IMG_5367.JPG",        [600, 900]),
    "barrel":    ("NIK_5097.jpg",        [600, 900]),
    # outside
    "house":     ("IMG_5369.JPG",        [600, 1200]),
    "drive":     ("MK_00872en-ps.jpg",   [600, 1200, 1800]),
    "olive":     ("MK_00878en.jpg",      [600, 1200]),
    "path":      ("IMG_5378.JPG",        [600, 1200]),
    "grounds":   ("MK_00950en-ps.jpg",   [600, 900]),
    "lawn":      ("MK_00449.jpg",        [600, 900]),
    "deck":      ("IMG_5365.JPG",        [600, 1200]),
    "dinner":    ("IMG_5381.JPG",        [600, 1200]),
    "pergola":   ("MK_01199enf-ps.jpg",  [600, 1000]),
    "table":     ("IMG_5371.JPG",        [600, 736]),
}


COSTA_RICA = {
    # The first pass used the pool candids. They are true and they are not the
    # best thing in this library: a headland across still water is the brand's
    # own picture, and Cydnie has thousands of frames of exactly that. These
    # six are the ones the Retreats page runs on now.
    "cr-horizon": ("IMG_4352.jpg", [600, 1200, 1800]),   # the hero
    "cr-dusk":    ("e0a610b5-bab4-42c4-8fbf-0e65fbbcf09a.jpg", [600, 1200, 1536]),
    "cr-room":    ("IMG_0784.jpg", [600, 1200, 1800]),
    "cr-cards":   ("DSC09127.jpg", [600, 1000]),
    "cr-water":   ("IMG_4900.jpg", [600, 1000]),
    "kris":       ("DSC08832.JPG", [600, 1000]),
}

# Cydnie's own portrait for the hosts block. The three portraits already on the
# site -- cydnie-hero, cydnie-reading, cydnie-veil -- are all seated and all
# spoken for by the home and About pages. This one stands, three-quarter, warm
# ground, which is the same shape as Kris's and the reason the pair now reads
# as a pair.
CYDNIE = {
    "cydnie-greece": ("Minnesota Wedding Photographer-93.jpg", [600, 1000]),
}


def index(root):
    """Case-insensitive filename index. The Costa Rica library has the same
    frame filed under several folders with different case on the extension."""
    found = {}
    for dirpath, _, names in os.walk(root):
        for n in names:
            found.setdefault(n.upper(), os.path.join(dirpath, n))
    return found


def emit(src, out_dir, slug, widths):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w0, h0 = im.size
    made = []
    for w in widths:
        if w > w0:                       # never upscale
            w = w0
        if any(m[1] == w for m in made):
            continue
        h = round(h0 * w / w0)
        out = os.path.join(out_dir, "%s-%d.webp" % (slug, w))
        # Quality falls with size. These pages carry twenty photographs
        # each; at q82 the wide variants alone ran over 4MB.
        q = 82 if w <= 700 else 76 if w <= 1200 else 70
        im.resize((w, h), Image.LANCZOS).save(out, "WEBP", quality=q, method=6)
        made.append((out, w, h))
    return made


def run(table, source_root, out_name):
    out_dir = os.path.join(ROOT, "assets", "img", out_name)
    os.makedirs(out_dir, exist_ok=True)
    files = index(source_root)
    for slug, (name, widths) in sorted(table.items()):
        src = files.get(name.upper())
        if not src:
            print("  MISSING %-12s %s" % (slug, name))
            continue
        for out, w, h in emit(src, out_dir, slug, widths):
            print("  %-34s %5d x %-5d %6.0f KB"
                  % (os.path.relpath(out, ROOT), w, h,
                     os.path.getsize(out) / 1024.0))


if __name__ == "__main__":
    print("Greece / Armonia:")
    run(GREECE, ARMONIA, "greece")
    print("Costa Rica:")
    run(COSTA_RICA, COSTA, "retreats")
    print("Branding:")
    run(CYDNIE, BRANDING, "retreats")


# Considered, not shipped. Paths are relative to `Costa Rica copy/` unless
# marked. Kept here so the next pass does not re-sift the library.
#
#   IMG_4351/4353/4375   more of the same headland, different light
#   IMG_4470/4471        sunset and rock at Playa Pelada
#   IMG_4234, IMG_4785   the pool with nobody in it, day and dusk
#   IMG_4864             the estuary from above, almost abstract
#   IMG_4939             the kitchen, one guest cooking
#   DSC09043             the whole group under the pavilion, wide
#   DSC09104/09112/09125 the goodbyes on the last morning
#   DSC08975, DSC09144   the pool session and the jump
#   IMG_4198             a guest at the pool edge in a sun hat
#   (Armonia) NIK_5097   the barrel sauna in the grounds
#   (Armonia) IMG_5367   the sauna interior
#   (Armonia) MK_00950   palms and the garden path
#   (Armonia) MK_09949   the second bedroom
