#!/usr/local/bin/python3

import json
import requests

_config = None

def load_config():
    fp = open('config.json', 'r')
    return json.load(fp)

def list_folders(user, usertoken=None):
    url = _config.baseurl + _config.paths['users'] + "/" + user + "/" + _config.paths['folders']
    if usertoken:
        url += "?token=" + usertoken
    
    return requests.get(url)

class Config:
    def __init__(self, filename):
        _conf = self._loadconfig(filename)
        self.baseurl = _conf['baseurl']
        self.user = _conf['user']
        self.paths = _conf['paths']
    
    def _loadconfig(self, filename):
        fp = open(filename, 'r')
        return json.load(fp)
        
if __name__ == "__main__":
    _config = Config('config.json')
    resp = list_folders(_config.user)
    json_out = json.loads(resp.text)
    print(json.dumps(json_out, indent=4))
