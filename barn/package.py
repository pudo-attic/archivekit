import os
from uuid import uuid4

from barn.artifact import Artifact
from barn.source import Source
from barn.logfile import LogFile
from barn.manifest import Manifest


class Package(object):
    """ An package is a resource in the remote bucket. It consists of a
    source file, a manifest metadata file and one or many processed
    version. """

    PREFIX = 'packages'
    MANIFEST = 'manifest.json'

    def __init__(self, bucket, id=None):
        self.bucket = bucket
        self.id = id or uuid4().hex
        self._keys = {}

    def get_key(self, name):
        if not self._keys.get(name):
            key_name = os.path.join(self.PREFIX, self.id, name)
            key = self.bucket.get_key(key_name)
            if key is None:
                key = self.bucket.new_key(key_name)
            self._keys[name] = key
        return self._keys[name]

    def has(self, cls, name):
        name = os.path.join(self.PREFIX, self.id, cls.GROUP, name)
        self._keys[name] = self.bucket.get_key(name)
        return bool(self._keys[name])

    def _iter_resources(self, cls, *extra):
        prefix = os.path.join(self.PREFIX, self.id, cls.GROUP, *extra)
        for key in self.bucket.get_all_keys(prefix=prefix):
            cut = os.path.join(self.PREFIX, self.id, cls.GROUP)
            name = key.name.replace(cut, '').strip('/')
            yield cls(self, name)
            
    @property
    def artifacts(self):
        return self._iter_resources(Artifact)

    @property
    def sources(self):
        return self._iter_resources(Source)

    def logfiles(self, prefix):
        return self._iter_resources(LogFile, prefix)

    @property
    def manifest(self):
        if not hasattr(self, '_manifest'):
            key = self.get_key(self.MANIFEST)
            self._manifest = Manifest(key)
        return self._manifest

    def save(self):
        self.manifest.save()

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return '<Package(%r)>' % self.id
