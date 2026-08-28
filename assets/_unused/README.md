# Not deployed, not deleted

Every file in here was in `assets/img/` and **no shipped page, stylesheet or
script referenced it.** Together they were about 1MB uploaded on every deploy
to be downloaded by nobody.

They are moved rather than deleted because most of them are alternates of
things that are still in use, and the next person to want one should find it
rather than have to reconstruct it:

| | |
|---|---|
| `mark-horiz-dark-*` | superseded by `mark-horiz-ink-*`, which is the mark the header actually paints |
| `mark-horiz-ink-1200` | the header's `image-set()` uses 500 and 800 only. The mark renders at 240px, so 1200w is never the right candidate |
| `mark-stacked-light-*` | a stacked lockup. Nothing on the site uses one |
| `hero-1600.jpg` / `hero-800.jpg` | JPEG originals of files that ship as WebP at roughly half the bytes |
| `cydnie-hero-*`, `hero-underwater-*`, `retreat-steps-1200` | from earlier passes, replaced during the picture passes in sessions three and five |
| `icon-512.png` | was declared `<link rel="icon" sizes="512x512">`. A browser picking it to draw a 32px tab icon fetches 18KB to do it, and there is no web app manifest here that wants a 512. `favicon-32` and `apple-touch-icon` cover every consumer the site actually has |
| `us-outline.svg` | output of `tools/us_map.py`. The map that ships on the retreats page is inline SVG |

**Moved, not `.vercelignore`d, and that is the point.** An ignore rule keeps a
file working in preview and 404ing only in production, which is the worst
possible failure. Moved, a stale reference breaks in front of you the moment
you look at the page.

To bring one back: `git mv assets/_unused/<file> assets/img/`, then reference it.

`tools/build.py` prints a warning if anything in `assets/img/` becomes
unreferenced again, so this list cannot quietly regrow.
