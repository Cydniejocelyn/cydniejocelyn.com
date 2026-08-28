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

# iCloud Drive syncs this Desktop and writes "about 2" style conflict copies
# into dist/ whenever build.py wipes and recreates it. build.py sweeps them,
# and this sweeps again here because iCloud can write a fresh one in the
# seconds between the build finishing and the upload starting. One of them
# vanishing mid-scan is what took a production deploy down on 28 August:
#   ENOENT: no such file or directory, scandir '.../dist/privacy-policy 2'
echo "==> sweeping iCloud conflict copies out of dist/"
find dist -depth -name "* [0-9]" -o -depth -name "* [0-9].*" | while read -r d; do
  echo "    removing $d"; rm -rf "$d"
done

echo "==> deploying dist/"
# CD INTO dist, DO NOT USE --cwd. This is not a style preference.
#
# `vercel deploy --cwd dist` uploads dist/ and then reads vercel.json from the
# SHELL's working directory, which is the repo root. Those two files are not
# the same: build.py seals the CSP script hashes into dist/vercel.json and
# leaves the root copy holding `__INLINE_SCRIPT_HASHES__`.
#
# On 28 August 2026 that shipped a production CSP whose script-src contained
# the literal placeholder. A browser drops an unrecognised source expression
# and enforces the rest, so every inline script on the site was blocked:
# analytics, the js-motion flip, and the Flodesk signup on /the-letters/.
# The HTML and the CSS were correct. Only the header was wrong, and nothing
# in the build or the suite could see it, because neither one deploys.
#
# Two deploys with --cwd both reproduced it. Deploying from inside dist/ with
# the identical file fixed it. The check below is what catches it next time.
( cd dist && vercel deploy --prod --yes )

echo "==> verifying the headers PRODUCTION actually sends"
# The suite runs against a preview server that sends no headers at all, so
# this is the only place the deployed CSP is ever looked at. Plain curl is
# useless while Deployment Protection is on: it returns 200 and a login page
# for every path, including ones that do not exist.
URL=$( cd dist && vercel ls --prod 2>/dev/null \
       | grep -oE "https://[a-z0-9-]+\.vercel\.app" | head -1 )
if [ -z "$URL" ]; then
  echo "    could not resolve the deployment URL. Check the headers by hand."
else
  HDRS=$( cd dist && vercel curl -I "$URL/" 2>/dev/null )
  echo "$HDRS" | grep -iE "^(content-security-policy|strict-transport-security|x-frame-options|permissions-policy|cross-origin-opener-policy|referrer-policy|x-content-type-options):" \
    | cut -c1-100
  FAIL=0
  echo "$HDRS" | grep -qi "__INLINE_SCRIPT_HASHES__" && {
    echo "    FAIL: the CSP placeholder reached production. Every inline"
    echo "          script on the site is blocked. See the note above."; FAIL=1; }
  for H in content-security-policy strict-transport-security x-frame-options \
           permissions-policy cross-origin-opener-policy x-content-type-options; do
    echo "$HDRS" | grep -qi "^$H:" || { echo "    FAIL: $H is not being sent."; FAIL=1; }
  done
  [ "$FAIL" = "0" ] && echo "    headers OK" || echo "    HEADERS ARE WRONG. Fix before telling anyone it is live."
fi
echo
echo "Now verify with vercel curl. Deployment Protection makes plain curl useless:"
echo "  it returns 200 with a login page for every path, including ones that do not exist."
