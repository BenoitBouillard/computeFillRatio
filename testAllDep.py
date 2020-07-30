import json
from fastkml import kml, styles
from tile import TileFromCoord, Tile
from pprint import pprint
from shapely.geometry import Polygon, Point
import shapely
import argparse
import os

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
                if polygon.contains(t.polygon):
                    tiles.append(t.uid)
    return frozenset(tiles)
        

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
    return frozenset(tiles)
       
    
def computeMaxSquare(tiles):

    def is_square(x, y, m):
        for dx in range(m):
            for dy in range(m):
                uid = "{}_{}".format(x+dx, y+dy)
                if uid not in tiles : return False
        return True

    max_square = 0
    for tile in tiles:
        x = int(tile.split('_')[0])
        y = int(tile.split('_')[1])
        while is_square(x, y, max_square+1):
            max_square += 1
    return max_square
    
with open("gen/zones_inner_tiles.json", encoding='utf-8' ) as f:
    inner_zones = json.load(f)
for zone in inner_zones:
    inner_zones[zone] = frozenset(inner_zones[zone])
    
with open("gen/zones_outer_tiles.json", encoding='utf-8' ) as f:
    outer_zones = json.load(f)
for zone in outer_zones:
    outer_zones[zone] = frozenset(outer_zones[zone])
    
with open("users.config", encoding='utf-8' ) as f:
    d = json.load(f)
user_zones = []

def computeEddigton(data, factor=1):
    eddington = 1
    while True:
        if len(list(filter(lambda x:x>=eddington*factor, data)))<eddington:
            break
        eddington += 1
    return eddington-1


for user in d['users']:
    print(user)
    url_uid = user['url'].split('/')[-1]
    user['fill'] = {}
    user['maxsquare'] = {}
    user['sum_maxsquare'] = 0
    user['fill_count'] = 0
    explored_tiles = tilesFromActivities(os.path.join("gen", "users", url_uid))
    
    for zone in inner_zones:
        # print(zones[zone])
        # print(tilesFromActivities(url_uid))
        explored_tiles_zone = inner_zones[zone] & explored_tiles
        if explored_tiles_zone:
            user['fill'][zone] = len(explored_tiles_zone)
            user['fill_count'] += 1
        zone_max_square = computeMaxSquare(outer_zones[zone] & explored_tiles)
        if zone_max_square > 0 :
            user['maxsquare'][zone] = zone_max_square
            user['sum_maxsquare'] += user['maxsquare'][zone]

    user['eddington']       = computeEddigton(user['fill'].values())
    user['eddington10']     = computeEddigton(user['fill'].values(), factor=10)
    user['eddingtonSquare'] = computeEddigton(user['maxsquare'].values())
    print(user)

pos = 0
print("#   {:35} {:>5} {:>5} {:>5} {:>5} {:>5}".format("NOM", "NB", "EDD.", "EDD.*10", "QUARES", "EDD.SQUARES"))
for user in sorted(d['users'], key=lambda u: u['fill_count'], reverse=True):
    pos += 1
    print("{1:<2}: {0[name]:35} {0[fill_count]:>5} {0[eddington]:>5} {0[eddington10]:>5} {0[sum_maxsquare]:>5} {0[eddingtonSquare]:>5}".format(user, pos))
