import os
from uuid import uuid4

from barn.manifest import Manifest
from barn.store.common import MANIFEST


class Package(object):
    """ An package is a resource in the remote bucket. It consists of a
    source file, a manifest metadata file and one or many processed
    version. """

    def __init__(self, store, id=None):
        self.store = store
        self.id = id or uuid4().hex

    def has(self, cls, name):
        return cls(self, name).exists()

    def all(self, cls, *extra):
        prefix = os.path.join(cls.GROUP, *extra)
        for path in self.store.list_resources(self.id):
            if path.startswith(prefix):
                yield cls.from_path(self, path)

    def exists(self):
        return self.store.get_object(self.id, MANIFEST).exists()

    @property
    def manifest(self):
        if not hasattr(self, '_manifest'):
            obj = self.store.get_object(self.id, MANIFEST)
            self._manifest = Manifest(obj)
        return self._manifest

    def save(self):
        self.manifest.save()

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return '<Package(%r)>' % self.id
