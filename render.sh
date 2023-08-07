#!/usr/bin/bash
cd project
t=$(date +"%H.%M.%S")
manim main.py $1
mv media/videos/main/1080p60/$1.mp4 ../output/$1.$t.mp4
rm -r media
cd ..