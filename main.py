import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PIMPage
import logging

# Configure logging to display INFO and higher level messages with timestamps and level info
logging.basicConfig(
    level=logging.INFO,  # Minimum log level to show
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create a logger object for this module
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting OrangeHRM automation workflow.")

    # Setup ChromeDriver service using WebDriverManager to automatically handle driver binaries
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Maximize browser window for consistent UI layout
    driver.maximize_window()

    # Set implicit wait for element searches to handle dynamic page loading
    driver.implicitly_wait(10)

    try:
        # Navigate to OrangeHRM login page
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

        # Instantiate page objects with the driver
        login = LoginPage(driver)
        dashboard = DashboardPage(driver)
        pim = PIMPage(driver)

        logger.info("Logging in as Admin.")
        # Perform login using provided credentials
        login.login("Admin", "admin123")
        logger.info("Login successful.")

        logger.info("Navigating to PIM module.")
        # From the dashboard, navigate to the PIM module
        dashboard.go_to_pim()

        # Define a list of employees to add, each with first and last name
        employees = [
            {"first": "Alice", "last": "Johnson"},
            {"first": "Bob", "last": "Smith"},
            {"first": "Charlie", "last": "Brown"},
            {"first": "Diana", "last": "Miller"}
        ]

        # List to keep track of the full names of added employees
        added_employee_names = []

        # Loop through each employee and add them via the PIM page
        for emp in employees:
            logger.info(f"Adding employee: {emp['first']} {emp['last']}")
            pim.click_add_employee()  # Navigate to Add Employee form
            time.sleep(1)  # Small pause to allow form to load
            pim.add_employee(emp['first'], emp['last'])  # Fill form and submit
            added_employee_names.append(f"{emp['first']} {emp['last']}")  # Store full name
            time.sleep(1)  # Pause to allow processing

        logger.info("All employees added. Verifying in Employee List...")

        # Navigate to Employee List page to verify additions
        pim.go_to_employee_list()
        time.sleep(2)  # Wait for list to load

        successfully_verified = []

        # Search and verify each added employee in the Employee List
        for full_name in added_employee_names:
            logger.info(f"Searching for employee: {full_name}")
            found = pim.search_employee_by_name(full_name)
            if found:
                logger.info(f"{full_name} successfully verified in Employee List.")
                successfully_verified.append(full_name)
            else:
                logger.warning(f"{full_name} NOT found in Employee List.")

        # Final verification summary
        if len(successfully_verified) == len(added_employee_names):
            logger.info("All employees successfully verified!")
        else:
            logger.warning("Some employees could not be verified.")

        logger.info("Logging out.")
        # Logout from the application via dashboard page
        dashboard.logout()
        logger.info("Logout successful.")

    except Exception as e:
        # Log any exception that causes the test to fail
        logger.error(f"Test failed due to exception: {e}")

    finally:
        # Ensure the browser is closed in all cases to free resources
        logger.info("Closing browser.")
        driver.quit()


# Run the main function when script is executed directly
if __name__ == "__main__":
    main()
