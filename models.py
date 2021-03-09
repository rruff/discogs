from dataclasses import dataclass, field
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
    client: object

    def __post_init__(self):
        self.releases_url = "{}/releases".format(self.resource_url)

    @property
    def releases(self):
        return [CollectionRelease(client=self.client, **r['basic_information']) for r in self.client._request(self.releases_url)['releases']]

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
class CollectionRelease:
    id: int
    master_id: int
    master_url: str
    client: Any
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

class Release:
    def __init__(self, client, dict_):
        self.client = client
        self.data = dict_
