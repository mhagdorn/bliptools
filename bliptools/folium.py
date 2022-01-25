import logging
import argparse
import pathlib
import folium
from folium.plugins import MarkerCluster
from branca.element import Element

from .model import BlipDB
from .config import readConfig


def main():
    cfg = pathlib.Path('~/.bliptools')
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='NAME', type=pathlib.Path,
                        help='read journal data from file NAME')
    parser.add_argument('--output', '-o', metavar='NAME',
                        type=pathlib.Path,
                        help='write geojson to file NAME')
    parser.add_argument('-c', '--config', metavar='CFG',
                        type=pathlib.Path, default=cfg,
                        help=f'read configuration from CFG, default {cfg}')
    parser.add_argument('-t', '--twitter', metavar="HANDLE",
                        help="twitter handler")
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

    if args.output is None:
        out = args.input.stem + '.html'
    else:
        out = str(args.output)

    popup = """<p>
<a href="https://blipfoto.com/entry/{e.entry_id}">
<img width="200px" src="{e.image_url}"></a>
<strong>{e.date}:</strong> {e.title}
</p>
"""

    m = folium.Map(location=[55.952060, -3.196480])
    mc = MarkerCluster()
    for e in db.get_entries_with_location():
        mc.add_child(folium.Marker(location=[e.lat, e.lon],
                                   popup=popup.format(e=e)))

    m.add_child(mc)

    html = m.get_root()
    description = "Interactive map showing all geotagged entries "\
        f"of blip journal https://www.blipfoto.com/{e.username}"
    html.header.add_child(Element(
        f'<meta name="description" content="{description}" />'))
    html.header.add_child(
        Element('<meta name="twitter:card" content="summary_large_image">'))
    if args.twitter is not None:
        html.header.add_child(
            Element(f'<meta name="twitter:site" content="{args.twitter}">'))
    html.header.add_child(
        Element(f'<meta name="twitter:title" content="{e.username}">'))
    html.header.add_child(
        Element(f'<meta name="twitter:description" content="{description}">'))
    html.header.add_child(
        Element(f'<meta name="twitter:image" content="{e.image_url}">'))

    m.save(out)


if __name__ == '__main__':
    main()
