from barn.package import Package
from barn.ingest import Ingestor


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

    def ingest(self, something, meta=None):
        """ Import a given object into the collection. The object can be
        either a URL, a file or folder name, an open file handle or a
        HTTP returned object from urllib, urllib2 or requests.

        Before importing it, a SHA1 hash will be generated and used as the
        package ID. If a package with the given name already exists, it
        will be overwritten. If you do not desire SHA1 de-duplication,
        create a package directly and ingest from there. """
        for ingestor in Ingestor.analyze(something):
            try:
                package = self.get(ingestor.hash())
                package.ingest(ingestor, meta=meta)
            finally:
                ingestor.dispose()

    def __iter__(self):
        for package_id in self.store.list_packages():
            yield Package(self.store, id=package_id)
