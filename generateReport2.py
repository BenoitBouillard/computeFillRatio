import os
import json
from computeFillRatio import computeFillRatio
from getStatHuntersUserActivities import getStatHuntersUserActivities

GEN_USER_PATH = os.path.join("gen", "users")

with open("users.config", encoding='utf-8' ) as f:
    d = json.load(f)
for user in d['users']:
    print(user)
    url_uid = user['url'].split('/')[-1]
    user_data_path = os.path.join(GEN_USER_PATH, url_uid)
    user['explored_tile_count'] = 0
    user['zone_tiles_count'] = 0
    user['zones_data'] = {}
    for zone in user['zones']:
        ratio, explored_tile_count, zone_tiles_count = computeFillRatio(d['zones'][zone], user_data_path, os.path.join(GEN_USER_PATH, "{}_{}.kml".format(user['name'], zone)))
        user['zones_data'][zone] = {}
        user['zones_data'][zone]['explored_tile_count'] = explored_tile_count
        user['zones_data'][zone]['zone_tiles_count'] = zone_tiles_count
        user['zones_data'][zone]['ratio'] = ratio
    
        user['explored_tile_count'] += explored_tile_count
        user['zone_tiles_count'] += zone_tiles_count
    user['ratio'] = user['explored_tile_count'] / user['zone_tiles_count']

pos = 0
print("#   {:20} {:4}".format("NOM", "RATIO"))
for user in sorted(d['users'], key=lambda u: u['ratio'], reverse=True):
    pos += 1
    print("{1:<2}: {0[name]:20} {0[ratio]:>5.1%} ({0[explored_tile_count]:5} / {0[zone_tiles_count]:5} )".format(user, pos))
    for zone in sorted(user['zones_data'], key=lambda u: user['zones_data'][u]['ratio'], reverse=True):
        if user['zones_data'][zone]['ratio'] == 1.0:
            print("                          {0:>15} : 8) ({1[zone_tiles_count]})".format(zone, user['zones_data'][zone]))
        else:
            print("                          {0:>15} : {1[ratio]:>5.1%} ({1[explored_tile_count]:5} / {1[zone_tiles_count]:5} )".format(zone, user['zones_data'][zone]))
