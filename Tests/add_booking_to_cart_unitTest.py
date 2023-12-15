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
            # Find and click the 'Bookings' button
            bookings_dropdown_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Bookings')]")
            bookings_dropdown_button.click()
            time.sleep(1)

            # Click the 'All Bookings' button
            all_bookings_button = driver.find_element(By.LINK_TEXT, "All Bookings")
            all_bookings_button.click()
            time.sleep(3)

            #add the first booking to cart
            add_to_cart_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/cart/?booking_id=')]")
            time.sleep(2)
            add_to_cart_links[0].click()
            time.sleep(3)

            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("User is unable to successfully add a booking to cart")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()