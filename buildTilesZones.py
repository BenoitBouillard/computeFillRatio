import json
from fastkml import kml, styles
from tile import TileFromCoord, Tile
from pprint import pprint
from shapely.geometry import Polygon, Point
import shapely
import argparse
import os

def kmlZoneToInnerTiles(kml_file):
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
                if polygon.contains(t.polygon):
                    tiles.append(t.uid)
    return tiles
    
def kmlZoneToOuterTiles(kml_file):
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
                if polygon.intersects(t.polygon):
                    tiles.append(t.uid)
    return tiles
        

    
with open("users.config", encoding='utf-8' ) as f:
    d = json.load(f)
user_zones = []
zones = {}
for zone in d['zones']:
    if len(zone) > 3 :  continue
    zones[zone] = kmlZoneToInnerTiles(d['zones'][zone])
    print("load zone {} : {} tiles".format(zone, len(zones[zone])))
    #if zone == "02": break

with open("gen/zones_inner_tiles.json", 'w', encoding='utf-8' ) as f:
    json.dump(zones, f)

with open("users.config", encoding='utf-8' ) as f:
    d = json.load(f)
user_zones = []
zones = {}
for zone in d['zones']:
    if len(zone) > 3 :  continue
    zones[zone] = kmlZoneToOuterTiles(d['zones'][zone])
    print("load zone {} : {} tiles".format(zone, len(zones[zone])))
    #if zone == "02": break
    
with open("gen/zones_outer_tiles.json", 'w', encoding='utf-8' ) as f:
    json.dump(zones, f)
