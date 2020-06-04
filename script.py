from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import re
import sqlite3
import os
import time

from urlChecker import urlChecker

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
if not os.path.exists("result/result.csv"):
    result = open("result/result.csv", "w")
    result.write("name, domainsBeforeAccept, numberBeforeAccept, numberAfterAccept, domainsAfterAccept\n")
    result.close()

isClicked = True


def clickAccept(typeElem, liste, brw):
    global isClicked
    if isClicked:
        for name in liste:
            try:
                if typeElem == "class":
                    cookieAccept = brw.find_element_by_class_name(name)
                elif typeElem == "id":
                    cookieAccept = brw.find_element_by_id(name)
                elif typeElem == "xpath":
                    cookieAccept = brw.find_element_by_xpath(name)
                print(cookieAccept)
                cookieAccept.click()
                isClicked = False
                break
            except Exception as exception:
                print("ERROR : ", exception, "\n")


def resultFileName(URL):
    currentUrlWhitoutHTTP = re.sub('(http://)|(https://)', '', URL)
    currentUrlWhitoutHTTP = re.sub('(/)|(&)|(=)|(\?)', '_', currentUrlWhitoutHTTP)
    return currentUrlWhitoutHTTP


def collectCookie(browsingUrl, cookiesCounter, cookiesList, brw, accept_noAccept):
    # Cookie brut in txt file
    cookieFile = open("result/" + resultFileName(browsingUrl) + "_" + accept_noAccept + ".csv", "w")
    cookieFile.write("name, domain, expiry, path, httpOnly, secure \n")
    dateTime = int(time.time())

    for cookie in brw.get_cookies():
        cookiesCounter += 1
        if str(cookie["domain"]) not in cookiesList:
            cookiesList.append(str(cookie["domain"]))
        expiry = str(cookie.get("expiry"))
        cookieFile.write(f'{str(cookie["name"])}, {str(cookie["domain"])}, '
                         f'{"0" if (expiry is None or expiry == "None") else str(int(expiry) - dateTime)}, '
                         f'{str(cookie["path"])}, {str(cookie["httpOnly"])}, {str(cookie["secure"])}  \n')
    brw.close()

    # Connexion a la BDD de chrome pour récuperer les cookies
    con = sqlite3.connect(r'C:\selenium\Default\Cookies')
    cur = con.cursor()
    cur.execute("SELECT * FROM cookies")
    rows = cur.fetchall()
    for row in rows:
        cookiesCounter += 1
        if str(row[1]) not in cookiesList:
            cookiesList.append(str(row[1]))
        cookieFile.write(f'{str(row[2])}, {str(row[1])}, '
                         f'{"0" if row[5] == 0 else str(int((row[5] - row[0]) / 1000000))}, '
                         f'{str(row[4])}, {"True" if row[7] == 1 else "False"}, '
                         f'{"True" if row[6] == 1 else "False"} \n')
    con.close()
    cookieFile.close()
    return cookiesCounter, cookiesList


