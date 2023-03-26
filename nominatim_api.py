import json
import pickle

import requests
import urllib3
import argparse
from pprint import pprint

urllib3.disable_warnings()

cache_file = "gen/cache_osm_toponyms_v2.pickle"

try:
    with open(cache_file, 'rb') as h:
        cache_osm_toponyms = pickle.load(h)
except:
    cache_osm_toponyms = {}


def osm_save_cache():
    with open(cache_file, 'wb') as h:
        pickle.dump(cache_osm_toponyms, h)

# hamlet locality

NOMONATIM_REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"

def nominatim_reverse(lat, lon, no_cache=False):
    if no_cache or (lat, lon) not in cache_osm_toponyms:
        payload = {
            'lat': lat,
            'lon': lon,
            'format': 'json',
            'zoom': 20
        }

        r = requests.get(NOMONATIM_REVERSE_URL, params=payload)
        pois = r.json()
        toponyms = []
        addrs = pois.get("address", {})
        cache_osm_toponyms[(lat, lon)] = addrs
    return cache_osm_toponyms[(lat, lon)]


TOPONYM_ORDER = ["village", "town", "city_district", "city", "municipality", "county",   "state", "region", "country"]
#                                                            arrondissement  Département Région   Fr. Metro  Pays

def nominatim_get_toponyms(lat, lon, no_cache=False):
    addrs = nominatim_reverse(lat, lon, no_cache)

    #print(pois['address'])
    toponyms = []
    for k in TOPONYM_ORDER:
        if k in addrs:
            toponyms.append( (k, addrs[k]) )

    #pprint(toponyms)
    # print("No POI for ", lat, lon)
    return toponyms



def nominatim_get_toponym(lat, lon, cache=False):
    ts = nominatim_reverse(lat, lon, cache)
    for k in TOPONYM_ORDER:
        if k in ts:
            return ts[k]
    return None


TOPONYM_ORDER_FIRST = ["village", "town", "city_district", "city", "municipality", "county", ]
TOPONYM_ORDER_SECOND = ["state", "region", "country"]
def nominatim_get_description(lat, lon, cache=False):
    ts = nominatim_reverse(lat, lon, cache)
    first = None
    for k in TOPONYM_ORDER_FIRST:
        if k in ts:
            first = ts[k]
            break
    for k in TOPONYM_ORDER_SECOND:
        if k in ts:
            second = ts[k]
            break
    if first and second:
        return first + ", "+second
    return None


search_order = ["hamlet", "village", "town", "city_district", "city", "municipality"]
NOMONATIM_SEARCH_URL = "https://nominatim.openstreetmap.org/search"

def nominatim_search(params):
    payload = {'format':"geojson"}
    payload.update(params)
    r = requests.get(NOMONATIM_SEARCH_URL, params=payload)
    search = r.json()
    pprint(search)

# class Squadrats(TilesInterface):
#    def __init__(self, config):
#        super(Statshunters, self).__init__(config['level'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='squadrats api')
    #parser.add_argument('-u', '--user', dest="user", default=None, help="for a specific user")
    args = parser.parse_args()
    print(nominatim_get_toponyms(49.23254491578095, 1.1231231287817809))
    print(nominatim_get_toponym(49.23254491578095, 1.1231231287817809))
    print(nominatim_get_description(49.23254491578095, 1.1231231287817809))

    #nominatim_search({'q': 'Montaure, 27400, France'})


    # print(osm_toponyms(49.23242907857599, 1.1230886278543386, True))
    # print(len(cache_osm_toponyms))
    # #pprint(cache_osm_toponyms)
    # osm_save_cache()


