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
# Go to “<www->dataroot>/user/editadvanced.php?id=-1"
driver.get(f"{www_dataroot}/user/editadvanced.php?id=-1")

# this require admin
login_as_admin(driver)

# Input a required fields
# username
username = f"test{time.time()}"
driver.find_element(By.ID, "id_username").send_keys(username)
# password
driver.find_element(By.XPATH, "//span[@data-passwordunmask='displayvalue']/span/em").click()
driver.implicitly_wait(5)
driver.find_element(By.ID, "id_newpassword").send_keys("Golly!1234")
# firstname
driver.find_element(By.ID, "id_firstname").send_keys("test")
# surname
driver.find_element(By.ID, "id_lastname").send_keys("user")
# email
driver.find_element(By.ID, "id_email").send_keys(f"testuser{time.time()}@example.com")
# Press "create user"
driver.find_element(By.ID, "id_submitbutton").click()

# check if the user is linked in the database "mdl_myplugin_dmoj_users"
print(f"checking {username}")
with connect_to_moodle_database() as conn:
    cursor = conn.cursor()
    data = cursor.execute("""
        SELECT mdu.*
        FROM mdl_user u
        JOIN mdl_myplugin_dmoj_users mdu ON u.id = mdu.moodle_user_id
        WHERE u.username = ?
    """, (username,))
    user = cursor.fetchone()
    if user:
        print(bcolors.OKGREEN + f"User successfully linked in the database table mdl_myplugin_dmoj_users {data}" + bcolors.ENDC)
    else:
        print(bcolors.ERROR + f"User {username} not found in the database table mdl_myplugin_dmoj_users" + bcolors.ENDC)

driver.quit()