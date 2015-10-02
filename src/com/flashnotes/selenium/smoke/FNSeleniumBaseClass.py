import sys
import selenium
import unittest2
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class FNSeleniumBaseClass(unittest2.TestCase):
    ##################### CLASS VARIABLES ###########################

    REGISTERED_EMAIL = None

    ##################### CLASS METHODS #############################


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
        cls.report()
        cls.cleanUp()

    @classmethod
    def init(self):
        print("cls.init()")
        self.loadTestConfigFile(self)
        self.browser = self.testProperties["browser"]
        self.platform = self.testProperties["platform"]
        self.browser2 = self.testProperties["browser2"]
        if(self.browser2 == 'IE'):
            self.browser2 = "internet explorer"
        self.platform2 = self.testProperties["platform2"]
        self.FIREFOX = self.testProperties["firefox"]
        self.CHROME = self.testProperties["chrome"]
        self.HTMLUNIT = self.testProperties["htmlunit"]
        # There is an assumption that USER_EMAIL exists - change set up to create it if it doesn't exist
        # Find out about DJango and connectivity to staging DB and what API's might already exist
        # to create testing artifacts
        self.USER_EMAIL = self.testProperties["user_email"]
        self.USER_PASSWORD = self.testProperties["user_password"]
        self.DOMAIN_AUTH = self.testProperties["domain_auth"]
        self.DOMAIN = self.testProperties["domain"]
        self.HTTP_BASIC_AUTH = self.testProperties["httpBasicAuth"]
        self.STARTING_URL = "http://" + self.HTTP_BASIC_AUTH + self.DOMAIN
        self.STARTING_URL_SEC = "https://" + self.HTTP_BASIC_AUTH + self.DOMAIN

        self.domainUser  = self.testProperties["domainUser"]
        self.domainPassword = self.testProperties["domainPassword"]
        self.DOMAIN_AUTH_SEC = self.testProperties["domain_auth_sec"]

        self.TIMEOUT = int(self.testProperties["timeout"])
        self.POLL_FREQ = float(self.testProperties["poll_freq"])
        # This one is a little weird - getStart page sets this and others then depend on it being set
        self.elem = None
        # These could/should be added to test data to permiate through length of data limits, character types,
        # script injection rejection, etc.
        self.FIRSTNAME = self.testProperties["firstname"]
        self.LASTNAME = self.testProperties["lastname"]
        self.SCHOOL = self.testProperties["school"]
        self.PHONE = self.testProperties["phone"]
        self.USER_NAME = None
        self.FACEBOOK_EMAIL = self.testProperties["facebook_email"]
        self.FACEBOOK_PASSWORD = self.testProperties["facebook_password"]
        self.tutoringUrlParam = self.testProperties["tutoringUrlParam"]
        self.tutoring = self.testProperties["tutoring"]
        self.isTutoringOn = True if self.tutoring == "on" else False
        self.DASHBOARD = self.testProperties["dashboard"]
        self.PROJECT_HOME = self.testProperties["projectHome"]
        self.KNOWN_NOTE   = self.testProperties["knownNote"]
        self.USER_NAME = None
        print(self.KNOWN_NOTE)



