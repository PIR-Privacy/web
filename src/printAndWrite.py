
def printAndWrite(path, txt):
    analyseResult = open(path, "a")
    print(str(txt))
    analyseResult.write(str(txt) + "\n")
    analyseResult.close()
