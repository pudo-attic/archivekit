from archivekit.collection import Collection # noqa
from archivekit.archive import Archive # noqa
from archivekit.resource import Resource # noqa
from archivekit.types.source import Source # noqa

from archivekit.ext import get_stores


def _open_store(store_type, **kwargs):
    store_cls = get_stores().get(store_type)
    if store_cls is None:
        raise TypeError("No such store type: %s" % store_type)
    return store_cls(**kwargs)


def open_collection(name, store_type, **kwargs):
    """ Create a ``archivekit.Collection`` of the given store type, passing
    along any arguments. The valid types at the moment are: s3, file.
    """
    return Collection(name, _open_store(store_type, **kwargs))


def open_archive(store_type, **kwargs):
    """ Create a ``archivekit.Archive`` of the given store type, passing
    along any arguments. The valid types at the moment are: s3, file.
    """
    return Archive(_open_store(store_type, **kwargs))
