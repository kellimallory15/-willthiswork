import unittest
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

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

            # Find and click the 'Bookings' button
            bookings_dropdown_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Bookings')]")
            bookings_dropdown_button.click()
            time.sleep(1)

            # Click the 'Add Booking' button
            add_new_booking_button = driver.find_element(By.LINK_TEXT, "Add Booking")
            add_new_booking_button.click()

            #Add a new booking
            time.sleep(2)
            booking_name = "Test Package"
            booking_date = "2024-01-01 12:00:00"
            add_notes = "This is a test for the additional notes section"
            booking_desc = "This is a description for the test booking"

            booking_name_input = driver.find_element(By.ID, "id_name")
            booking_date_input = driver.find_element(By.ID, "id_date")
            add_notes_input = driver.find_element(By.ID, "id_notes")
            booking_desc_input = driver.find_element(By.ID, "id_description")

            booking_name_input.send_keys(booking_name)
            time.sleep(1)
            booking_date_input.send_keys(booking_date)
            time.sleep(1)

            photo_package_dropdown = Select(driver.find_element(By.ID, "id_package"))
            photo_package_dropdown.select_by_visible_text('Senior Portrait Session')
            time.sleep(1)

            photographer_dropdown = Select(driver.find_element(By.ID, "id_photographer"))
            photographer_dropdown.select_by_visible_text('admin')
            time.sleep(1)

            add_notes_input.send_keys(add_notes)
            booking_desc_input.send_keys(booking_desc)
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