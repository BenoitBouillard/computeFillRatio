import argparse
import os
import re
from datetime import datetime
from collections import OrderedDict

from common import statshunters
from common.config import load_users, load_config
from common.squares import compute_max_square, compute_cluster

# FIELDS = ['square', 'cluster', 'tiles', 'activities', 'useful_ac', 'unique_tiles']
FIELDS = ['square', 'cluster', 'tiles', 'activities']


def compute_challenges(challenge_str=None, index=None):
    config = load_config()
    users_json = load_users()

    if challenge_str in config['challenges']:
        challenges = [challenge_str]
    elif challenge_str is None:
        challenges = config['challenges'].keys()
    else:
        challenges = list(filter(lambda c: challenge_str in c, config['challenges'].keys()))

    for challenge in challenges:
        print("")
        print("=== {} ===".format(challenge))

        challenge_config = config['challenges'][challenge]
        activity_types = config['activity_types_equiv'][challenge_config['activity_type']]

        users = list(filter(lambda u: challenge_config.get('user_default', False) or challenge in u.get('challenges', []), users_json))

        compare = challenge_config.get('compare', False)
        if not isinstance(compare, bool):
            compare = eval(compare, {}, {'index': index})

        sort_fields = challenge_config.get('sort', [])
        sort_fields += [f for f in FIELDS if f not in sort_fields]

        def compute_results(users, for_index):
            results = OrderedDict()

            for user in users:
                url_uid = user['url'].split('/')[-1]
                activities_list = statshunters.load_user_activities(os.path.join(url_uid))
                activities_list = list(filter(lambda a: a['type'] in activity_types, activities_list))
                for filter_str in challenge_config.get('filter', []):
                    activities_list = list(filter(lambda a: eval(filter_str,
                                                                 {"re": re, "datetime": datetime},
                                                                 {"activity": a, "index": for_index}), activities_list))

                tiles = set()
                useful_activities_count = 0
                unique_tiles = set()
                for a in activities_list:
                    unique_tiles -= a['tiles']
                    unique_tiles |= (a['tiles'] - tiles)
                    if not a['tiles'].issubset(tiles):
                        useful_activities_count += 1
                        tiles |= a['tiles']
                results[user['name']] = {
                    'user': user['name'],
                    'activities': len(activities_list),
                    'tiles': len(tiles),
                    'square': compute_max_square(tiles),
                    'cluster': compute_cluster(tiles),
                    'useful_ac': useful_activities_count,
                    'unique_tiles': len(unique_tiles),
                }
            results = OrderedDict(sorted(results.items(), key=lambda kvp: tuple([kvp[1][f] for f in sort_fields]), reverse=True))
            rank = 1
            for user, result in results.items():
                result['rank'] = rank
                rank += 1
            return results

        users_results = compute_results(users, index)

        users = list(filter(lambda u: users_results[u['name']]['activities'] > 0, users))
        users_results = OrderedDict(filter(lambda kvp: kvp[1]['activities'] > 0, users_results.items()))

        if compare:
            users_results_prev = compute_results(users, index - 1)
            for userName in users_results_prev:
                users_results[userName]["rank_diff"] = users_results_prev[userName]['rank'] - \
                                                           users_results[userName]['rank']
                for field in FIELDS:
                    users_results[userName][field + "_diff"] = users_results[userName][field] - \
                                                               users_results_prev[userName][field]

        if compare:
            format_str = "{0:<2} {2:>4} {1:<16}"
        else:
            format_str = "{0:<2} {1:<16}"

        header = format_str.format("##", "Name", "Diff")

        for sf in sort_fields:
            if compare:
                header += " {:^11}".format(sf)
            else:
                line = " {:>5}".format(sf)
                line += " " * (11 - len(line))
                header += line

        print(header)

        rank = 1
        for user, result in users_results.items():
            if compare:
                line_str = format_str.format(result['rank'], result['user'], "({:+2})".format(result["rank_diff"]))
            else:
                line_str = format_str.format(result['rank'], result['user'], "")

            for sf in sort_fields:
                line = " {:>5}".format(result[sf])
                if compare:
                    p = "({:+3})".format(result[sf + "_diff"])
                    if len(p) < 6:
                        p += " " * (6 - len(p))
                    line += p
                else:
                    line += "     "

                line_str += line

            print(line_str)
            rank += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute challenge stats')
    parser.add_argument('-c', '--challenge', dest="challenge", help="Challenges to compute")
    parser.add_argument('-i', '--index', dest="index", type=int, default=1, help="index of computation (ie month)")

    args = parser.parse_args()

    challenge = vars(args)['challenge']
    index = vars(args)['index']

    compute_challenges(challenge, index)
