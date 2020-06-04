import re


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

resultList = sorted(resultList, reverse=True, key=lambda e: e[2])
print("---------Top 10 nombre de cookies avant accepter ------------")
for i in range(0, 10):
    print(resultList[i])

resultList = sorted(resultList, reverse=True, key=lambda e: e[4])
print("---------Top 10 nombre de cookies apres accepter ------------")
for i in range(0, 10):
    print(resultList[i])

topDomainBefore = {}
topDomainAfter = {}

for value in baseDomain:
    topDomainBefore[value] = listAllDomainsBefore.count(value)
    topDomainAfter[value] = listAllDomainsAfter.count(value)

topDomainBefore = {k: v for k, v in sorted(topDomainBefore.items(), reverse=True, key=lambda item: item[1])}
topDomainAfter = {k: v for k, v in sorted(topDomainAfter.items(), reverse=True, key=lambda item: item[1])}

top10ExternDomainBefore = "---------Top 10 3rd party domain before ------------ \n"
top10ExternDomainAfter = "---------Top 10 3rd party domain after ------------ \n"
for i in range(0, 10):
    top10ExternDomainBefore += list(topDomainBefore)[i] + "\n"
    top10ExternDomainAfter += list(topDomainAfter)[i] + "\n"

print(top10ExternDomainBefore)
print(top10ExternDomainAfter)
