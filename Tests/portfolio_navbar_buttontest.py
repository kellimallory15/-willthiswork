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
            # Find the about button by link text
            portfolio_button = driver.find_element(By.LINK_TEXT, "Portfolio")

            # Click the home button
            portfolio_button.click()
            time.sleep(3)

            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("User is unable to press the 'Portfolio' button in the navbar and be taken to the 'Portfolio' page")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()