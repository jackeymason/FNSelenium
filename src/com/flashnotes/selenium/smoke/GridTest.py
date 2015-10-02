# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest
import sys
from time import sleep

class GridTest(unittest.TestCase):


    def setUp(self):
        self.driver = webdriver.Remote(desired_capabilities={
            "browserName": "safari",
            "platform": "mac"

        })

    def test_example(self):
        self.driver.get("http://www.google.com")
        self.assertEqual(self.driver.title, "Google")
        sleep(3);

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
