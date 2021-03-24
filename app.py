# Lilleth Snavely (lls4abt)

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Greeting (Resource):
    def get(self):
        return { "message" : "Hello Flask API World!" }
api.add_resource(Greeting, '/') # Route_1

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

