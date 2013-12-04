#!/usr/bin/env python2.7

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

def get(what, email, password, gradebook=None):
    session = AeriesSession.Session(email, password)
    if what == 'grades':
        data = Gradebooks.getGradebooks(session)
    if what == 'assignments':
        data = Assignments.getAssignments(session)
    if what == 'gradebook':
        #gradebook is treated as a regular expression
        data = GradebookDetails.getGradebook(gradebook, session)
    json = toJSON(data)
    return json

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
