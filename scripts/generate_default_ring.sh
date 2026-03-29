#!/usr/bin/env sh
set -eu
mkdir -p assets
ffmpeg -y -f lavfi -i "sine=frequency=880:duration=0.35" \
  -f lavfi -i "sine=frequency=1174:duration=0.35" \
  -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1,volume=0.4" \
  -c:a libmp3lame -q:a 4 assets/default-ring.mp3
