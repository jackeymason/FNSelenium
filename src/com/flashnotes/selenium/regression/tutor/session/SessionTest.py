# -*- coding: utf-8 -*-
import sys
import os.path
# Python packages are really lame - you have to add the path to com relative to module
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../../..'))

# from .FNSeleniumBaseClass import FNSeleniumBaseClass
from com.flashnotes.selenium.smoke.FNSeleniumBaseClass import FNSeleniumBaseClass
from time import sleep

import selenium
import unittest2
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException


class SessionTest(FNSeleniumBaseClass):
    studentEmail = "20150903A@flashnotes.com"
    studentPassword = "password"
    tutorEmail = "20150903A@flashnotes.com"
    tutorPassword = "password"

    ##############  FIXTURES ##################################################
    @classmethod
    def setUpClass(cls):
        super(SessionTest, cls).setUpClass()
        cls.sellerEmail = None
        cls.buyerEmail = None

        print("cls.setupClass()")
        try:
            cls.init()
        except:
            print("Unexpected Error:", sys.exc_info()[0])
            cls.tearDownClass()
            raise


    @classmethod
    def tearDownClass(cls):
        super(SessionTest, cls).tearDownClass()
        #print("cls.tearDownClass()")
        #cls.report(cls)
        #cls.cleanUp(cls)


    def setUp(self):
        try:
            super(SessionTest, self).setUp();
            '''
            self.driver2 = webdriver.Remote(desired_capabilities={
                "browserName": self.browser2,
                "platform": self.platform2

            })

            #self.driver2 = webdriver.Chrome()
            self.wait2 = WebDriverWait(self.driver2, self.TIMEOUT, self.POLL_FREQ, TimeoutException)
            self.driver2.maximize_window()
            '''
            print("setUp()")
        except:
            print("Unexpected Error:", sys.exc_info()[0])
            self.tearDown()
            raise

    def tearDown(self):
        super(SessionTest, self).tearDown()
        #self.driver2.close()
        #self.driver2.quit()

    '''
    @ATC-006 A new user can become a tutor
    '''
    @unittest2.skip("skipping")
    def test_newUserTransitionToTutor(self):
        try:
            sleep(5);

        except:
            print("Unexpected Error:", sys.exc_info()[0])
            raise

    '''
    @ATC-007 Peer Tutor Now Session
    '''
    def test_peerTutorNowSession(self):
        # Student uses driver Tutor uses driver2
        #self.driver.execute_script("window.alert('javascript works');")
        #self.driver2.execute_script("window.alert('javascript works');")
        self.login(self.studentEmail, self.studentPassword);
        sleep(300)
        self.login(self.tutorEmail, self.tutorPassword, self.driver2, self.wait2);
        #Student requests a session
        self.requestSession(self.driver, self.wait)
        #Tutor accepts the session
        self.exceptSession(self.driver2, self.wait2)
        #Tutor goes to session
        self.wait2.until(EC.visibility_of_element_located(By.XPATH, "//a[contains(text(), 'Go to session')]")).click()
        #Student enters payment info
        self.wait.until(EC.visibility_of_element_located(By.XPATH, "//a[contains(text(), 'Enter Payment Info')]")).click()
        sleep(10)

    ################################## Helper Methods #########################

    def requestSession(self, *args):
        driver = args[0]
        wait = args[1]
        #self.goToStoreFrontOf(self.tutorEmail.replace(".", "").replace("@", ""), driver, wait);
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text() = 'Tutoring: email.20150827C@flashnotes.com']"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text() = 'Start a session']"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Select a Subject')]"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[text() = 'Accounting']"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea"))).sendKeys("A")
        wait.unitl(EC.element_to_be_clickable((By.xpath, "//button[text() = 'Request Tutoring Now']"))).click()

    def exceptSession(self, *args):
        driver = args[0]
        wait = args[1]
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Accept']"))).click()



    def goToStoreFrontOf(self, stripedEmail, *args):
        if(len(args) == 2):
            driver = args[0]
            wait = args[1]
        else:
            driver = self.driver
            wait = self.wait
        driver.get("http://" + self.DOMAIN +  "/members/" + stripedEmail + "/")


if __name__ == "__main__":
    unittest2.main()
