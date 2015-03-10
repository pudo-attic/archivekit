from moto import mock_s3
from StringIO import StringIO

from helpers import DATA_FILE
from archivekit import Collection
from archivekit.store.s3 import S3Store
from archivekit.types.source import Source
from archivekit.util import checksum


@mock_s3
def test_store_loader():
    from archivekit.ext import get_stores
    stores = get_stores()
    assert 's3' in stores, stores
    assert stores['s3'] == S3Store, stores


@mock_s3
def test_open_collection():
    from archivekit import open_collection
    coll = open_collection('test', 's3', bucket_name='foo')
    assert isinstance(coll.store, S3Store), coll.store
    assert coll.store.bucket.name == 'foo', coll.store.bucket


@mock_s3
def test_list_collections():
    store = S3Store(bucket_name='foo', prefix='bar')
    coll = Collection('test', store)
    coll.ingest(DATA_FILE)
    colls = list(store.list_collections())
    assert len(colls) == 1, colls
    assert colls[0] == coll.name, colls


@mock_s3
def test_basic_package():
    store = S3Store(bucket_name='test_bucket')
    coll = Collection('test', store)

    assert len(list(coll)) == 0, list(coll)

    pkg = coll.create()
    assert pkg.id is not None, pkg
    assert pkg.exists(), pkg

    pkg = coll.get(None)
    assert not pkg.exists(), pkg


@mock_s3
def test_basic_manifest():
    store = S3Store(bucket_name='test_bucket')
    coll = Collection('test', store)
    pkg = coll.create()
    pkg.manifest['foo'] = 'bar'
    pkg.save()

    npkg = coll.get(pkg.id)
    assert npkg.id == pkg.id, npkg
    assert npkg.manifest['foo'] == 'bar', npkg.meta.items()


@mock_s3
def test_collection_ingest():
    store = S3Store(bucket_name='test_bucket')
    coll = Collection('test', store)
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
    coll = Collection('test', store)
    pkg = coll.create()
    source = pkg.ingest(DATA_FILE)
    assert source.meta.get('name') == 'test.csv', source.meta
    assert source.meta.get('extension') == 'csv', source.meta
    assert source.meta.get('slug') == 'test', source.meta


@mock_s3
def test_package_local_file():
    store = S3Store(bucket_name='test_bucket')
    coll = Collection('test', store)
    pkg = coll.create()
    source = pkg.ingest(DATA_FILE)
    with source.local() as file_name:
        assert file_name != DATA_FILE, file_name
        assert file_name.endswith('test.csv'), file_name


@mock_s3
def test_package_save_data():
    store = S3Store(bucket_name='test_bucket')
    coll = Collection('test', store)
    pkg = coll.create()
    src = Source(pkg, 'foo.csv')
    src.save_data('huhu!')

    src2 = Source(pkg, 'bar.csv')
    sio = StringIO("bahfhkkjdf")
    src2.save_fileobj(sio)

