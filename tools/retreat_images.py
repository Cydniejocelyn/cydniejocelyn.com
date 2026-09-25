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
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

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
    # own picture, and Cydnie has thousands of frames of exactly that.
    #
    # SECOND PICTURE PASS, 26 August 2026, on Cydnie's note that two of these
    # clashed with the site. Both were replaced rather than reprocessed,
    # because the clash was the subject and not the grade:
    #
    #   cr-cards  DSC09127  amber floorboards under low sun, with a spread of
    #             rainbow oracle cards on them. Two saturated colour families
    #             the palette does not contain, in the same frame. Replaced by
    #             DSC09043, the whole group on the floor among palms, seen
    #             mostly from behind. It carries the same caption honestly and
    #             its dominant register is green, which sits beside Breath and
    #             Meniscus rather than fighting them.
    #
    #   cr-water  IMG_4900  a guest facing camera, posed, holding a coconut.
    #             It is a holiday snapshot, it is the one frame on the page
    #             that looks like stock, and the alt text shipped describing a
    #             completely different photograph: "walking alone out of the
    #             surf". Replaced by IMG_4894, two women from behind standing
    #             in the shallows, which is what the caption always claimed.
    #             It is also the coolest frame in the library.
    #
    # Slugs renamed with the pictures. A stem that still said `cards` when the
    # photograph has no cards in it is how the caption bugs in the drafts got
    # missed in the first place.
    "cr-horizon": ("IMG_4352.jpg", [600, 1200, 1800]),   # the hero
    "cr-dusk":    ("e0a610b5-bab4-42c4-8fbf-0e65fbbcf09a.jpg", [600, 1200, 1536],
                   {"color": 0.60, "contrast": 0.94}),
    "cr-room":    ("IMG_0784.jpg", [600, 1200, 1800]),
    # A light pull only. The floorboards and one coral vest are the warm mass
    # in this frame; at 0.85 they settle beside Held instead of shouting over
    # it, and the greens are still green. Anything lower started bleaching the
    # palms, which are the reason the picture works.
    "cr-floor":   ("DSC09043.jpg", [600, 1000],
                   {"ratio": 0.62, "center": (0.5, 0.42), "color": 0.85}),
    "cr-surf":    ("IMG_4894.jpg", [600, 1000]),
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

# A Sounding, 22 September 2026. The page had no photograph at all, and it is
# the page every main button on the site points at ("I am the brand. I must
# be sold."). Three frames, sides alternating down the page: standing in the
# head, holding a sheet of paper beside the written page, looking straight
# out beside "you don't need me", and the full bleed band of her at work. Frame -104 was the first pick for the head and was dropped:
# it is the same pose, jacket and laptop as -54, which is the About head.
SOUNDING = {
    "cydnie-stand": ("Minnesota Wedding Photographer-18.jpg", [700, 1000, 1400]),
    "cydnie-page":  ("Minnesota Wedding Photographer-19.jpg", [600, 1000]),
    # -20, not -36: the close up was the first pick and is motion blurred at
    # the size the page shows it. -20 is sharp and looks straight at her.
    "cydnie-direct": ("Minnesota Wedding Photographer-20.jpg", [600, 1000]),
    # The full bleed band under the statement: black and white, on the floor
    # with the notebook, laptop and mug. The work, not the pose. Cropped to
    # 1.75:1 from the top of the frame: at 2:1 centred the band's parallax
    # overhang took the top of her head off.
    "cydnie-work":  ("Minnesota Wedding Photographer-108.jpg", [900, 1400, 2048],
                     {"ratio": 1.75, "center": (0.5, 0.0)}),
}


def index(root):
    """Case-insensitive filename index. The Costa Rica library has the same
    frame filed under several folders with different case on the extension."""
    found = {}
    for dirpath, _, names in os.walk(root):
        for n in names:
            found.setdefault(n.upper(), os.path.join(dirpath, n))
    return found


