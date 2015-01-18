import os

from barn.manifest import ResourceMetaData


class Resource(object):
    """ Any file within the prefix of the given package, except the
    manifest. """

    GROUP = None

    def __init__(self, package, name):
        self.package = package
        self.name = name
        self.path = os.path.join(self.GROUP, name)
        self._obj = package.store.get_object(package.id, self.path)
        self.meta = ResourceMetaData(self)

    @classmethod
    def from_path(cls, package, path):
        """ Instantiate a resource class with a path which is relative
        to the root of the package. """
        if path.startswith(cls.GROUP):
            _, name = path.split(os.path.join(cls.GROUP, ''))
            return cls(package, name)

    def exists(self):
        return self._obj.exists()

    def save(self):
        """ Save the metadata. """
        return self.package.save()

    def save_data(self, data):
        """ Save a string to the given resource. Overwrites any existing
        data in the resource. """
        return self._obj.save_data(data)

    def save_file(self, file_name, destructive=False):
        """ Update the contents of this resource from the given file
        name. If ``destructive`` is set, the original file may be
        lost (i.e. it will be moved, not copied). """
        return self._obj.save_file(file_name, destructive=destructive)

    def save_fileobj(self, fh):
        """ Save the contents of the given file handle to the given
        resource. Overwrites any existing data in the resource. """
        return self._obj.save_fileobj(fh)

    def fh(self):
        """ Read the contents of this resource as a file handle. """
        return self._obj.load_fileobj()

    @property
    def url(self):
        """ Return the public URL of the resource, if it exists. If
        no public url is available, returns ``None``. """
        if not hasattr(self, '_url'):
            try:
                self._url = self._obj.public_url()
            except ValueError:
                self._url = None
        return self._url

    def __repr__(self):
        return '<Resource(%r)>' % self.path

