barn
====

[![Build Status](https://travis-ci.org/pudo/barn.png?branch=master)](https://travis-ci.org/pudo/barn)

A simple mechanism for storing a (potentially large) set of immutable documents in an organized way. Metadata is stored along with the data as a YAML file.


``docstash`` is inspired by [OFS](https://github.com/okfn/ofs), [BagIt](https://github.com/LibraryOfCongress/bagit-python) and [Pairtree](https://pythonhosted.org/Pairtree/). It replaces a previous project, [docstash](https://github.com/pudo/docstash).


Installation
------------

The easiest way of using ``barn`` is via PyPI:

```bash
$ pip install barn
```

Alternatively, check out the repository from GitHub and install it locally:

```bash
$ git clone https://github.com/pudo/barn.git
$ cd barn
$ python setup.py develop
```


Example
-------

``barn`` manages ``Packages`` which are part of a ``Collection``. 


```python
from docstash import Stash

# open a stash in the current working directory:
stash = Stash(path='.stash')

# print a list of collections:
print list(stash)

# access (or create) a specific collection:
collection = stash.get('test')

# import a file from the local working directory:
collection.ingest('README.md')

# import an http resource:
collection.ingest('http://pudo.org/index.html')
# ingest will also accept file objects and httplib/urllib/requests responses

# iterate through each document and set a metadata
# value:
for doc in collection:
    with open(doc.file, 'rb') as fh:
        doc['body_length'] = len(fh.read())
    doc.save()
```

The code for this library is very compact, go check it out.


Configuration
-------------

The storage directory for the stash is an optional value. If it isn't passed in (or if it is ``None``), the value of the environment variable ``DOCSTASH_PATH`` will be used. If that variable is unused, docstash will default to ``~/.docstash``.


License
-------

``barn`` is open source, licensed under a standard MIT license (included in this repository as ``LICENSE``).
