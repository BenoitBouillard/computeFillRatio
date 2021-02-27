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

    lan_name = datadict['lan_name']
    lan_code = datadict['lan_code']

    # Create a KML Document and add it to the KML root object
    d = kml.Document(ns, lan_name, lan_name, lan_name)
    k.append(d)

    # Create a Placemark with a simple polygon geometry and add it to the
    # second folder of the Document
    d.append(placemark)

    filepath = os.path.join(GEN_ZONES, 'DE-{}-{}.kml'.format(lan_code, lan_name))
    with open(filepath, 'w', encoding='utf-8') as myfile:
        myfile.write(k.to_string(prettyprint=True))
    return 'DE-' + lan_code, filepath


k = kml.KML()
with open('sources/georef-germany-land.kml', 'rb') as myfile:
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
