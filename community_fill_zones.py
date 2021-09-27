from shapely.ops import unary_union

from common import statshunters, zones
from common.config import *
from common.kmlutils import kml_file_from_polygons
from common.tile import Tile
from common.fileutils import FileCheck

users = load_users()
config = load_config()

community_tiles = set()
geoms_users = []

for user in users:
    print(user['name'])
    url_uid = user['url'].split('/')[-1]

    user_tiles = statshunters.tiles_from_activities(url_uid, filter_fct=lambda act: 'Virtual' not in act['type'])
    community_tiles |= user_tiles

    geom_z = unary_union([Tile(*t).polygon for t in user_tiles])
    geoms_users.append(geom_z)

geom_z = unary_union(geoms_users)

output_file = os.path.join(GEN_USERS, "kikourou_tiles.kml")
if output_file:
    kml_file_from_polygons(geom_z, output_file)

report = ""
db_report = ""
for country in config['countries']:
    outer_zones = zones.load_zones_outer(re_filter=config['countries'][country])

    all_tiles_country = set()
    for zt in outer_zones.values():
        all_tiles_country |= zt

    community_tiles_country = community_tiles & all_tiles_country

    zone_results = []
    for zone in outer_zones:
        community_tiles_zone = community_tiles_country & outer_zones[zone]
        zone_results.append([zone, len(community_tiles_zone), len(outer_zones[zone]),
                             len(community_tiles_zone) / len(outer_zones[zone]) * 100])
        db_report += ",".join([country.title(), zone, str(len(outer_zones[zone])), str(len(community_tiles_zone)) ]) + "\n"

    report += "{:<9} : {:>6.2f}% ({:>6}/{:>6})\n".format(country.title(),
                                                   len(community_tiles_country) / len(all_tiles_country) * 100,
                                                   len(community_tiles_country), len(all_tiles_country))
    for zone in sorted(zone_results, key=lambda z: z[3], reverse=True):
        report += "{0[0]:<9} : {0[3]:>6.2f}% ({0[1]:>5}/{0[2]:>5})\n".format(zone)
    report += "\n"

with FileCheck(os.path.join(GEN_USERS, 'countries_report.txt')) as hF:
    hF.write(report)

with FileCheck(os.path.join(GEN_USERS, 'countries_report.csv')) as hF:
    hF.write(db_report)

