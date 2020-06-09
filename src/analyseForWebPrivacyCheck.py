import os
import shutil
import datetime
import re

import src
from src import printAndWrite


if os.path.exists("../result/analyseResult.txt"):
    shutil.copyfile("../result/analyseResult.txt",
                    f"../result/{datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}analyseResult.txt")
    analyseResult = open("../result/analyseResult.txt", "w")
    analyseResult.close()

resultList = []


with open("../result/result.csv", "r") as resultFile:
    resultFile.readline()

    regexClearDomain = r"(\')|(\])|(\[)|( )|(\n)"
    for line in resultFile.readlines():
        field = line.split(";")
        resultList.append([field[0],
                           1 if field[1] == " One" else int(field[1]),
                           [re.sub(regexClearDomain, "", domain) for domain in field[2].split(",")],
                           1 if field[3] == " One" else int(field[3]),
                           [re.sub(regexClearDomain, "", domain) for domain in field[4].split(",")],
                           1 if field[5] == " One" else int(field[5]),
                           [re.sub(regexClearDomain, "", domain) for domain in field[6].split(",")],
                           ])


resultList = sorted(resultList, reverse=True, key=lambda e: e[1])
src.printAndWrite.printAndWrite("../result/analyseResult.txt",
                                "---------Top 10 First-party cookies number ------------")
try:
    for i in range(0, 10):
        src.printAndWrite.printAndWrite("../result/analyseResult.txt",
                                        resultList[i][0])
except IndexError:
    pass
print(resultList)

resultList = sorted(resultList, reverse=True, key=lambda e: e[3])
src.printAndWrite.printAndWrite("../result/analyseResult.txt",
                                "---------Top 10 Third-party cookies number ------------")
try:
    for i in range(0, 10):
        src.printAndWrite.printAndWrite("../result/analyseResult.txt",
                                        resultList[i][0])
except IndexError:
    pass

resultList = sorted(resultList, reverse=True, key=lambda e: e[5])
src.printAndWrite.printAndWrite("../result/analyseResult.txt",
                                "---------Top 10 Third-party requests number ------------")
try:
    for i in range(0, 10):
        src.printAndWrite.printAndWrite("../result/analyseResult.txt",
                                        resultList[i][0])
except IndexError:
    pass

topFirstPartyCookieDomain = {}
topThirdPartyCookieDomain = {}
topThirdPartyRequestsDomain = {}


def doDict(domainList, domainDict):
    for domain in domainList:
        if domain in domainDict:
            domainDict[domain] += 1
        else:
            domainDict[domain] = 1


for value in resultList:
    if value[2] != ['']:
        doDict(value[2], topFirstPartyCookieDomain)
    if value[4] != ['']:
        doDict(value[4], topThirdPartyCookieDomain)
    if value[6] != ['']:
        doDict(value[6], topThirdPartyRequestsDomain)

topFirstPartyCookieDomain = {k: v for k, v in
                             sorted(topFirstPartyCookieDomain.items(), reverse=True, key=lambda item: item[1])}
topThirdPartyCookieDomain = {k: v for k, v in
                             sorted(topThirdPartyCookieDomain.items(), reverse=True, key=lambda item: item[1])}
topThirdPartyRequestsDomain = {k: v for k, v in
                               sorted(topThirdPartyRequestsDomain.items(), reverse=True, key=lambda item: item[1])}

top10FirstPartyCookie = "---------Top 10 First-party cookies domain ------------ \n"
top10ThirdPartyCookie = "---------Top 10 Third-party cookies domain ------------ \n"
top10ThirdPartyRequests = "---------Top 10 Third-party requests domain ------------ \n"
try:
    for i in range(0, 10):
        top10FirstPartyCookie += list(topFirstPartyCookieDomain)[i] \
                                   + " : " \
                                   + str(topFirstPartyCookieDomain[list(topFirstPartyCookieDomain)[i]]) \
                                   + "/" \
                                   + str(len(resultList)) \
                                   + "\n"

        top10ThirdPartyCookie += list(topThirdPartyCookieDomain)[i] \
                                  + " : " \
                                  + str(topThirdPartyCookieDomain[list(topThirdPartyCookieDomain)[i]]) \
                                  + "/" \
                                  + str(len(resultList)) \
                                  + "\n"

        top10ThirdPartyRequests += list(topThirdPartyRequestsDomain)[i] \
                                 + " : " \
                                 + str(topThirdPartyRequestsDomain[list(topThirdPartyRequestsDomain)[i]]) \
                                 + "/" \
                                 + str(len(resultList)) \
                                 + "\n"
except IndexError:
    pass

src.printAndWrite.printAndWrite("../result/analyseResult.txt",
                                top10FirstPartyCookie)
src.printAndWrite.printAndWrite("../result/analyseResult.txt",
                                top10ThirdPartyCookie)
src.printAndWrite.printAndWrite("../result/analyseResult.txt",
                                top10ThirdPartyRequests)

