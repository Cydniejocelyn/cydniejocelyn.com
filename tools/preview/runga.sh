#!/bin/sh
# Run _ga.html in headless Chrome and print the GA4 event tally.
#
#   sh tools/preview/runga.sh "$SP" 8817            # all nine pages
#   sh tools/preview/runga.sh "$SP" 8817 /about/    # one
#
# Analytics cannot be tested in the Claude preview pane. Setting scrollTop
# there moves the page and fires no scroll event at all, so every
# scroll_depth assertion reads as a failure against code that is correct.
# Verified 28 August 2026. Same shape as the IntersectionObserver failure
# documented at the top of runsuite.sh.
#
# Chrome does not exit reliably after --dump-dom on this machine, so it is
# backgrounded, polled for, and killed, exactly as runsuite.sh does.
SP="$1"; PORT="${2:-8817}"; ONE="$3"
[ -n "$SP" ] || { echo "usage: sh tools/preview/runga.sh <scratchpad> [port] [/page/]"; exit 1; }
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

one() {
  NAME="$1"; PATHQ="$2"
  OUT="$SP/ga-$NAME.html"; rm -f "$OUT"
  "$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
    --window-size=1400,1000 --virtual-time-budget=30000 \
    --user-data-dir="$SP/ga-cr-$NAME" \
    --dump-dom "http://127.0.0.1:$PORT/_ga.html?p=$PATHQ" > "$OUT" 2>/dev/null &
  PID=$!
  i=0
  while [ $i -lt 60 ]; do
    if [ -s "$OUT" ] && grep -q 'failing of' "$OUT" 2>/dev/null; then break; fi
    sleep 1; i=$((i+1))
  done
  kill $PID 2>/dev/null; wait $PID 2>/dev/null
  python3 - "$OUT" "$NAME" <<'PY'
import sys, re, html
s = open(sys.argv[1], encoding="utf-8", errors="replace").read()
m = re.search(r'<div id="log">(.*?)</div>\s*<iframe', s, re.S) or re.search(r'<div id="log">(.*)', s, re.S)
t = html.unescape(re.sub(r'<[^>]+>', '\n', m.group(1))) if m else ""
p, f = len(re.findall(r'PASS', t)), len(re.findall(r'FAIL', t))
print("%-12s %2d pass / %d fail" % (sys.argv[2], p, f))
for l in t.split("\n"):
    if "FAIL" in l:
        print("    ", l.strip())
PY
}

if [ -n "$ONE" ]; then
  one "$(echo "$ONE" | tr -d '/' )" "$ONE"
else
  one home      /
  one about     /about/
  one build     /the-build/
  one retreats  /retreats/
  one greece    /retreats/greece/
  one sounding  /a-sounding/
  one letters   /the-letters/
  one privacy   /privacy-policy/
  one questions /thequestions/
fi
