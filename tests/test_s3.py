from moto import mock_s3

from helpers import DATA_FILE
from barn import Collection
from barn.store.s3 import S3Store
from barn.types.source import Source
from barn.util import checksum


@mock_s3
def test_store_loader():
    from barn.ext import get_stores
    stores = get_stores()
    assert 's3' in stores, stores
    assert stores['s3'] == S3Store, stores


@mock_s3
def test_create():
    from barn import create
    coll = create('s3', bucket_name='foo')
    assert isinstance(coll.store, S3Store), coll.store
    assert coll.store.bucket.name == 'foo', coll.store.bucket


@mock_s3
def test_basic_package():
    store = S3Store(bucket_name='test_bucket')
    coll = Collection(store)

    assert len(list(coll)) == 0, list(coll)

    pkg = coll.create()
    assert pkg.id is not None, pkg
    assert pkg.exists(), pkg

    pkg = coll.get(None)
    assert not pkg.exists(), pkg


@mock_s3
def test_basic_manifest():
    store = S3Store(bucket_name='test_bucket')
    coll = Collection(store)
    pkg = coll.create()
    pkg.manifest['foo'] = 'bar'
    pkg.save()

    npkg = coll.get(pkg.id)
    assert npkg.id == pkg.id, npkg
    assert npkg.manifest['foo'] == 'bar', npkg.meta.items()


@mock_s3
def test_collection_ingest():
    store = S3Store(bucket_name='test_bucket')
    coll = Collection(store)
    coll.ingest(DATA_FILE)
    pkgs = list(coll)
    assert len(pkgs) == 1, pkgs
    pkg0 = pkgs[0]
    assert pkg0.id == checksum(DATA_FILE), pkg0.id
    print pkg0
    sources = list(pkg0.all(Source))
    assert len(sources) == 1, sources
    assert sources[0].name == 'test.csv', sources[0].name


@mock_s3
def test_package_ingest_file():
    store = S3Store(bucket_name='test_bucket')
    coll = Collection(store)
    pkg = coll.create()
    source = pkg.ingest(DATA_FILE)
    assert source.meta.get('name') == 'test.csv', source.meta
    assert source.meta.get('extension') == 'csv', source.meta
    assert source.meta.get('slug') == 'test', source.meta
