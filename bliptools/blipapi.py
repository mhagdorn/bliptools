__all__ = ['BLIPApi']

import logging
import requests
import datetime

class BlipError(Exception):
    """blip API error"""
    pass

class BLIPApi:
    def __init__(self,token,baseurl):
        self._accesstoken = token
        self._baseurl = baseurl
        self._headers = {'Authorization':'Bearer paSmmahmNKBjh3lbTSWbeLOmih6HIB'}
        
    @property
    def accesstoken(self):
        return self._accesstoken
    @property
    def baseurl(self):
        return self._baseurl
    @property
    def headers(self):
        return self._headers
    def url(self,api):
        return '{}/{}'.format(self.baseurl,api)
    
    def journal_entries(self,username,newer=None):
        index = 0
        num_entries = 2
        while index<2:
            logging.info('requesting page {} with {} entries'.format(index,num_entries))
            r = requests.get(self.url('entries/journal'),
                             params={'username':username,
                                     'page_size':num_entries,
                                     'page_index':index},
                             headers=self.headers)
            data = r.json()
            if data['error'] is not None:
                raise BlipError(data['error']['message'])
            data = data['data']
            page = data['page']
            entries = data['entries']
            
            for e in entries:
                entry = {}
                entry['date'] = datetime.datetime.strptime(e['date'],'%Y-%m-%d').date()
                if newer is not None:
                    if entry['date'] <= newer:
                        logging.info('done - entry is too old')
                        break
                for k in ['entry_id','title','username','thumbnail_url','image_url']:
                    entry[k] = e[k]
                for k in ['lat','lon']:
                    entry[k] = e['location'][k]
                yield entry
            
            if page['more'] == 1:
                index += 1
            else:
                logging.info('done - no more pages')
                break



if __name__ == '__main__':
    from .config import readConfig

    cfg = readConfig()
    
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    import pprint
    blip = BLIPApi(cfg['accesstoken'],cfg['baseurl'])

    for entry in blip.journal_entries(cfg['username']):
        pprint.pprint(entry)
