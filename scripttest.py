from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sqlite3
import os

url = "https://www.laposte.fr"
# url = "https://www.etudiant.gouv.fr/"

# --| Setup
if os.path.exists("C:\selenium\Default\Cookies"):
    os.remove("C:\selenium\Default\Cookies")

options = Options()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-cookie-encryption")
options.add_argument(r"user-data-dir=C:\selenium")
browser = webdriver.Chrome(executable_path=r'chromedriver.exe', options=options)
# browser = webdriver.Firefox(executable_path=r'geckodriver.exe')
browser.delete_all_cookies()

print("=================================")

con = sqlite3.connect(r'C:\selenium\Default\Cookies')
cur = con.cursor()
cur.execute("SELECT * FROM cookies")
rows = cur.fetchall()
con.close()

for row in rows:
    print("- {}".format(row))

for cookie in browser.get_cookies():
    print(cookie)
print("=================================")

# --| Parse or automation
browser.get(url)
browser.implicitly_wait(2)
try:
    cookieACK = browser.find_element_by_id("footer_tc_privacy_button")  # a generaliser
    cookieACK.click()
except Exception as e:
    print("ERROR : \n", e)

print(browser.get_cookies())

for cookie in browser.get_cookies():
    print(cookie)

time.sleep(20)

browser.close()

# --| DB
con = sqlite3.connect(r'C:\selenium\Default\Cookies')
cur = con.cursor()
cur.execute("SELECT * FROM cookies")
rows = cur.fetchall()

for row in rows:
    print("- {}".format(row))

