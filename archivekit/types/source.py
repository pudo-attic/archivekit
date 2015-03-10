from archivekit.resource import Resource


class Source(Resource):
    """ A source file, as initially submitted to the ``archivekit``. """

    GROUP = 'source'

    def __repr__(self):
        return '<Source(%r)>' % self.name
