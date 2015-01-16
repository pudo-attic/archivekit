from moto import mock_s3

from helpers import DATA_FILE
from barn import Collection
from barn.store.s3 import S3Store


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
def test_storing_a_file():
    store = S3Store(bucket_name='test_bucket')
    coll = Collection(store)
    pkg = coll.create()
    
    # TODO: implement ingest.
