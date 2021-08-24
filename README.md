# Tiles Challenges

## Configuration

### Global configuration

Configuration is in json file `config.json`.

It contains 4 parts:

1. Challenges configuration
1. Activity types equivalence (from statshunters/strava activity types)
1. Zones list files
1. Country filter from zone name

### Users configuration

Users configuration is in json file `users.json`.

For security reason, this file is not under source control. An example is given in `users.example.json`

```json
  {
    "name" : "BouBou27",
    "url"  : "https://www.statshunters.com/share/b83b3a6d86d6",
    "zones" : [ "27", "75" ],
    "challenges": ["2021_Run", "2021_Ride", "2021_RunFromHome"]
  }
```

Fields:

* `name`: the name of the user
* `url`: statshunters.com shared link
* `zones`: list of zone for fill zone challenge
* `challenges`: list of challenge to play (defined in `config.json`)


## Process to generate zones data (to do one time)

### Extract kml zones from kml sources

Run `zones/extract_kml....py` to generate a kml file for each zone from a general kml by country: 

```
cd zones
python extract_kml_france.py
python extract_kml_belgium.py
python extract_kml_germany.py
python extract_kml_switzerland.py
```

### Compute all tiles for each zones

Run `build_tiles_zones.py` to generate a file that list all tiles for each zones (to not have to compute them at ech time)

```
python build_tiles_zones.py
```

### Generate kml tiles by zones

It is possible to generate kml file of tiles for each zones.
It is not needed for the results, but some user could ask for it.

```
python kml_tiles_by_zones.py
```

## Process to update data

### Update user activities
 
```
python get_users_activities.py
```

By default, only the latest 500 activities will be updated. If you want to reload all activities, add `--full` (or `-f`) argument:

```
python get_users_activities.py --full
```

###  Compute statistics and ranking


#### Challenges

To compute challenges results for a given month.

```
python challenge.py -c 2021 -i 2
```

#### Ranking fill zones

```
python ranking_fill_zones.py
```

terminal output:
* list of raking for user/zone fill ratio

#### Ranking FR stats

```
python ranking_fr_stats.py
```

console output:
* list of ranking for users, sorted by number of visited departement

statistics:
* **NB**: number of visited departement
* **BBI**: Index of numer of departement vs. number of visited tiles (i.e. value of 10 means that user has visited 10 departements with at least 10 visited tiles for each)
* __BBI*10__: Index of  number departement vs. 10*(number of visited tiles) (i.e. value of 10 means that user has visited 10 departements with at least 100 visited tiles for each)
* **SQUARES**: Sum of the max square on each departement
* **BBI.SQUARES**: Index of number departement vs. departement max square (i.e. value of 10 means that user has 10 departements with at least 10x10 max square)

#### Community fill zones

```
python community_fill_zones.py
```

output:
* kml file of all the users `gen/users/kikourou_tiles.py`
* terminal output:

   for each country:
  
     * global fill ratio
     * fill ratio for each zone of the country

#### users report
```
python users_report.py
```

output:
* files `gen/users/{user name}/{user name}_{zone name}.kml`: kml for non visited tiles of the zone
* files `gen/users/{user name}/report {user name}txt`: report of fill ratio for each zones

