import argparse

from common.kmlutils import create_kml_for_tiles, kml_zone_to_tiles
from common.statshunters import tiles_from_activities


def compute_fill_ratio(zone_file, explored_file, output_file=None):
    # Get tiles from the zone
    if isinstance(zone_file, str):
        _, tiles = kml_zone_to_tiles(zone_file)
    else:
        tiles = zone_file

    if isinstance(explored_file, str):
        explored_tiles = tiles_from_activities(explored_file)
    else:
        explored_tiles = explored_file

    explored_tiles = explored_tiles & tiles
    unexplored_tiles = tiles - explored_tiles

    explored_tile_count = len(explored_tiles)

    ratio = explored_tile_count / len(tiles)

    if output_file:
        create_kml_for_tiles(unexplored_tiles, output_file)

    return ratio, explored_tile_count, len(tiles)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute exploration ratio of a zone')
    parser.add_argument('-z', '--zone', dest="zonefile", default=r"zone.kml", help="Zone KML file")
    parser.add_argument('-e', '--explored', dest="exploredfile", default=r"explored_tiles.kml",
                        help="Explored KML file from veloviewer or folder of activities.json for stathunter")
    parser.add_argument('-o', '--output', dest="outputfile", default=r"zone_unexplored_tiles.kml",
                        help="Output KML file of unexplored tiles")
    args = parser.parse_args()

    zonefile = vars(args)['zonefile']
    exploredfile = vars(args)['exploredfile']
    outputfile = vars(args)['outputfile']

    ratio, exploredTileCount, tiles_count = compute_fill_ratio(zonefile, exploredfile, outputfile)
    print("Exploration ratio : {:.1f}% ({} of {})".format(100.0 * ratio, exploredTileCount, tiles_count))
