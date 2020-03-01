import configparser
import pathlib

def readConfig(fname=pathlib.Path('~/.bliptools')):
    config = configparser.ConfigParser()
    config.read_file(fname.expanduser().open())

    cfg = {}

    if 'general' not in config.sections():
        raise RuntimeError('configuration file {} does not contain general section'.format(fname))

    for k in ['accesstoken','username','baseurl']:
        if not config.has_option('general',k):
            raise RuntimeError('configuration file {} has no option {} in section general'.format(fname,k))
        cfg[k] = config.get('general',k)

    return cfg

if __name__ == '__main__':
    print (readConfig())
