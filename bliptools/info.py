import logging
import argparse
import pathlib

from .model import BlipDB
from .config import readConfig


def main():
    cfg = pathlib.Path('~/.bliptools')
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='NAME',
                        help='read journal data from file NAME')
    parser.add_argument('-c', '--config', metavar='CFG',
                        type=pathlib.Path, default=cfg,
                        help=f'read configuration from CFG, default {cfg}')
    parser.add_argument('--verbose', action='store_true', default=False,
                        help='be verbose')
    parser.add_argument('--latest', action='store_true', default=False,
                        help='get the date of the latest entry')

    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(format='%(levelname)s:%(message)s', level=level)
    cfg = readConfig(args.config)

    db = BlipDB('sqlite:///{}'.format(args.input))

    if args.latest:
        print(db.latest)


if __name__ == '__main__':
    main()
