import os

from common.config import load_users, GEN_RESULTS
from common.squares import compute_max_square
from common.statshunters import tiles_from_activities
from common.zones import load_zones_outer

outer_zones = load_zones_outer("[0-9].*")
users = load_users()

user_zones = []


def eddigton(data, factor=1):
    eddington = 1
    while True:
        if len(list(filter(lambda x: x >= eddington * factor, data))) < eddington:
            break
        eddington += 1
    return eddington - 1

for user in users:
    print("Treat " + user['name'])
    url_uid = user['url'].split('/')[-1]
    user['fill'] = {}
    user['maxsquare'] = {}
    user['sum_maxsquare'] = 0
    user['fill_count'] = 0
    explored_tiles = tiles_from_activities(url_uid, filter_fct=lambda act: 'Virtual' not in act['type'])

    for zone in outer_zones:
        explored_tiles_zone = outer_zones[zone] & explored_tiles
        if explored_tiles_zone:
            user['fill'][zone] = len(explored_tiles_zone)
            user['fill_count'] += 1
            zone_max_square = compute_max_square(outer_zones[zone] & explored_tiles)
            user['maxsquare'][zone] = zone_max_square
            user['sum_maxsquare'] += user['maxsquare'][zone]
            user['rank'] = 1

    user['eddington'] = eddigton(user['fill'].values())
    user['eddington10'] = eddigton(user['fill'].values(), factor=10)
    user['eddingtonSquare'] = eddigton(user['maxsquare'].values())


with open(os.path.join(GEN_RESULTS, 'ranking_fr_stats.txt'), 'w') as h:
    pos = 0
    header = "#   {:17} {:>6} {:>6} {:>6} {:>6} {:>6}".format("NOM", "NB", "BBI", "BBI*10", "SQUARES", "BBI.SQUARES")
    print(header)
    h.write(header+"\n")

    fields = ["fill_count", "eddington", "eddington10", "sum_maxsquare", "eddingtonSquare"]
    fields_results = {}
    for f in fields:
        fields_results[f] = sorted([u[f] for u in users], reverse=True)
        for user in users:
            rank = fields_results[f].index(user[f])
            user["rank_"+f] = rank + 1
            user["rank"] += rank

    for user in sorted(users, key=lambda u: u['rank']):
        pos += 1
        line = "{1:<3}: {0[name]:17}".format(user, user['rank'])
        for f in fields:
            if user[f]==max([u[f] for u in users]):
                val = "*{}*".format(user[f])
            else:
                val = "{} ".format(user[f])
            line += " {:>6}".format(val)
        print(line)
        h.write(line+"\n")
