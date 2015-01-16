from tempfile import mkdtemp
from shutil import rmtree

from helpers import DATA_FILE
from barn import Collection
from barn.store.file import FileStore


def test_basic_package():
    path = mkdtemp()
    store = FileStore(path=path)
    coll = Collection(store)

    assert len(list(coll)) == 0, list(coll)

    pkg = coll.create()
    assert pkg.id is not None, pkg
    assert pkg.exists(), pkg

    pkg = coll.get(None)
    assert not pkg.exists(), pkg

    rmtree(path)


def test_basic_manifest():
    path = mkdtemp()
    store = FileStore(path=path)
    coll = Collection(store)
    pkg = coll.create()
    pkg.manifest['foo'] = 'bar'
    pkg.save()

    npkg = coll.get(pkg.id)
    assert npkg.id == pkg.id, npkg
    assert npkg.manifest['foo'] == 'bar', npkg.meta.items()

    rmtree(path)
