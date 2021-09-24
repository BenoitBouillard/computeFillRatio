from fastkml import kml
import os
from common.config import GEN_ZONES


def create_kml_for_placemark(placemark):
    # Create the root KML object
    kml_doc = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'

    data = placemark.extended_data.elements[0].data
    datadict = {}
    for kv in data:
        datadict[kv['name']] = kv['value']

    nom_province = datadict['nom_province']

    # Create a KML Document and add it to the KML root object
    d = kml.Document(ns, nom_province, nom_province, nom_province)
    kml_doc.append(d)

    # Create a Placemark with a simple polygon geometry and add it to the
    # second folder of the Document
    d.append(placemark)

    filepath = os.path.join(GEN_ZONES, 'BE-{}.kml'.format(nom_province))
    with open(filepath, 'w', encoding='utf-8') as kml_handle:
        kml_handle.write(kml_doc.to_string(prettyprint=True))
    return nom_province, filepath

k = kml.KML()
with open('sources/provinces-belges-2019.kml', 'rb') as myfile:
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
