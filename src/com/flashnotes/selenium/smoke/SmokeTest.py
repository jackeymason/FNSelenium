# -*- coding: utf-8 -*-

from FNSeleniumBaseClass import FNSeleniumBaseClass
from time import sleep
import sys
import selenium
import unittest2
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException


class SmokeTest(FNSeleniumBaseClass):
    # Class variable (static member)


    ##############  FIXTURES ##################################################
    @classmethod
    def setUpClass(cls):
        super(SmokeTest, cls).setUpClass()
        cls.sellerEmail = None
        cls.buyerEmail = None

    @classmethod
    def tearDownClass(cls):
        super(SmokeTest, cls).tearDownClass()
        #cls.report(cls)

    def setUp(self):
        try:
            super(SmokeTest, self).setUp();
            print("setUp()")
            #SmokeTest.REGISTERED_EMAIL = "676028@flashnotes.com"
            #self.USER_NAME = "676028"
            #if SmokeTest.REGISTERED_EMAIL is None:
            #    self.registerByEmail(self.getUniqueEmail())
            #    self.logout()
        except:
            print("Unexpected Error:", sys.exc_info()[0])
            self.tearDown()
            raise

    def tearDown(self):
        super(SmokeTest, self).tearDown()


    '''
    @ATC-001 A person can register with an email address and then logout and back
    in with their new credentials
    '''
    # @unittest2.skip("skipping")
    def test_2registerByEmail(self):
        try:
            email = self.registerByEmail(self.getUniqueEmail())
            # Logout and then back in to verify user credentials
            self.logout()
            self.login(email, self.USER_PASSWORD)
            self.logout()
            print("registered by email: " + email + "/" + self.USER_PASSWORD)
        except:
            print("Unexpected Error:", sys.exc_info()[0])
            raise

    '''
    @ATC-002 An existing user can login and logout
    '''
    @unittest2.skip("skipping")
    def test_1existingUserlogin(self):
        try:
            self.login(self.USER_EMAIL, "j9799106")
            self.logout()
        except:
            print("Unexpected Error:", sys.exc_info()[0])
            raise
    '''

    @ATC-003 A newly registered user can upload a note via the
    "Upload My First Note" CTA and upon return to their dashboard
    the CTA is no longer present
    '''
    # @unittest2.skip("skipping")
    def test_3uploadFirstNote(self):
        try:
            #email = self.registerByEmail(self.getUniqueEmail())

            # TEMP CODE SHORT CUT FOR LINE ABOVE FOR TEST DEV ONLY
            self.login("20150918151847@flashnotes.com", "password")

            self.wait.until( EC.presence_of_element_located((By.XPATH, "//div[ normalize-space(text()) = 'Upload My First Note']")))
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[ normalize-space(text()) = 'Upload My First Note']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Notes']"))).click()

            '''
            self.driver.execute_script( \
                "var elements = document.getElementsByTagName('input');" + \
                "for( index in elements){" + \
                "   var element = elements[index];" + \
                "   if( element.type = 'file'){" + \
                "       element.class = 'show';" + \
                "}" + \
                "}")

            # Try from the outside in
            elem = self.wait.until((EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))))
            elem.clear
            elem.send_keys( self.PROJECT_HOME + "testAssets/255.txt")
            self.driver.execute_script( \
                "var elements = document.getElementsByTagName('input');" + \
                "for( index in elements){" + \
                "   var element = elements[index];" + \
                "   if( element.type = 'file'){" + \
                "       element.class = 'hidden';" + \
                "}" + \
                "}")
            '''
            elem = self.wait.until((EC.presence_of_element_located((By.XPATH, "//h2[text()='Drop files here!']"))))
            elem.send_keys( self.PROJECT_HOME + "testAssets/255.txt")
            sleep(3)

            # Find file input on notes upload page
            # elem = self.wait.until( EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))

            #elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='file-drop']")))
            '''
            self.driver.execute_script( \
                "var elements = document.getElementsByTagName('input');" + \
                "for( index in elements){" + \
                "   var element = elements[index];" + \
                "   if( element.type = 'file'){" + \
                "       element.class = 'show';" + \

                    "}" + \
                "}")



            elem = self.wait.until( EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
            # elem = self.wait.until( EC.visibility_of_element_located((By.CSS_SELECTOR, "div.file-drop")))
            elem.click()
            # Send it the file path

            elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains( @class, 'file-drop')]/input" )))
            #elem.is_displayed = True
            elem.send_keys( self.PROJECT_HOME + "testAssets/255.txt")



            sleep(3)

            '''


            # Find the upload button
            elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/notes/sell/']")))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/notes/sell/']"))).click()

            ''' TODO Pull this when http basic authentication isn't needed for staging
            self.driver.execute_script( \
                "var elements = document.getElementsByTagName('a');" + \
                "for( index in elements){" + \
                "var element = elements[index];" + \
                "if( element.href === 'http://" + self.DOMAIN + "/notes/sell/' ){" + \
                "element.href = '" + self.DOMAIN_AUTH + self.DOMAIN + "/notes/sell/';" + \
                "}" + \
                "}"
                )
            #sleep(10)
            '''

            #Wait on upload button to be ready


            # Notes add info page
            self.wait.until( EC.presence_of_element_located((By.ID, "title"))).send_keys("title_" + self.USER_NAME)
            self.wait.until( EC.presence_of_element_located((By.ID, "description"))).send_keys("description")

            # Iterate to verify each can be selected
            previewOptionsList = ["First Half of First Page", "First Page Only", "First Three Pages", "No Preview"]
            self.wait.until( EC.presence_of_element_located((By.XPATH, "//div[text()='First Page Only']"))).click()
            lastSelected = None
            for option in previewOptionsList:
                print(option)
                # Select
                self.wait.until( EC.visibility_of_element_located( (By.XPATH, "//div[text()='" + option + "']"))).click()
                sleep(1);
                # Click the one just selected in the drop down to view the others
                # Expand
                self.wait.until( EC.presence_of_element_located((By.XPATH, "//div[text()='" + option + "']"))).click()
                lastSelected = option
            # Set final selection
            print(lastSelected)
            # Select
            self.wait.until( EC.presence_of_element_located((By.XPATH, "//div[text()='" + lastSelected + "']"))).click()
            # Expand
            self.wait.until( EC.presence_of_element_located((By.XPATH, "//div[text()='" + lastSelected + "']"))).click()
            # Select
            self.wait.until( EC.visibility_of_element_located( (By.XPATH, "//div[text()='" + previewOptionsList[2] + "']"))).click()
            sleep(1)
            # Test setting Sale and You get Price NOTE: they have the same id='price'
            # Test that you get is updated correctly
            self.wait.until( EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='$9.99']"))).send_keys("10.00")
            sleep(1);
            youGet = self.wait.until( EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='$6.99']"))).get_attribute('value')
            self.assertEquals("$7.00", youGet, "$7.00 was the expected 70% value. Actual value was " + youGet)
            # Test that Sale price is updated correctly
            self.wait.until( EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='$6.99']"))).clear()
            self.wait.until( EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='$6.99']"))).send_keys("3.50")
            sleep(1)
            salePrice = self.wait.until( EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='$9.99']"))).get_attribute('value')
            self.assertEquals("$5.00", salePrice, "$5.00 was the expected 100/70% value. Actual value was " + salePrice)
            sleep(1)

            # Add a course
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'or add new')]"))).click()
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Add a Course']")));
            self.wait.until(EC.visibility_of_element_located((By.XPATH, \
                "//span[ contains( normalize-space(text()), 'Select a Subject')]"))).click()
            # Add course number
            elem = self.wait.until( EC.visibility_of_element_located((By.XPATH, "//div[text()='ACCO - Accounting and Computer Science']"))).click()

            inputElements = self.driver.find_elements_by_css_selector("input[type='text']")
            for input in inputElements:
                if input.get_attribute("placeholder") == "Enter Course Number":
                    input.send_keys("101")
                    sleep(1)
                    elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.option.active")))
                    elem.click()
                    break
            #elem = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Add a Course']/..//input[placeholder='Enter Course Number']")))
            #elem.click()
            # self.wait.until( EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Enter Course Number']"))).click();
            #self.wait.until( EC.visibility_of_element_located((By.XPATH, "//input[placeholder='Enter Course Number']"))).send_keys("101\r\n")
            self.wait.until( EC.element_to_be_clickable(( By.XPATH, "//button[text()='Add']"))).click()
            self.wait.until( EC.visibility_of_element_located((By.CSS_SELECTOR, "input#professor"))).send_keys("Smith")
            sleep(5)
            self.wait.until( EC.presence_of_element_located(( By.CSS_SELECTOR, "a.button.orange.full-width.text-center.ng-binding"))).click()
            self.wait.until( EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Promote your notes and make more money.')]")))
            self.wait.until( EC.visibility_of_element_located((By.XPATH, "//em[text() = '(Nope)']")))
            self.wait.until( EC.presence_of_element_located((By.CSS_SELECTOR, "img[src='/site_media/static/images/progress/seller-tools-progress-0.svg']")))
            self.wait.until( EC.presence_of_element_located((By.XPATH, "//a[normalize-space(text()) = 'I’ll Promote Later']"))).click()
            self.wait.until( EC.presence_of_element_located((By.XPATH, "//span[normalize-space(text()) = 'Visit my store.']"))).click()

            # Go to Dashboard to verify CTA "Upload My First Note" is NOT displayed
            # First wait for Sales navigation tab
            self.navigateToDashboard()
            if(self.isTutoringOn):
                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[normalize-space(text()) = 'Your Sales']"))).click()
            else:
                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space(text()) = 'My Sales Results']")))

            try:
                self.driver.find_element_by_xpath("//div[ normalize-space(text()) = 'Upload My First Note']")
            except NoSuchElementException as nsee:
                print(nsee.msg)
            self.logout()

        except:
            print("Unexpected Error:", sys.exc_info()[0])
            raise

    '''
    ATC-004 A newly register user can buy a note
    '''
    # @unittest2.skip("skipping")
    def test_4purchaseFirstNote(self):
        SmokeTest.buyerEmail = self.REGISTERED_EMAIL = self.getUniqueEmail();
        print("buyer: " + SmokeTest.buyerEmail)
        self.registerByEmail(self.REGISTERED_EMAIL)
        #Click Buy button
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Buy']"))).click()
        # Click on school input field and enter school
        elem = self.wait.until(EC.presence_of_element_located(( By.CSS_SELECTOR, "div[class^='selectize-input']")))
        elem.click()
        elem = self.wait.until(EC.presence_of_element_located(( By.CSS_SELECTOR, "div[class^='selectize-input'] input")))
        elem.send_keys("Flashnotes Beta U")
        # Select the active option
        self.wait.until(EC.visibility_of_element_located(( By.CSS_SELECTOR, "div[class='option active']"))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Flashnotes Beta U']")))
        self.wait.until(EC.visibility_of_element_located((By.ID, "notes-facet-link"))).click()
        # Enter search criterea
        elem = self.wait.until(EC.presence_of_element_located(( By.CSS_SELECTOR, "div[class^='selectize-input']")))
        elem.click()
        elem = self.wait.until(EC.presence_of_element_located(( By.CSS_SELECTOR, "div[class^='selectize-input'] input")))
        elem.click()
        elem.send_keys(self.KNOWN_NOTE)
        try:
            self.wait.until(EC.presence_of_element_located(( By.CSS_SELECTOR, "div.selectize-dropdown-content > div"))).click()
        except StaleElementReferenceException as sere:
            print(sere.msg)
            self.wait.until(EC.presence_of_element_located(( By.CSS_SELECTOR, "div.selectize-dropdown-content > div"))).click()
        while len(self.driver.find_elements_by_xpath("//span[contains(text(), 'Add to Bag')]")) > 1:
            sleep(1)
        # Verify search results
        self.wait.until(EC.presence_of_element_located(( By.XPATH, "//span[text() = '" + self.KNOWN_NOTE + "']")))
        #elems = self.driver.find_elements_by_tag_name("span");
        elems = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(text(), 'Add to Bag')]")))
        self.assertEqual(1, len(elems), "Expected a download button count of 1 but found " + str(len(elems)))
        # Add to Bag
        elems[0].click()
        # Checkout
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Checkout']"))).click()
        # Proceed to payment
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Proceed to Payment']"))).click()
        # Paypal link
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@href='/checkout/paypal/redirect/']"))).click()
        # Paypal authenticate
        self.wait.until(EC.visibility_of_element_located((By.ID, "login_email"))).clear()
        self.wait.until(EC.visibility_of_element_located((By.ID, "login_email"))).send_keys("jasonPPtest@flashnotes.com")
        self.wait.until(EC.visibility_of_element_located((By.ID, "login_password"))).clear()
        self.wait.until(EC.visibility_of_element_located((By.ID, "login_password"))).send_keys("pwpwpwpw")
        self.wait.until(EC.visibility_of_element_located((By.ID, "submitLogin"))).click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "continue"))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Place My Order')]"))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Your payment was successful!']")))
        self.logout()

    '''
    ATC-05 A seller can see that a note has sold
    '''
    # @unittest2.skip("skipping")
    def test_sellerSalesDataUpdated(self):
        self.login(SmokeTest.sellerEmail, self.USER_PASSWORD)
        # Verify a Your Sales navigation and section now exists
        if(self.isTutoringOn):
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[normalize-space(text()) = 'Your Sales']"))).click()
            elems = self.driver.find_elements_by_tag_name("h2");
            found = False
            for elem in elems:
                if "Your Sales" in elem.get_attribute("innerHTML"):
                    found = True
                    break;
            self.assertTrue(found, "Failed to find 'Your Sales' section on dashboard")
        else:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space(text()) = 'My Sales Results']")))

        # Your next check section and results
        if(self.isTutoringOn):
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[text() = 'Your Next Check']")))
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[text() = 'Your Results']")))
        else:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'My Next Check')]")))
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'My Sales Results')]")))

    ############################### Helper Methods ##############################################

    def registerByEmail(self, email):
        href = self.getLoginPage("register")
        elem = self.wait.until( EC.presence_of_element_located((By.XPATH, "//a[@href = '" + href + "']")))
        elem.click();
        elem = self.wait.until( EC.visibility_of_element_located((By.XPATH, "//a[text()= 'your email']")))
        elem.click();
        elem = self.wait.until( EC.presence_of_element_located((By.ID, "id_registration-email")))
        elem = self.wait.until( EC.visibility_of_element_located((By.ID, "id_registration-email")))
        elem.send_keys(email)
        elem = self.wait.until( EC.presence_of_element_located((By.ID, "id_registration-username")))
        # Hack as this self.USER_NAME set in getUnitqueEmail()
        elem.send_keys(email)
        elem = self.wait.until( EC.presence_of_element_located((By.ID, "id_registration-first_name")))
        elem.send_keys(self.FIRSTNAME + self.USER_NAME)
        elem = self.wait.until( EC.presence_of_element_located((By.ID, "id_registration-last_name")))
        elem.send_keys(self.LASTNAME + self.USER_NAME)
        elem = self.wait.until( EC.presence_of_element_located((By.ID, "id_registration-password1")))
        elem.send_keys(self.USER_PASSWORD)
        elem = self.wait.until( EC.presence_of_element_located((By.ID, "id_registration-password2")))
        elem.click();
        elem.send_keys(self.USER_PASSWORD)

        # text input for school doesn't have an ID - depending on count and placement
        elements = self.driver.find_elements_by_css_selector("input[type='text']")
        # print(elements.__len__())
        elem = elements[5]
        elem.clear();
        elem.send_keys(self.SCHOOL)
        elem = self.wait.until( EC.presence_of_element_located((By.CSS_SELECTOR, "div.option")))
        self.assertIsNotNone(elem)
        sleep(5);
        elem = self.wait.until(EC.visibility_of(self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.option.active")))))
        elem.click()

        # Enter phone number and submit - note there is an interstitial/splash page before landing at the dashboard
        elem = self.wait.until( EC.presence_of_element_located((By.ID, "id_registration-phone_number")))
        elem.send_keys(self.PHONE)
        elem = self.wait.until( EC.presence_of_element_located((By.NAME, "registration_submit")))
        elem.click()


        # Validate login - this is really lame as the dashboard lacks ID's - this could happen on interstitial page or
        # dashboard.
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[src='//ads.socialtheater.com/mark/47a826ee-a5d2-4f17-ac06-5e1cfedea66d/b457f7ed6b537158d147b14c534d0006/pixel.gif']")))
        elem = self.wait.until(EC.presence_of_element_located((By.NAME, "terms")))
        self.assertIsNotNone(elem)
        self.assertTrue(elem.is_displayed())

        if(not self.isTutoringOn):
            elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".avatar-container > img")))
            self.assertTrue( self.USER_NAME in elem.get_attribute("alt"))
        else:
            # TUTORING ON only via membership in STAGING TUTOR TESTING group
            # /site_media/static/images/avatars/1.png
            # elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[src='/site_media/static/images/avatars/1.png']")))
            # elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='" + "username" + self.USER_NAME + "' ]")))
            # Tutoring off mode
            elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[src='/site_media/static/images/avatars/1.png']")))
            elem = self.wait.until(EC.presence_of_element_located((By.XPATH, "//a[text() = '" + email + "']")))

        #Verify initial dashboard
        # Title not present on initial dashboard
        # self.driver.find_element_by_xpath("//h1[contains(text(), 'Your Dashboard.')]")

        # Upload my first note
        self.driver.find_element_by_xpath("//div[contains(text(), 'Upload My First Note')]")

        # Search to buy by...
        browseBy =  ["by subject", "by content type", "top schools"]
        for text in browseBy:
            self.driver.find_element_by_xpath("//h2[text()='Browse " + text + "']")
        self.driver.find_element_by_css_selector("div[class^='friendbuy-']")

        # Upload content links
        self.driver.find_element_by_css_selector("a[href='/notes/upload/']")
        self.driver.find_element_by_css_selector("a[href='/flashcards/upload/']")
        self.driver.find_element_by_css_selector("a[href='/offlinelearning/upload/']")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Set up a')]")
        self.driver.find_element_by_xpath("//a/span[text() = 'Become a Tutor']")
        print("new registration: " + email)
        return email

if __name__ == "__main__":
    unittest2.main()

