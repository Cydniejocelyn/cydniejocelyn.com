#!/bin/sh
# The reviews carousel on a touch screen.
#
#   sh tools/preview/runcarousel.sh "$SP" 8814
#
# The flags are the whole point. Headless Chrome reports `pointer: fine` by
# default, so without them site.js takes the desktop branch and this harness
# quietly tests the wrong carousel and passes.
SP="$1"; PORT="${2:-8814}"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="$SP/dom-carousel.html"; rm -f "$OUT"
"$CHROME" --headless --disable-gpu --no-sandbox --window-size=1400,1000 \
  --blink-settings=primaryPointerType=2,availablePointerTypes=2,primaryHoverType=1,availableHoverTypes=1 \
  --virtual-time-budget=60000 --user-data-dir="$SP/cr-carousel" \
  --dump-dom "http://127.0.0.1:$PORT/_carousel.html" > "$OUT" 2>/dev/null &
PID=$!; i=0
while [ $i -lt 70 ]; do [ -s "$OUT" ] && grep -q DONE "$OUT" 2>/dev/null && break; sleep 1; i=$((i+1)); done
kill $PID 2>/dev/null; wait $PID 2>/dev/null
python3 - "$OUT" <<'PY'
import sys, re, html
s = open(sys.argv[1], encoding="utf-8", errors="replace").read()
m = re.search(r'<div id="log">(.*?)</div>', s, re.S)
print(html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).replace("\nDONE", "") if m else "(no log)")
PY
