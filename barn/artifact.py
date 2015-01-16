import logging
import json
import tempfile
from contextlib import contextmanager

from barn.resource import Resource
from barn.util import json_default, json_hook

log = logging.getLogger(__name__)


class Artifact(Resource):
    """ The artifact holds a temporary, cleaned representation of the
    package resource (as a newline-separated set of JSON
    documents). """

    GROUP = 'artifacts'
    
    @contextmanager
    def store(self):
        """ Create a context manager to store records in the cleaned
        table. """
        output = tempfile.NamedTemporaryFile(suffix='.json')
        try:

            def write(o):
                line = json.dumps(o, default=json_default)
                return output.write(line + '\n')

            yield write

            output.seek(0)
            log.info("Uploading generated artifact to S3 (%r)...", self.key)
            self.key.set_contents_from_file(output)
        finally:
            output.close()

    def records(self):
        """ Get each record that has been stored in the table. """
        output = tempfile.NamedTemporaryFile(suffix='.json')
        try:
            log.info("Loading artifact from S3 (%r)...", self.key)
            self.key.get_contents_to_file(output)
            output.seek(0)

            for line in output.file:
                yield json.loads(line, object_hook=json_hook)
        
        finally:
            output.close()

    def __repr__(self):
        return '<Artifact(%r)>' % self.name
