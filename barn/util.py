import os
from decimal import Decimal
from slugify import slugify
from datetime import datetime, date


def make_secure_filename(source):
    if source:
        source = os.path.basename(source).strip()
    source = source or 'source'
    fn, ext = os.path.splitext(source)
    ext = ext or '.raw'
    ext = ext.lower().strip().replace('.', '')
    return source, slugify(fn), ext


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
