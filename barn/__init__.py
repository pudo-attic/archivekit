from barn.collection import Collection # noqa
from barn.resource import Resource # noqa
from barn.types.source import Source # noqa

from barn.ext import get_stores


def create(store_type, **kwargs):
    """ Create a ``barn.Collection`` of the given store type, passing
    along any arguments. The valid types at the moment are: s3, file.
    """
    store_cls = get_stores().get(store_type)
    if store_cls is None:
        raise TypeError("No such store type: %s" % store_type)
    store = store_cls(**kwargs)
    return Collection(store)
