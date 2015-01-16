import os

from boto.s3.connection import S3Connection, S3ResponseError
from boto.s3.connection import Location

from barn.store.common import Store, StoreObject, MANIFEST


class S3Store(Store):
    
    def __init_(self, aws_key_id=None, aws_secret=None, bucket_name=None,
                prefix=None, location=Location.EU, **kwargs):
        self.aws_key_id = aws_key_id
        self.aws_secret = aws_secret
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.location = location
        self._bucket = None

    @property
    def bucket(self):
        if self._bucket is None:
            self.conn = S3Connection(self.aws_key_id, self.aws_secret)
            try:
                self._bucket = self.conn.get_bucket(self.bucket_name)
            except S3ResponseError, se:
                if se.status != 404:
                    raise
                self._bucket = self.conn.create_bucket(self.bucket_name,
                                                       location=self.location)
        return self._bucket

    def get_object(self, package_id, path):
        raise S3StoreObject(self, package_id, path)

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


class S3StoreObject(StoreObject):

    def __init__(self, store, package_id, path):
        self.store = store
        self.package_id = package_id
        self.path = path
        self._key = None
        self._key_name = os.path.join(store.prefix, package_id, path)

    @property
    def key(self):
        if self._key is None:
            self._key = self.bucket.get_key(self._key_name)
            if self._key is None:
                self._key = self.bucket.new_key(self._key_name)
        return self._key

    def exists(self):
        if self._key is None:
            self._key = self.bucket.get_key(self._key_name)
        return self._key is not None

    def save_fileobj(self, fileobj):
        self.key.send_file(fileobj)

    def save_data(self, data):
        self.key.set_contents_from_string(data)

    def load_fileobj(self):
        return self.key.open_read()

    def public_url(self):
        if not self.exists:
            raise ValueError('Object does not exist!')
        # Welcome to the world of open data:
        self.key.make_public()
        return self.key.generate_url(expires_in=0, query_auth=False)


