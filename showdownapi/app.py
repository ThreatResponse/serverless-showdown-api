import os
import boto3
import uuid
import StringIO
import gzip
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

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


class ServerlessProfile(Resource):
    def post(self):
        try:
            data = request.json
            e = EventToDisk()
            e.to_s3(data)
            return {'result': 'stored'}, 200
        except:
            return {'result': 'could not process payload'}, 500

    def get(self):
        return {'result': 'not supported'}, 200


api.add_resource(ServerlessProfile, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
