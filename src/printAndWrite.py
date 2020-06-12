
def printAndWrite(path, txt):
    with open(path, "a") as analyseResult:
        print(str(txt))
        analyseResult.write(str(txt) + "\n")
