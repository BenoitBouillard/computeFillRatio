from fastkml import kml, styles
from tile import TileFromCoord, Tile
from pprint import pprint
from shapely.geometry import Polygon
import shapely
import argparse
import os
import json

def kmlZoneToTiles(kml_file):
    k = kml.KML()
    with open(kml_file, 'rb') as myfile:
        doc=myfile.read()
        k.from_string(doc)

    features = list(k.features())
    folder = list(features[0].features())[0]
    geometry = folder.geometry
    tiles = []
    n = 0
    
    if hasattr(geometry, 'geoms'):
    #if isinstance(geometry, shapely.geometry.collection.GeometryCollection):
        geoms = geometry.geoms
    else:
        geoms = [ geometry ]

    for geo in geoms:
        polygon = Polygon(geo)
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
        p.geometry =  t.polygon
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

def tilesFromActivities(activities_dir):
    # Get tiles from activities files from stathunters
    directory = os.fsencode(activities_dir)
    tiles = []
        
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"): 
            with open(os.path.join(activities_dir, filename)) as f:
                d = json.load(f)
                for activity in d['activities']:
                    for tile in activity['tiles']:
                        uid = "{0}_{1}".format(tile['x'], tile['y'])
                        if uid not in tiles:
                            tiles.append(uid)
    return tiles
       
def computeFillRatio(zonefile, exploredfile, outputfile=None):
    # Get tiles from the zone
    tiles = kmlZoneToTiles(zonefile)

    if os.path.isdir(exploredfile):
        exploredTiles = tilesFromActivities(exploredfile)
    else:
        exploredTiles = tilesFromKml(exploredfile)

    unexploredTiles = []

    for tile in tiles:
        if tile.uid not in exploredTiles:
           unexploredTiles.append(tile) 
           
    exploredTileCount = len(tiles) - len(unexploredTiles)
    
    ratio = exploredTileCount/len(tiles)
          
    if outputfile:
        createKmlForTiles(unexploredTiles, outputfile)
        
    return ratio, exploredTileCount, len(tiles)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute exploration ratio of a zone')
    parser.add_argument('-z','--zone', dest="zonefile", default=r"zone.kml", help="Zone KML file")
    parser.add_argument('-e','--explored', dest="exploredfile", default=r"explored_tiles.kml",  help="Explored KML file from veloviewer or folder of activities.json for stathunter")
    parser.add_argument('-o','--output', dest="outputfile", default=r"zone_unexplored_tiles.kml", help="Output KML file of unexplored tiles")
    args = parser.parse_args()

    zonefile          = vars(args)['zonefile']
    exploredfile      = vars(args)['exploredfile']
    outputfile        = vars(args)['outputfile']

    ratio, exploredTileCount, tiles_count = computeFillRatio(zonefile, exploredfile, outputfile)
    print("Exploration ratio : {:.1f}% ({} of {})".format(100.0*ratio, exploredTileCount, tiles_count))
    