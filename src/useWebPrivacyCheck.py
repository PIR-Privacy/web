import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import src
from src import verifFile, resultFilename, urlChecker

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os
import re

webprivacycheckURL = "https://webprivacycheck.plehn-media.de/en"
urlRegex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
urlDatabase = open("../export-ITM_URL_2013-10-14.csv", "r", encoding="utf-8").read()
previousUrl = []

options = Options()
options.add_argument(r"user-data-dir=C:\selenium")

src.verifFile.verif("../result/result.csv",
                    "name;"
                    "First-party cookies number; "
                    "First-party cookies domains; "
                    "Third-party cookies number; "
                    "Third-party cookies domains; "
                    "Third-party requests number; "
                    "Third-party requests domains \n")

src.verifFile.verif("../result/urlNotWorking.log",
                    "Url with 404 or 403 error \n")

src.verifFile.verif("../result/error.log",
                    "url dont il y a eu un probleme avec l'analyse \n")

browser = webdriver.Chrome(executable_path=r'../lib/chromedriver.exe', options=options, )
browser.get(webprivacycheckURL)
browser.implicitly_wait(5)

for field in urlDatabase.split('\n'):
    for url in re.findall(urlRegex, field):
        currentURL = url[0]
        if currentURL not in previousUrl:
            if os.path.exists(f"../result/{src.resultFilename.resultFileName(currentURL)}.csv"):
                print("Aborted, report exist for : " + currentURL)
                continue
            else:
                print("Work in progress : " + currentURL)
                if not src.urlChecker.urlChecker(currentURL):
                    with open("../result/urlNotWorking.log", "a") as notWorkingLog:
                        notWorkingLog.write(currentURL + "\n")
                        continue
                else:
                    with open("../result/result.csv", "a") as resultLine:
                        browser.find_element_by_name("url").send_keys(currentURL + Keys.ENTER)
                        try:
                            WebDriverWait(browser, 60) \
                                .until(EC.presence_of_all_elements_located((By.CLASS_NAME, "light")))
                        except selenium.common.exceptions.TimeoutException as e:
                            try:
                                browser.find_element_by_xpath("//a[contains(text(),'Try again?')]")
                                WebDriverWait(browser, 60) \
                                    .until(EC.presence_of_all_elements_located((By.CLASS_NAME, "light")))
                            except Exception as e:
                                with open("../result/error.log", "a") as errorLog:
                                    print("Something went wrong")
                                    errorLog.write(currentURL + '\n')
                                    continue

                        firstPartyCookieList = []
                        thirdpartyCookieList = []
                        thirdpartyRequestsList = []

                        with open(f"../result/{src.resultFilename.resultFileName(currentURL)}.csv",
                                  "w") as currentResult:
                            currentResult.write("Domain, Name, Expires on \n")
                            data = browser.find_elements_by_class_name("cookies")

                            try:
                                cookiesNumbers = browser.find_elements_by_css_selector('#cookies + p > strong')
                            except selenium.common.exceptions.NoSuchElementException as e:
                                cookiesNumbers = []
                                print(e)

                            try:
                                firstPartyCookieNumber = cookiesNumbers[0].text
                            except IndexError as e:
                                firstPartyCookieNumber = 0

                            try:
                                thirdpartyCookieNumber = cookiesNumbers[1].text
                            except IndexError as e:
                                thirdpartyCookieNumber = 0

                            try:
                                requestsNumber = browser.find_elements_by_css_selector("#requests+ p > strong")
                            except selenium.common.exceptions.NoSuchElementException as e:
                                requestsNumber = []
                                print(e)

                            try:
                                thirdpartyRequestsNumber = requestsNumber[0].text
                            except IndexError as e:
                                thirdpartyRequestsNumber = 0

                            try:
                                if data[0]:
                                    currentResult.write(f"\n ======== First-party cookies "
                                                        f"({firstPartyCookieNumber}) "
                                                        f"========\n")
                                    for cookie in data[0].find_elements_by_tag_name("tr")[1:]:
                                        cookieData = cookie.find_elements_by_tag_name("td")
                                        currentResult.write(f"{cookieData[0].text}; "
                                                            f"{cookieData[1].text}; "
                                                            f"{cookieData[3].text} \n")

                                        if cookieData[0].text not in firstPartyCookieList:
                                            firstPartyCookieList.append(cookieData[0].text)
                            except IndexError as e:
                                currentResult.write(f"\n ======== First-party cookies "
                                                    f"({firstPartyCookieNumber}) "
                                                    f"========\n")
                                print("No First-party cookie")

                            try:
                                if data[1]:
                                    currentResult.write(f"\n ======== Third-party cookies "
                                                        f"({thirdpartyCookieNumber}) "
                                                        f"========\n")
                                    for cookie in data[1].find_elements_by_tag_name("tr")[1:]:
                                        cookieData = cookie.find_elements_by_tag_name("td")
                                        currentResult.write(f"{cookieData[0].text}; "
                                                            f"{cookieData[1].text}; "
                                                            f"{cookieData[3].text} \n")

                                        if cookieData[0].text not in thirdpartyCookieList:
                                            thirdpartyCookieList.append(cookieData[0].text)
                            except IndexError as e:
                                currentResult.write(f"\n ======== Third-party cookies "
                                                    f"({thirdpartyCookieNumber}) "
                                                    f"========\n")
                                print("No third-party cookie")

                            try:
                                requestData = browser.find_element_by_class_name("requests")
                                if requestData:
                                    currentResult.write(f"\n ======== Third-party requests "
                                                        f" ({thirdpartyRequestsNumber}) "
                                                        f"========\n"
                                                        f"Host; Classification \n")
                                    for request in requestData.find_elements_by_tag_name("tr")[1:]:
                                        requestField = request.find_elements_by_tag_name("td")
                                        currentResult.write(f"{requestField[0].text}; "
                                                            f"{requestField[1].text} \n")

                                        thirdpartyRequestsList.append(requestField[0].text)
                            except selenium.common.exceptions.NoSuchElementException as e:
                                print("No third-party requests")

                        resultLine.write(f"{currentURL}; "
                                         f"{firstPartyCookieNumber}; "
                                         f"{firstPartyCookieList}; "
                                         f"{thirdpartyCookieNumber}; "
                                         f"{thirdpartyCookieList}; "
                                         f"{thirdpartyRequestsNumber}; "
                                         f"{thirdpartyRequestsList} \n"
                                         )
                        print("Finished")
            previousUrl.append(currentURL)

browser.quit()
