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

            # Find and click the 'Account' button
            account_dropdown_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Account')]")
            account_dropdown_button.click()
            time.sleep(1)

            # Click the 'Admin Dashboard' button
            admin_dashboard_link = driver.find_element(By.LINK_TEXT, "Admin Dashboard")
            admin_dashboard_link.click()
            time.sleep(3)

            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("User is unable to login to their account and/or access the Admin Dashboard button")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()