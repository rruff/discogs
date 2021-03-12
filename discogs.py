#!/usr/local/bin/python3

import json
import requests
import urllib.error
import sys

from models import Artist, Folder, Release

class Client:
    _baseurl = "https://api.discogs.com/"
    _useragent = "FooBarApp/3.0"

    _folders_url_template = "/users/{user}/collection/folders"
    _releases_by_folder_url_template = "/users/{user}/collection/folders/{folder_id}/releases"

    def __init__(self, token=None, useragent=None, debug=False):
        self.token = token
        self._isdebug = debug
        self.useragent = useragent if useragent else self._useragent

    def artist(self, id):
        return Artist(self, self._request(self._baseurl + "/artists/" + str(id)))
    
    def list_folders(self, user):
        """ Lists the folders in `user`'s collection. """
        url = self._build_url(self._folders_url_template.format(user=user))
        body = self._get(url)
        return [Folder(client=self, **f) for f in body['folders']]

    def _request(self, method, url, params={}, data=None):
        if self.token:
            params['token'] = self.token
        params['User-Agent'] = self.useragent
        
        self._debug(f'Requesting {url}')

        request = Request(method, url, params, data)
        content, status_code = request.send()
        
        if status_code == 204:
            return status_code
        
        body = json.loads(content)

        if 200 <= status_code < 300:
            return body
        else:
            raise urllib.error.HTTPError(status_code, body['message'])
    
    def _get(self, url, params={}, data=None):
        return self._request('GET', url, params, data)
    
    def _post(self, url, params={}, data=None):
        return self._request('POST', url, params, data)
    
    def _build_url(self, path):
        if not path.startswith("/"):
            path = "/" + path
        return self._baseurl + path
    
    def _debug(self, message):
        if self._isdebug:
            print(message)

    def __str__(self):
        return "Discogs API Client"

class Request:
    def __init__(self, method, url, params={}, data=None, isjson=True):
        self.method = method
        self.url = url
        self.params = params
        self.data = data
        self.isjson = isjson
        self.headers = {'Accept-Encoding': 'gzip'}

    def send(self):
        if self.data and self.isjson:
            self.headers['Content-Type'] = 'application/json'
            self.data = json.dumps(self.data)
        
        response = requests.request(self.method, self.url, params=self.params, data=self.data, headers=self.headers)
        return response.content, response.status_code
    
def main():
    if len(sys.argv) == 3:
        username = sys.argv[1]
        token = sys.argv[2]
        client = Client(token, True)
        folders = client.list_folders(username)
        releases_by_folder = {}
        for folder in folders:
            releases_by_folder.update({folder.name: folder.releases})
        
        print("Retrieved releases:")
        print(releases_by_folder)
    else:
        print("Usage: {0} {1} {2}".format(sys.argv[0], '<username>', '<token>'))

if __name__ == "__main__":
    main()
