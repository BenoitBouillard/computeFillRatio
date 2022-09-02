import argparse
import os

from common.config import load_users, GEN_USER_DATA
from common.statshunters import get_statshunters_user_activities


def get_users_activities(full=True, name=None):
    users = load_users()

    last_activity_dates = {}

    for user in users:
        if 'url' not in user or user['url'] == False:
            continue
        if name and name not in user['name']:
            continue
        print("Update", user['name'])
        url_uid = user['url'].split('/')[-1]
        user_data_path = os.path.join(GEN_USER_DATA, url_uid)
        date = get_statshunters_user_activities(user_data_path, user['url'], full=full)
        if date:
            last_activity_dates[user['name']] = date

    from collections import OrderedDict
    last_activity_dates = OrderedDict(sorted(last_activity_dates.items(), key=lambda kvp: kvp[1], reverse=True))
    for k, v in last_activity_dates.items():
        print("{:<20} : {}".format(k, v))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute exploration ratio of a zone')
    parser.add_argument('-f', '--full', dest="full", action='store_true', help="Read the full history")
    parser.add_argument('-n', '--name', dest="name", default=None, help="name to update")
    args = parser.parse_args()

    full = vars(args)['full']
    name = vars(args)['name']

    get_users_activities(full, name)
