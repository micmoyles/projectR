#!/usr/bin/python
# pip install flask
# pip install flask-restful
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
data = {}


class User(Resource):

	def __init__(self):
		self.data = {}
	
	def get(self, name = None):
		if not self.data:
			return 'Empty dataset'
		if not name:
			return self.data
		return self.data
        #return {
        #    'Name': 'John',
        #    'DOB' : '01-01-1970'
        #}
	def put(self,input):
		print input

# Create routes
api.add_resource(User, '/hello')

if __name__ == '__main__':
	#app.run(host='0.0.0.0', port=5000, debug=True)
	app.run(debug=True)