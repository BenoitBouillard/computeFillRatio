from fastkml import kml
from shapely.geometry import Polygon
from common.tile import tile_from_coord, Tile
from collections import Iterable


def kml_zone_to_tiles(kml_file):
    k = kml.KML()
    with open(kml_file, 'rb') as kml_handle:
        doc = kml_handle.read()
        k.from_string(doc)

    features = list(k.features())
    folder = list(features[0].features())[0]
    geometry = folder.geometry
    tiles_inner = set()
    tiles_outer = set()

    if hasattr(geometry, 'geoms'):
        geoms = geometry.geoms
    else:
        geoms = [geometry]

    for geo in geoms:
        polygon = Polygon(geo)
        (min_x, min_y, max_x, max_y) = polygon.bounds

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
                if polygon.intersects(t.polygon):
                    tiles_outer.add((x, y))
                    if polygon.contains(t.polygon):
                        tiles_inner.add((x, y))
    return tiles_inner, tiles_outer


def kml_file_from_polygons(polygons, kml_file):
    if not isinstance(polygons, Iterable):
        polygons = [polygons]
    # Create the root KML object
    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'

    # Create a KML Document and add it to the KML root object
    d = kml.Document(ns, 'docid', 'Zone unexplored tiles', 'Zone unexplored tiles')
    k.append(d)

    # Create a KML Folder and add it to the Document
    f = kml.Folder(ns)
    d.append(f)

    # Create a KML Folder and nest it in the first Folder
    nf = kml.Folder(ns)
    f.append(nf)

    # Create a second KML Folder within the Document
    f2 = kml.Folder(ns)
    d.append(f2)

    # ls = styles.LineStyle(ns, color='red', width=3)
    # s1 = styles.Style(styles=[ls])

    # Create a Placemark with a simple polygon geometry and add it to the
    # second folder of the Document
    for polygon in polygons:
        # p = kml.Placemark(ns, styles=[s1])
        p = kml.Placemark(ns)
        p.geometry = polygon
        f2.append(p)

    with open(kml_file, 'w') as myfile:
        myfile.write(k.to_string(prettyprint=True))


def create_kml_for_tiles(tiles, kml_file):
    kml_file_from_polygons([Tile(x, y).polygon for (x, y) in tiles], kml_file)
