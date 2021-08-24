from fill_ratio import compute_fill_ratio

from common.config import load_users
from common.zones import load_zones_outer
from common.statshunters import tiles_from_activities


users = load_users()
outer_zones = load_zones_outer("[0-9].*")

user_zones = []
zones_results = {}
for user in users:
    print(user['name'])
    user_data = tiles_from_activities(user['url'].split('/')[-1])
    for zone in outer_zones:
        if zone not in zones_results:
            zones_results[zone] = []
        ratio, explored_tile_count, zone_tiles_count = compute_fill_ratio(outer_zones[zone], user_data)
        if explored_tile_count>0:
            user_zone = {
                'name': user['name'],
                'explored_tile_count': explored_tile_count,
                'ratio': ratio
            }
            zones_results[zone].append(user_zone)

for zone in zones_results:
    zones_results[zone].sort(key=lambda r:r['explored_tile_count'], reverse=True)
    line = "{:<4}: ".format(zone)
    for res in zones_results[zone][0:3]:
        line += "({:>3.0f}%) {:<17} ".format(res["ratio"]*100, res["name"])
    print(line)
