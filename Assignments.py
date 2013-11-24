#!/usr/bin/python2

#BeautifulSoup provides a model for the HTML recieved from the Session
from bs4 import BeautifulSoup
#dateutil.parser parses dates into datetimes from plain text
#re allows for the use of regular expressions to match patterns (including
#   through BeautifulSoup)
import dateutil.parser, re

ADDRESS = 'https://abi.ausdk12.org/aeriesportal/default.aspx'

def getAssignments(session):
        soup = BeautifulSoup(getMonthPage(session))
        month_id = {'id': re.compile('ctl(\d\d)_MainContent_ctl(\d\d)_lblDate')}
        month_str = soup.find('span', month_id).get_text()
        month = dateutil.parser.parse(month_str)
        day_id = {'id': re.compile('ctl(\d\d)_MainContent_ctl(\d\d)_tdWk(\d)Dy(\d)')}
	day_tags = soup.find_all('td', day_id)
	assignments = []
        in_month = False
	for day_tag in day_tags:
                day_of_month = getDayOfMonth(day_tag)
                if int(day_of_month) == 1:
                    in_month = not in_month
                if in_month == False:
                    continue
                date = month.replace(day=int(day_of_month)).isoformat()
                day = getDay(day_tag, date)
                #intentional avoidance of .append(); += combines lists at the same level
		assignments += day
	return assignments

def getMonthPage(session):
    page = session.getPage(ADDRESS)
    soup = BeautifulSoup(page)
    select_id = {'id': re.compile('ctl(\d\d)_MainContent_ctl(\d\d)_CalendarView')}
    select_tag = soup.find('select', select_id)
    session.select(select_tag.get('id'), 'Month')
    return session.executeJS(select_tag.get('onchange'))

def getDayOfMonth(tag):
        return tag.get_text('\n').split('\n')[0]

def getDay(tag, date):
        assignment_id = {'id': re.compile('CalEventLong_(\d*)')}
	assignment_rows = tag.find_all('span', assignment_id)
	assignments = []
        i = 0
	for assignment_row in assignment_rows:
                assignment = getAssignment(assignment_row, date)
                #Deals with non-expanding assignments or ones that do not follow Pd # ... format
                if assignment['short description'] == None:
                        long_description = assignment['long description']
                        short_assignment_row = assignment_row.previous_sibling
                        assignment = getAssignment(short_assignment_row, date)
                        assignment['long description'] = long_description
		assignments.append(assignment)
                i += 1
        return assignments

def getAssignment(tag, date):
	assignment =	{
				'date':                 date,
                                'period':               getAssignmentPart('period', tag),
                                'action':               getAssignmentPart('action', tag),
                                'short description':    getAssignmentPart('short description', tag),
                                'long description':     getAssignmentPart('long description', tag)
			}
	return assignment

def getAssignmentPart(part, tag):
        text = tag.get_text('|')
        part_patterns = {
                            'period':               '.*Pd (\d*).*',
                            'action':               '.*?(\S*):.*',
                            'short description':    '.*?: (.*)',
                            'long description':     '(?:Pd.*)|(?:(.*)[|])|(.*)'
                        }
        match = re.match(part_patterns[part], text)
        try:
            part = match.group(match.lastindex)
            if part == '':
                return None
            return part
        except AttributeError:
            return None
        except IndexError:
            return None
