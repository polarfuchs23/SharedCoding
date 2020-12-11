import math

def writeFile(name,string):
    with open(name,'a') as file:
        file.writelines(string)


def readFile(name):
    with open(name,'r') as file:
        return file.read()

def readFileHex(name):
    with open(name,'rb') as file:
        return file.read().hex

def readFileLines(name):
    with open(name,'r') as file:
        return file.read().split("\n")


fileContent = readFile("file.test")

writeFile("file.test","a")

if fileContent == readFile("file.test"):
    print("same")
else:
    print("different")

