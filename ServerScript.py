#
#       notes:  -taking files in folders into account
#               -sending both ways
#               -checking for changes in files (Asynchronus?!)
#

import socket
import selectors
import time
import types
import sys
import os
import FileInterface
from PrintFormatter import printf

'''

            Codes (Client perspective)
---------------------------------------------------              
| Disconnect:                     g3i3Nf8320:wJd[ |
| Request files:                  =)vjq0eVnd)sth} |
| Received file:                  /mRJ|M+@m&NND@N |
| Request to send files:          5whR;FGW)>:62hO |
---------------------------------------------------

'''

#filesarray = []
def searchFiles(folderPath, allFiles):
    subFolders = []
    for file in os.listdir(folderPath):
        if os.path.isfile(folderPath + "/" + file) and ".py" not in file:
            name, extension = os.path.splitext(file)
            allFiles.append((name+extension).encode("utf-8") + b'qyz' + FileInterface.readfilebytes(folderPath + "/" + file))
        elif os.path.isdir(os.path.join(folderPath, file)):
            subFolders.append(file)
            allSubFiles = []
            allSubFiles = searchFiles(os.path.join(folderPath, file), allSubFiles)
            for subFile in allSubFiles:
                firstPart, secondPart = subFile.split(b'qyz')
                firstPart = firstPart.decode("ascii")
                firstPart = (file + "/" + firstPart).encode("utf-8")
                subFile = firstPart + b'qyz' + secondPart
                allFiles.append(subFile)
    return allFiles
    pass

emptyArray = []
serverPath = sys.argv[0]
folderPath = os.path.dirname(serverPath)
filesarray = searchFiles(folderPath, emptyArray)
#print(filesarray)

DISCONNECTAFTERNOTSENDING = 30
FORMAT = [0, 12, 140, 148]
DEVIDERSTRING = 500 * "-"

sel = selectors.DefaultSelector()
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "0.0.0.0"
print(ip)
lsock.bind((ip, 5000))
lsock.listen()
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

events = selectors.EVENT_READ | selectors.EVENT_WRITE
global startTimes
global sockets

startTimes = []
sockets = []


def disconnect(sock):
    print("Received disconnect request")
    sel.unregister(sock)
    print(DEVIDERSTRING)
    print("disconnected: ", sock)
    print(DEVIDERSTRING)
    del startTimes[sockets.index(sock)]
    del sockets[sockets.index(sock)]
    sock.close()
    return -1


def awnserfilerequest(sock):
    print("Received file request")
    print("fileamount: ", str(len(filesarray)))
    sendstring(str(len(filesarray)), sock)

    for file in filesarray:
        send(file, sock)

        while True:
            try:
                recv = sock.recv(15).decode("ascii")
                if recv == "/mRJ|M+@m&NND@N":
                    break
            except:
                pass

    return -1


def awaitdata(sock):
    recieved = sock.recv(15)

    if recieved == b'g3i3Nf8320:wJd[':
        return disconnect(sock)

    elif recieved == b'=)vjq0eVnd)sth}':
        return awnserfilerequest(sock)

    elif recieved == b'':
        return -1

    else:
        return getdata(recieved, sock)


def getdata(recieved, sock):
    length = ""
    recv_data = b''

    recv = recieved.split(b'a', 1)

    for s in recv[0].decode("ascii"):
        length += s

    recv_data += recv[1]

    while len(recv_data) < int(length):
        run = True
        while run:
            try:
                recv_data += (sock.recv(int(length)-len(recv_data)))
                run = False
            except:
                run = True

    recvParts = recv_data.split(b'qyz')
    if len(recvParts) == 2:
        filename = recvParts[0].decode("ascii")
        print("Received ", filename)
        recv_data = recvParts[1]
        FileInterface.writefilebytes(filename, recv_data)

    return recv_data


def send(content, sock):
    sock.send(str(len(content)).encode("utf-8") + b'a' + content)
#   print("send: ", str(len(content)).encode("utf-8") + b'a' + content)


def sendstring(content, sock):
    sock.send((str(len(content)) + "a" + content).encode("utf-8"))
#   print("send: ", (str(len(content)) + "a" + content).encode("utf-8"))


def accept_wrapper(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    print(DEVIDERSTRING)
    print("accepted:    ", sock)
    print(DEVIDERSTRING)
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data

    if sock not in sockets:
        startTimes.append(time.time())
        sockets.append(sock)


    if mask & selectors.EVENT_READ:
        startTimes[sockets.index(sock)] = time.time()

        print("read")
        recv_data=-1;
        try:
            recv_data = awaitdata(sock)
        except ConnectionResetError:
            disconnect(sock)

        if recv_data and recv_data != -1:
            data.outb += recv_data
            # printf(["received:", recv_data, "from  ", sock], FORMAT)
        elif recv_data==-1:
            pass
        else:
            print("\033[93m"+ str(recv_data) + " was Recieved even though the selector had an EVENT_READ!"
                                               " there might be a problem"+"\033[0;0m")
            disconnect(sock)


    elif mask & selectors.EVENT_WRITE:
        if data.outb:
            print("write")
            # printf(["echoing:", repr(data.outb), "to", data.addr], FORMAT)
            send(data.outb, sock)
            data.outb = b''


while True:
    events = sel.select()
    for i in range(-1, len(startTimes) - 1):
        if time.time() - startTimes[i] > DISCONNECTAFTERNOTSENDING:
            send(b'You were disconnected', sockets[i])
            sel.unregister(sockets[i])
            print(DEVIDERSTRING)
            print("disconnected: ", sockets[i])
            print(DEVIDERSTRING)
            sockets[i].close()
            del sockets[i]
            del startTimes[i]
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)