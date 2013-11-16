#!/usr/bin/python2

import mechanize

BASEADDRESS = 	'https://abi.ausdk12.org/aeriesportal/'
LOGIN_PAGE = 	'LoginParent.aspx'
FORM_ID =	'form1'
EMAIL_ID =	'txtEmailAddress'
PASSWORD_ID =	'txtPassword'

class Session:

	global br

	def __init__(self, email, password):
		self.br = mechanize.Browser()
		self.br.open(BASEADDRESS + LOGIN_PAGE)
		self.br.select_form(FORM_ID)
		self.br[EMAIL_ID] = email
		self.br[PASSWORD_ID] = password
		self.br.submit()

	def getPage(self, address):
		response = self.br.open(address)
		return response.read()
