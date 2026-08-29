#!/bin/sh
# Screenshot a built page, reliably.
#
#   sh tools/shot.sh <port> <path> <out.png> [width] [height] [#anchor|scrollY]
#
#   sh tools/shot.sh 8801 /            /tmp/hero.png   1440 900 0
#   sh tools/shot.sh 8801 /            /tmp/band.png   1440 820 band-h
#   sh tools/shot.sh 8801 /contact/    /tmp/ct.png      390 900 0
#
# WHY NOT JUST POINT CHROME AT THE PAGE
# -------------------------------------
# Three things break a naive `chrome --screenshot` on this site, and all three
# were rediscovered the hard way in session twenty-four:
#
# 1. THE REVEALS. Nearly everything is held at opacity 0 until an
#    IntersectionObserver fires, and it does not fire in a headless capture.
#    A direct screenshot returns a page of empty grounds. `tools/preview/_shot.html`
#    already solves this: it loads the page in a sized iframe and walks the
#    scroll down in steps, dispatching scroll events, so the reveals run.
#    That harness is what this script drives.
#
# 2. THE HOME PAGE'S RELATIVE PATHS. index.html links `assets/...` with no
#    leading slash, so a probe copy written to `/anything/index.html` 404s its
#    own stylesheet and you measure an unstyled page. Every measurement taken
#    that way in session twenty-four was wrong and had to be redone. The shot
#    harness sidesteps it entirely by loading the real URL in an iframe.
#
# 3. CHROME DOES NOT EXIT after --screenshot on this machine. Backgrounded,
#    polled for a file that has stopped growing, then killed. A foreground
#    call hangs until the tool times out.
#
# The Claude preview pane is not an alternative. It degrades to a zero-height
# viewport and then returns confidently wrong numbers: scrollHeight equal to
# scrollY, elementFromPoint null, contrast ratios computed against the wrong
# ground. See tools/preview/runsuite.sh, which says the same about the suite.
set -e
PORT="${1:?usage: sh tools/shot.sh <port> <path> <out.png> [w] [h] [#anchor|y]}"
PAGE="${2:?}"
OUT="${3:?}"
W="${4:-1440}"
H="${5:-900}"
AT="${6:-0}"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DIR=$(dirname "$OUT")
PROFILE="$DIR/.chrome-shot-$$"

case "$AT" in
  ''|*[!0-9]*) Q="id=$AT" ;;   # anything non-numeric is treated as an element id
  *)           Q="y=$AT"  ;;
esac

rm -f "$OUT"
( "$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
    --window-size="$W,$H" --virtual-time-budget=20000 --user-data-dir="$PROFILE" \
    --screenshot="$OUT" \
    "http://127.0.0.1:$PORT/_shot.html?p=$PAGE&w=$W&h=$H&$Q" >/dev/null 2>&1 & )

prev=0
i=0
while [ $i -lt 40 ]; do
  sleep 2
  cur=$(stat -f%z "$OUT" 2>/dev/null || echo 0)
  if [ "$cur" -gt 20000 ] && [ "$cur" = "$prev" ]; then break; fi
  prev=$cur
  i=$((i + 1))
done
pkill -f "$PROFILE" 2>/dev/null || true
sleep 1
rm -rf "$PROFILE" 2>/dev/null || true

if [ ! -s "$OUT" ]; then
  echo "no screenshot produced. Is the preview server running on $PORT," >&2
  echo "and was tools/preview/_shot.html copied next to the built pages?" >&2
  exit 1
fi
echo "$OUT  $(stat -f%z "$OUT") bytes  ${W}x${H}  $PAGE  $Q"
