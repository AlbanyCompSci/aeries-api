#!/usr/bin/python2

#Selenium allows for scripting a full web browser
#   (including graphical ones such as Chrome and Firefox)
#   though here, graphics are not wanted and so a headless
#   browser is used
#Webdriver is interface to the selected browser (PhantomJS)
from selenium import webdriver
#Ability to select values in HTML <select> tags
from selenium.webdriver.support import select

#Base address of the AUSDK12 Aeries system
BASEADDRESS = 	'https://abi.ausdk12.org/aeriesportal/'
#Name of the login page (relative to the base address)
LOGIN_PAGE = 	'LoginParent.aspx'
#<form> id, not currently used
#FORM_ID =	'form1'
#id for email <input>
EMAIL_ID =	'txtEmailAddress'
#id for password <input>
PASSWORD_ID =	'txtPassword'
#id for login button
LOGIN_ID =      'btnLogin'

class Session:

        #Maintain an instance of a browser, preserving the
        #   page accross calls
	global driver

        #Initialize the Session and login in to the Aeries website
        #   if successful, the browser will be on the home page
        #   (having been redirected from the login page on submit)
	def __init__(self, email, password):
                self.driver = webdriver.PhantomJS()
                self.driver.get(BASEADDRESS + LOGIN_PAGE)
                email_elem = self.driver.find_element_by_id(EMAIL_ID)
                email_elem.send_keys(email)
                password_elem = self.driver.find_element_by_id(PASSWORD_ID)
                password_elem.send_keys(password)
                login_elem = self.driver.find_element_by_id(LOGIN_ID)
                login_elem.click()

        #Execute Javascript on the current page
        def executeJS(self, js):
                self.driver.execute_script(js)
                return self.driver.page_source

        #Select a value given the <select> tag's id (elem_id) and the
        #   option value (option)
        def select(self, elem_id, option):
                elem = self.driver.find_element_by_id(elem_id)
                select_elem = select.Select(elem)
                select_elem.select_by_value(option)

        #If the page is not already loaded, go to the page; either way,
        #   return the page
	def getPage(self, address):
            if self.driver.current_url != address:
	        self.driver.get(address)
            return self.driver.page_source
