
## How to implement de-duped collections in archivekit?

* Store a content hash in the manifest and traverse to find
  duplicates (too slow, too mutable).
* Make local copies of the data, generate a content hash, upload
  by hash ID.


Sources:

    * From file name
    * From URL
    * From fileobj

Options: 

    * Content hashed
    * Move or copy?
