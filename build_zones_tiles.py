from common.config import *
from common.kmlutils import kml_zone_to_tiles

if __name__ == '__main__':
    config = load_config()

    inner_zones = {}
    outer_zones = {}
    for zone in config['zones']:
        path = config['zones'][zone].replace("%GEN_ZONES%", GEN_ZONES)
        inner_tiles, outer_tiles = kml_zone_to_tiles(path)
        inner_zones[zone] = list(inner_tiles)
        outer_zones[zone] = list(outer_tiles)
        print("load zone {} : {} / {} tiles".format(zone, len(outer_zones[zone]), len(inner_zones[zone])))

    with open(GEN_TILES_ZONES_INNER, 'w', encoding='utf-8') as f:
        json.dump(inner_zones, f)

    with open(GEN_TILES_ZONES_OUTER, 'w', encoding='utf-8') as f:
        json.dump(outer_zones, f)
