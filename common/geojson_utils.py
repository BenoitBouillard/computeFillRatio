from shapely import geometry
import geojson


def shapely_to_geojson(shape):
    if isinstance(shape, geometry.Polygon):
        return geojson.Polygon([list(shape.exterior.coords), *[list(x.coords) for x in shape.interiors]])
    if isinstance(shape, geometry.MultiPolygon):
        return geojson.MultiPolygon([shapely_to_geojson(p) for p in shape.geoms])
    if shape.is_empty:
        return geojson.MultiPolygon()
    raise Exception("Not manage", shape)


