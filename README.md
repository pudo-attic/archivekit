# archivekit

[![Build Status](https://travis-ci.org/pudo/archivekit.png?branch=master)](https://travis-ci.org/pudo/archivekit) [![Coverage Status](https://coveralls.io/repos/pudo/archivekit/badge.svg)](https://coveralls.io/r/pudo/archivekit)

``archivekit`` provides a mechanism for storing a (large) set of immutable documents and data files in an organized way. Transformed versions of each file can be stored the alongside the original data in order to reflect a complete processing chain. Metadata is kept with the data as a YAML file.

This library is inspired by [OFS](https://github.com/okfn/ofs), [BagIt](https://github.com/LibraryOfCongress/bagit-python) and [Pairtree](https://pythonhosted.org/Pairtree/). It replaces a previous project, [docstash](https://github.com/pudo/docstash).


## Installation

The easiest way of using ``archivekit`` is via PyPI:

```bash
$ pip install archivekit
```

Alternatively, check out the repository from GitHub and install it locally:

```bash
$ git clone https://github.com/pudo/archivekit.git
$ cd archivekit
$ python setup.py develop
```


## Example

``archivekit`` manages ``Packages`` which contain one or several ``Resources`` and their associated metadata. Each ``Package`` is part of a ``Collection``. 

```python
from archivekit import open_collection, Source

# open a collection of packages
collection = open_collection('file', path='/tmp')

# or via S3:
collection = open_collection('s3', aws_key_id='..', aws_secret='..',
                             bucket_name='test.pudo.org')

# import a file from the local working directory:
collection.ingest('README.md')

# import an http resource:
collection.ingest('http://pudo.org/index.html')
# ingest will also accept file objects and httplib/urllib/requests responses

# iterate through each document and set a metadata
# value:
for package in collection:
    for source in package.all(Source):
        with source.fh() as fh:
            source.meta['body_length'] = len(fh.read())
    package.save()
```

The code for this library is very compact, go check it out.


## Configuration

If AWS credentials are not supplied for an S3-based collection, the application will attempt to use the ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY`` environment variables. ``AWS_BUCKET_NAME`` is also supported.

## License

``archivekit`` is open source, licensed under a standard MIT license (included in this repository as ``LICENSE``).
