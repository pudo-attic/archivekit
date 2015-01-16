import os

from loadkit.core.manifest import ResourceMetaData


class Resource(object):
    """ Any file within the prefix of the given package, including
    source data and artifacts. """

    GROUP = None

    def __init__(self, package, name):
        self.package = package
        self.name = name
        self.key = package.get_key(self.path)
        self.meta = ResourceMetaData(self)

    @property
    def path(self):
        return os.path.join(self.GROUP, self.name)

    @classmethod
    def from_path(cls, package, path):
        if path.startswith(cls.GROUP):
            _, name = path.split(cls.GROUP)
            return cls(package, name)

    @property
    def url(self):
        # Welcome to the world of open data:
        self.key.make_public()
        return self.key.generate_url(expires_in=0, query_auth=False)

    def __repr__(self):
        return '<Resource(%r)>' % self.path

