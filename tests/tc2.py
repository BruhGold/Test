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

# Go to “<www->dataroot>/admin/settings.php?section=local_myplugin”
driver.get(f"{www_dataroot}/admin/settings.php?section=local_myplugin")
login_as_admin(driver)

# Input a valid DMOJ URL Where you are hosting it
form = driver.find_element(By.ID, "adminsettings")

dmoj_url_field = form.find_element(By.ID,"id_s_local_myplugin_dmoj_domain")
dmoj_url_field.clear()
dmoj_url_field.send_keys("https://dmoj.ca") # This is a real DMOJ URL that is not modified for the plugin

# Press “save change” 
save_button = form.find_element(By.TAG_NAME,"button")
save_button.click()
print("First save completed")

# Users beside admin shouldn't be generated in the database
# Old users should be unlinked
# Check if there are linked users in the database aside from admin
time.sleep(1)
print("checking database for users who are still linked")
with connect_to_moodle_database() as conn:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.username, u.email, u.firstname, u.lastname
        FROM mdl_user u
        WHERE u.deleted = 0 AND u.username <> 'guest' AND u.username <> 'admin' AND exists (
            SELECT 1 FROM mdl_myplugin_dmoj_users mdu WHERE mdu.moodle_user_id = u.id
        )
    """)
    users = cursor.fetchall()
    if users:
        print(bcolors.ERROR + "Users found unlinked in database:")
        for user in users:
            print(user[0],user[1])
        print(bcolors.ENDC)

    conn.close()

# The second time is to change the URL for repeatable tests
driver.get(f"{www_dataroot}/admin/settings.php?section=local_myplugin")
form = driver.find_element(By.ID, "adminsettings")

dmoj_url_field = form.find_element(By.ID,"id_s_local_myplugin_dmoj_domain")
dmoj_url_field.clear()
dmoj_url_field.send_keys("https://example.com")

save_button = form.find_element(By.TAG_NAME,"button")
save_button.click()
print("Second save completed")

driver.quit()