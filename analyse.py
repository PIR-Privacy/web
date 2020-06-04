import re
import os
import shutil
import datetime

def listeRefactor(chaine):
    liste = []
    for elem in chaine:
        try:
            int(elem)
        except ValueError:
            newelem = re.sub(r"(\')|(\])|( )", "", elem)
            if newelem != "":
                liste.append(newelem)
        else:
            number = int(elem)
    return liste, number


resultList = []
maxNumberBeforeAccept = []
maxNumberAfterAccept = []
listAllDomainsBefore = []
listAllDomainsAfter = []
baseDomain = []

file = open("result/result.csv", "r")
file.readline()

if os.path.exists("result/analyseResult.txt"):
    shutil.copyfile("result/analyseResult.txt",
                    f"result/{datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}analyseResult.txt")
    os.remove("result/analyseResult.txt")

for line in file.readlines():
    field = line.split("[")
    name = field[0][:-2]
    domainsBeforeAccept, numberBeforeAccept = listeRefactor(field[1].split(","))
    domainsAfterAccept, numberAfterAccept = listeRefactor(field[2].split(","))

    resultList.append([name, domainsBeforeAccept, numberBeforeAccept, domainsAfterAccept, numberAfterAccept])
    listAllDomainsBefore += domainsBeforeAccept
    listAllDomainsAfter += domainsAfterAccept
    for domain in domainsAfterAccept + domainsBeforeAccept:
        if domain not in baseDomain:
            baseDomain.append(domain)

file.close()


def printAndWrite(txt):
    analyseResult = open("result/analyseResult.txt", "a")
    print(str(txt))
    analyseResult.write(str(txt) + "\n")


resultList = sorted(resultList, reverse=True, key=lambda e: e[2])
printAndWrite("---------Top 10 nombre de cookies avant accepter ------------")
for i in range(0, 10):
    printAndWrite(resultList[i][0])

resultList = sorted(resultList, reverse=True, key=lambda e: e[4])
printAndWrite("---------Top 10 nombre de cookies apres accepter ------------")
for i in range(0, 10):
    printAndWrite(resultList[i][0])

topDomainBefore = {}
topDomainAfter = {}

for value in baseDomain:
    topDomainBefore[value] = listAllDomainsBefore.count(value)
    topDomainAfter[value] = listAllDomainsAfter.count(value)

topDomainBefore = {k: v for k, v in sorted(topDomainBefore.items(), reverse=True, key=lambda item: item[1])}
topDomainAfter = {k: v for k, v in sorted(topDomainAfter.items(), reverse=True, key=lambda item: item[1])}

top10ExternDomainBefore = "---------Top 10 domain avant accepter ------------ \n"
top10ExternDomainAfter = "---------Top 10 domain apres accepter ------------ \n"
for i in range(0, 10):
    top10ExternDomainBefore += list(topDomainBefore)[i] \
                               + " : " \
                               + str(topDomainBefore[list(topDomainBefore)[i]]) \
                               + "/" \
                               + str(len(resultList)) \
                               + "\n"

    top10ExternDomainAfter += list(topDomainAfter)[i] \
                              + " : " \
                              + str(topDomainAfter[list(topDomainAfter)[i]]) \
                              + "/" \
                              + str(len(resultList)) \
                              + "\n"

printAndWrite(top10ExternDomainBefore)
printAndWrite(top10ExternDomainAfter)
