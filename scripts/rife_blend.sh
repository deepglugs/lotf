#!/bin/bash
# RIFE 2x on ComfyUI, then fold back to 24 fps with a 1:2:1 centred blend
# (same duration, in-betweens become motion blur). Usage: rife_blend.sh in.mp4 out.mp4 [--loop]
set -e
cd /home/kev/stheno/legacy_of_the_fallen
in=$1; out=$2; r=${out%.*}_rife2_48fps.webm
uv run python docs/scripts/rife.py "$in" "$r" 2 $3
ffmpeg -loglevel error -y -i "$r" -vf "tmix=frames=3:weights='1 2 1',select='mod(n,2)',setpts=N/24/TB" -r 24 -c:v libsvtav1 -crf 8 -preset 6 -pix_fmt yuv420p10le "$out"
echo "blend -> $out"
