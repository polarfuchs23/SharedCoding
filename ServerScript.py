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

filesarray = []


serverPath = sys.argv[0]
folderPath = os.path.dirname(serverPath)
for file in os.listdir(folderPath):
    if os.path.isfile(file) and ".py" not in file:
        name, extension = os.path.splitext(file)
        filesarray.append((name+extension).encode("utf-8") + b'qyz' + FileInterface.readfilebytes(file))


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
                recv = sock.recv(10).decode("ascii")
                if recv == "/mRJ|M+@m&":
                    break
            except:
                pass

    return -1


def awaitdata(sock):
    recieved = sock.recv(10)

    print("Received:", recieved)

    if recieved == b'g3i3Nf8320':
        return disconnect(sock)

    elif recieved == b'=)vjq0eVnd':
        return awnserfilerequest(sock)

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
    else:
        startTimes[sockets.index(sock)] = time.time()
        pass
    if mask & selectors.EVENT_READ:
        recv_data = awaitdata(sock)

        if recv_data and recv_data != -1:
            data.outb += recv_data
            # printf(["received:", recv_data, "from  ", sock], FORMAT)
        try:
            print()
        except:
            disconnect(sock)

    elif mask & selectors.EVENT_WRITE:
        if data.outb:
            # printf(["echoing:", repr(data.outb), "to", data.addr], FORMAT)
            send(data.outb, sock)
            data.outb = b''


while True:
    events = sel.select()
    for i in range(-1, len(startTimes) - 1):
        if time.time() - startTimes[i] > DISCONNECTAFTERNOTSENDING:
            sockets[i].send(b'Your were disconnected')
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
