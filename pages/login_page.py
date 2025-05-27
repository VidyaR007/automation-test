from selenium.webdriver.common.by import By  # Import the By class to locate web elements

class LoginPage:
    """
    Page Object Model class for interacting with the OrangeHRM login page.
    """

    def __init__(self, driver):
        """
        Constructor that takes a WebDriver instance and assigns it to the class.
        This driver will be used to interact with web elements.
        """
        self.driver = driver

    def login(self, username, password):
        """
        Logs into the OrangeHRM application using the provided username and password.
        """
        # Locate the username input field and enter the username
        self.driver.find_element(By.NAME, "username").send_keys(username)

        # Locate the password input field and enter the password
        self.driver.find_element(By.NAME, "password").send_keys(password)

        # Locate the login button and click it to submit the credentials
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
