from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

class Artist:
    """ An artist who contributed to a release. """
    def __init__(self, client, dict_):
        self.client = client
        self.id = dict_['id']
        self.name = dict_['name']
        self.resource_url = dict_['resource_url']
        self.releases_url = dict_['releases_url']

    def __str__(self):
        return self.name
    
    @property
    def releases(self):
        return [Release(r) for r in self.client._request(self.releases_url)]

@dataclass
class SimpleArtist:
    """ A simplified artist object that is part of a release object. """
    id: int
    name: str
    resource_url: str
    anv: str = field(default = '')
    join: str = field(default = '')
    role: str = field(default = '')
    tracks: str = field(default = '')

@dataclass
class Folder:
    """ A folder in a user's Discogs collection """
    id: int
    name: str
    count: int
    resource_url: str
    client: Any = field(repr=False)

    def __post_init__(self):
        self.releases_url = "{}/releases".format(self.resource_url)

    @property
    def releases(self):
        resp = self.client._get(self.releases_url)
        return [CollectionRelease(client=self.client, folder=self, **r) for r in resp['releases']]

    def __len__(self):
        return self.count

@dataclass
class Format:
    """ A media format. """
    name: str
    qty: str
    text: str = field(default='')
    descriptions: list = field(default_factory=list)

@dataclass
class Label:
    name: str
    catno: str
    entity_type: str
    entity_type_name: str
    id: int
    resource_url: str

@dataclass
class Note:
    field_id: int
    value: str

@dataclass
class BasicInformation:
    id: int
    master_id: int
    master_url: str
    cover_image: str
    artists: list
    formats: list
    labels: list
    thumb: str
    title: str
    year: str
    resource_url: str
    genres: list
    styles: list
    
    def __post_init__(self):
        self.artists = [SimpleArtist(**a) for a in self.artists]
        self.formats = [Format(**f) for f in self.formats]
        self.labels = [Label(**l) for l in self.labels]

@dataclass
class CollectionRelease:
    id: int
    basic_information: Any
    date_added: str
    folder: Folder
    folder_id: str
    instance_id: str
    rating: int
    client: Any = field(repr=False)
    notes: list = field(default_factory=list)
    date_format_str = "%Y-%m-%dT%H:%M:%S%z"

    def __post_init__(self):
        self.basic_information = BasicInformation(**self.basic_information)
        self.notes = [Note(**n) for n in self.notes]
        self.date_added = datetime.strptime(self.date_added, self.date_format_str)
        self.instance_url = "{}/releases/{}/instances/{}".format(self.folder.resource_url, self.id, self.instance_id)

    def set_rating(self, rating):
        params = {"rating":rating}

class Release:
    def __init__(self, client, dict_):
        self.client = client
        self.data = dict_
