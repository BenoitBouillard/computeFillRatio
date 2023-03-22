import argparse
import os
import json
from pathlib import Path

import overpy
from fastkml import kml
from qwikidata.sparql import return_sparql_query_results
from shapely import geometry
from shapely.ops import linemerge, unary_union, polygonize

from common.config import GEN_PATH
from common.config import load_config, GEN_ZONES
from common.kmlutils import geom2kml
from common.geojson_utils import shapely_to_geojson
from common.fileutils import FileCheck
from common.tile import geom_to_tiles

parser = argparse.ArgumentParser(description='Compute exploration ratio of a zone')
parser.add_argument('-f', '--force', dest="force", action='store_true', help="Force regeneration")
args = parser.parse_args()

force = vars(args)['force']

overpass = overpy.Overpass(max_retry_count=5, retry_timeout=30)


def create_kml_for_placemark(placemark):
    # Create the root KML object
    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'

    data = placemark.extended_data.elements[0].data
    datadict = {}
    for kv in data:
        datadict[kv['name']] = kv['value']

    insee_dep = datadict['insee_dep']
    nom_dep = datadict['nom_dep']

    # Create a KML Document and add it to the KML root object
    d = kml.Document(ns, nom_dep, nom_dep, nom_dep)
    k.append(d)

    # Create a Placemark with a simple polygon geometry and add it to the
    # second folder of the Document
    d.append(placemark)

    if len(insee_dep) < 2:
        insee_dep = '0' + insee_dep
    filepath = os.path.join(GEN_ZONES, '{}-{}.kml'.format(insee_dep, nom_dep))
    with open(filepath, 'w', encoding='utf-8') as myfile:
        myfile.write(k.to_string(prettyprint=True))
    return insee_dep, filepath


def get_osm_limits(rel):
    result = overpass.query("rel({});out skel geom;".format(rel))
    try:
        relation = result.get_relations()[0]
    except:
        return None
    boundary_osm_url = 'https://www.openstreetmap.org/relation/{}'.format(rel)
    print("boundary_osm_url : ", boundary_osm_url)
    inners = [geometry.LineString([(float(g.lon), float(g.lat)) for g in m.geometry]) for m in relation.members if m.role == 'inner']
    inner = linemerge(inners)
    borders = unary_union(inner)  # linestrings to a MultiLineString
    polygons = list(polygonize(borders))
    inner_geom = geometry.MultiPolygon(polygons)
    outers = [geometry.LineString([(float(g.lon), float(g.lat)) for g in m.geometry]) for m in relation.members if m.role == 'outer']
    outer = linemerge(outers)
    borders = unary_union(outer)
    polygons = list(polygonize(borders))
    admin_geom = geometry.MultiPolygon(polygons)
    admin_geom = admin_geom.difference(inner_geom)
    return admin_geom


def geom_to_kml(geom, file):
    Path(file).parent.mkdir(exist_ok=True, parents=True)
    k = geom2kml(geom)
    with FileCheck(kml_file) as f:
        f.write(k.to_string(prettyprint=True))
    return file


def geom_to_geojson(geom, file):
    Path(file).parent.mkdir(exist_ok=True, parents=True)
    geojson = shapely_to_geojson(geom)
    with FileCheck(file, encoding='utf-8') as f:
        f.write(json.dumps(geojson))
    return file


config = load_config()

zones_config = {}
if not force:
    if os.path.exists(os.path.join(GEN_PATH, 'zones_desc.json')):
        with open(os.path.join(GEN_PATH, 'zones_desc.json'), 'r') as hr:
            zones_config = json.load(hr)

#zones_config["Italie"] = {'name': "Italie", 'zones': {}}
zones_config.pop("Pays-Bas")

for country, cc in config['coutries_wikidata'].items():
    print("Process country", country)
    if country not in zones_config:
        zones_config[country] = {'name': country, 'zones': {}}
    wikidata_sparqls = cc['wikidata_sparql']
    if not isinstance(wikidata_sparqls, list):
        wikidata_sparqls = [wikidata_sparqls]
    for wikidata_sparql in wikidata_sparqls:
        res = return_sparql_query_results(wikidata_sparql)
        for r in res['results']['bindings']:
            zone_name = r['zoneLabel']['value']
            zone_code = r['code']['value']
            if (not force) and (zone_name in zones_config[country]['zones']):
                print("  Zone", zone_name, "already done")
                continue

            print("  Process zone", zone_name)
            admin_geom = get_osm_limits(r['osm_rel']['value'])
            if admin_geom is None:
                print("    !!! relation error !!!")
                continue
            zones_config[country]['zones'][zone_name] = {'name': zone_name, 'id': zone_code}

            kml_file = os.path.join(GEN_ZONES, country, zone_name+'.kml')
            zones_config[country]['zones'][zone_name]['boundary'] = {
                'kml': geom_to_kml(admin_geom, kml_file),
                'geojson': geom_to_geojson(admin_geom, os.path.join(GEN_ZONES, country, zone_name+'.geojson'))
            }
            tiles_inner, tiles_outer = geom_to_tiles(admin_geom)
            zones_config[country]['zones'][zone_name]['tiles'] = {
                'outer': list(tiles_outer),
                'inner': list(tiles_inner)
            }
            with FileCheck(os.path.join(GEN_PATH, 'zones_desc.json')) as hw:
                json.dump(zones_config, hw)

with FileCheck(os.path.join(GEN_PATH, 'zones_desc.json')) as hw:
    json.dump(zones_config, hw)
