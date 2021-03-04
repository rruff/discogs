class Folder:
    """ A folder in a user's Discogs collection """
    def __init__(self, dict_):
        self.id = dict_['id']
        self.name = dict_['name']
        self.count = dict_['count']
        self.resource_url = dict_['resource_url']
    
    def __str__(self):
        return str(vars(self))

class SimpleObject:
    """ Generic object for quickly desereializing JSON """
    def __init__(self, attrs):
        self.__dict__.update(attrs)

    def __str__(self):
        return str(vars(self))
