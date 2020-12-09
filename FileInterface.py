import math

def appendFile(name,string):
    with open(name,'a') as file:
        file.writelines(string)

def writeFile(name,string):
    with open(name,'w') as file:
        file.writelines(string)

def writeFileBytes(name,b):
    with open(name,'wb') as file:
        file.write(b)



def readFile(name):
    with open(name, 'r') as file:
        return file.read()

def readFileBytes(name):
    with open(name, 'rb') as file:
        
        bytes = file.read()

        return bytes


def readFileHex(name):
    with open(name, 'rb') as file:
        return file.read().hex

def readFileLines(name):
    with open(name, 'r') as file:
        return file.read().split("\n")



"""
fileContent = readFileBytes("Chemie Orbitalmodell-1.pptx")


print(fileContent)


writeFileBytes("Chemie Orbitalmodell-2.pptx",fileContent)
"""








