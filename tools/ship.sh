#!/bin/sh
# Ship the site. This is the whole sequence, in order, and it is the only
# supported one now that the deploy comes out of dist/ rather than the
# working directory.
#
#   sh tools/ship.sh "$SP"      # $SP is this session's scratchpad, for the suite
#   sh tools/ship.sh "$SP" --no-suite
#
# WHY THE DEPLOY MOVED TO dist/
# -----------------------------
# `vercel deploy` used to upload the working directory, comments and all. The
# comments are 45% of site.css, and site.css is render blocking, so every
# first-time reader waited for 25KB of notes-to-ourselves before the page
# painted. `tools/build.py` writes a comment-free copy to dist/ and leaves the
# source exactly as documented as it has always been.
#
# Nothing here is optional. In particular `stamp.py` runs BEFORE the build,
# and build.py refuses to run if the stamps are stale: /assets/css/ and
# /assets/js/ are `immutable` for a year in vercel.json, which is only safe
# because the ?v= hash changes when the file does. A stale stamp plus
# immutable is a returning reader pinned to an old stylesheet forever.
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/.."

SP="$1"
SUITE=1
[ "$2" = "--no-suite" ] && SUITE=0
[ "$1" = "--no-suite" ] && { SUITE=0; SP=""; }

echo "==> stamping"
python3 tools/stamp.py

echo "==> building dist/"
python3 tools/build.py

if [ "$SUITE" = "1" ] && [ -n "$SP" ]; then
  echo "==> serving dist/ and running the suite against WHAT SHIPS, not the source"
  rm -rf "$SP/distpreview"
  cp -R dist "$SP/distpreview"
  # the harnesses are local tooling and are not in dist, which is the point
  cp tools/preview/_shot.html tools/preview/_test.html tools/preview/_probe.html \
     tools/preview/_audit.html tools/preview/_menu.html tools/preview/_carousel.html \
     "$SP/distpreview/"
  python3 tools/preview/serve.py "$SP/distpreview" 8817 >"$SP/ship-serve.log" 2>&1 &
  SRV=$!
  sleep 2
  sh tools/preview/runsuite.sh "$SP" 8817
  kill $SRV 2>/dev/null || true
  echo "    (read that. Do not ship a red suite.)"
fi

echo "==> deploying dist/"
vercel deploy --prod --yes --cwd dist
echo
echo "Now verify with vercel curl. Deployment Protection makes plain curl useless:"
echo "  it returns 200 with a login page for every path, including ones that do not exist."
