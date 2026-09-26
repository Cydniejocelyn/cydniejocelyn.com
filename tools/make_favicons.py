"""The site icons, from Cydnie's 2026 monogram (26 September 2026).

Source: CydnieJocelyn-Site/NEW LOGOS 2026 PROPER LOGOS/Monogram.png, ink
letters only (the aqua hairline dropped: it vanishes below 48px), saved as
tools/cj-monogram-mask.png. Ink #0c2830 on the signature aqua #9fccc6, so
the icon holds on light and dark browser tabs. Small sizes are drawn a
little bolder, because the Light weight fades to nothing at 16px.

New file names on purpose: vercel.json caches /assets/img/* as immutable
for a year, so overwriting favicon-32.png would never reach a returning
visitor. favicon.ico sits at the root, outside that rule.

    python3 tools/make_favicons.py
"""
import json, os
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASK = Image.open(os.path.join(ROOT, "tools", "cj-monogram-mask.png")).convert("L")
AQUA, INK = (159, 204, 198, 255), (12, 40, 48, 255)


def tile(size, fill, bold=0):
    big = size * 8
    t = Image.new("RGBA", (big, big), AQUA)
    m = MASK.copy()
    sc = fill * big / max(m.size)
    m = m.resize((round(m.width * sc), round(m.height * sc)), Image.LANCZOS)
    if bold:
        m = m.filter(ImageFilter.MaxFilter(bold))
    t.paste(Image.new("RGBA", m.size, INK), ((big - m.width) // 2, (big - m.height) // 2 + round(big * .02)), m)
    return t.resize((size, size), Image.LANCZOS)


img = os.path.join(ROOT, "assets", "img")
small = {16: tile(16, .80, 7), 32: tile(32, .76, 5), 48: tile(48, .72, 3)}
small[16].save(os.path.join(img, "cj-icon-16.png"))
small[32].save(os.path.join(img, "cj-icon-32.png"))
small[48].save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)],
               append_images=[small[16], small[32]])
tile(180, .62).save(os.path.join(img, "cj-apple-180.png"))
tile(192, .56).save(os.path.join(img, "cj-icon-192.png"))
tile(512, .56).save(os.path.join(img, "cj-icon-512.png"))
json.dump({
    "name": "Cydnie Jocelyn", "short_name": "Cydnie Jocelyn", "start_url": "/",
    "display": "browser", "background_color": "#ffffff", "theme_color": "#ffffff",
    "icons": [
        {"src": "/assets/img/cj-icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
        {"src": "/assets/img/cj-icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
    ],
}, open(os.path.join(ROOT, "site.webmanifest"), "w"), indent=2)
print("icons written")
