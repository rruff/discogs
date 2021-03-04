#!/usr/local/bin/python3

import json
import requests
import sys

from models import Folder, SimpleObject

class Client:
    _baseurl = "https://api.discogs.com/"
    _useragent = "FooBarApp/3.0"

    def __init__(self, token=None):
        self.token = token

    def list_folders(self, user):
        url = "{}/users/{}/collection/folders".format(self._baseurl, user)
        
        body = self._request(url)

        folders = []
        for folder in body['folders']:
            folders.append(Folder(folder))
        return folders
    
    def list_releases_by_folder(self, user, folder):
        url = "{}/users/{}/collection/folders/{}/releases".format(self._baseurl, user, folder.id)
        
        body = self._request(url)

        releases = []
        for release in body['releases']:
            releases.append(SimpleObject(release))
        return releases

    def _request(self, url, params=None):
        if self.token:
            if not params: params = {}
            params['token'] = self.token
        
        response = requests.get(url, params)
        if response.status_code >= 200 and response.status_code < 300:
            return json.loads(response.text)
        else:
            response.raise_for_status()


def main():
    if len(sys.argv) == 3:
        username = sys.argv[1]
        token = sys.argv[2]
        client = Client(token)
        folders = client.list_folders(username)
        for folder in folders:
            print(folder)
    else:
        print("Usage: {0} {1} {2}".format(sys.argv[0], '<username>', '<token>'))

if __name__ == "__main__":
    main()
