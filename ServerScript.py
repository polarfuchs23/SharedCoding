import socket
import selectors
import time
import types
from PrintFormatter import printf

DISCONNECTAFTERNOTSENDING = 30
FORMAT=[0, 12, 140, 148]
DEVIDERSTRING = 500*"-"


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
    if mask & selectors.EVENT_READ:
        #print("---------------hi---------------")
        length1 = sock.recv(10).decode("ascii")  # Should be ready to read
        length=""
        recv_data=b''
        print(length1)
        for s in length1:
            if s.isdigit():
                length+=s
            else:
                recv_data+=s.encode("utf-8")


        print(length)
        t1=time.time();
        while len(recv_data)<int(length):
            run=True
            while run:
                try:
                    recv_data += (sock.recv(int(length)))
                    run = False
                except:
                    run = True

        totaltime += time.time()-t1
        runs += 1

        print("took",time.time()-t1)
      #  for i in range(int(int(length)/100)-1):
      #      recv_data += (sock.recv(100))

        print("average",totaltime/runs,"over",runs,"runs")

        if recv_data:
            data.outb += recv_data
            #printf(["received:", recv_data, "from  ", sock], FORMAT)
            if sock not in sockets:
                startTimes.append(time.time())
                sockets.append(sock)
            else:
                startTimes[sockets.index(sock)] = time.time()
                pass

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            #printf(["echoing:", repr(data.outb), "to", data.addr], FORMAT)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

while True:
    events = sel.select()
    for i in range(-1, len(startTimes)-1):
        if time.time()-startTimes[i] > DISCONNECTAFTERNOTSENDING:
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
