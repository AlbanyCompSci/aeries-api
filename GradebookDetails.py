#!/usr/bin/python2

from bs4 import BeautifulSoup
import re, dateutil.parser, time

BASE_URL = 'https://abi.ausdk12.org/aeriesportal/'
DEFAULT_PAGE = 'default.aspx'
GRADEBOOK_PAGE = 'GradebookDetails.aspx'

def getGradebook(gradebook_name, session):
    page = getGradebookPage(gradebook_name, session)
    soup = BeautifulSoup(page)
    #print "Soup: " + soup.prettify()
    entries = getEntries(soup)
    #weighting = getWeighting(soup)
    #return {'entries': entries, 'weighting': weighting}
    return entries

def getGradebookPage(gradebook_name, session):
    default_text = session.getPage(BASE_URL + DEFAULT_PAGE)
    default_soup = BeautifulSoup(default_text)
    link_tag = default_soup.find('a', text=gradebook_name)
    js_link = link_tag.get('href')
    session.executeJS(js_link)
    gradebook_page = session.getPage(BASE_URL + GRADEBOOK_PAGE)
    return gradebook_page

def getEntries(soup):
    table_id = {'id': re.compile('ctl00_MainContent_subGBS_tblEverything')}
    table = soup.find('table', table_id).find_all('table')[2]
    #table = getTable(soup, 'td', 'ctl(\d\d)_MainContent_subGBS_DataDetails_ctl(\d\d)_imgExpand')
    #print "Table: " + str(table)
    rows = table.find_all('tr')
    entries = []
    for row in rows:
        try:
            first_td_class = row.find('td').get('class')[0]
            #print "First TD Class: " + first_td_class
            if first_td_class != 'DataLE':
                continue
        except (AttributeError, TypeError):
            continue
        entry = getEntry(row)
        entries.append(entry)
    return entries

def getEntry(row):
    tds = row.find_all('td', {'class': 'Data'})
    entry = {
                'assignment number':        clean(tds[0].get_text()),
                #description/name
                'description':              clean(tds[1].get_text('|').split('|')[0]),
                'date assigned':            getDate(getExpand('date assigned', tds[1])),
                #cannot figure out what format would look like; omitting
                #'due time':                getExpand('due time', tds[1]),
                'long description':         getExpand('long description', tds[1]),
                #type of assignment (Formative/Summative)
                'type':                     tds[2].get_text(),
                #weighting category
                'category':                 tds[3].get_text(),
                #score recieved on assignment (my points)
                'recieved score':           getScore(tds[4])['numerator'],
                #max score on assignment (out of points)
                'max score':                getScore(tds[4])['denominator'],
                #appears to be essentially the same as score; omitting
                #'recieved number correct': getScore(tds[5])['numerator'],
                #'max number correct':      getScore(tds[5])['denominator'],
                #percentage on assignment (could also be calculated directly from score)
                'percent':                  tds[6].get_text().rstrip('%'),
                #unknown
                'status/comment':           tds[7].get_text(),
                #date grading completed
                'date completed':           getDate(tds[8].get_text()),
                #consider combining with due time
                'due date':                 getDate(tds[9].get_text()),
                #'grading complete':         tds[10].get_text(),
                'attachments':              getAttachments(tds[11])
            }
    return entry

def clean(string):
    #newline or whitespace
    #nl_ws = r'(?:\n|\s)'
    #match = re.match(nl_ws + '*(.*)' + nl_ws + '*', string)
    cleaned = string.strip(' \t\n\r')
    cleaned = cleaned.encode('ascii', 'ignore')
    return cleaned

def getExpand(key, super_td):
    #print "Expand " + str(super_td.get_text().encode('ascii', 'ignore'))
    sub_tr_ids =    {
                        'date assigned':    re.compile('.*trDA'),
                        'due time':         re.compile('.*trDUT'),
                        'long description': re.compile('.*trCOM')
                    }
    sub_tr = super_td.find('tr', {'id': sub_tr_ids[key]})
    data_td = sub_tr.find_all('td')[1]
    try:
        text = clean(data_td.get_text())
    except:
        text = None
    return text

def getScore(td):
    text = clean(td.get_text())
    #print "Score: " + text
    split = text.split('/')
    try:
        numerator = clean(split[0])
    except:
        numerator = None
    try:
        denominator = clean(split[1])
    except:
        denominator = None
    fraction = {'numerator': numerator, 'denominator': denominator}
    return fraction

def getDate(date_str):
    return dateutil.parser.parse(date_str).isoformat()

def getAttachments(td):
    link_id = {'id': re.compile('ctl(\d\d)_MainContent_subGBS_DataDetails_ctl(\d\d)_dlDocuments_ctl(\d\d)_lnkDoc')}
    links = td.find_all('a', link_id)
    attachments = []
    for link in links:
        attachment =    {
                            'name': link.get('title'),
                            'file name': link.get('href')
                        }
        attachments.append(attachment)
    return attachments

def getWeighting(soup):
    table = getTable(soup, 'td', 'ctl(\d\d)_MainContent_subGBS_DataSummary_ctl(\d\d).*')
    rows = table.find_all('tr')
    categories = []
    for row in rows:
        category = getCategory(row)
        categories.append(category)
    return categories

def getTable(soup, tag_name, regex_id):
    tables = soup.find_all('table')
    tag_id = {'id': re.compile(regex_id)}
    for table in tables:
        if table.find(tag_name, tag_id) != None:
            last_inclusive_table = table
    return last_inclusive_table

def getCategory(row):
    category = {}
    part_ids =  {
                    #name of category
                    'name':             re.compile('.*tdDESC'),
                    #percentage of grade when category active
                    'weight percent':   re.compile('.*tdPctOfGrade'),
                    #points recieved (my points)
                    'recieved points':  re.compile('.*tdPTS'),
                    #max points (out of points)
                    'max points':       re.compile('.*tdMX'),
                    #my percentage (can also be calculated with recieved points and max points)
                    'grade percent':    re.compile('.*tdPCT'),
                    #letter grade
                    'mark':             re.compile('.*tdMK')
                }
    for part in part_ids:
        try:
            part_value = row.find('td', part_ids[part]).get_text()
        except:
            category[part] = None
            continue
        if re.match('.*percent.*', part):
            part_value = part_value.rstrip('%')
        category[part] = part_value
    return category
