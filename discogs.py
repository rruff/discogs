#!/usr/local/bin/python3

import json
import requests
import sys

from models import Artist, Folder, Release

class Client:
    _baseurl = "https://api.discogs.com/"
    _useragent = "FooBarApp/3.0"

    _folders_url_template = "/users/{user}/collection/folders"
    _releases_by_folder_url_template = "/users/{user}/collection/folders/{folder_id}/releases"

    def __init__(self, token=None, debug=False):
        self.token = token
        self._isdebug = debug

    def artist(self, id):
        return Artist(self, self._request(self._baseurl + "/artists/" + str(id)))
    
    def list_folders(self, user):
        """ Lists the folders in `user`'s collection. """
        url = self._build_url(self._folders_url_template.format(user=user))
        body = self._request(url)
        return [Folder(self, f) for f in body['folders']]

    def _request(self, url, params=None):
        if self.token:
            if not params: params = {}
            params['token'] = self.token
        
        self._debug(f'Requesting {url}')
        response = requests.get(url, params)
        
        self._debug(f'Response: {response.status_code} {response.text}')
        if 200 <= response.status_code < 300:
            return json.loads(response.text)
        else:
            response.raise_for_status()
    
    def _build_url(self, path):
        return self._baseurl + (path if path.startswith("/") else "/" + path)
    
    def _debug(self, message):
        if self._isdebug:
            print(message)

    def __str__(self):
        return "Discogs API Client"

def main():
    if len(sys.argv) == 3:
        username = sys.argv[1]
        token = sys.argv[2]
        client = Client(token, True)
        folders = client.list_folders(username)
        releases_by_folder = {}
        for folder in folders:
            releases_by_folder.update({folder.name: folder.releases})
    else:
        print("Usage: {0} {1} {2}".format(sys.argv[0], '<username>', '<token>'))

if __name__ == "__main__":
    main()
