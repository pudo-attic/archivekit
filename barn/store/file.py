import os
import shutil
from lockfile import LockFile

from barn.store.common import Store, StoreObject, MANIFEST
from barn.util import safe_id, fullpath


class FileStore(Store):
    
    def __init__(self, path=None, **kwargs):
        self.path = fullpath(path)
        if os.path.exists(path) and not os.path.isdir(path):
            raise ValueError('Not a directory: %s' % path)

    def get_object(self, collection, package_id, path):
        return FileStoreObject(self, collection, package_id, path)

    def list_collections(self):
        if self.path is None:
            return
        for collection in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, collection)):
                yield collection

    def list_packages(self, collection):
        if self.path is None:
            return
        coll_path = os.path.join(self.path, collection)
        if not os.path.exists(coll_path):
            return
        for (dirpath, dirnames, filenames) in os.walk(coll_path):
            if MANIFEST not in filenames:
                continue
            _, id = os.path.split(dirpath)
            if self._make_path(collection, id) == dirpath:
                yield id

    def _make_path(self, collection, package_id):
        id = safe_id(package_id)
        path = os.path.join(self.path, collection, *id[:5])
        return os.path.join(path, id)

    def list_resources(self, collection, package_id):
        prefix = self._make_path(collection, package_id)
        if not os.path.exists(prefix):
            return
        skip = os.path.join(prefix, MANIFEST)
        for (dirpath, dirnames, filenames) in os.walk(self.path):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                if path == skip:
                    continue
                yield os.path.relpath(path, start=prefix)


class FileStoreObject(StoreObject):

    def __init__(self, store, collection, package_id, path):
        self.store = store
        self.package_id = package_id
        self.path = path
        pkg_path = self.store._make_path(collection, package_id)
        self._abs_path = os.path.join(pkg_path, path)
        self._abs_dir = os.path.dirname(self._abs_path)
        self._lock = LockFile(self._abs_path)

    def exists(self):
        return os.path.exists(self._abs_path)

    def _prepare(self):
        try:
            os.makedirs(self._abs_dir)
        except:
            pass

    def save_fileobj(self, fileobj):
        self._prepare()
        with self._lock:
            with open(self._abs_path, 'wb') as fh:
                shutil.copyfileobj(fileobj, fh)

    def save_file(self, file_name, destructive=False):
        self._prepare()
        with self._lock:
            if destructive:
                shutil.move(file_name, self._abs_path)
            else:
                shutil.copy(file_name, self._abs_path)

    def save_data(self, data):
        self._prepare()
        with self._lock:
            with open(self._abs_path, 'wb') as fh:
                fh.write(data)

    def load_fileobj(self):
        if not self.exists():
            raise ValueError('Object does not exist: %s' % self._abs_path)
        with self._lock:
            return open(self._abs_path, 'rb')

    def load_data(self):
        if not self.exists():
            raise ValueError('Object does not exist: %s' % self._abs_path)
        with self._lock:
            with open(self._abs_path, 'rb') as fh:
                return fh.read()

    def local_path(self):
        return self._abs_path

