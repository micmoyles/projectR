#!/usr/bin/python
# pip install flask
# pip install flask-restful
from flask import Flask, request
from flask_restful import Resource, Api
import MySQLdb as mdb

app = Flask(__name__)
api = Api(app)
data = {}
getQuery = '''
	select name, dob from users where name = "%s"
''' 

responseString = "Hello %s!, your birthday is in %d days"
# when running from a container we cannot use localhost or 127.0.0.1
# as they reference virtual networks within the container
db = mdb.connect( "database-container", "root", "chelsea" )
cursor = db.cursor(mdb.cursors.DictCursor)
cursor.execute( "use projectR" )

def getDaystoBirthday(birthday):
	return 10

class User(Resource):

	
	def get(self, name):
		
		if name in data.keys():
			return responseString % (name,getDaystoBirthday(data[name]))

		query = getQuery % name
		cursor.execute( query )
		response = cursor.fetchone()
		if not response:
			return '{ "message": "user not found"}'
		
		
		if len(response) > 0 and response['name'].lower() != name.lower():
			print('Some kind of serious error')
			return 400
		return "Hello %s!, your birthday is in %d days" % (name,getDaystoBirthday(response['dob']))


	def put(self,name):

		try:
			json_data = request.get_json()
			dob = json_data['dob']
			data[name] = dob
			return 204

		except:
			return 400
		

# Create routes
api.add_resource(User, '/hello/<name>','/hello')

if __name__ == '__main__':
	# when running in a container we must listen on 0.0.0.0 not localhost	
	app.run(host = '0.0.0.0' , port=5000, debug=True)