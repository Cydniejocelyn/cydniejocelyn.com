#!/bin/sh
# Mirror the project into the scratchpad the preview server can read.
# Run after every edit. SCRATCH must point at the current session scratchpad.
SRC="/Users/cydniebrown/Desktop/Claude Code/cydniejocelyn-v2/"
SCRATCH="${SCRATCH:?set SCRATCH to this session's scratchpad path}"
mkdir -p "$SCRATCH/preview"
rsync -a --delete --exclude 'tools/' "$SRC" "$SCRATCH/preview/"
echo "synced -> $SCRATCH/preview/"
