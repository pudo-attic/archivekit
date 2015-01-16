import logging

from loadkit.core.resource import Resource

log = logging.getLogger(__name__)


class Source(Resource):
    """ A source file, as uploaded by the user. """

    GROUP = 'sources'

    def __repr__(self):
        return '<Source(%r)>' % self.name
