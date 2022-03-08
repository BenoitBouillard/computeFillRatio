import os
from pathlib import Path
import json

from common.config import load_users, GEN_PUBLIC_PATH, load_config, GEN_ZONES, GEN_USERS
from common.statshunters import tiles_from_activities
from common.zones import load_zones_outer
from fill_ratio import compute_fill_ratio
from common.fileutils import FileCheck
from common.squares import get_max_square, compute_max_cluster
from common.kmlutils import shapely_to_geojson
from shapely.ops import unary_union
from shapely import geometry
from common.tile import Tile
import geojson
from common.tile import coord_from_tile

users = load_users()
config = load_config()


result_dict = {}


def generate_user(user):
    user_json_filename = os.path.join(GEN_USERS, user['name'], user['name'] + ".json")
    Path(os.path.join(GEN_USERS, user['name'])).mkdir(exist_ok=True, parents=True)
    url_uid = user['url'].split('/')[-1]
    explored_tiles = tiles_from_activities(url_uid, filter_fct=lambda act: 'Virtual' not in act['type'])

    try:
        with open(user_json_filename, 'r') as hr:
            previous_result = json.load(hr)
    except:
        previous_result = None


    if previous_result:
        if previous_result.get("visited", 0) == len(explored_tiles):
            # no change
            print("No change for "+user['name'])
            return previous_result
    print("Treat "+user['name'])
    max_square = get_max_square(explored_tiles)
    cluster = compute_max_cluster(explored_tiles)
    geojson_filename = os.path.join(GEN_USERS, user['name'], user['name'] + ".geojson")
    sc = []
    explored_geojson = shapely_to_geojson(unary_union([Tile(*t).polygon for t in explored_tiles]))
    sc.append(geojson.Feature(geometry=explored_geojson,
                              properties={"kind": "visited",
                                          "size": len(explored_tiles)
                                          }))
    explored_geojson = shapely_to_geojson(unary_union([Tile(*t).polygon for t in cluster]))
    sc.append(geojson.Feature(geometry=explored_geojson,
                              properties={"kind": "cluster",
                                          "size": len(cluster)
                                          }))
    ms1 = coord_from_tile(max_square[0], max_square[1], 14)
    ms2 = coord_from_tile(max_square[0] + max_square[2], max_square[1] + max_square[2], 14)
    geometry_square = geojson.Polygon([[
        [ms1[1], ms1[0]], [ms1[1], ms2[0]], [ms2[1], ms2[0]], [ms2[1], ms1[0]], [ms1[1], ms1[0]]
    ]])
    sc.append(geojson.Feature(
        geometry=geometry_square,
        properties={"kind": "max_square",
                    "size": max_square[2]
                    }
    ))
    geojson_collection = geojson.FeatureCollection(sc)
    with FileCheck(geojson_filename) as h:
        h.write(geojson.dumps(geojson_collection))
    user_result = {
        'name': user['name'],
        'visited': len(explored_tiles),
        'square': max_square[2],
        'cluster': len(cluster),
        'geojson': geojson_filename,
        'zones': {}
    }
    for country in config['countries']:
        outer_zones = load_zones_outer(re_filter=config['countries'][country])
        for zone in outer_zones:
            sc = []

            zone_tiles = outer_zones[zone]
            zone_limit_file = config['zones'][zone].replace("%GEN_ZONES%", GEN_ZONES).replace('.kml', '.geojson')
            explored_tiles_zone = zone_tiles & explored_tiles
            if not explored_tiles_zone:
                continue
            non_explored_tiles_zone = zone_tiles - explored_tiles_zone
            zone_max_square = get_max_square(explored_tiles_zone)

            explored_geojson = shapely_to_geojson(unary_union([Tile(*t).polygon for t in explored_tiles_zone]))
            non_explored_geojson = shapely_to_geojson(
                geometry.MultiPolygon([Tile(*t).polygon for t in non_explored_tiles_zone]))

            geojson_filename = os.path.join(GEN_USERS, user['name'], user['name'] + '_' + zone + ".geojson")

            sc.append(geojson.Feature(geometry=non_explored_geojson,
                                      properties={"kind": "unvisited",
                                                  "size": len(non_explored_tiles_zone)
                                                  }))

            sc.append(geojson.Feature(geometry=explored_geojson,
                                      properties={"kind": "visited",
                                                  "size": len(explored_tiles_zone)
                                                  }))

            if zone_max_square:
                ms1 = coord_from_tile(zone_max_square[0], zone_max_square[1], 14)
                ms2 = coord_from_tile(zone_max_square[0] + zone_max_square[2], zone_max_square[1] + zone_max_square[2],
                                      14)
                geometry_square = geojson.Polygon([[
                    [ms1[1], ms1[0]],
                    [ms1[1], ms2[0]],
                    [ms2[1], ms2[0]],
                    [ms2[1], ms1[0]],
                    [ms1[1], ms1[0]]
                ]])

                sc.append(geojson.Feature(
                    geometry=geometry_square,
                    properties={"kind": "max_square",
                                "size": zone_max_square[2]
                                }
                ))

            geojson_collection = geojson.FeatureCollection(sc)

            with FileCheck(geojson_filename) as h:
                h.write(geojson.dumps(geojson_collection))

            user_result['zones'][zone] = {
                'name': zone,
                'visited': len(explored_tiles_zone),
                'total': len(zone_tiles),
                'square': zone_max_square[2],
                'geojson': geojson_filename
            }
    with FileCheck(user_json_filename) as h:
        h.write(geojson.dumps(user_result))
    return user_result


for user in users:
    result_dict[user['name']] = generate_user(user)

with FileCheck(os.path.join(GEN_PUBLIC_PATH, "users.json")) as hF:
    hF.write(json.dumps(result_dict, indent=2))
