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

    python3 tools/retreat_images.py
"""

import os
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARMONIA = os.path.join(
    ROOT,
    "CydnieJocelyn-Site",
    "08.13.2027-08.20.2027 | Crete Greece | Armonia Retreat Center copy",
    "Armonia Retreat Center",
    "wetransfer_armonia-retreat-photos_2026-06-01_1053",
)
COSTA = os.path.join(ROOT, "Costa Rica copy")

# slug -> (source file, [widths])
GREECE = {
    "house":     ("IMG_5369.JPG",        [600, 1200]),
    "drive":     ("MK_00872en-ps.jpg",   [600, 1200, 1800]),
    "olive":     ("MK_00878en.jpg",      [600, 1200]),
    "path":      ("IMG_5378.JPG",        [600, 1200]),
    "grounds":   ("MK_00950en-ps.jpg",   [600, 1200, 1800]),
    "room":      ("MK_09994en-ps.jpg",   [600, 1000]),
    "room-two":  ("MK_09949en-ps.jpg",   [600, 1000]),
    "bath":      ("Bathroom 3.jpg",      [600, 1200]),
    "lounge":    ("MK_00162en.jpg",      [600, 1000]),
    "dining":    ("MK_00132en.jpg",      [600, 1000]),
    "kitchen":   ("MK_00197en.jpg",      [600, 1000]),
    "pool":      ("NIK_5065.jpg",        [600, 1200, 1800]),
    "pool-view": ("NIK_5070.jpg",        [600, 1200, 1800]),
    "sauna":     ("IMG_5367.JPG",        [600, 900]),
    "barrel":    ("NIK_5097.jpg",        [600, 1200]),
    "studio":    ("studio.jpg",          [600, 1200]),
    "deck":      ("IMG_5365.JPG",        [600, 1200]),
    "dinner":    ("IMG_5381.JPG",        [600, 1200]),
    "pergola":   ("MK_01199enf-ps.jpg",  [600, 1000]),
    "table":     ("IMG_5371.JPG",        [600, 736]),
    "night":     ("IMG_5370.JPG",        [600, 1200]),
}

COSTA_RICA = {
    "cr-circle": ("DSC09026.jpg",  [600, 1200, 1800]),
    "cr-mats":   ("DSC09015.jpg",  [600, 1200]),
    "cr-pool":   ("DSC08975.JPG",  [600, 1200, 1800]),
    "cr-jump":   ("DSC09144.JPG",  [600, 1000]),
    "cr-hold":   ("DSC09104.jpg",  [600, 1000]),
    "cr-arrive": ("DSC09112.jpg",  [600, 1000]),
    "kris":      ("DSC08832.JPG",  [600, 1000]),
    "kris-lead": ("DSC08693.JPG",  [600, 1200]),
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
