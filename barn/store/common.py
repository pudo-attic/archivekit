
MANIFEST = 'manifest.json'


class Store(object):
    """ A host object to represent a specific type of storage,
    in which objects are managed. """

    def __init__(self, collection):
        self.collection = collection

    def get_object(self, package_id, path):
        raise NotImplemented()

    def list_packages(self):
        raise NotImplemented()

    def list_resources(self, package_id):
        raise NotImplemented()


class StoreObject(object):
    """ An abstraction over the on-disk representation of a
    stored object. This can be subclassed for specific storage
    mechanisms. """

    def exists(self):
        raise NotImplemented()

    def save_fileobj(self, fileobj):
        raise NotImplemented()

    def save_data(self, data):
        raise NotImplemented()

    def load_fileobj(self):
        raise NotImplemented()

    def public_url(self):
        raise NotImplemented()
