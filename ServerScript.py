#
#       note: sending to requests with 10 seconds between them to (mineburg.firewall-gateway.com, 5000) will wake up the computer from standby and connect to the server
#

import socket
import selectors
import time
import types
import sys, os
import FileInterface
from PrintFormatter import printf

filesarray = []
serverPath = sys.argv[0]
folderPath = os.path.dirname(serverPath)
for file in os.listdir(folderPath):
    if os.path.isfile(file) and ".py" not in file:
        filesarray.append(FileInterface.readFile(file))

for file in filesarray:
    print(file)

DISCONNECTAFTERNOTSENDING = 30
FORMAT = [0, 12, 140, 148]
DEVIDERSTRING = 500 * "-"

runs = 0
totaltime = 0

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

def awaitdata(sock):
    global runs
    global totaltime
    recievedlength = sock.recv(10).decode("ascii")  # Should be ready to read

    print(recievedlength, " ", recievedlength.encode("utf-8"))

    if recievedlength == "g3i3Nf8320":
        sel.unregister(sock)
        print(DEVIDERSTRING)
        print("disconnected: ", sock)
        print(DEVIDERSTRING)
        del startTimes[sockets.index(sock)]
        del sockets[sockets.index(sock)]
        sock.close()
        return -1
    elif recievedlength == "=)vjq0eVnd":
        print("hi")
        print(str(len(filesarray)))
        sendstring(str(len(filesarray)), sock)
        for file in filesarray:
            sendstring(file, sock)
            time.sleep(0.1)
        return -1
    else:
        length = ""
        recv_data = b''
        print(recievedlength)

        digits = True
        for s in recievedlength:
            if s.isdigit() and digits:
                length += s
            elif s == "a" and digits:
                digits = False
            else:
                recv_data += s.encode("utf-8")

        print(length)
        t1 = time.time();
        while len(recv_data) < int(length):
            run = True
            while run:
                try:
                    recv_data += (sock.recv(int(length)))
                    run = False
                except:
                    run = True

        totaltime += time.time() - t1
        runs += 1

        print("took", time.time() - t1)

        print("average", totaltime / runs, "over", runs, "runs")

        return recv_data



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
    global runs
    global totaltime
    sock = key.fileobj
    data = key.data
    if sock not in sockets:
        startTimes.append(time.time())
        sockets.append(sock)
    else:
        startTimes[sockets.index(sock)] = time.time()
        pass
    if mask & selectors.EVENT_READ:
        print("hi2")
        recv_data = awaitdata(sock)
        if recv_data and recv_data != -1:
            data.outb += recv_data
            # printf(["received:", recv_data, "from  ", sock], FORMAT)
        try:
            print()
        except:
            sel.unregister(sock)
            print(DEVIDERSTRING)
            print("disconnected: ", sock)
            print(DEVIDERSTRING)
            del startTimes[sockets.index(sock)]
            del sockets[sockets.index(sock)]
            sock.close()

    elif mask & selectors.EVENT_WRITE:
        if data.outb:
            # printf(["echoing:", repr(data.outb), "to", data.addr], FORMAT)
            send(data.outb, sock)
            data.outb = b''


def send(content, sock):
    sock.send(str(len(content.decode("ascii"))).encode("utf-8") + "a".encode("utf-8") + content)


def sendstring(content, sock):
    sock.send((str(len(content)) + "a" + content).encode("utf-8"))


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
