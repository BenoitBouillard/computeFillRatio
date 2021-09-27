import os

from common.config import load_users, GEN_RESULTS
from common.statshunters import tiles_from_activities
from common.zones import load_zones_outer
from fill_ratio import compute_fill_ratio
from common.fileutils import FileCheck

users = load_users()
outer_zones = load_zones_outer()

user_zones = []
for user in users:
    print(user['name'])
    user_data = tiles_from_activities(user['url'].split('/')[-1])
    for zone in user['zones']:
        user_zone = {
            "name": user['name'],
            "namedep": "{0[name]} ({1})".format(user, zone),
            "url": user['url'],
            "zone": zone
        }
        user_zones.append(user_zone)

        ratio, explored_tile_count, zone_tiles_count = compute_fill_ratio(outer_zones[zone], user_data)
        user_zone['explored_tile_count'] = explored_tile_count
        user_zone['zone_tiles_count'] = zone_tiles_count
        user_zone['ratio'] = ratio

pos = 0
full = ""
with FileCheck(os.path.join(GEN_RESULTS, 'ranking_fill_zones.txt')) as h:
    print("#   {:35} {:4}".format("NOM", "RATIO"))
    h.write("#   {:35} {:4}\n".format("NOM", "RATIO"))
    for user in sorted(user_zones, key=lambda u: u['ratio'], reverse=True):
        if user['ratio'] < 1:
            pos += 1
            print("{1:<2}: {0[namedep]:35} {0[ratio]:>5.1%} ({0[explored_tile_count]:5} / {0[zone_tiles_count]:5} )".format(
                user, pos))
            h.write(
                "{1:<2}: {0[namedep]:35} {0[ratio]:>5.1%} ({0[explored_tile_count]:5} / {0[zone_tiles_count]:5} )\n".format(
                    user, pos))
        else:
            full += "{0[name]} {0[zone]}({0[zone_tiles_count]}) / ".format(user)
    if full:
        print("8) " + full[:-2])
        h.write("8) " + full[:-2]+"\n")
