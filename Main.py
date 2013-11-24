#!/usr/bin/python2

#system
#JSON for language agnostic output
try:
	import simplejson as json
except ImportError:
	import json

#local
#AeriesSession provides an object for interacting with the Aeries
#   website (also used internally by Gradebooks and Assignments)
#Gradebooks gets gradebook information from the home page
#Assignments gets assignment information from the home page
import AeriesSession, Gradebooks, Assignments, GradebookDetails

def getUserData(email, password):
        #Initializes a session object, which logs in to Aeries
	session = AeriesSession.Session(email, password)
        #Passes the session object to the Gradebooks class to
        #   read general gradebook information (in python format)
        #   from the home page
	gradebooks = Gradebooks.getGradebooks(session)
        #Passes the session object to the Assignments class to read
        #   the current month's (starting on the 1st ending on the
        #   last day) assignments (in python format) from the home page
	assignments = Assignments.getAssignments(session)
	return {'gradebooks': gradebooks, 'assignments': assignments}

def toJSON(python_hierachy):
	return json.dumps(python_hierachy, sort_keys=True, indent=4, separators=(',', ': '))

def getLoginData(file_name):
		with open(file_name) as f:
		        lines = f.readlines()
                        #Reads first line of file as email used for login
		        email = lines[0].rstrip('\n')
                        #Reads second line of file as password used for login
		        password = lines[1].rstrip('\n')
		return {'email': email, 'password': password}

#Get user login data from file MyLoginData in the working directory
login_data = getLoginData('MyLoginData')
#Gets users basic gradebooks and assignments from the home page and
#   returns them in python format
user_data = getUserData(login_data['email'], login_data['password'])
#Returns user data converted into JSON
json = toJSON(user_data)
print json
