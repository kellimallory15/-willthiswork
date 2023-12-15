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
            # Find the 'Family Package' section first
            family_package_section = driver.find_element(By.XPATH,
                                                         "//h2[contains(., '02. Family Package')]/ancestor::section")

            # Within this section, find the 'Book Now' button and click it
            book_now_button = family_package_section.find_element(By.XPATH, ".//button[span[contains(., 'Book Now')]]")
            book_now_button.click()
            time.sleep(3)
            assert True


        except NoSuchElementException:
            driver.close()
            self.fail("User is unable to press the 'Book Now' button from the Family Package section")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()