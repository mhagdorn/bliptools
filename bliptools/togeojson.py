from pprint import pprint

import logging
import argparse
import pathlib
import geojson
import datetime

from .model import BlipDB
from .config import readConfig


def main():
    cfg = pathlib.Path('~/.bliptools')
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='NAME',
                        help='read journal data from file NAME')
    parser.add_argument('-s', '--start-date', metavar='YYYY-MM-DD',
                        help='the start date from which to extract data')
    parser.add_argument('-e', '--end-date', metavar='YYYY-MM-DD',
                        help='the end date until which to extract data')
    parser.add_argument('--output', '-o', metavar='NAME',
                        help='write geojson to file NAME')
    parser.add_argument('-c', '--config', metavar='CFG',
                        type=pathlib.Path, default=cfg,
                        help=f'read configuration from CFG, default {cfg}')
    parser.add_argument('--verbose', action='store_true', default=False,
                        help='be verbose')

    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(format='%(levelname)s:%(message)s', level=level)
    cfg = readConfig(args.config)

    start = None
    if args.start_date is not None:
        try:
            start = datetime.datetime.strptime(
                args.start_date, '%Y-%m-%d').date()
        except Exception as e:
            parser.error(f'Cannot parse start date: {e}')
    end = None
    if args.end_date is not None:
        try:
            end = datetime.datetime.strptime(args.end_date, '%Y-%m-%d').date()
        except Exception as e:
            parser.error('Cannot parse end date: {}'.format(e))

    db = BlipDB('sqlite:///{}'.format(args.input))
    features = []
    for e in db.get_entries_with_location(start=start, end=end):
        feature = geojson.Feature(geometry=geojson.Point((e.lon, e.lat)),
                                  properties={'img': e.image_url,
                                              'title': e.title,
                                              'entry_id': str(e.entry_id),
                                              'date': str(e.date)})
        features.append(feature)
    features = geojson.FeatureCollection(features)
    features['last_updated'] = str(db.latest)

    if args.output:
        with open(args.output, 'w') as out:
            out.write(geojson.dumps(features))
    else:
        pprint(features)


if __name__ == '__main__':
    main()
