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
        user = "admin"
        pwd = "Mavericks1b"
        driver.get("http://127.0.0.1:8000/admin")
        time.sleep(2)  # Ensure the page has loaded

        # Login
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        elem.submit()
        time.sleep(2)

        try:
            # Go to the Packages section
            driver.find_element(By.XPATH, "//a[contains(., 'My Packages')]").click()
            time.sleep(2)  # Ensure the Packages page has loaded

            # Click on 'Add package'
            driver.find_element(By.LINK_TEXT, "ADD MY PACKAGE").click()
            time.sleep(2)

            # Fill out the form for the new package
            pkg_name = "Test Package"
            pkg_desc = "This is a description for the test package"
            pkg_price = "100.0"
            pkg_time = "1 hour"

            # Locate form fields and populate them with data
            pkg_name_input = driver.find_element(By.NAME, "name")
            pkg_desc_input = driver.find_element(By.NAME, "description")
            pkg_price_input = driver.find_element(By.NAME, "price")
            pkg_time_input = driver.find_element(By.NAME, "duration")

            pkg_name_input.send_keys(pkg_name)
            pkg_desc_input.send_keys(pkg_desc)
            pkg_price_input.send_keys(pkg_price)
            pkg_time_input.send_keys(pkg_time)
            time.sleep(2)

            # Submit the form
            submit_button = driver.find_element(By.NAME, "_save")
            submit_button.click()
            time.sleep(2)

            assert True

        except NoSuchElementException as e:
            driver.close()
            self.fail("User is unable to add a package from the admin backend page")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
