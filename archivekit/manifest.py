import json
import collections
from datetime import datetime


from archivekit.util import json_default, json_hook


class Manifest(dict):
    """ A manifest has metadata on a package. """

    def __init__(self, obj):
        self.object = obj
        self.load()

    def load(self):
        if self.object.exists():
            data = self.object.load_data()
            self.update(json.loads(data, object_hook=json_hook))
        else:
            self['created_at'] = datetime.utcnow()
            self.update({'resources': {}})

    def save(self):
        self['updated_at'] = datetime.utcnow()
        content = json.dumps(self, default=json_default, indent=2)
        self.object.save_data(content)

    def __repr__(self):
        return '<Manifest(%r)>' % self.key


class ResourceMetaData(collections.MutableMapping):
    """ Metadata for a resource is derived from the main manifest. """

    def __init__(self, resource):
        self.resource = resource
        self.manifest = resource.package.manifest
        if not isinstance(self.manifest.get('resources'), dict):
            self.manifest['resources'] = {}
        existing = self.manifest['resources'].get(self.resource.path)
        if not isinstance(existing, dict):
            self.manifest['resources'][self.resource.path] = {
                'created_at': datetime.utcnow()
            }

    def touch(self):
        self.manifest['resources'][self.resource.path]['updated_at'] = \
            datetime.utcnow()

    def __getitem__(self, key):
        return self.manifest['resources'][self.resource.path][key]

    def __setitem__(self, key, value):
        self.manifest['resources'][self.resource.path][key] = value
        self.touch()

    def __delitem__(self, key):
        del self.manifest['resources'][self.resource.path][key]
        self.touch()

    def __iter__(self):
        return iter(self.manifest['resources'][self.resource.path])

    def __len__(self):
        return len(self.manifest['resources'][self.resource.path])

    def __keytransform__(self, key):
        return key

    def save(self):
        self.touch()
        self.resource.package.save()

    def __repr__(self):
        return '<ResourceMetaData(%r)>' % self.resource.path