################### TEST FIXTURES ############################################
    # From https://pypi.python.org/pypi/unittest-data-provider/1.0.0
    def data_provider(fn_data_provider):
        """Data provider decorator, allows another callable to provide the data for the test"""
        def test_decorator(fn):
            def repl(self, *args):
                for i in fn_data_provider():
                    try:
                        fn(self, *i)
                    except AssertionError:
                        print("Assertion error caught with data set ", i)
                        raise
            return repl
        return test_decorator

    browserPlatforms = lambda: (
        ("firefox", "mac"),
        ("chrome", "mac" ),
        ("safari", "mac")
    )



    def setUp(self):
        try:
            '''
            # sudo pip3 install chromedriver_installer
            if self.browser == self.FIREFOX:
                self.driver = webdriver.Firefox()
            elif self.browser == self.CHROME:
                self.driver = webdriver.Chrome()
                # sudo pip3 install chromedriver_installer
                # At first test-case REGISTERED_EMAIL this will be None
            elif self.browser == self.SAFARI:
                self.driver = webdriver.Safari
            else:
                print(self.testProperties["browser"])
                self.assertTrue(False,  "browser is not a supported browser")
            '''

            self.driver = webdriver.Remote(desired_capabilities={
                "browserName": self.browser,
                "platform": self.platform,
                "locationContextEnabled": True
            })


            #self.driver = webdriver.Chrome()

            self.wait = WebDriverWait(self.driver, self.TIMEOUT, self.POLL_FREQ, TimeoutException)
            self.driver.maximize_window()

        except:
            print("Unexpected Error:", sys.exc_info()[0])
            self.tearDown()
            raise


    def tearDown(self):
        print("tearDown()")
        self.driver.close()
        self.driver.quit()



    ############################# TEST CASES ##################################
    '''
    If this were exposed it would run with each child class executed - we don't want that
    just the inherited members and methods

    def test_someTest(self):
        self.assertTrue(True, "Big trouble")
    '''
    ############################# HELPER METHODS ###############################

    def getTutoringParam(self):
        return self.tutoringUrlParam + "=1" if self.isTutoringOn else self.tutoringUrlParam + "=0"

    def loadTestConfigFile(self):
        self.testProperties = {}
        try:
            with open("/Users/johnmason/git/Flashnotes/Flashnotes/FlashnotesSeleniumTests/config/test.config") as configFile:
                for line in configFile:
                    property = line.strip()
                    if ("=" in line) and (not line.startswith("#")):
                        self.testProperties[ property.split("=")[0].strip()] = property.split("=")[1].strip()
        except:
            print("Unexpected Error:", sys.exc_info()[0])
            raise
        finally:
            configFile.close()

    def waitForTimeout(self):
        try:
            elem = self.wait.until(EC.presence_of_element_located((By.NAME, "blah blah blah")))
            # Throw and exception should this start working correctly in the future with newer release of Py or Selenium
            self.assertTrue(False)
        except TimeoutException as te:
            # Show the message
            print(te.msg)

    def getUniqueEmail(self):
        self.USER_NAME = self.getUniqueUsername()
        val =  self.USER_NAME + "@flashnotes.com"
        print(val)
        return val


    def getUniqueUsername(self):
        import datetime
        time = datetime.datetime.now()
        strTime = time.strftime("%Y%m%d%H%M%S")
        return str(strTime)

    def login(self, *args):
        if(len(args) == 2):
            driver = self.driver
            wait = self.wait
        else:
            driver = args[2]
            wait = args[3]

        userName = args[0]
        password = args[1]

        href = self.getLoginPage(driver, wait)
        wait.until( EC.visibility_of_element_located((By.XPATH, "//a[@href='" + href + "']"))).click()
        elem = wait.until( EC.visibility_of_element_located((By.ID, "id_login-username")))
        elem.clear()
        elem.send_keys(userName)
        elem = wait.until( EC.presence_of_element_located((By.ID, "id_login-password")))
        elem.clear()
        elem.click();
        elem.send_keys(password)
        elem = wait.until(EC.presence_of_element_located((By.NAME, "login_submit")))
        elem.click();

        # Validate login - this is really lame as the dashboard lacks ID's
        wait.until(EC.visibility_of_element_located((By.NAME, "terms")))
        # Wait for navigation drop down
        elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fn-hover-menu.span-7")))

        self.verifyDashboardSections(driver, wait);
        # Sanity check - try except block needed as WebDriverWait ignoring exceptions to ignore arg, TimeoutException.
        '''
        elem = None
        try:
            elem = self.wait.until(EC.presence_of_element_located((By.NAME, "Oscar")))
            # Throw and exception should this start working correctly in the future with newer release of Py or Selenium
            self.assertTrue(False)
        except TimeoutException as te:
            # Show the message
            print(te.msg)
        self.assertTrue(elem == None)
        '''

    def logout(self):
        # If present, close the "new branding" overlay as it blocks logging out
        elems = self.driver.find_elements_by_id("self.webklipper-publisher-widget-container-notification-close-div")
        self.assertFalse(len(elems) > 1, "Found more than one element with the id: " + "webklipper-publisher-widget-container-notification-close-div")
        if(len(elems) == 1):
            elems[0].click();

        self.driver.get("http://" + self.DOMAIN + self.DASHBOARD)
        try:
            elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fn-hover-menu.span-7")))
        except TimeoutException as te:
            print(te.msg)
            # check if logged in
            self.assertTrue(self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/accounts/login/']"))))
            return

        self.assertTrue(elem is not None, "Failed to find hoverable element used to make logout link visible")
        hover = ActionChains(self.driver).move_to_element(elem)
        hover.perform()
        elem = self.wait.until(EC.visibility_of(self.driver.find_element_by_css_selector( "a[href='/accounts/logout/']")))
        elem.click()
        self.elem = self.wait.until( EC.presence_of_element_located((By.XPATH, "//a[@href='/accounts/login/']")))

    def getLoginPage(self, *args):
        if(len(args) < 2):
            driver = self.driver
            wait = self.wait
        else:
            driver = args[0]
            wait = args[1]
        # Handle registration for 1 or two drivers
        register = False;
        if(len(args) == 1 or len(args) == 3):
            register = True;
        # print(self.STARTING_URL)
        driver.get(self.STARTING_URL)

        # TODO Pull this when http basic authentication isn't needed for environments
        # Do to site security the href has to be manipulated to get around native dialogs
        href = None;
        if(register):
            href = "https://bluejet:letmein@" + self.DOMAIN + "/accounts/login/?tab=register"
        else:
            href = "https://bluejet:letmein@" + self.DOMAIN + "/accounts/login/"

        driver.execute_script( \
            "var elem = document.getElementsByClassName('mine-shaft-text')[0];" + \
            "elem.href='" + href + "';" + \
            "href = document.getElementsByClassName('mine-shaft-text')[0];"
            )
        print("href: " + str(href))
        # Get and click the login/signup link we modified the href for above
        # elem = wait.until( EC.presence_of_element_located((By.CSS_SELECTOR, ".home-top-link")))
        # elem.click()
        # Wait for page to load
        # self.waitForTimeout()
        wait.until( EC.presence_of_element_located((By.XPATH, "//a[@href = '" + str(href) + "']")))
        #wait.until( EC.visibility_of_element_located((By.XPATH, "//a[@href = '/accounts/login/?tab=register']")))
        return href



    def navigateToDashboard(self):
        try:
            elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fn-hover-menu.span-7")))
            hover = ActionChains(self.driver).move_to_element(elem)
            hover.perform()
            sere = None
        except StaleElementReferenceException as sere:
            # Just retrying around unexpected dom changes
            try:
                print(sere.msg)
                elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fn-hover-menu.span-7")))
                hover = ActionChains(self.driver).move_to_element(elem)
                hover.perform()
            except StaleElementReferenceException as sere:
                print(sere.msg)
                print(sere.msg)
                raise
        sleep(5);
        self.wait.until(EC.presence_of_element_located(( By.CSS_SELECTOR, "a[href='/']")))
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='/']"))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text() = 'Questions?']")))

        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Spread the Word']")))
        elems = self.driver.find_elements_by_tag_name("h1")

        self.verifyDashboardSections()

    def verifyDashboardSections(self, *args):
        if(len(args) > 0):
            driver = args[0]
            wait = args[1]
        else:
            driver = self.driver
            wait = self.wait
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Spread the Word']")))
        elems = driver.find_elements_by_tag_name("h1")
        if self.isTutoringOn:
            sectionHeaders = ["Your Dashboard.", "Spread the Word", "Questions?"]
        else:
            sectionHeaders = ["Spread the Word", "Questions?"]

        foundCount = 0;
        for elem in elems:
            for header in sectionHeaders:
                if(  header in elem.get_attribute("innerHTML")):
                    foundCount += 1;
                    break;
        self.assertTrue(foundCount == len(sectionHeaders),
                        "Not all section headers where found on the dashboard. sectionHaders: " + str(len(sectionHeaders)) +
                        "\nfoundCount: " + str(foundCount))

    @classmethod
    def report(cls):
        pass

    @classmethod
    def cleanUp(cls):
        pass





if __name__ == "__main__":
    browser = sys.argv[1]
    platform = sys.argv[2]
    unittest2.main()