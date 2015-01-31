import os
import six
from hashlib import sha1
from decimal import Decimal
from slugify import slugify
from datetime import datetime, date


def safe_id(name, len=5):
    """ Remove potential path escapes from a content ID. """
    if name is None:
        return None
    name = slugify(os.path.basename(name)).strip('-')
    name = name.ljust(len, '_')
    return name


def make_secure_filename(source):
    # TODO: don't let users create files called ``manifest.json``.
    if source:
        source = os.path.basename(source).strip()
    source = source or 'source'
    fn, ext = os.path.splitext(source)
    ext = ext or '.raw'
    ext = ext.lower().strip().replace('.', '')
    return source, slugify(fn), ext


def fullpath(filename):
    """ Perform normalization of the source file name. """
    if filename is None:
        return
    # a happy tour through stdlib
    filename = os.path.expanduser(filename)
    filename = os.path.expandvars(filename)
    filename = os.path.normpath(filename)
    return os.path.abspath(filename)


def clean_headers(headers):
    """ Convert HTTP response headers into a common format
    for storing them in the resource meta data. """
    result = {}
    for k, v in dict(headers).items():
        k = k.lower().replace('-', '_')
        result[k] = v
    return result


def checksum(filename):
    hash = sha1()
    with open(filename, 'rb') as fh:
        while True:
            block = fh.read(2 ** 10)
            if not block:
                break
            hash.update(block)
    return hash.hexdigest()


def encode_text(text):
    if isinstance(text, six.text_type):
        return text.encode('utf-8')
    try:
        return text.decode('utf-8').encode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text.encode('ascii', 'replace')


def json_default(obj):
    if isinstance(obj, datetime):
        obj = obj.isoformat()
    if isinstance(obj, Decimal):
        obj = float(obj)
    if isinstance(obj, date):
        return 'new Date(%s)' % obj.isoformat()
    return obj


def json_hook(obj):
    for k, v in obj.items():
        if isinstance(v, basestring):
            try:
                obj[k] = datetime.strptime(v, "new Date(%Y-%m-%d)").date()
            except ValueError:
                pass
            try:
                obj[k] = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                pass
    return obj
