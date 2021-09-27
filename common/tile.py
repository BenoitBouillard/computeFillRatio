import math

from shapely.geometry import Polygon

coords_tile = dict()


def coord_from_tile(x, y):
    if (x, y) in coords_tile:
        return coords_tile[(x, y)]
    n = 2 ** 14
    lat = math.atan(math.sinh(math.pi * (1 - 2 * y / n))) * 180.0 / math.pi
    lon = x / n * 360.0 - 180.0
    coords_tile[(x, y)] = (lat, lon)
    return lat, lon


def geom_from_tile(x, y):
    return [list(coord_from_tile(x, y))[::-1], list(coord_from_tile(x + 1, y + 1))[::-1]]


def tile_from_coord(lat, lon, output="list"):
    n = 2 ** 14
    x = math.floor(n * (lon + 180) / 360)
    lat_r = lat * math.pi / 180
    y = math.floor(n * (1 - (math.log(math.tan(lat_r) + 1 / math.cos(lat_r)) / math.pi)) / 2)
    if output == "list":
        return x, y
    else:
        return "{}_{}".format(x, y)


class Tile(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        geometry = geom_from_tile(self.x, self.y)

        self.lonW = min([x[0] for x in geometry])
        self.lonE = max([x[0] for x in geometry])
        self.latS = min([x[1] for x in geometry])
        self.latN = max([x[1] for x in geometry])
        self.polygon = Polygon(
            [(self.lonW, self.latN), (self.lonW, self.latS), (self.lonE, self.latS), (self.lonE, self.latN)])

    def __repr__(self):
        return "Tile {0.x}_{0.y}".format(self)

