import config

import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchFrameException, NoSuchElementException

###########
# Selector Config 
##########

# Once logged in, we redirect to this page to scrape.
SCRAPE_PAGE = "https://console.aws.amazon.com/billing/home?#/credits"

# Selector for balance field:
BALANCE_SELECTOR = "td.credits-priority-2:nth-child(3)"
TOTAL_SELECTOR = "td.credits-priority-2:nth-child(2)"

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
        return self.__scrapeCredits()

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

    def __scrapeCredits(self):
        self.driver.get(SCRAPE_PAGE)

        # Scrape out the string representation of our credit.balance
        balanceText = self.driver.find_element_by_css_selector(BALANCE_SELECTOR).text
        totalText = self.driver.find_element_by_css_selector(TOTAL_SELECTOR).text

        balanceCents = CurrencyConverter.getStringCents(balanceText)
        totalCents = CurrencyConverter.getStringCents(totalText)

        return [balanceCents, totalCents]

class CurrencyConverter():

    @staticmethod
    def getStringCents(toParse):
        """
        Parses a provided value and returns the number of cents.

        For example, "$3.52" would return 232.
        """
        # Parse out the dollars and cents
        matchObj = re.match(r'\$(\d+)\.(\d+)', toParse)

        if matchObj.lastindex != 2:
            # Got more/less matches than anticipated.
            # TODO: Throw an exception here.
            pass

        dollars = int(matchObj.group(1))
        cents = int(matchObj.group(2))

        return (dollars*100)+cents

for account in config.ACCOUNTS:
    email = account[0]
    password = account[1]
    print "Scraping credit data for %s" % (email)
    AWSBrowser(email, password).getCreditData()

