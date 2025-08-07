import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

def login_as_admin(driver):
    """
    Logs into a website as an admin with credentials stored in environment variables.
    
    :param driver: The Selenium WebDriver instance.
    """
    load_dotenv()
    username = os.getenv("MOODLE_ADMIN_USER")
    password = os.getenv("MOODLE_ADMIN_PASSWORD")

    # Locate the username and password fields and input the credentials
    driver.find_element(By.ID,"username").send_keys(username)
    driver.find_element(By.ID,"password").send_keys(password)

    # Submit the login form
    driver.find_element(By.ID,"loginbtn").click()