def emit(src, out_dir, slug, widths, grade=None, crisp=False):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")

    # A box, where the frame was cut by hand: (left, top, right, bottom) as
    # fractions of the source. Applied before anything else, so a `ratio`
    # after it trims the box rather than the whole frame. It exists so the
    # hand cuts live in the table and can be made again, instead of being
    # lost with the session that made them (which happened to four of
    # Arizona's, and they had to be recovered by matching pixels).
    if grade and grade.get("box"):
        x0, y0, x1, y1 = grade["box"]
        w0, h0 = im.size
        im = im.crop((round(x0 * w0), round(y0 * h0), round(x1 * w0), round(y1 * h0)))

    # A grade, where one frame needs calming rather than replacing. Only
    # cr-dusk uses it. That photograph is the one unguarded thing on the
    # Retreats page and Cydnie wants to keep it; it had also been through
    # heavy HDR before it reached here, and arrived as neon teal against neon
    # orange. At full strength it was the loudest thing on a site whose whole
    # palette is restrained. 0.60 saturation keeps the sky and the moment and
    # drops the neon; 0.50 went flat and lost the light on the water. The
    # small contrast pull is because the HDR had already crushed the shadows.
    if grade:
        if grade.get("color") is not None:
            im = ImageEnhance.Color(im).enhance(grade["color"])
        if grade.get("contrast") is not None:
            im = ImageEnhance.Contrast(im).enhance(grade["contrast"])

        # A crop, where the page wants a portrait and the frame is landscape.
        # `.pair .layer-fig img` is aspect-ratio 0.62/1 with object-fit cover,
        # so a 3:2 frame dropped in there loses 59% of its width to a crop
        # nobody chose. cr-floor is a wide group shot and the middle third of
        # it cuts two women in half. Framing it here makes the decision once,
        # in a file, instead of leaving it to the viewport.
        if grade.get("ratio"):
            r = grade["ratio"]
            cx, cy = grade.get("center", (0.5, 0.5))
            w0, h0 = im.size
            tw, th = (w0, round(w0 / r)) if w0 / h0 > r else (round(h0 * r), h0)
            im = ImageOps.fit(im, (tw, th), Image.LANCZOS, centering=(cx, cy))

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
        out_im = im.resize((w, h), Image.LANCZOS)
        if crisp:
            # CRISP, for sources that arrive soft. Arizona's are listing
            # screenshots, already resized once by the listing site, and
            # Cydnie read them as blurry on 24 September. A light unsharp
            # mask after the resize restores edge contrast without halos
            # (radius under a pixel, threshold 3 so flat walls and sky stay
            # smooth), and the quality floor rises so the edges it restores
            # are not smeared straight back out by the encoder.
            out_im = out_im.filter(ImageFilter.UnsharpMask(radius=0.8, percent=70, threshold=3))
            q = max(q, 84 if w <= 700 else 82 if w <= 1200 else 78)
        out_im.save(out, "WEBP", quality=q, method=6)
        made.append((out, w, h))
    return made


def run(table, source_root, out_name, crisp=False):
    out_dir = os.path.join(ROOT, "assets", "img", out_name)
    os.makedirs(out_dir, exist_ok=True)
    files = index(source_root)
    for slug, spec in sorted(table.items()):
        name, widths = spec[0], spec[1]
        grade = spec[2] if len(spec) > 2 else None
        src = files.get(name.upper())
        if not src:
            print("  MISSING %-12s %s" % (slug, name))
            continue
        for out, w, h in emit(src, out_dir, slug, widths, grade, crisp):
            print("  %-34s %5d x %-5d %6.0f KB"
                  % (os.path.relpath(out, ROOT), w, h,
                     os.path.getsize(out) / 1024.0))


