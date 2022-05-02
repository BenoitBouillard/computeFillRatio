import math

from shapely.geometry import Polygon, LineString

coords_tile = dict()


def coord_from_tile(x, y=None, level=14):
    n = 2 ** level
    if y is None:
        s = x.split('_')
        x = int(s[0])
        y = int(s[1])
    lat = math.atan(math.sinh(math.pi * (1 - 2 * y / n))) * 180.0 / math.pi
    lon = x / n * 360.0 - 180.0
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


def tile_to_line_string(x, y, level=17):
    geometry = [list(coord_from_tile(x, y, level))[::-1], list(coord_from_tile(x + 1, y + 1, level))[::-1]]

    lonW = min([x[0] for x in geometry])
    lonE = max([x[0] for x in geometry])
    latS = min([x[1] for x in geometry])
    latN = max([x[1] for x in geometry])
    nw = (lonW, latN)
    ne = (lonE, latN)
    se = (lonE, latS)
    sw = (lonW, latS)
    return LineString([nw, ne, se, sw, nw])


def tile_id_to_line_string(tile_id, level=17):
    (x, y) = [int(a) for a in tile_id.split("_")]
    return tile_to_line_string(x, y, level)


def tile_to_polygon(x, y, level=17):
    return Polygon(tile_to_line_string(x, y, level))


def tile_id_to_polygon(tile_id, level=17):
    return Polygon(tile_id_to_line_string(tile_id, level))


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


def geom_to_tiles(geom):
    tiles_inner = set()
    tiles_outer = set()

    (min_x, min_y, max_x, max_y) = geom.bounds

    tile_min_x, tile_min_y = tile_from_coord(min_y, min_x)
    tile_max_x, tile_max_y = tile_from_coord(max_y, max_x)
    if tile_max_x < tile_min_x:
        tmp = tile_min_x
        tile_min_x = tile_max_x
        tile_max_x = tmp
    if tile_max_y < tile_min_y:
        tmp = tile_min_y
        tile_min_y = tile_max_y
        tile_max_y = tmp
    for x in range(tile_min_x, tile_max_x + 1):
        for y in range(tile_min_y, tile_max_y + 1):
            t = Tile(x, y)
            if geom.intersects(t.polygon):
                tiles_outer.add((x, y))
                if geom.contains(t.polygon):
                    tiles_inner.add((x, y))
    return tiles_inner, tiles_outer


