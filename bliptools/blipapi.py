__all__ = ['BLIPApi']

import logging
import requests
import datetime


class BlipError(Exception):
    """blip API error"""
    pass


class BLIPApi:
    def __init__(self, token, baseurl, client_id):
        self._accesstoken = token
        self._baseurl = baseurl
        self._client_id = client_id
        self._headers = {
            'Authorization': f'Bearer {client_id}'}

    @classmethod
    def from_cfg(cls, cfg):
        return cls(cfg['accesstoken'], cfg['baseurl'], cfg['client_id'])

    @property
    def accesstoken(self):
        return self._accesstoken

    @property
    def baseurl(self):
        return self._baseurl

    @property
    def headers(self):
        return self._headers

    def url(self, api):
        return '{}/{}'.format(self.baseurl, api)

    def _get_entries(self, url, params, newer=None):  # NOQA: C901
        index = 0
        num_entries = 100
        if newer is not None:
            logging.info(f'selecting entries newer than {newer}')
        while True:
            logging.info(f'requesting page {index} with {num_entries} entries')
            params['page_size'] = num_entries
            params['page_index'] = index
            r = requests.get(self.url(url),
                             params=params,
                             headers=self.headers)
            data = r.json()
            if data['error'] is not None:
                raise BlipError(data['error']['message'])
            data = data['data']
            page = data['page']
            entries = data['entries']

            for e in entries:
                entry = {}
                entry['date'] = datetime.datetime.strptime(
                    e['date'], '%Y-%m-%d').date()
                if newer is not None:
                    if entry['date'] <= newer:
                        logging.info('done - entry is too old')
                        return
                for k in ['entry_id', 'title', 'username',
                          'thumbnail_url', 'image_url']:
                    entry[k] = e[k]
                if e['location'] is not None:
                    for k in ['lat', 'lon']:
                        entry[k] = e['location'][k]
                else:
                    for k in ['lat', 'lon']:
                        entry[k] = None
                yield entry

            if page['more'] == 1:
                index += 1
            else:
                logging.info('done - no more pages')
                break

    def journal_entries(self, username, newer=None):
        for entry in self._get_entries(
                'entries/journal',
                params={'username': username},
                newer=newer):
            yield entry

    def query(self, query, newer=None):
        for entry in self._get_entries(
                'entries/search',
                params={'query': query,
                        'sort': 'date'},
                newer=newer):
            yield entry


if __name__ == '__main__':
    from .config import readConfig

    cfg = readConfig()

    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    import pprint
    blip = BLIPApi(cfg['accesstoken'], cfg['baseurl'])

    for entry in blip.journal_entries(cfg['username']):
        pprint.pprint(entry)
