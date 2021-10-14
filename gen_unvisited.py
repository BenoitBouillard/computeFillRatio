import urllib3
from fastkml import kml
from fastkml.styles import LineStyle, PolyStyle, Style

from common.tile import tile_to_polygon
from common.squares import compute_max_cluster, expand_cluster

urllib3.disable_warnings()


def gen_kml_unvisited(tiles, level=17):

    cluster = compute_max_cluster(tiles)
    unvisited_tiles = expand_cluster(cluster, 25 if level == 17 else 15) - tiles

    # Create the root KML object
    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'

    # Create a KML Document and add it to the KML root object
    d = kml.Document(ns)
    k.append(d)

    # Create a KML Folder within the Document
    f2 = kml.Folder(ns)
    d.append(f2)

    for (x, y) in unvisited_tiles:
        p = kml.Placemark(ns, styles=[ Style(styles=[LineStyle(color="7fff0000", width=1), PolyStyle(fill=1, color="0fff0000")])])
        p.geometry = tile_to_polygon(x, y, level=level)
        f2.append(p)

    return k

