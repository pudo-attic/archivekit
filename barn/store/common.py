
MANIFEST = 'manifest.json'


class Store(object):
    """ A host object to represent a specific type of storage,
    in which objects are managed. """

    def __init__(self):
        pass

    def get_object(self, collection, package_id, path):
        raise NotImplemented()

    def list_packages(self, collection):
        raise NotImplemented()

    def list_resources(self, collection, package_id):
        raise NotImplemented()


class StoreObject(object):
    """ An abstraction over the on-disk representation of a
    stored object. This can be subclassed for specific storage
    mechanisms. """

    def exists(self):
        raise NotImplemented()

    def save_fileobj(self, fileobj):
        raise NotImplemented()

    def save_file(self, file, destructive=False):
        """ Update the contents of this resource from the given file
        name. If ``destructive`` is set, the original file may be
        lost (i.e. it will be moved, not copied). """
        raise NotImplemented()

    def save_data(self, data):
        raise NotImplemented()

    def load_fileobj(self):
        raise NotImplemented()

    def public_url(self):
        return None

    def local_path(self):
        return None
