import os
from pathlib import Path

from common.config import GEN_ZONES_TILES
from common.zones import load_zones_outer
from common.kmlutils import create_kml_for_tiles

Path(GEN_ZONES_TILES).mkdir(exist_ok=True)

outer_zones = load_zones_outer()

for zone in outer_zones:
    print(zone)
    create_kml_for_tiles(outer_zones[zone], os.path.join(GEN_ZONES_TILES, "tiles_{}.kml".format(zone)))
