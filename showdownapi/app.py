import os
import boto3
import uuid
import StringIO
import gzip

from chalice import Chalice

app = Chalice(app_name='showdown-api')
app.debug = True

s3_bucket = os.environ["S3_BUCKET"]


class EventToDisk():
    """Writes the content to s3 for ingestion to elastic later."""
    def __init__(self):
        self.client = boto3.client('s3')

    def __gzip(self, contents):
        out = StringIO.StringIO()
        with gzip.GzipFile(fileobj=out, mode="w") as f:
            f.write(contents)
        return out.getvalue()

    def to_s3(self, contents):
        """Puts contents of a post to s3."""
        payload = self.__gzip(str(contents))
        response = self.client.put_object(
            ACL='private',
            Key="{id}.json.gz".format(id=uuid.uuid4().hex),
            Body=str(payload),
            Bucket=s3_bucket
        )
    pass


@app.route('/', methods=['POST', 'GET'])
def index():
    print app.current_request.method
    if app.current_request.method == 'POST':
        data = app.current_request.raw_body
        e = EventToDisk()
        e.to_s3(data)
        return {'result': 'stored'}, 200

    else:
        return {'result': 'not supported'}, 200
