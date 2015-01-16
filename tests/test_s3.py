import boto
from moto import mock_s3
from datetime import date

from helpers import DATA_FILE
from barn import Collection


@mock_s3
def test_basic_api():
    pass
