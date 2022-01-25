__all__ = ['readConfig']

import configparser
import pathlib


def readConfig(fname=pathlib.Path('~/.bliptools')):
    config = configparser.ConfigParser()
    config.read_file(fname.expanduser().open())

    cfg = {}

    if 'general' not in config.sections():
        raise RuntimeError(
            f'configuration file {fname} does not contain general section')

    for k in ['accesstoken', 'username', 'baseurl']:
        if not config.has_option('general', k):
            raise RuntimeError(
                f'configuration file {fname} has no option {k} '
                'in section general')
        cfg[k] = config.get('general', k)

    return cfg


if __name__ == '__main__':
    print(readConfig())
