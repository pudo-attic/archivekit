import os

from barn.store.common import Store, StoreObject, MANIFEST


class FileStore(Store):
    
    def __init__(self, path=None, **kwargs):
        self.path = path

    def get_object(self, package_id, path):
        return FileStoreObject(self, package_id, path)

    def list_packages(self):
        for key in self.bucket.get_all_keys(prefix=self.prefix):
            _, id, part = key.name.split('/')
            if part == MANIFEST:
                yield id

    def list_resources(self, package_id):
        prefix = os.path.join(self.prefix, package_id)
        skip = os.path.join(prefix, MANIFEST)
        offset = len(skip) - len(MANIFEST)
        for key in self.bucket.get_all_keys(prefix=prefix):
            if key.name == skip:
                continue
            yield key.name[offset:]


class FileStoreObject(StoreObject):

    def __init__(self, store, package_id, path):
        self.store = store
        self.package_id = package_id
        self.path = path
        self._key = None
        self._key_name = os.path.join(package_id, path)
        if store.prefix:
            self._key_name = os.path.join(store.prefix, self._key_name)

    @property
    def key(self):
        if self._key is None:
            self._key = self.store.bucket.get_key(self._key_name)
            if self._key is None:
                self._key = self.store.bucket.new_key(self._key_name)
        return self._key

    def exists(self):
        if self._key is None:
            self._key = self.store.bucket.get_key(self._key_name)
        return self._key is not None

    def save_fileobj(self, fileobj):
        self.key.send_file(fileobj)

    def save_data(self, data):
        self.key.set_contents_from_string(data)

    def load_fileobj(self):
        return self.key

    def public_url(self):
        if not self.exists:
            raise ValueError('Object does not exist!')
        # Welcome to the world of open data:
        self.key.make_public()
        return self.key.generate_url(expires_in=0, query_auth=False)


