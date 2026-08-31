#!/bin/sh
# Run _test.html in headless Chrome and print the PASS/FAIL tally.
#
#   sh tools/preview/runsuite.sh "$SP" 8814 /a-sounding/
#   sh tools/preview/runsuite.sh "$SP" 8814          # all six covered pages
#
# WHY THIS EXISTS. The Claude preview pane degraded again in session four, the
# same way it did in session three: `javascript_tool` started returning "the
# Browser pane is currently hidden", and before it failed outright it began
# returning WRONG ANSWERS. Greece reported 41 pass / 2 fail on a page nothing
# had touched, because an IntersectionObserver does not fire in a pane the
# compositor has stopped drawing, so every reveal read as unrevealed. Headless
# Chrome ran the identical URL at 43 / 0.
#
# If the suite starts failing on a page you did not touch, run it here before
# you believe it.
#
# Chrome does not exit reliably after --dump-dom on this machine, so it is
# backgrounded, polled for, and killed. A plain foreground call hangs until the
# tool times out at two minutes.
SP="$1"; PORT="${2:-8814}"; ONE="$3"
[ -n "$SP" ] || { echo "usage: sh tools/preview/runsuite.sh <scratchpad> [port] [/page/]"; exit 1; }
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

one() {
  NAME="$1"; PATHQ="$2"
  OUT="$SP/dom-$NAME.html"; rm -f "$OUT"
  "$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
    --window-size=1280,900 --virtual-time-budget=20000 \
    --user-data-dir="$SP/cr-$NAME" \
    --dump-dom "http://127.0.0.1:$PORT/_test.html?p=$PATHQ" > "$OUT" 2>/dev/null &
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
m = re.search(r'<div id="log">(.*?)</div>', s, re.S)
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
  one greece   /retreats/greece/
  one gatlinburg /retreats/gatlinburg/
  one retreats /retreats/
  one sounding /a-sounding/
  one letters  /the-letters/
  # Added 28 August 2026, after The Build page's ten questions became the
  # objection picker and the suite that went green on the deploy had never
  # once loaded the page that changed. Six of nine pages was not a suite,
  # it was the six that happened to get written first. All three of these
  # were green the first time they were run, so this costs nothing and the
  # picker assertions now cover all three pages that carry one.
  one home     /
  one build    /the-build/
  one about    /about/
  # Built 28 August. Static pages, but they carry two assertions each that
  # run nowhere else: the relative privacy and terms links in the footer,
  # and, on /thequestions/ only, the bare header and its button's contrast.
  one privacy  /privacy-policy/
  one questions /thequestions/
fi
