import json
import pickle

import requests
import urllib3
import argparse
from pprint import pprint

urllib3.disable_warnings()

cache_file = "gen/cache_osm_toponyms_v1.pickle"

try:
    with open(cache_file, 'rb') as h:
        cache_osm_toponyms = pickle.load(h)
except:
    cache_osm_toponyms = {}


def osm_save_cache():
    with open(cache_file, 'wb') as h:
        pickle.dump(cache_osm_toponyms, h)

# hamlet locality
address_order = ["village", "town", "city_district", "city", "municipality", "county",   "state", "region", "country"]
#                                                            arrondissement  Département Région   Fr. Metro  Pays

NOMONATIM_REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"

def nominatim_get_toponyms(lat, lon, no_cache=False):
    if no_cache or (lat, lon) not in cache_osm_toponyms:
        payload = {
            'lat': lat,
            'lon': lon,
            'format': 'json',
            'zoom': 20,
            'addressdetails': 1
           # 'extratags': 1
        }
        #print(payload)

        r = requests.get(NOMONATIM_REVERSE_URL, params=payload)
        # print(r.status_code)
        pois = r.json()
        # pprint(pois)
        toponyms = []
        if "address" in pois:
            #print(pois['address'])
            for k, v in pois["address"].items():
                if k in address_order:
                    toponyms.append( (k, v) )
            toponyms.sort(key=lambda x:address_order.index(x[0]))
            #pprint(toponyms)
        else:
            print("No POI for ", lat, lon)
        cache_osm_toponyms[(lat, lon)] = toponyms
    return cache_osm_toponyms[(lat, lon)]


def nominatim_get_toponym(lat, lon, cache=False):
    ts = nominatim_get_toponyms(lat, lon, cache)
    if ts:
        return ts[0][1]
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
    nominatim_get_toponyms(49.23254491578095, 1.1231231287817809, True)

    nominatim_search({'q': 'Montaure, 27400, France'})


    # print(osm_toponyms(49.23242907857599, 1.1230886278543386, True))
    # print(len(cache_osm_toponyms))
    # #pprint(cache_osm_toponyms)
    # osm_save_cache()


