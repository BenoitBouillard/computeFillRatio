from computeFillRatio import computeFillRatio
import json
import os

GEN_USER_PATH = os.path.join("gen", "users")

with open("users.config", encoding='utf-8' ) as f:
    d = json.load(f)
user_zones = []
for user in d['users']:
    print(user)
    url_uid = user['url'].split('/')[-1]
    user_data_path = os.path.join(GEN_USER_PATH, url_uid)
    for zone in user['zones']:
        user_zone = {
          "name" : user['name'],
          "namedep" : "{0[name]} ({1})".format(user, zone),
          "url"  : user['url'],
          "zone" : zone
        }
        user_zones.append(user_zone)

        ratio, explored_tile_count, zone_tiles_count = computeFillRatio(d['zones'][zone], user_data_path, os.path.join(GEN_USER_PATH, "{}_{}.kml".format(user['name'], zone)))
        user_zone['explored_tile_count'] = explored_tile_count
        user_zone['zone_tiles_count'] = zone_tiles_count
        user_zone['ratio'] = ratio
    
 
pos = 0
full = ""
print("#   {:35} {:4}".format("NOM", "RATIO"))
for user in sorted(user_zones, key=lambda u: u['ratio'], reverse=True):
    if user['ratio']<1:
        pos += 1
        print("{1:<2}: {0[namedep]:35} {0[ratio]:>5.1%} ({0[explored_tile_count]:5} / {0[zone_tiles_count]:5} )".format(user, pos))
    else:
        full += "{0[name]} {0[zone]}({0[zone_tiles_count]}) / ".format(user)
if full:
    print("8) "+full[:-2])