import os
from pathlib import Path

from common.config import load_users, GEN_USERS
from common.kmlutils import create_kml_for_tiles
from common.squares import compute_max_square
from common.statshunters import tiles_from_activities
from common.zones import load_zones_outer

outer_zones = load_zones_outer()
users = load_users()

print("Generate reports in", GEN_USERS)

for user in users:
    print("Treat " + user['name'])
    gen_path = os.path.join(GEN_USERS, user['name'])
    Path(gen_path).mkdir(exist_ok=True, parents=True)

    url_uid = user['url'].split('/')[-1]
    explored_tiles = tiles_from_activities(url_uid, filter_fct=lambda act: 'Virtual' not in act['type'])
    dep_explorer = []

    for zone in outer_zones:
        explored_tiles_zone = outer_zones[zone] & explored_tiles
        if explored_tiles_zone:
            kml_path = os.path.join(gen_path, "{}_{}.kml".format(user['name'], zone))
            create_kml_for_tiles(outer_zones[zone] - explored_tiles_zone, kml_path)

            explored_tile_count = len(explored_tiles_zone)
            zone_tiles_count = len(outer_zones[zone])
            ratio = explored_tile_count / zone_tiles_count

            zone_max_square = compute_max_square(explored_tiles_zone)

            dep_explorer.append((zone, ratio, explored_tile_count, zone_tiles_count, zone_max_square))

    if dep_explorer:
        report = ""
        for dep in sorted(dep_explorer, key=lambda x: x[1], reverse=True):
            report += "{0[0]:10} fill: {0[1]:>5.1%} ({0[2]:>5} / {0[3]:>5} ) max square: {0[4]:>3}\n".format(dep, )
        with open(os.path.join(gen_path, "report {}.txt".format(user['name'])), "w") as hF:
            hF.write(report)