for field in urlDatabase.split('\n'):
    for url in re.findall(urlRegex, field):
        currentUrl = url[0]

        if currentUrl not in previousUrl:

            if (os.path.exists(f"result/{resultFileName(currentUrl)}_noAccept.csv")
                    and os.path.exists(f"result/{resultFileName(currentUrl)}_accept.csv")):
                print(currentUrl + " : aborted, report exist")
                continue

            print("Work in progress :" + currentUrl)
            if not urlChecker(currentUrl):
                notWorkingLog = open("result/urlNotWorking.log", "a")
                notWorkingLog.write(currentUrl + "\n")
                notWorkingLog.close()
                continue

            resultLine = open("result/result.csv", "a")

            time.sleep(5)
            if os.path.exists("C:\selenium\Default\Cookies"):
                try:
                    os.remove("C:\selenium\Default\Cookies")
                except Exception as e:
                    # message de notification via mail ou sms
                    raise e
            browser = webdriver.Chrome(executable_path=r'chromedriver.exe', options=options, )
            browser.delete_all_cookies()
            browser.get(currentUrl)
            browser.implicitly_wait(5)
            if ("404" or "403") in browser.title:
                browser.close()
                continue

            cookieNumberBefore, domainsBefore = collectCookie(currentUrl, 0, [], browser, "noAccept")

            # Generalisation du click sur accepter
            browserAccept = webdriver.Chrome(executable_path=r'chromedriver.exe', options=options, )
            browserAccept.delete_all_cookies()
            browserAccept.get(currentUrl)
            browserAccept.implicitly_wait(5)

            isClicked = True

            classButton = ["agree-button",
                           "eu-cookie-compliance-secondary-button",
                           "optanon-allow-all",
                           "accept-cookies-button",
                           "agree-button",
                           "eu-cookie-compliance-default-button",
                           "agree-button",
                           "cb-enable",
                           "close",
                           "alert-close-btn",
                           "ct-icon-cancel",
                           "alert-cnil_close",
                           "close-panel",
                           "cc-btn",
                           "cn-set-cookie",
                           "cc_btn ",
                           "cookieClose",
                           "cookieButton",
                           "popup-modal-dismiss",
                           "valideCNILCookie",
                           "safe",
                           "accept",
                           "wordpress-gdpr-popup-agree",
                           "button_button--lgX0P",
                           "cicb_fermer",
                           "close-button",
                           "gdpr-agreement",
                           "cookiebanner-close",
                           ]

            idButton = ["footer_tc_privacy_button",
                        "cb-enable",
                        "CBhide",
                        "tarteaucitronPersonalize",
                        "tx-anil-cookieconsent-close",
                        "cn-accept-cookie",
                        " footer_tc_privacy_button",
                        "cookie-close",
                        "CybotCookiebotDialogBodyLevelButtonAccept",
                        "epdsubmit",
                        "cookie_action_close_header",
                        "cookieChoiceDismiss",
                        "impliedsubmit",
                        "cnilAccept",
                        ]

            xpathButton = ["//button[contains(text(),'ok')]",
                           "//button[contains(text(),'OK')]",
                           "//button[contains(text(),'Ok')]",
                           "//button[contains(text(),'accepter')]",
                           "//button[contains(text(),'Accepter')]",
                           "//button[contains(text(),'Autoriser')]",
                           "//button[contains(text(),'autoriser')]",
                           "//button[contains(text(),'cookie')]",
                           "//button[contains(text(),'Cookie')]",
                           "//button[contains(text(),'cookies')]",
                           "//button[contains(text(),'Cookies')]",
                           "//button[contains(text(),'oui')]",
                           "//button[contains(text(),'Oui')]",
                           "// button[contains(text(), 'Valider')]",
                           "//a[contains(text(),'accepter')]",
                           "//a[contains(text(),'Accepter')]",
                           "//a[contains(text(),'accepte')]",
                           "//a[contains(text(),'Accepte')]",
                           "//a[contains(text(),'Autoriser')]",
                           "//a[contains(text(),'autoriser')]",
                           "//a[contains(text(),'cookie')]",
                           "//a[contains(text(),'Cookie')]",
                           "//a[contains(text(),'cookies')]",
                           "//a[contains(text(),'Cookies')]",
                           "//a[contains(text(),'oui')]",
                           "//a[contains(text(),'Oui')]",
                           ]

            try:
                fermer = browserAccept.find_element_by_class_name("dismiss")
                fermer.click()
            except Exception as e:
                print("no alert : ", e)

            try:
                fermer = browserAccept.find_element_by_id("closeBtn")
                fermer.click()
            except Exception as e:
                print("no alert : ", e)

            clickAccept("class", classButton, browserAccept)
            clickAccept("id", idButton, browserAccept)
            clickAccept("xpath", xpathButton, browserAccept)

            # Traitement des cookies
            cookieNumberAfter, domainsAfter = collectCookie(currentUrl, 0, [], browserAccept, "accept")

            if isClicked:
                log = open("result/error.log", "a")
                log.write(currentUrl + "\n")
                log.close()

            resultLine.write(
                f'{currentUrl}, {domainsBefore}, {cookieNumberBefore}, {domainsAfter}, {cookieNumberAfter} \n')
            resultLine.close()

            previousUrl.append(currentUrl)
