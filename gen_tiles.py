import json

import urllib3
import time
import argparse
from pathlib import Path


from common.config import load_users
from common.fileutils import FileCheck
from common.statshunters import tiles_from_activities

urllib3.disable_warnings()

def gen_json_tiles(name, tiles, level=14):
    tiles_dict = {}
    for tile in tiles:
        if tile[0] not in tiles_dict:
            tiles_dict[tile[0]] = []
        tiles_dict[tile[0]].append(tile[1])

    Path("static/gen/users/{0}".format(name, level)).mkdir(exist_ok=True, parents=True)
    #with open("static/gen/users/{0}/tiles_{1}.json".format(name, level), "w") as h:
    with FileCheck("static/gen/users/{0}/tiles_{1}.json".format(name, level)) as h:
        json.dump(tiles_dict, h)

    return tiles


def action(user):
    url_uid = user['url'].split('/')[-1]
    name = user['name']
    print("Generate", name)
    tiles = tiles_from_activities(url_uid, filter_fct=lambda act: 'Virtual' not in act['type'])
    gen_json_tiles(name, tiles, level=14)


def for_each_users(action, *args):
    users = load_users()
    for user in users:
        action(user, *args)
    return users


def find_user(user_name):
    for user in load_users():
        if user['name'] == user_name:
            return user
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate clusters')
    parser.add_argument('-u', '--user', dest="user", default=None, help="for a specific user")
    args = parser.parse_args()
    user = vars(args)['user']
    if user:
        start_time = time.time()
        action(find_user(user))
        end_time = time.time()
        print("Duration:", end_time - start_time)
    else:
        for_each_users(action)

