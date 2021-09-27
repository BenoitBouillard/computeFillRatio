import argparse

from common.statshunters import get_statshunters_user_activities

parser = argparse.ArgumentParser(description='Compute exploration ratio of a zone')
parser.add_argument('-n', '--name', dest="username", help="User name for saving data")
parser.add_argument('-s', '--sharelink', dest="sharelink", help="Stathunters share link to recover data")
args = parser.parse_args()

username = vars(args)['username']
sharelink = vars(args)['sharelink']

get_statshunters_user_activities(username, sharelink)
