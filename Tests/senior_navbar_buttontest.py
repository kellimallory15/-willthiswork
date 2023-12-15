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
            # Find and click the 'Packages' button
            packages_dropdown_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Packages')]")
            packages_dropdown_button.click()
            time.sleep(1)

            # Click the 'Senior Portrait' button
            senior_portrait_button = driver.find_element(By.LINK_TEXT, "Senior Portrait")
            senior_portrait_button.click()

            time.sleep(3)

            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("User is unable to press the 'Senior Portrait' button in the navbar and be taken to the 'Senior Portrait' page")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()