import sys
import time
import selenium
import unittest2
from FNSeleniumBaseClass import FNSeleniumBaseClass
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class BasicHTTPAuthTesting(FNSeleniumBaseClass):



    ##################### CLASS VARIABLES ###########################
    REGISTERED_EMAIL = None

    @classmethod
    def setUpClass(cls):
        print("cls.setupClass()")
        try:
            cls.init()
        except:
            print("Unexpected Error:", sys.exc_info()[0])
            cls.tearDownClass()
            raise



    @classmethod
    def tearDownClass(cls):
        print("cls.tearDownClass()")


    def setUp(self):
        try:
            # sudo pip3 install chromedriver_installer
            if self.browser == self.FIREFOX:
                self.driver = webdriver.Firefox()
            elif self.browser == self.CHROME:
                self.driver = webdriver.Chrome()
            else:
                print(self.testProperties["browser"])
                self.assertTrue(False,  "browser is not a supported browser")

            self.wait = WebDriverWait(self.driver, self.TIMEOUT, self.POLL_FREQ, TimeoutException);
        except:
            print("Unexpected Error:", sys.exc_info()[0])
            self.tearDown()
            raise

    def tearDown(self):
        print("tearDown()")
        self.driver.close()

    ############################# TEST CASES ##################################

    def test_someTest(self):
        # print(self.DOMAIN_AUTH + self.DOMAIN + "/accounts/login");
        # self.driver.get(self.DOMAIN_AUTH + self.DOMAIN + "/accounts/login")
        # time.sleep(5)
        print(self.DOMAIN_AUTH_SEC + self.DOMAIN + "/accounts/login")
        self.driver.get(self.DOMAIN_AUTH_SEC + self.DOMAIN + "/accounts/login")
        time.sleep(5)
    ############################# HELPER METHODS ###############################


if __name__ == "__main__":
    unittest2.main()
