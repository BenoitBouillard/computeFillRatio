from common.config import *
from common.config import GEN_PATH
from common.kmlutils import load_kml_geom
from common.geojson_utils import shapely_to_geojson
import geojson
from shapely.geometry import shape
from common.fileutils import FileCheck

if __name__ == '__main__':
    config = load_config()

    inner_zones = {}
    outer_zones = {}
    for zone in config['zones']:
        print(zone)
        path = config['zones'][zone].replace("%GEN_ZONES%", GEN_ZONES)
        geom = shape(load_kml_geom(path)[0])

        geojson_path = path[:-3] + "geojson"

        json = shapely_to_geojson(geom)

        with FileCheck(geojson_path, encoding='utf-8') as f:
            f.write(geojson.dumps(json))
