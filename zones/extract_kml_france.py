from fastkml import kml
import os
from common.config import GEN_ZONES


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


k = kml.KML()
with open('sources/contours-geographiques-des-departements-2019.kml', 'rb') as myfile:
    doc = myfile.read()
    k.from_string(doc)

features = list(k.features())
doc = features[0]
deps = {}
for p in doc.features():
    dep, path = create_kml_for_placemark(p)
    deps[dep] = path
for dep in sorted(deps.keys()):
    print('"{}" : "{}",'.format(dep, deps[dep]))
