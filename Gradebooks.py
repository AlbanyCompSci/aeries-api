#!/usr/bin/python2

import re, dateutil.parser

def getGradebooks(soup):
	gradebook_row_id =	{
				'id': re.compile('ctl(..)_MainContent_ctl(..)_DataDetails_ctl(..)_trGBKItem')
				}
	gradebook_rows = soup.find_all('tr', gradebook_row_id)
	gradebooks = []
	for row in gradebook_rows:
		gradebooks.append(getGradebook(row))
	return gradebooks

def getGradebook(soup):
	cells = soup.find_all('td')
	gradebook =	{
			'name': cells[1].get_text(),
			'period': cells[2].get_text(),
			'teacher': cells[3].get_text(),
			'percent': cells[4].find('span').get('title'),
			'mark': cells[6].get_text(),
			'trend': getTrend(cells[7]),
			'predicted percent': getPredicted(cells[7]),
			'recent average': getRecentAverage(cells[7]),
			'missing assignments': cells[8].get_text(),
			'updated': getDate(cells[15])
			}
	return gradebook

def getTrend(cell):
	image = cell.find('img').get('src')
	if image == 'images/BlueLineGraphEqual.gif':
		return 'stable'
	elif image == 'images/GreenLineGraphNoArrow.gif':
		return 'up'
	elif image == 'images/RedLineGraphNoArrow.gif':
		return 'down'
	else:
		return 'none'

def getPredicted(cell):
	return getTrendPercents(cell)[0]

def getRecentAverage(cell):
	return getTrendPercents(cell)[1]

def getTrendPercents(cell):
	sentence = cell.find('img').get('title')
	#Consider reversing the two, for a more inclusive else
	if re.match('Insufficient.*', sentence):
		return ['none', 'none']
	else:
		m = re.match('Forecasted value of (.*\..*)% compared to the average of the last four overall scores (.*\..*)%', sentence)
		predicted = m.group(1)
		recent_average = m.group(2)
		return [predicted, recent_average]

def getDate(cell):
	written_date = cell.find('span').get('title')
	date_object = dateutil.parser.parse(written_date)
	return date_object.strftime('%Y-%m-%d')
