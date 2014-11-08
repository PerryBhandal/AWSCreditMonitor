import config

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchFrameException, NoSuchElementException

###########
# Selector Config 
##########


class AWSBrowser():
    """
    AWSBrowser wraps a single browser and represents a single
    attempt to scrape credit data.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getCreditData(self):
        """
        getCreditData runs a single scrape attempt on AWS.

        If successful it returns a list containing two elements:
        
        [0]: Credits used (cents)
        [1]: Total credits (cents)

        If it fails, it throws an AWSBrowserException
        """
        # TODO: Add error check.
        self.__createBrowser()
        self.__login()

    def __createBrowser(self):
        self.driver = webdriver.Firefox()

    def __login(self):
        # Go to login page
        self.driver.get("https://console.aws.amazon.com/?nc2=h_m_mc")

        # Enter username and password
        userField = self.driver.find_element_by_id('ap_email')
        userField.send_keys(self.username)

        passField = self.driver.find_element_by_id('ap_password')
        passField.send_keys(self.password)

        # Submit form
        self.driver.find_element_by_id('signInSubmit-input').click()

for account in config.ACCOUNTS:
    email = account[0]
    password = account[1]
    print "Scraping credit data for %s" % (email)
    AWSBrowser(email, password).getCreditData()

