from pprint import pprint

import logging
import argparse
import pathlib
import geojson

from .model import *
from .config import *


def main():
    cfg = pathlib.Path('~/.bliptools')
    parser = argparse.ArgumentParser()
    parser.add_argument('input',metavar='NAME',help='read journal data from file NAME')
    parser.add_argument('--output','-o',metavar='NAME',help='write geojson to file NAME')
    parser.add_argument('-c','--config',metavar='CFG',type=pathlib.Path,default=cfg,help='read configuration from CFG, default {}'.format(cfg))
    parser.add_argument('--verbose',action='store_true',default=False,help='be verbose')

    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
        
    logging.basicConfig(format='%(levelname)s:%(message)s', level=level)
    cfg = readConfig(args.config)

    db = BlipDB('sqlite:///{}'.format(args.input))
    features=[]
    for e in db.get_entries_with_location():
        feature = geojson.Feature(geometry=geojson.Point((e.lon,e.lat)),
                                  properties = {'img':e.image_url,
                                                'title':e.title,
                                                'entry_id':str(e.entry_id),
                                                'date':str(e.date)})
        features.append(feature)
    features = geojson.FeatureCollection(features)
    features['last_updated'] = str(db.latest)

    if args.output:
        with open(args.output,'w') as out:
            out.write(geojson.dumps(features))
    else:
        pprint (features)
    
if __name__ == '__main__':
    main()
