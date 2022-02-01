#!/bin/bash

git pull
pip3 install -r requirements.txt
python3 extract_kml_belgium.py
python3 extract_kml_france.py
python3 extract_kml_germany.py
python3 extract_kml_switzerland.py
python3 build_zones_tiles.py
python3 kml_tiles_by_zones.py
