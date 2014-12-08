#!/bin/bash
for ((i=1;i<=28;i+=1)); do
convert -size 25x25 Smiley$i.gif -resize 16x16 smallSmiley$i.gif
done
