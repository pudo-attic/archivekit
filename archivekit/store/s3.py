import os
from urllib2 import urlopen

from boto.s3.connection import S3Connection, S3ResponseError
from boto.s3.connection import Location

from archivekit.store.common import Store, StoreObject, MANIFEST

DELIM = os.path.join(' ', ' ').strip()
ALL_USERS = 'http://acs.amazonaws.com/groups/global/AllUsers'


class S3Store(Store):
    
    def __init__(self, aws_key_id=None, aws_secret=None, bucket_name=None,
                 prefix=None, location=Location.EU, **kwargs):
        if aws_key_id is None:
            aws_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
            aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.aws_key_id = aws_key_id
        self.aws_secret = aws_secret
        if bucket_name is None:
            bucket_name = os.environ.get('AWS_BUCKET_NAME')
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

    def get_object(self, collection, package_id, path):
        return S3StoreObject(self, collection, package_id, path)

    def _get_prefix(self, collection):
        prefix = collection
        if self.prefix:
            prefix = os.path.join(self.prefix, prefix)
        return os.path.join(prefix, '')

    def list_collections(self):
        prefix = os.path.join(self.prefix, '') if self.prefix else None
        for prefix in self.bucket.list(prefix=prefix, delimiter=DELIM):
            yield prefix.name.rsplit(DELIM, 2)[-2]

    def list_packages(self, collection):
        prefix = self._get_prefix(collection)
        for sub_prefix in self.bucket.list(prefix=prefix, delimiter=DELIM):
            yield sub_prefix.name.rsplit(DELIM, 2)[-2]

    def list_resources(self, collection, package_id):
        prefix = os.path.join(self._get_prefix(collection), package_id)
        skip = os.path.join(prefix, MANIFEST)
        offset = len(skip) - len(MANIFEST)
        for key in self.bucket.get_all_keys(prefix=prefix):
            if key.name == skip:
                continue
            yield key.name[offset:]

    def __repr__(self):
        return '<S3Store(%r, %r)>' % (self.bucket_name, self.prefix)

    def __unicode__(self):
        return os.path.join(self.bucket_name, self.prefix)


class S3StoreObject(StoreObject):

    def __init__(self, store, collection, package_id, path):
        self.store = store
        self.package_id = package_id
        self.path = path
        self._key = None
        self._key_name = os.path.join(collection, package_id, path)
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
        self.key.set_contents_from_file(fileobj)

    def save_file(self, file_name, destructive=False):
        with open(file_name, 'rb') as fh:
            self.save_fileobj(fh)

    def save_data(self, data):
        self.key.set_contents_from_string(data)

    def load_fileobj(self):
        return urlopen(self.public_url())

    def load_data(self):
        return self.key.get_contents_as_string()

    def _is_public(self):
        try:
            for grant in self.key.get_acl().acl.grants:
                if grant.permission == 'READ':
                    if grant.uri == ALL_USERS:
                        return True
        except:
            pass
        return False

    def public_url(self):
        if not self.exists():
            return
        # Welcome to the world of open data:
        if not self._is_public():
            self.key.make_public()
        return self.key.generate_url(expires_in=0,
                                     force_http=True,
                                     query_auth=False)

    def __repr__(self):
        return '<S3StoreObject(%r, %r, %r)>' % (self.store, self.package_id,
                                                self.path)

    def __unicode__(self):
        return self.public_url()
