from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

puppies = []

class HelloWorld(Resource):
    def get(self):
        return {'hello':'world'}

    def post(self):
        return {'methods':'post'}


api.add_resource(HelloWorld,'/')

if __name__ == '__main__':
    app.run(debug=True)
