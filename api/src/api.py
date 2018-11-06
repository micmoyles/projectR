#!/usr/bin/python

from flask import Flask, request
from flask_restful import Resource, Api
import MySQLdb as mdb
import time, json, os, yaml
import datetime as dt

app = Flask(__name__)
api = Api(app)
data = {}
BADREQUEST = 400
NOCONTENT  = 204

getQuery = '''
	select name, dob from users where name = "%s"
''' 
insertQuery = '''
	replace into users values('%s','%s')
'''
timeToBirthdayString = "Hello, %s! Your birthday is in %d days"
happyBirthday  = "Hello, %s! Happy Birthday!"

def executeDBQuery(query):
	db = mdb.connect( dbHost, dbUser, dbPass, 'projectR' )
	cursor = db.cursor(mdb.cursors.DictCursor)
	query = query.strip()

	if 'select' in query:

		cursor.execute( query )
		response = cursor.fetchall()

		if len(response) == 1:
			
			(code,text)  = (0,response[0])
		else:
			(code,text) = (1,'Unexpected DB response')

	elif query.startswith('insert') or query.startswith('replace'):
		
		try:
			cursor.execute( query )
			db.commit()
			(code,text) = (0,NOCONTENT)
		except Exception as e:
			print(e)
			code = BADREQUEST
			text  = type(e).__name__

	cursor.close()
	db.close()

	return (code,text)

def getConfig(cfgpath):

    config = {}
    if not os.path.exists(cfgpath):
        if not os.path.exists(os.path.join(CUR_DIR, cfgpath)):
            raise ValueError("Config file %s is not found!" % cfgpath)
        cfgpath = os.path.join(CUR_DIR, cfgpath)
    with open(cfgpath, 'r') as cfgf:
        config = yaml.load(cfgf.read())
    return config


def isProperData(dobString):
	try:
		res = dt.datetime.strptime(dobString,'%Y-%m-%d').date()
		return True
	except ValueError:
		return False

def getDaystoBirthday(dob):
	
	today = dt.date.today()

	# needed to accomodate for leapyear
	numDaysThisYear = int(dt.date(today.year,12,31).strftime('%j'))

	# birthdayThisYear
	bTY = dt.date(today.year,dob.month,dob.day)
	# birthdayNextYear - needed to accomodate for leap years
	bNY = dt.date(today.year + 1,dob.month,dob.day)
	todayAsInt = int(today.strftime('%j'))
	bTYAsInt   = int(bTY.strftime('%j'))
	bNYAsInt   = int(bTY.strftime('%j'))
		
	if (dob.month,dob.day) == (today.month,today.day):
		daysToBirthday = 0
	else:

		# if we have already passed this years birthday we need to use 
		# the numerical day from next year to accomodate for leap years
		if todayAsInt > bTYAsInt: 
			daysToBirthday = numDaysThisYear - todayAsInt + bNYAsInt
		else:
			daysToBirthday = bTYAsInt - todayAsInt

	return daysToBirthday
		


class User(Resource):

	
	def get(self, name):

		name = name.lower()
		responseDict = {}
		query = getQuery % name

		code, response = executeDBQuery( query )
		
		if code != 0:
			return BADREQUEST
		
		daysToBirthday = getDaystoBirthday(response['dob'])

		if daysToBirthday == 0:
			responseDict['message'] = happyBirthday % name
		else:
			responseDict['message'] = timeToBirthdayString % (name,daysToBirthday)
		
		# convert dict to json for response
		return json.loads(json.dumps(responseDict))


	def put(self,name):

		name = name.lower()

		json_data = request.get_json()
		print(json_data)
		
		# ensure we receive expected field
		try:
			dob = json_data['dateOfBirth']
		except KeyError:
			print('KeyError')
			return BADREQUEST
		# ensure data is formatted correctly
		if not isProperData(dob):
			print('Cannot insert malformatted dob string')
			return BADREQUEST

		code, response = executeDBQuery( insertQuery % (name,dob) )
		print((code,response))
		if code == 0:
			return int(response) # 204
		else:
			return code
		

# Create routes
api.add_resource(User, '/hello/<name>','/hello')

if __name__ == '__main__':

	# quick check to see if we're in a container
	if os.path.exists('settings.yaml'):
		print('Loading Configs')
		config = getConfig('settings.yaml')
		dbHost = config['database']['host']
		dbUser = config['database']['user']
		dbPass = config['database']['password']
		debug = True
	else:
		# we're in a container
		print('Sleeping to allow database-container to initialise.')
		time.sleep(10)
		dbHost = 'database-container'
		dbUser = 'lenny'
		dbPass = '1etM3In'
		debug = False
	
	# when running in a container we must listen on 0.0.0.0 not localhost	
	app.run(host = '0.0.0.0' , port=5000, debug=debug)