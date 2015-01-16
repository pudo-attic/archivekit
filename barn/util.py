import os
from decimal import Decimal
from slugify import slugify
from datetime import datetime, date


def safe_id(name):
    """ Remove potential path escapes from a content ID. """
    if name is None:
        return None
    name = os.path.basename(name).strip()
    name = slugify(name).strip('-')
    name = name.ljust(5, '_')
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
    # a happy tour through stdlib
    filename = os.path.expanduser(filename)
    filename = os.path.expandvars(filename)
    filename = os.path.normpath(filename)
    return os.path.abspath(filename)


def clean_headers(headers):
    result = {}
    for k, v in dict(headers).items():
        k = k.lower().replace('-', '_')
        result[k] = v
    return result


def guess_extension(name):
    _, ext = os.path.splitext(name or '')
    return ext.replace('.', '').lower().strip()
            

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
