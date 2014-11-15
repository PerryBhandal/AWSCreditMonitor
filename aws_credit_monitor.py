import config
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchFrameException, NoSuchElementException

from selenium.webdriver.common.by import By

##### Selector Constants

## Login Form
LOGIN_FORM_URL = "https://console.aws.amazon.com/?nc2=h_m_mc"
LOGIN_FIELD_EMAIL = 'ap_email'
LOGIN_FIELD_PASSWORD = 'ap_password'
LOGIN_FIELD_SUBMIT = 'signInSubmit-input'

## Credit Page
CREDIT_URL = "https://console.aws.amazon.com/billing/home?region=us-east-1#/credits"
CREDIT_TABLE_SELECTOR = ".credits-table"
CREDIT_TABLE_ROW_SELECTOR = ".credits-table tbody tr" 

# Wait this long after a failed get attempt before trying again.
RECONNECT_INTERVAL = 0.5

class AWSBrowser():
    """
    AWSBrowser wraps the Selenium driver and provides the functionality for a single
    scrape attempt.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getCreditData(self):
        self.__createBrowser()
        self.__login()
        scrapedCredits = self.__scrapeCreditPage()
        
        for credit in scrapedCredits:
            print "--- Credit Entry ---"
            print "Owner: %s" % (self.username)
            print "Credit Name: %s" % (credit[0])
            print "Credit: %s used of %s" % (credit[1], credit[2])

    def closeBrowser(self):
        self.driver.quit()

    def __createBrowser(self):
        self.driver = webdriver.Firefox()

    def __login(self):
        self.driver.get(LOGIN_FORM_URL)

        # Enter username and password.
        userField = self.driver.find_element_by_id(LOGIN_FIELD_EMAIL)
        userField.send_keys(self.username)

        passField = self.driver.find_element_by_id(LOGIN_FIELD_PASSWORD)
        passField.send_keys(self.password)

        # Submit
        self.driver.find_element_by_id(LOGIN_FIELD_SUBMIT).click()

        self.__verifyLogin()

    def __verifyLogin(self):
        if "Sign In" in self.driver.title:
            raise RuntimeError("Sign In Failed")

    def __scrapeCreditPage(self):
        creditInfo = []

        self.driver.get(CREDIT_URL)

        self.__creditTableLoaded()

        tableRows = self.driver.find_elements(By.CSS_SELECTOR, CREDIT_TABLE_ROW_SELECTOR)

        for row in tableRows:
            columns = row.find_elements(By.TAG_NAME, "td")
            creditName = columns[1].get_attribute('innerHTML')
            creditUsed = columns[2].get_attribute('innerHTML')
            creditTotal = columns[3].get_attribute('innerHTML')
            creditInfo.append([creditName, creditUsed, creditTotal])

        return creditInfo

    def __creditTableLoaded(self):
        loadFails = 0

        while loadFails < config.MAX_ATTEMPTS:
            creditTableList = self.driver.find_elements(By.CSS_SELECTOR, CREDIT_TABLE_SELECTOR)

            if len(creditTableList) == 0:
                loadFails += 1
                time.sleep(0.5)
            else:
                return True

        raise RuntimeError("Failed to load account after %d tries." % (loadFails))

for account in config.ACCOUNTS:
    browser = AWSBrowser(account[0], account[1])
    browser.getCreditData()
    browser.closeBrowser()
