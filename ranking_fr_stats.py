from common.config import load_users
from common.zones import load_zones_outer
from common.statshunters import tiles_from_activities
from common.squares import compute_max_square

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

    user['eddington'] = eddigton(user['fill'].values())
    user['eddington10'] = eddigton(user['fill'].values(), factor=10)
    user['eddingtonSquare'] = eddigton(user['maxsquare'].values())

pos = 0
print("#   {:17} {:>6} {:>6} {:>6} {:>6} {:>6}".format("NOM", "NB", "BBI", "BBI*10", "SQUARES", "BBI.SQUARES"))
for user in sorted(users, key=lambda u: u['fill_count'], reverse=True):
    pos += 1
    print("{1:<2}: {0[name]:17} {0[fill_count]:>6} {0[eddington]:>6} {0[eddington10]:>6} {0[sum_maxsquare]:>6} {0[eddingtonSquare]:>6}".format(
            user, pos))
