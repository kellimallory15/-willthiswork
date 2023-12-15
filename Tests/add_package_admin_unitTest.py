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
        time.sleep(2)
        try:
            # Find and click the 'Account' button
            account_dropdown_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Account')]")
            account_dropdown_button.click()
            time.sleep(1)

            # Click the 'Login' button
            login_button = driver.find_element(By.LINK_TEXT, "Login")
            login_button.click()
            time.sleep(1)

            # Log into account
            user = "admin"
            pwd = "Mavericks1b"

            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")

            username_input.send_keys(user)
            password_input.send_keys(pwd)
            time.sleep(2)

            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()
            time.sleep(3)

            # Find and click the 'Packages' button
            packages_dropdown_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Packages')]")
            packages_dropdown_button.click()
            time.sleep(1)

            # Click the 'Add New Package' button
            add_new_package_button = driver.find_element(By.LINK_TEXT, "Add New Package")
            add_new_package_button.click()

            #Add a new package
            time.sleep(2)
            pkg_name = "Test Package"
            pkg_desc = "This is a description for the test package."
            pkg_price = "100"
            pkg_time = "1 hour"

            pkg_name_input = driver.find_element(By.ID, "id_name")
            pkg_desc_input = driver.find_element(By.ID, "id_description")
            pkg_price_input = driver.find_element(By.ID, "id_price")
            pkg_time_input =  driver.find_element(By.ID, "id_duration")

            pkg_name_input.send_keys(pkg_name)
            pkg_desc_input.send_keys(pkg_desc)
            pkg_price_input.send_keys(pkg_price)
            pkg_time_input.send_keys(pkg_time)
            time.sleep(5)

            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()
            time.sleep(5)

            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("Admin is unable to add a new package")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()