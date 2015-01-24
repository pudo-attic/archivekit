from barn.collection import Collection


class Archive(object):
    """ An archive is composed of collections. """

    def __init__(self, store):
        self.store = store

    def get(self, name):
        """ Get a collection of packages. """
        return Collection(name, self.store)

    def __iter__(self):
        for name in self.store.list_collections():
            yield Collection(name, self.store)

    def __repr__(self):
        return '<Archive(%r)>' % (self.store)
