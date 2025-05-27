from selenium.webdriver.common.by import By  # For locating web elements
from selenium.webdriver.common.action_chains import ActionChains  # For mouse hover actions

class DashboardPage:
    """
    Page Object Model class for interacting with the OrangeHRM Dashboard page.
    Handles navigation to modules and logout functionality.
    """

    def __init__(self, driver):
        """
        Constructor that takes a WebDriver instance and assigns it to the class.
        """
        self.driver = driver

    def go_to_pim(self):
        """
        Navigates to the PIM module by hovering and clicking on the PIM menu item.
        """
        # Locate the PIM menu item on the dashboard
        pim_menu = self.driver.find_element(By.XPATH, "//span[text()='PIM']")

        # Use ActionChains to hover over and click the PIM menu
        ActionChains(self.driver).move_to_element(pim_menu).click().perform()

    def logout(self):
        """
        Logs out of the OrangeHRM application from the dashboard.
        """
        # Locate and click on the user profile dropdown
        profile = self.driver.find_element(By.CLASS_NAME, "oxd-userdropdown-tab")
        profile.click()

        # Click on the 'Logout' option from the dropdown
        self.driver.find_element(By.XPATH, "//a[text()='Logout']").click()
