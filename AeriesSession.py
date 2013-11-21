#!/usr/bin/python2

from selenium import webdriver

BASEADDRESS = 	'https://abi.ausdk12.org/aeriesportal/'
LOGIN_PAGE = 	'LoginParent.aspx'
#FORM_ID =	'form1'
EMAIL_ID =	'txtEmailAddress'
PASSWORD_ID =	'txtPassword'
LOGIN_ID =      'btnLogin'

class Session:

	global driver

	def __init__(self, email, password):
                self.driver = webdriver.PhantomJS()
                self.driver.get(BASEADDRESS + LOGIN_PAGE)
                email_elem = self.driver.find_element_by_id(EMAIL_ID)
                email_elem.send_keys(email)
                password_elem = self.driver.find_element_by_id(PASSWORD_ID)
                password_elem.send_keys(password)
                login_elem = self.driver.find_element_by_id(LOGIN_ID)
                login_elem.click()

	def getPage(self, address):
		self.driver.get(address)
		return self.driver.page_source
