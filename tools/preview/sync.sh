#!/bin/sh
# Mirror the site into a session scratchpad the preview sandbox can read, and
# re-lay the three harnesses, which `rsync --delete` removes every time.
#
#   SP=<this session's scratchpad>  sh tools/preview/sync.sh
#
# The excludes are not optional: without them rsync copies ~59GB of brand
# library and video into the scratchpad.
[ -n "$SP" ] || { echo "set SP to this session's scratchpad path"; exit 1; }
SRC="$(cd "$(dirname "$0")/../.." && pwd)"
mkdir -p "$SP/preview"
rsync -a --delete \
  --exclude 'CydnieJocelyn-Site' --exclude 'cydniejocelyn' --exclude '* copy' \
  --exclude '.git' --exclude '.vercel' --exclude 'The Build page' \
  --exclude 'Retreat drafts' --exclude 'Greece Retreat' \
  --exclude 'A Sounding' --exclude 'The Letters Page' \
  --exclude 'the questions' --exclude 'Privacy terms page' \
  --exclude 'April Retreat Gatlinburg April 13th - 18th ' \
  "$SRC/" "$SP/preview/"
cp "$SRC/tools/preview/_shot.html"  "$SP/preview/_shot.html"
cp "$SRC/tools/preview/_test.html"  "$SP/preview/_test.html"
cp "$SRC/tools/preview/_probe.html" "$SP/preview/_probe.html"
cp "$SRC/tools/preview/_audit.html" "$SP/preview/_audit.html"
cp "$SRC/tools/preview/_menu.html"  "$SP/preview/_menu.html"
cp "$SRC/tools/preview/_carousel.html" "$SP/preview/_carousel.html"
