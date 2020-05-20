from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import re
import sqlite3
import os
import time

# Current directory
currentDir = os.getcwd()

# Variable pour le traitement de la database de data.gouv.fr
# https://www.data.gouv.fr/fr/datasets/liste-des-applications-et-des-versions-mobiles-des-sites-internet-publics/#_
urlRegex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
urlDatabase = open("export-ITM_URL_2013-10-14.csv", "r", encoding="utf-8").read()
previousUrl = []

# Options pour le navigateur
options = Options()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-cookie-encryption")
options.add_argument(r"user-data-dir=C:\selenium")

# Database avec analyse


for field in urlDatabase.split('\n'):
    for url in re.findall(urlRegex, field):
        currentUrl = url[0]
        if currentUrl not in previousUrl:
            print("Work in progress :" + currentUrl)
            if os.path.exists("C:\selenium\Default\Cookies"):
                os.remove("C:\selenium\Default\Cookies")
            browser = webdriver.Chrome(executable_path=r'chromedriver.exe', options=options)
            browser.delete_all_cookies()
            browser.get(currentUrl)
            browser.implicitly_wait(2)
            # Cookie brut in txt file
            currentUrlWhitoutHTTP = re.sub('(http://)|(https://)','', currentUrl)
            cookieFile = open("result/" + currentUrlWhitoutHTTP + ".txt", "w")
            for cookie in browser.get_cookies():
                cookieFile.write(str(cookie) + "\n")
            time.sleep(5)
            browser.close()
            # Connexion a la BDD de chrome pour récuperer les cookies
            con = sqlite3.connect(r'C:\selenium\Default\Cookies')
            cur = con.cursor()
            cur.execute("SELECT * FROM cookies")
            rows = cur.fetchall()
            for row in rows:
                cookieFile.write(str(row) + "\n")
            con.close()
            cookieFile.close()

            # Generalisation du clic sur accepter

        previousUrl.append(currentUrl)
