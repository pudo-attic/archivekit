from os import path, walk, unlink
from os import name as osname
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from httplib import HTTPResponse
from StringIO import StringIO
from urlparse import urlparse
import mimetypes

import requests

from archivekit.util import clean_headers, checksum, fullpath
from archivekit.util import make_secure_filename, slugify


def directory_files(fpath):
    for (dir, _, files) in walk(fpath):
        for file_name in files:
            yield path.join(dir, file_name)


class Ingestor(object):
    """ An ingestor is an intermedia object used when importing data.
    Since the source types (URLs, file names or file handles) are very
    diverse, this may require data to be cached locally, e.g. to
    generate a SHA1 hash signature. """

    def __init__(self, file_name=None, file_obj=None, meta=None):
        self._file_name = file_name
        self._file_obj = file_obj
        self._file_cache = None
        self._hash = None
        self.is_local = file_name is not None
        self.meta = meta or {}

    def local(self):
        if self.is_local:
            return self._file_name
        if self._file_cache is None:
            tempfile = NamedTemporaryFile(delete=False)
            copyfileobj(self._file_obj, tempfile)
            self._file_cache = tempfile.name
            tempfile.close()
        return self._file_cache

    def has_local(self):
        cached = self._file_cache and path.exists(self._file_cache)
        return self.is_local or cached

    def hash(self):
        """ Generate an SHA1 hash of the given ingested object. """
        if self._hash is None:
            self._hash = checksum(self.local())
        return self._hash

    def generate_meta(self, meta):
        """ Set up some generic metadata for the resource, based on
        the available file name, HTTP headers etc. """
        meta = meta or {}
        for key, value in self.meta.items():
            if key not in meta:
                meta[key] = value
        if 'source_file' not in meta and self._file_name:
            meta['source_file'] = self._file_name

        if not meta.get('name'):
            if meta.get('source_url') and len(meta.get('source_url')):
                path = meta['source_url']
                try:
                    path = urlparse(path).path
                except:
                    pass
                meta['name'] = path
            elif meta.get('source_file') and len(meta.get('source_file')):
                meta['name'] = meta['source_file']
        name, slug, ext = make_secure_filename(meta.get('name'))
        meta['name'] = name
        if not meta.get('slug'):
            meta['slug'] = slug
        if not meta.get('extension'):
            meta['extension'] = ext
        if not meta.get('mime_type') and 'http_headers' in meta:
            mime_type = meta.get('http_headers').get('content_type')
            if mime_type not in ['application/octet-stream', 'text/plain']:
                meta['mime_type'] = mime_type
                ext = mimetypes.guess_extension(mime_type)
                if ext is not None:
                    meta['extension'] = ext.strip('.')
        elif not meta.get('mime_type') and meta.get('name'):
            mime_type, encoding = mimetypes.guess_type(meta.get('name'))
            meta['mime_type'] = mime_type

        if meta.get('extension'):
            meta['extension'] = slugify(meta.get('extension'))
        return meta

    def store(self, source):
        if not self.has_local():
            source.save_fileobj(self._file_obj)
        elif self.is_local:
            source.save_file(self._file_name)
        elif self._file_cache:
            source.save_file(self._file_cache, destructive=True)

    def dispose(self):
        if self._file_cache is not None and path.exists(self._file_cache):
            unlink(self._file_cache)

    @classmethod
    def analyze(cls, something):
        """ Accept a given input (e.g. a URL, file path, or file handle
        and determine how to normalize it into an ``Ingestor`` while
        generating metadata. """
        if isinstance(something, cls):
            return (something, )

        if isinstance(something, basestring):
            # Treat strings as paths or URLs
            url = urlparse(something)
            if url.scheme.lower() in ['http', 'https']:
                something = requests.get(something)
            elif url.scheme.lower() in ['file', '']:
                finalpath = url.path
                if osname == 'nt':
                    finalpath = finalpath[1:]
                upath = fullpath(finalpath)
                if path.isdir(upath):
                    return (cls(file_name=f) for f in directory_files(upath))
                return (cls(file_name=upath),)

        # Python requests
        if isinstance(something, requests.Response):
            fd = StringIO(something.content)
            return (cls(file_obj=fd, meta={
                'http_status': something.status_code,
                'http_headers': clean_headers(something.headers),
                'source_url': something.url
            }), )

        if isinstance(something, HTTPResponse):
            # Can't tell the URL for HTTPResponses
            return (cls(file_obj=something, meta={
                'http_status': something.status,
                'http_headers': clean_headers(something.getheaders()),
                'source_url': something.url
            }), )

        elif hasattr(something, 'geturl') and hasattr(something, 'info'):
            # assume urllib or urllib2
            return (cls(file_obj=something, meta={
                'http_status': something.getcode(),
                'http_headers': clean_headers(something.headers),
                'source_url': something.url
            }), )

        elif hasattr(something, 'read'):
            # Fileobj will be a bit bland
            return (cls(file_obj=something), )

        return []
