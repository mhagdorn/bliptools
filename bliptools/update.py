import logging
import argparse
import pathlib

from .model import BlipDB
from .blipapi import BLIPApi
from .config import readConfig


def main():
    cfg = pathlib.Path('~/.bliptools')
    parser = argparse.ArgumentParser()
    parser.add_argument('output', metavar='NAME',
                        help='store journal data in file NAME')
    parser.add_argument('-u', '--user', metavar='USER',
                        help="get journal for user USER")
    parser.add_argument('-q', '--query', metavar="QUERY",
                        help="text query which may include # or @ shortcuts")
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

    blip = BLIPApi.from_cfg(cfg)
    db = BlipDB('sqlite:///{}'.format(args.output))

    if args.query is not None:
        for entry in blip.query(args.query, newer=db.latest):
            db.add(**entry)
    else:
        if args.user is None:
            u = cfg['username']
        else:
            u = args.user

        for entry in blip.journal_entries(u, newer=db.latest):
            db.add(**entry)
    db.commit()


if __name__ == '__main__':
    main()
