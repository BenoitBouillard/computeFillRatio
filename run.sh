#!/bin/bash

git pull
pip3 install -r requirements.txt
python3 get_users_activities.py
python3 challenge.py -c 2021 -i 10 je
python3 ranking_fill_zones.py
python3 ranking_fr_stats.py
python3 ranking_dep.py
python3 community_fill_zones.py
python3 users_report.py

./upload.sh
