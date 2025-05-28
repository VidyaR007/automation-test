from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# Configure logger
logger = logging.getLogger("Automation")

class PIMPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def click_add_employee(self):
        self.driver.find_element(By.LINK_TEXT, "Add Employee").click()

    def add_employee(self, first_name, last_name):
        self.driver.find_element(By.NAME, "firstName").send_keys(first_name)
        self.driver.find_element(By.NAME, "lastName").send_keys(last_name)

        # Wait for any loading overlay to disappear
        self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "oxd-form-loader")))

        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        submit_button.click()

    def go_to_employee_list(self):
        self.driver.find_element(By.LINK_TEXT, "Employee List").click()

    def search_employee_by_name(self, full_name):
        try:
            search_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Type for hints...']")

            # Clear input reliably
            search_input.click()
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.DELETE)

            # Enter the full employee name (e.g., "John Smith")
            search_input.send_keys(full_name)

            # Click Search button
            self.driver.find_element(By.XPATH, "//button[normalize-space()='Search']").click()

            # Wait until the search results container is present
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='rowgroup']")))

            # Small sleep to allow rendering
            time.sleep(1)

            # Get all employee rows
            rows = self.driver.find_elements(By.XPATH, "//div[@role='row']")

            for row in rows:
                # Assuming first name is in 3rd div, last name in 4th div inside each row
                first_name_el = row.find_element(By.XPATH, ".//div[3]")
                last_name_el = row.find_element(By.XPATH, ".//div[4]")

                employee_full_name = (first_name_el.text + " " + last_name_el.text).strip()

                # Case-insensitive exact match
                if full_name.strip().lower() == employee_full_name.lower():
                    return True

            logger.info(f"Employee '{full_name}' NOT found.")
            return False

        except Exception as e:
            logger.info(f"Error while searching employee '{full_name}': {e}")
            return False