# WILD CANVAS: THE ARIZONA EDITION, May 2027, added 21 September 2026.
# Nine listing screenshots, 1636 to 1944px wide, so every width below is
# capped at the source the same way Gatlinburg's are. TWO FRAMES ARE
# DELIBERATELY NOT HERE: the pool at dusk, because the mural on that wall
# paints the property's name across it, and the street elevation, because it
# is a house on a named street with a number on it. Cydnie is keeping the
# location quiet ("I want to keep the location a secret right now"), and a
# photograph gives an address away as surely as a sentence does.
ARIZONA_SRC = os.path.join(ROOT, "Wild Canva The Arizona Edition May 5-9")
ARIZONA = {
    "great-room":  ("Screenshot 2026-09-03 at 6.13.02 AM.png", [600, 1000, 1600]),
    "kitchen":     ("Screenshot 2026-09-03 at 6.12.56 AM.png", [600, 1000, 1600]),
    "patio":       ("Screenshot 2026-09-03 at 6.13.16 AM.png", [600, 1000, 1600]),
    "room-saguaro":("Screenshot 2026-09-03 at 6.13.40 AM.png", [600, 1000]),
    "room-palms":  ("Screenshot 2026-09-03 at 6.13.47 AM.png", [600, 1000]),
    "room-dusk":   ("Screenshot 2026-09-03 at 6.13.55 AM.png", [600, 1000]),
    "bath":        ("Screenshot 2026-09-03 at 6.14.21 AM.png", [600, 1000]),
    "lounge":      ("Screenshot 2026-09-03 at 6.14.49 AM.png", [600, 1000, 1600]),

    # A second set arrived 24 September, and it is the half of the house the
    # first set did not show: what a guest does between sessions. Cydnie:
    # "Highlight that there will be mini golf, bowling onsite as well as a
    # 2 person sauna, small gym, tons of creative games."
    "patio-dusk":  ("Screenshot 2026-09-24 at 2.46.09 PM.png", [600, 1000, 1702]),
    "bar-dusk":    ("Screenshot 2026-09-24 at 2.46.37 PM.png", [600, 1000, 1702]),
    "minigolf":    ("Screenshot 2026-09-24 at 2.46.32 PM.png", [600, 1000, 1702]),
    "bowling":     ("Screenshot 2026-09-24 at 2.47.22 PM.png", [600, 1000, 1702]),
    "sauna-gym":   ("Screenshot 2026-09-24 at 2.46.43 PM.png", [600, 1000, 1702]),
    "games":       ("Screenshot 2026-09-24 at 2.47.51 PM.png", [600, 1000, 1702]),
    "arcade":      ("Screenshot 2026-09-24 at 2.47.41 PM.png", [600, 1000]),
    # THE HERO since 24 September evening: the long table set for dinner at
    # dusk. Cydnie asked for a different hero; the great room went back to
    # being a rail frame. The portrait is the phone hero, 3:4 on the table.
    "table-set":   ("Screenshot 2026-09-24 at 2.44.37 PM.png", [600, 1000, 1702]),
    "table-set-portrait": ("Screenshot 2026-09-24 at 2.44.37 PM.png", [600, 1000],
                    {"box": (0.40, 0.0, 0.8977, 1.0), "ratio": 0.75}),
    "bath-white":  ("Screenshot 2026-09-24 at 2.45.51 PM.png", [600, 1000]),
    "room-arizona":("Screenshot 2026-09-24 at 2.45.09 PM.png", [600, 1000, 1702]),
    "room-teal":   ("Screenshot 2026-09-24 at 2.45.02 PM.png", [600, 1000, 1702]),
    "room-sports": ("Screenshot 2026-09-24 at 2.45.29 PM.png", [600, 1000]),
    # Added 24 September evening, when Cydnie asked for the frames that
    # "stand out": the dusk mural bedroom replaces the teal one in the room
    # band, and the bonsai on the set table replaces the bar at dusk in the
    # rail. The games room already here replaces the garage (sauna and gym).
    "room-moon":   ("Screenshot 2026-09-24 at 2.45.20 PM.png", [600, 1000, 1702]),
    "table-bonsai":("Screenshot 2026-09-24 at 2.46.21 PM.png", [600, 1000, 1702]),
    # THE POOL IS CUT BY BOX. The property's name is painted on the wall
    # behind it, high and left of centre, and no ratio crop clears it. The
    # box is 919 x 746 source pixels, so that is the largest this frame can
    # honestly be: the old pool-1000 was an upscale.
    "pool":        ("Screenshot 2026-09-24 at 2.47.10 PM.png", [600, 1000],
                    {"box": (0.46, 0.34, 1.0, 1.0)}),

    # THE HAND CUTS, recovered 24 September by matching the shipped files
    # back against these sources, and written down so they stop being lost.
    # The phone hero: the great room at 3:4, 744 source pixels wide. The old
    # file was 834, an upscale, on the first thing a phone reader sees.
    "great-room-portrait": ("Screenshot 2026-09-03 at 6.13.02 AM.png", [600, 1000],
                    {"box": (0.3007, 0.0, 0.8138, 1.0), "ratio": 0.75}),
    # Clarissa at the table, 4:5 from a 2401 x 3600 original. It was capped
    # at 1000, which is under what a Retina screen asks of the host pair.
    "clarissa":    ("unnamed.jpg", [600, 1000, 1400],
                    {"box": (0.0, 0.0633, 1.0, 0.8967), "ratio": 0.8}),
    # Holding her painting, the whole 1800 x 1201 frame.
    "clarissa-piece": ("unnamed-3.jpg", [600, 1000, 1450]),
    # NOT HERE: clarissa-face-72/144, a hand cut from unnamed-2.jpg at
    # (0.26, 0.031, 0.80, 0.391). Small, sharp already, and left alone.
}


if __name__ == "__main__":
    print("Greece / Armonia:")
    run(GREECE, ARMONIA, "greece")
    print("Costa Rica:")
    run(COSTA_RICA, COSTA, "retreats")
    print("Branding:")
    run(CYDNIE, BRANDING, "retreats")
    print("A Sounding:")
    run(SOUNDING, BRANDING, "")
    print("Arizona:")
    run(ARIZONA, ARIZONA_SRC, "arizona", crisp=True)


# Considered, not shipped. Paths are relative to `Costa Rica copy/` unless
# marked. Kept here so the next pass does not re-sift the library.
#
#   IMG_4351/4353/4375   more of the same headland, different light
#   IMG_4470/4471        sunset and rock at Playa Pelada
#   IMG_4234, IMG_4785   the pool with nobody in it, day and dusk
#   IMG_4864             the estuary from above, almost abstract
#   IMG_4939             the kitchen, one guest cooking
#   DSC09043             SHIPPED 26 Aug as cr-floor
#   DSC09104/09112/09125 the goodbyes on the last morning
#   DSC08975, DSC09144   the pool session and the jump
#   DSC09127             was cr-cards; amber floor and rainbow cards, cut
#   IMG_4900             was cr-water; posed with a coconut, cut
#   IMG_4894             SHIPPED 26 Aug as cr-surf
#   IMG_4198             a guest at the pool edge in a sun hat
#   (Armonia) NIK_5097   the barrel sauna in the grounds
#   (Armonia) IMG_5367   the sauna interior
#   (Armonia) MK_00950   palms and the garden path
#   (Armonia) MK_09949   the second bedroom
