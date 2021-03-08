from dataclasses import dataclass, field

class SimpleObject:
    """ Generic object for quickly desereializing JSON """
    def __init__(self, dict_):
        self.__dict__.update(dict_)

    def __str__(self):
        return str(vars(self))
    
    def __repr__(self):
        return str(vars(self))

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
        return [CollectionRelease(self.client, r) for r in self.client._request(self.releases_url)['releases']]

    def __len__(self):
        return self.count

@dataclass
class Format:
    """ A media format. """
    name: str
    qty: str
    text: str = field(default='')
    descriptions: list = field(default_factory=list)

class ObjectField:
    def __init__(self, dict_):
        self.__dict__.update(dict_)

    def __str__(self):
        return ', '.join("{0} = {1}".format(str(f), str(self.__dict__.get(f, "Unknown"))) for f in self.__dict__)

class ListField:
    def __init__(self, field_name, list_):
        self.field_name = field_name
        self.data = [ObjectField(i) for i in list_]
    
    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        if 0 > index < len(self.data):
            raise IndexError
        return self.data[index]

    def __str__(self):
        return "{} [{}]".format(self.field_name, ', '.join(str(artist) for artist in self.data))

class CollectionRelease:
    def __init__(self, client, dict_):
        basicinfo = dict_['basic_information']
        self.artists = ListField('Artists', basicinfo['artists'])
        self.formats = [Format(**f) for f in basicinfo['formats']]
        self.title = basicinfo['title']
        self.year = basicinfo['year']
        self.resource_url = basicinfo['resource_url']
        self.genres = basicinfo['genres']
        self.styles = basicinfo['styles']
        self.id = dict_['id']
        self.client = client
    
    def __str__(self):
        return "Release: {0} {1} -- {2}".format(self.title, self.year, ', '.join(self.artists))
    
    def __repr__(self):
        return "Release: " + str(vars(self))

class Release:
    def __init__(self, client, dict_):
        self.client = client
        self.data = dict_
    

