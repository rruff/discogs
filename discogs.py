#!/usr/local/bin/python3

import json
import requests

token = ""
base_url = "https://api.discogs.com/"
user = "robruff"
user_agent = "FooBarApp/3.0"

def list_folders(user):
    url = base_url + "users/" + user + "/collection/folders?token=" + token
    return requests.get(url)

if __name__ == "__main__":
    resp = list_folders(user)
    json_out = json.loads(resp.text)
    print(json.dumps(json_out, indent=4))
