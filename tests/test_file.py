from tempfile import mkdtemp
from shutil import rmtree
import urllib

from helpers import DATA_FILE, DATA_URL
from barn import Collection
from barn.store.file import FileStore
from barn.types.source import Source
from barn.util import checksum


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


def test_collection_ingest():
    path = mkdtemp()
    store = FileStore(path=path)
    coll = Collection(store)
    coll.ingest(DATA_FILE)
    pkgs = list(coll)
    assert len(pkgs) == 1, pkgs
    pkg0 = pkgs[0]
    assert pkg0.id == checksum(DATA_FILE), pkg0.id
    sources = list(pkg0.all(Source))
    assert len(sources) == 1, sources
    assert sources[0].name == 'test.csv', sources[0].name
    rmtree(path)


def test_package_ingest_file():
    path = mkdtemp()
    store = FileStore(path=path)
    coll = Collection(store)
    pkg = coll.create()
    source = pkg.ingest(DATA_FILE)
    assert source.meta.get('name') == 'test.csv', source.meta
    assert source.meta.get('extension') == 'csv', source.meta
    assert source.meta.get('slug') == 'test', source.meta
    rmtree(path)


def test_package_get_resource():
    path = mkdtemp()
    store = FileStore(path=path)
    coll = Collection(store)
    pkg = coll.create()
    source = pkg.ingest(DATA_FILE)
    other = pkg.get_resource(source.path)
    assert isinstance(other, Source), other.__class__
    assert other.path == source.path, other
    rmtree(path)


def test_package_source():
    path = mkdtemp()
    store = FileStore(path=path)
    coll = Collection(store)
    pkg = coll.create()
    assert pkg.source is None, pkg.source
    source = pkg.ingest(DATA_FILE)
    other = pkg.source
    assert isinstance(other, Source), other.__class__
    assert other.path == source.path, other
    rmtree(path)


def test_package_ingest_url():
    path = mkdtemp()
    store = FileStore(path=path)
    coll = Collection(store)
    pkg = coll.create()
    source = pkg.ingest(DATA_URL)
    assert source.name == 'barnet-2009.csv', source.name
    assert source.meta['source_url'] == DATA_URL, source.meta

    source = pkg.ingest(urllib.urlopen(DATA_URL))
    assert source.name == 'barnet-2009.csv', source.name
    assert source.meta['source_url'] == DATA_URL, source.meta
    rmtree(path)


def test_package_ingest_fileobj():
    path = mkdtemp()
    store = FileStore(path=path)
    coll = Collection(store)
    pkg = coll.create()
    with open(DATA_FILE, 'rb') as fh:
        source = pkg.ingest(fh)
        assert source.name == 'source.raw', source.name
    rmtree(path)
