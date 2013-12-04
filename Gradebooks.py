#!/usr/bin/python2

#re allows for matching text with regular expressions (including through BeautifulSoup)
#dateutil.parser provies .parse() to convert plain text dates in a variety of formats into datetime objects
import re, dateutil.parser
#BeautifulSoup provide a model for the source HTML
from bs4 import BeautifulSoup

#The default address of the gradebook page for AUSDK12 Aeries
ADDRESS = 'https://abi.ausdk12.org/aeriesportal/default.aspx'

#Get all gradebooks from the ADDRESS page
def getGradebooks(session):
    page = session.getPage(ADDRESS)
    soup = BeautifulSoup(page)
    gradebook_row_id =  {'id': re.compile('ctl(\d\d)_MainContent_ctl(\d\d)_DataDetails_ctl(\d\d)_trGBKItem')}
    gradebook_rows = soup.find_all('tr', gradebook_row_id)
    gradebooks = []
    for row in gradebook_rows:
        gradebooks.append(getGradebook(row))
    return gradebooks

#Get and individual gradebook, given a gradebook row tag
def getGradebook(soup):
    cells = soup.find_all('td')
    gradebook = {
                    #Gradebook/class name
                    'name':                 cells[1].get_text(),
                    #Period number (as string)
                    'period':               cells[2].get_text(),
                    #Teacher
                    'teacher':              cells[3].get_text(),
                    #Total grade percent (as string)
                    'percent':              cells[4].find('span').get('title'),
                    #Letter grade
                    'mark':                 cells[6].get_text(),
                    #Grade trend (up, down, stable, None)
                    'trend':                getTrend(cells[7]),
                    #Predicted grade percent (as string)
                    'predicted percent':    getPredicted(cells[7]),
                    #Average of four most recent scores
                    'recent average':       getRecentAverage(cells[7]),
                    #Number of missing assignments (as string)
                    'missing assignments':  cells[8].get_text(),
                    #Last date the gradebook was updated (as string in ISO format including a blank time)
                    'updated':              getDate(cells[15])
                }
    return gradebook

#Returns the grade trend based on the image link
def getTrend(cell):
    image = cell.find('img').get('src')
    if image == 'images/BlueLineGraphEqual.gif':
        return 'stable'
    elif image == 'images/GreenLineGraphNoArrow.gif':
        return 'up'
    elif image == 'images/RedLineGraphNoArrow.gif':
        return 'down'
    else:
        return None

#Get predicted total grade percent (as string)
def getPredicted(cell):
    return getTrendPercents(cell)['predicted']

#Get average of last four scores (as string)
def getRecentAverage(cell):
    return getTrendPercents(cell)['recent_average']

#Get either predicted grade or average of last fore scores from hidden string using regular expression matching
def getTrendPercents(cell):
    sentence = cell.find('img').get('title')
    #Consider reversing the two, for a more inclusive else
    if re.match('Insufficient.*', sentence):
        return {'predicted': None, 'recent_average': None}
    else:
        m = re.match('Forecasted value of (?P<predicted>\d*\.\d*)% compared to the average of the last four overall scores (?P<recent_average>\d*\.\d*)%', sentence)
        return m.groupdict()

#Get the last day the gradebook was updated (as a string in ISO format)
def getDate(cell):
    written_date = cell.find('span').get('title')
    date_object = dateutil.parser.parse(written_date)
    return date_object.isoformat()
