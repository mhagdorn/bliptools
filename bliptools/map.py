import logging
import argparse
import pathlib

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

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

    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(format='%(levelname)s:%(message)s', level=level)
    cfg = readConfig(args.config)

    db = BlipDB('sqlite:///{}'.format(args.input))

    plt.figure(figsize=(10, 5))
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
    ax.coastlines()
    ax.gridlines()

    data = db.get_locations()
    ax.plot(data[:, 0], data[:, 1], 'o')

    plt.show()


if __name__ == '__main__':
    main()
