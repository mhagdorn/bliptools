import logging
import argparse
import pathlib

from .model import *
from .blipapi import *
from .config import *

def main():
    cfg = pathlib.Path('~/.bliptools')
    parser = argparse.ArgumentParser()
    parser.add_argument('output',metavar='NAME',help='store journal data in file NAME')
    parser.add_argument('-c','--config',metavar='CFG',type=pathlib.Path,default=cfg,help='read configuration from CFG, default {}'.format(cfg))
    parser.add_argument('--verbose',action='store_true',default=False,help='be verbose')
    
    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
        
    logging.basicConfig(format='%(levelname)s:%(message)s', level=level)
    cfg = readConfig(args.config)
    
    blip = BLIPApi(cfg['accesstoken'],cfg['baseurl'])
    db = BlipDB('sqlite:///{}'.format(args.output))
    
    for entry in blip.journal_entries('magi',newer=db.latest):
        db.add(**entry)
    db.commit()
    

if __name__ == '__main__':
    main()

