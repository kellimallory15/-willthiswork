import unittest
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_ll(self):
        driver = self.driver
        driver.maximize_window()

        driver.get("http://127.0.0.1:8000")
        time.sleep(3)
        try:
            # Find the home button by link text
            home_button = driver.find_element(By.LINK_TEXT, "Home")

            # Click the home button
            home_button.click()
            time.sleep(3)

            #Check the URL to ensure I'm still on the index page
            self.assertEqual(driver.current_url, "http://127.0.0.1:8000/")

            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("User is unable to press the 'Home' button in the navbar and be taken back to the index page")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()