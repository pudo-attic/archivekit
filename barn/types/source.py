from barn.resource import Resource


class Source(Resource):
    """ A source file, as initially submitted to the ``barn``. """

    GROUP = 'source'

    def __repr__(self):
        return '<Source(%r)>' % self.name
