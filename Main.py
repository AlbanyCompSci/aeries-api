#!/usr/bin/python2

#system
import re
try:
	import simplejson as json
except ImportError:
	import json
from bs4 import BeautifulSoup
#local
import AeriesSession, Gradebooks #, Assignments

DEFAULT_PAGE = 'http://abi.ausdk12.org/aeriesportal/default.aspx'

def getUserData(email, password):
	session = AeriesSession.Session(email, password)
	default_page = session.getPage(DEFAULT_PAGE)
	#print default_page
	default_soup = BeautifulSoup(default_page)
	gradebooks = Gradebooks.getGradebooks(default_soup)
	#Insufficient example data to fully determine the structure of assignments
	#assignments = Assignments.getAssignments(default_soup)
	#return {'gradebooks': gradebooks, 'assignments': assignments}
	return gradebooks

def toJSON(python_hierachy):
	return json.dumps(python_hierachy, sort_keys=True,
			indent=4, separators=(',', ': '), default=dthandler)

def dthandler(obj):
	if hasattr(obj, 'isoformat'):
		return obj.isoformat()
	else:
		raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

def getLoginData(file_name):
		with open(file_name) as f:
				lines = f.readlines()
				email = lines[0].rstrip('\n')
				password = lines[1].rstrip('\n')
		return {'email': email, 'password': password}

def getJSON(email, password):
    user_data = getUserData(email, password)
    return toJSON(user_data)

login_data = getLoginData('MyLoginData')
print getJSON(login_data['email'], login_data['password'])
