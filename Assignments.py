#!/usr/bin/python2

#Need more examples before completion
def getAssignments(soup):
	day_id =	{
			'id': re.compile('ctl00_MainContent_ctl(..)_lblDate')
			}
	days = soup.find_all('span', day_id)
	assignments = []
	for day in days:
		assignments += getDay(day)
	return assignments

def getDay(day):
	getDate(day)
	assignment_rows = 
	assignments = []
	for assignment_row in assignement_rows:
		assignments.append(getAssignment(assignment_row))

def getAssignment(cell, date):
	assignment =	{
			'date': date,
			'period': getPeriod(cell),
			#'action': eg Due
			'description': getDescription(cell),
			}
	return assignment
