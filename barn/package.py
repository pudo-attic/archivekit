import os
from uuid import uuid4
from itertools import count

from barn.manifest import Manifest
from barn.ext import get_resource_types
from barn.ingest import Ingestor
from barn.types.source import Source
from barn.store.common import MANIFEST


class Package(object):
    """ An package is a resource in the remote bucket. It consists of a
    source file, a manifest metadata file and one or many processed
    version. """

    def __init__(self, store, id=None):
        self.store = store
        self.id = id or uuid4().hex

    def has(self, cls, name):
        """ Check if a resource of a given type and name exists. """
        return cls(self, name).exists()

    def all(self, cls, *extra):
        """ Iterate over all resources of a given type. """
        prefix = os.path.join(cls.GROUP, *extra)
        for path in self.store.list_resources(self.id):
            if path.startswith(prefix):
                yield cls.from_path(self, path)

    def exists(self):
        """ Check if the package identified by the given ID exists. """
        return self.store.get_object(self.id, MANIFEST).exists()

    @property
    def manifest(self):
        if not hasattr(self, '_manifest'):
            obj = self.store.get_object(self.id, MANIFEST)
            self._manifest = Manifest(obj)
        return self._manifest

    def get_resource(self, path):
        """ Get a typed resource by it's path. """
        for resource_type in get_resource_types().values():
            prefix = os.path.join(resource_type.GROUP, '')
            if path.startswith(prefix):
                return resource_type.from_path(self, path)

    def save(self):
        """ Save the package metadata (manifest). """
        self.manifest.save()

    @property
    def source(self):
        """ Return the sole source of this package if present, or
        None if there is no source, or if there are multiple sources. """
        sources = list(self.all(Source))
        # TODO: should this raise for multiple sources instead?
        if len(sources) == 1:
            return sources[0]

    def ingest(self, something, meta=None, overwrite=True):
        """ Import a given object into the package as a source. The
        object can be either a URL, a file or folder name, an open
        file handle or a HTTP returned object from urllib, urllib2 or
        requests. If ``overwrite`` is ``False``, the source file
        will be renamed until the name is not taken. """
        ingestors = list(Ingestor.analyze(something))
        
        if len(ingestors) != 1:
            raise ValueError("Can't ingest: %r" % something)
        ingestor = ingestors[0]
        
        try:
            meta = ingestor.generate_meta(meta)
            name = None
            for i in count(1):
                suffix = '-%s' % i if i > 1 else ''
                name = '%s%s.%s' % (meta['slug'], suffix, meta['extension'])
                if overwrite or not self.has(Source, name):
                    break

            source = Source(self, name)
            source.meta.update(meta)
            ingestor.store(source)
            self.save()
            return source
        finally:
            ingestor.dispose()

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return '<Package(%r)>' % self.id
