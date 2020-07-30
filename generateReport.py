from computeFillRatio import computeFillRatio
from getStatHuntersUserActivities import getStatHuntersUserActivities
import json


with open("users.config", encoding='utf-8' ) as f:
    d = json.load(f)
for user in d['users']:
    print(user)
    #getStatHuntersUserActivities(user['name'], user['url'])
    ratio, explored_tile_count, zone_tiles_count = computeFillRatio(user['zone'], user['name'])
    user['explored_tile_count'] = explored_tile_count
    user['zone_tiles_count'] = zone_tiles_count
    user['ratio'] = ratio*100.0
    
 
pos = 0
print(" #  {:20} {:4}".format("NOM", "RATIO"))
for user in sorted(d['users'], key=lambda u: u['ratio'], reverse=True):
    pos += 1
    print("{1:2}: {0[name]:20} {0[ratio]:.1f}% ({0[explored_tile_count]:4} / {0[zone_tiles_count]:4} - {2})".format(user, pos, user['zone'].split('/')[1].split('.')[0]))