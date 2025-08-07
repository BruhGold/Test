import os
import sys
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database import connect_to_moodle_database, bcolors
from utils.login import login_as_admin

load_dotenv()

www_dataroot = os.getenv("MOODLE_WWW_DATAROOT")
service = webdriver.ChromeService(executable_path=os.getenv("CHROMEDRIVER_PATH"))
driver = webdriver.Chrome(service=service)
# Go to “<www->dataroot>/admin/user.php”
driver.get(f"{www_dataroot}/admin/user.php")

# this require admin
login_as_admin(driver)

# get delete button
delete_buttons = driver.find_elements(By.XPATH, "//a[i[@aria-label='Delete']]")

print(bcolors.OKGREEN + "Found delete buttons for users:" + bcolors.ENDC)
for button in delete_buttons:
    print(button.get_attribute("href").split("&delete=")[-1].split("&")[0])

delete_button = delete_buttons[0] if delete_buttons else None
id = None
if delete_button:
    id = delete_button.get_attribute("href").split("&delete=")[-1].split("&")[0]
    print(f"Deleting user with ID: {id}")
    delete_button.click()
    driver.implicitly_wait(5)
    confirm_button = driver.find_element(By.XPATH, "//div[@id='modal-footer']//button[@type='submit']")
    confirm_button.click()
    print("User deleted successfully.")

    # check the database user removed in the database table mdl_myplugin_dmoj_users
    with connect_to_moodle_database() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT mdu.*
            FROM mdl_user u
            JOIN mdl_myplugin_dmoj_users mdu ON u.id = mdu.moodle_user_id
            WHERE u.id = ?
        """, (id,))
        user = cursor.fetchone()
        if user:
            print(bcolors.ERROR + f"User {id} still exists in the database table mdl_myplugin_dmoj_users" + bcolors.ENDC)
        else:
            print(bcolors.OKGREEN + "User successfully removed from the database" + bcolors.ENDC)
else:
    print(bcolors.WARNING + "No delete button found for any user" + bcolors.ENDC)
driver.quit()