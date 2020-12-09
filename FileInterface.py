

def appendfile(name, string):
    with open(name, 'a') as file:
        file.writelines(string)


def writefile(name, string):
    with open(name, 'w') as file:
        file.writelines(string)


def writefilebytes(name, b):
    with open(name, 'wb') as file:
        file.write(b)


def readfile(name):
    with open(name, 'r') as file:
        return file.read()


def readfilebytes(name):
    with open(name, 'rb') as file:

        byt = file.read()

        return byt


def readfilehex(name):
    with open(name, 'rb') as file:
        return file.read().hex


def readfilelines(name):
    with open(name, 'r') as file:
        return file.read().split("\n")


"""
fileContent = readFileBytes("Chemie Orbitalmodell-1.pptx")


print(fileContent)


writeFileBytes("Chemie Orbitalmodell-2.pptx",fileContent)
"""
