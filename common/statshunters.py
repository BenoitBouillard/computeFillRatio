import os
from common import config
import json
from pathlib import Path
from common.urlutils import my_urlretrieve


def get_statshunters_user_activities(path, sharelink, full=False):
    page = 1
    Path(path).mkdir(exist_ok=True, parents=True)

    if not full:
        while os.path.exists(os.path.join(path, "activities_{}.json".format(page + 2))):
            page += 1




    last_activity = None
    while True:
        filepath = os.path.join(path, "activities_{}.json".format(page))
        url = sharelink + "/api/activities?page={0}".format(page)
        print("Get page {} ({})".format(page, url))
        my_urlretrieve(url, filepath)
        with open(filepath) as f:
            d = json.load(f)
            if len(d['activities']) == 0:
                break
            last_activity = d['activities'][-1]['date']
        page += 1
    print("Last activity:", last_activity)

    return last_activity


def load_user_activities(user_id, filter_fct=None):
    # Get tiles from activities files from stathunters
    activities_dir = os.path.join(config.GEN_USER_DATA, user_id)
    directory = os.fsencode(activities_dir)
    activities = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            with open(os.path.join(activities_dir, filename)) as f:
                d = json.load(f)
                for activity in d['activities']:
                    if filter_fct and not filter_fct(activity):
                        continue
                    activity['tiles'] = set([(tile['x'], tile['y']) for tile in activity['tiles']])
                    activities.append(activity)
    return activities


def tiles_from_activities(user_id, filter_fct=None):
    # Get tiles from activities files from stathunters
    activities_dir = os.path.join(config.GEN_USER_DATA, user_id)
    directory = os.fsencode(activities_dir)
    tiles = []

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            with open(os.path.join(activities_dir, filename)) as f:
                d = json.load(f)
                for activity in d['activities']:
                    if filter_fct and not filter_fct(activity):
                        continue
                    for tile in activity['tiles']:
                        uid = (tile['x'], tile['y'])
                        if uid not in tiles:
                            tiles.append(uid)
    return frozenset(tiles)


def decode_polyline(polyline):
    """Decodes a Polyline string into a list of lat/lng dicts.
    See the developer docs for a detailed description of this encoding:
    https://developers.google.com/maps/documentation/utilities/polylinealgorithm
    :param polyline: An encoded polyline
    :type polyline: string
    :rtype: list of dicts with lat/lng keys
    """
    points = []
    index = lat = lng = 0
    try:
        while index < len(polyline):
            result = 1
            shift = 0
            while True:
                b = ord(polyline[index]) - 63 - 1
                index += 1
                result += b << shift
                shift += 5
                if b < 0x1f:
                    break
            lat += (~result >> 1) if (result & 1) != 0 else (result >> 1)

            result = 1
            shift = 0
            while True:
                b = ord(polyline[index]) - 63 - 1
                index += 1
                result += b << shift
                shift += 5
                if b < 0x1f:
                    break
            lng += ~(result >> 1) if (result & 1) != 0 else (result >> 1)

            points.append((lat * 1e-5, lng * 1e-5))
    except:
        print("decode error {}/{}".format(index, len(polyline)))

    return points
