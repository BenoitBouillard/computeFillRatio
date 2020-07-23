from fastkml import kml, styles
from tile import TileFromCoord, Tile
from pprint import pprint
from shapely.geometry import Polygon
import argparse

def kmlZoneToTiles(kml_file):
    k = kml.KML()
    with open(kml_file, 'rb') as myfile:
        doc=myfile.read()
        k.from_string(doc)

    features = list(k.features())
    folder = list(features[0].features())[0]
    geometry = folder.geometry
    if len(geometry.geoms) != 1:
        print("!!! Only manage geometry with 1 line !!!")
        exit(0)
    lineString = geometry.geoms[0]
    polygon = Polygon(lineString)
    (minx, miny, maxx, maxy) = polygon.bounds
    
    tileMinX, tileMinY = TileFromCoord(miny, minx)
    tileMaxX, tileMaxY = TileFromCoord(maxy, maxx)
    if tileMaxX < tileMinX:
        tmp = tileMinX
        tileMinX = tileMaxX
        tileMaxX = tmp
    if tileMaxY < tileMinY:
        tmp = tileMinY
        tileMinY = tileMaxY
        tileMaxY = tmp
    tiles = []
    n = 0
    for x in range(tileMinX, tileMaxX+1):
        for y in range(tileMinY, tileMaxY+1):
            n = n+1
            t = Tile("{}_{}".format(x, y))
            if t.polygon.intersects(polygon):
                tiles.append(t)
    return tiles
    

def createKmlForTiles(tiles, kml_file):
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

    # Create a Placemark with a simple polygon geometry and add it to the
    # second folder of the Document
    for t in tiles:
        p = kml.Placemark(ns)
        p.geometry =  t.polygon #Polygon([(0, 0, 0), (1, 1, 0), (1, 0, 1)])
        f2.append(p)
    
    with open(kml_file, 'w') as myfile:
        myfile.write(k.to_string(prettyprint=True))


def tilesFromKml(kml_file):
    k = kml.KML()
    with open(kml_file, 'rb') as myfile:
        doc=myfile.read()
        k.from_string(doc)

    features = list(k.features())
    folder = list(features[0].features())[0]
    xmin, xmax, ymin, ymax = None, None, None, None
    tiles = []
    for placemark in folder.features():
        tile = Tile(placemark.geometry.coords)
        tiles.append(tile.uid)
    return tiles



parser = argparse.ArgumentParser(description='Compute exploration ratio of a zone')
parser.add_argument('-z','--zone', dest="zonefile", default=r"zone.kml", help="Zone KML file")
parser.add_argument('-e','--explored', dest="exploredfile", default=r"explored_tiles.kml",  help="Explored KML file from veloviewer")
parser.add_argument('-o','--output', dest="outputfile", default=r"zone_unexplored_tiles.kml", help="Output KML file of unexplored tiles")
args = parser.parse_args()

zonefile          = vars(args)['zonefile']
exploredfile      = vars(args)['exploredfile']
outputfile        = vars(args)['outputfile']

tiles = kmlZoneToTiles(zonefile)
exploredTiles = tilesFromKml(exploredfile)

unexploredTiles = []

for tile in tiles:
    if tile.uid not in exploredTiles:
       unexploredTiles.append(tile) 
       
exploredTileCount = len(tiles) - len(unexploredTiles)
      
print("Exploration ratio : {:.1f}% ({} of {})".format(100*exploredTileCount/len(tiles), exploredTileCount, len(tiles)))

createKmlForTiles(unexploredTiles, outputfile)
