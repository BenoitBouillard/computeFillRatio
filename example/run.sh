#!/bin/bash
BASEDIR=$(dirname "$0")
echo "$BASEDIR"

pwd
python "$BASEDIR"/../computeFillRatio.py -z "$BASEDIR"/zone.kml -e "$BASEDIR"/explored_tiles.kml -o "$BASEDIR"/zone_unexplored_tiles.kml