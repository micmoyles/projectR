#!/usr/bin/python

from flask import Flask, request
from flask_restful import Resource, Api
import MySQLdb as mdb
import time, json
import datetime as dt

app = Flask(__name__)
api = Api(app)
data = {}
getQuery = '''
	select name, dob from users where name = "%s"
''' 
insertQuery = '''
	replace into users values('%s','%s')
'''
userNotFoundString = '{ "message": "user not found"}'
timeToBirthdayString = "Hello, %s! Your birthday is in %d days"
happyBirthday  = "Hello, %s! Happy Birthday!"

#print('Sleeping to allow database-container to initialise.')
#time.sleep(2)

# when running from a container we cannot use localhost or 127.0.0.1
# as they reference virtual networks within the container

db = mdb.connect( "localhost", "root", "wiarreft" )
cursor = db.cursor(mdb.cursors.DictCursor)
cursor.execute( "use projectR" )

def isProperData(dobString):
	try:
		res = dt.datetime.strptime(dobString,'%Y-%m-%d').date()
		return True
	except ValueError:
		return False

def getDaystoBirthday(dobString):
	
	#dob = dt.datetime.strptime(dobString,'%Y-%m-%d').date()
	dob = dobString
	today = dt.datetime.today()
	
	if (dob.month,dob.day) == (today.month,today.day):
		daysToBirthday = 0
	else:
		todayAsInt = int(today.strftime('%j'))
		dobAsInt   = int(dob.strftime('%j'))
		if todayAsInt > dobAsInt:
			daysToBirthday = 365 - todayAsInt + dobAsInt
		else:
			daysToBirthday = dobAsInt - todayAsInt

	return daysToBirthday
		

class User(Resource):

	
	def get(self, name):
		
		responseDict = {}
		query = getQuery % name
		cursor.execute( query )
		response = cursor.fetchone()

		if not response:
			return json.loads(userNotFoundString)
		
		if len(response) > 0 and response['name'].lower() != name.lower():
			print('Some kind of serious error')
			return 400

		daysToBirthday = getDaystoBirthday(response['dob'])
		if daysToBirthday == 0:
			responseDict['message'] = happyBirthday % name
		else:
			responseDict['message'] = timeToBirthdayString % (name,daysToBirthday)
		
		# convert dict to json for response
		return json.loads(json.dumps(responseDict))


	def put(self,name):

		json_data = request.get_json()
		
		# ensure we receive expected field
		try:
			dob = json_data['dateOfBirth']	
		except KeyError:
			return 400
		# ensure data is formatted correctly
		if not isProperData(dob):
			print('Cannot insert malformatted dob string')
			return 400

		query = insertQuery % (name,dob)
		
		cursor.execute( query )
		db.commit()
		return 204
		

# Create routes
api.add_resource(User, '/hello/<name>','/hello')

if __name__ == '__main__':
	# when running in a container we must listen on 0.0.0.0 not localhost	
	app.run(host = '0.0.0.0' , port=5000, debug=True)