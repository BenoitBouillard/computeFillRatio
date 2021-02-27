import os
import argparse
from common.statshunters import get_statshunters_user_activities
from common.config import load_users, GEN_USER_DATA


def get_users_activities(full=True):
    users = load_users()

    for user in users:
        print("Update", user['name'])
        url_uid = user['url'].split('/')[-1]
        user_data_path = os.path.join(GEN_USER_DATA, url_uid)
        get_statshunters_user_activities(user_data_path, user['url'], full=full)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute exploration ratio of a zone')
    parser.add_argument('-f', '--full', dest="full", action='store_true', help="Read the full history")
    args = parser.parse_args()

    full = vars(args)['full']

    get_users_activities(full)
