import json
from common import config
import re


def load_zones(file, re_filter=None):
    with open(file, encoding='utf-8') as f:
        zones = json.load(f)
    for zone in list(zones):
        zones[zone] = frozenset([tuple(z) for z in zones[zone]])
        if re_filter and not re.match(re_filter, zone):
            zones.pop(zone)
    return zones


def load_zones_inner(re_filter=None):
    return load_zones(config.GEN_TILES_ZONES_INNER, re_filter)


def load_zones_outer(re_filter=None):
    return load_zones(config.GEN_TILES_ZONES_OUTER, re_filter)
