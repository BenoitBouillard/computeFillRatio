import json
import os
from pathlib import Path

USERS_CONFIG_FILE = "users.json"
CONFIG_FILE = "config.json"

GEN_PATH = os.path.join('gen')
PUBLIC_PATH = os.path.join('static')
GEN_PUBLIC_PATH = os.path.join(PUBLIC_PATH, 'gen')

GEN_TILES_ZONES_INNER = os.path.join(GEN_PATH, "zones_inner_tiles.json")
GEN_TILES_ZONES_OUTER = os.path.join(GEN_PATH, "zones_outer_tiles.json")
GEN_USER_DATA = os.path.join(GEN_PATH, 'data')
GEN_USERS = os.path.join(GEN_PUBLIC_PATH, 'users')
GEN_ZONES = os.path.join(GEN_PUBLIC_PATH, 'zones')
GEN_COMMUNITY = os.path.join(GEN_PUBLIC_PATH, 'community')
GEN_ZONES_TILES = os.path.join(GEN_PUBLIC_PATH, 'zones_tiles')
GEN_RESULTS = os.path.join(GEN_PUBLIC_PATH, 'results')

Path(GEN_USER_DATA).mkdir(exist_ok=True, parents=True)
Path(GEN_USERS).mkdir(exist_ok=True, parents=True)
Path(GEN_ZONES).mkdir(exist_ok=True, parents=True)
Path(GEN_COMMUNITY).mkdir(exist_ok=True, parents=True)
Path(GEN_ZONES_TILES).mkdir(exist_ok=True, parents=True)
Path(GEN_RESULTS).mkdir(exist_ok=True, parents=True)


def load_users(only_url=True):
    with open(USERS_CONFIG_FILE, encoding='utf-8') as f:
        users = json.load(f)
    if only_url:
        users = list(filter(lambda user: 'url'  in user and user['url'] is not False, users))
    return users


def load_config():
    with open(CONFIG_FILE, encoding='utf-8') as f:
        config = json.load(f)
    if os.path.exists(os.path.join(GEN_PATH, 'zones_desc.json')):
        with open(os.path.join(GEN_PATH, 'zones_desc.json'), 'r') as hr:
            zones_desc = json.load(hr)
        for country, cc in config['coutries_wikidata'].items():
            config['countries'][country] = cc['prefix']+".*"
            if country in zones_desc:
                for zone, zc in zones_desc[country]['zones'].items():
                    if 'boundary' in zc:
                        config['zones'][zc['id']] = zc['boundary']['kml']
    return config
