from getStatHuntersUserActivities import getStatHuntersUserActivities
import json
import os
import argparse

def updateUsersActivities(full=True):
    with open("users.config", encoding='utf-8' ) as f:
        d = json.load(f)
    user_zones = []
    for user in d['users']:
        print(user)
        url_uid = user['url'].split('/')[-1]
        user_data_path = os.path.join("gen", "users", url_uid)
        getStatHuntersUserActivities(user_data_path, user['url'], full=full)
  
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute exploration ratio of a zone')
    parser.add_argument('-f','--full', dest="full", action='store_true', help="Read the full history")
    args = parser.parse_args()

    full          = vars(args)['full']
    
    updateUsersActivities(full)
