from barn.package import Package


class Collection(object):
    """ The list of all packages with an existing manifest which exist in
    the given storage """

    def __init__(self, store):
        self.store = store

    def create(self, id=None, manifest=None):
        """ Create a package and save a manifest. If ``manifest`` is
        given, the values are saved to the manifest. """
        package = Package(self.store, id=id)
        if manifest is not None:
            package.manifest.update(manifest)
        package.save()
        return package

    def get(self, id):
        """ Get a ``Package`` identified by the ``id``. """
        return Package(self.store, id=id)

    def __iter__(self):
        for package_id in self.store.list_packages():
            yield Package(self.store, id=package_id)
