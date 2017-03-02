from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class EventToElastic():
    pass

class EventToDisk():
    pass


class ServerlessProfile(Resource):
    def post(self):
        try:
            data = request.json
            return {'result': 'stored'}, 200
        except:
            return {'result': 'could not process payload'}, 500

    def get(self):
        return {'result': 'not supported'}, 200


api.add_resource(ServerlessProfile, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
