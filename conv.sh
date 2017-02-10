#!/bin/bash

for x in `ls src`; do
    convert -colors 256 -depth 8 -dither FloydSteinberg -channel A -threshold 50% -filter point -resize 64x src/$x dst/$x
done

