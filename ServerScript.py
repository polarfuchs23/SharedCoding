import socket
import selectors
import time
import types

sel = selectors.DefaultSelector()
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "0.0.0.0"
print(ip)
lsock.bind((ip, 5000))
lsock.listen()
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

headersize = 9

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
    print("Accepted:", sock)
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(16)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
            print("Received data:", recv_data, "from", sock)
            if sock not in sockets:
                startTimes.append(time.time())
                sockets.append(sock)
            else:
                startTimes[sockets.index(sock)] = time.time()
                pass
        #Das ist das seltsame rturn
        return recv_data
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

while True:
    events = sel.select(timeout=None)
    for i in range(len(startTimes)):
        if time.time()-startTimes[i-1] > 10:
            sockets[i-1].send(b'Your were disconnected')
            sel.unregister(sockets[i-1])
            print("Disconnected connection to", sockets[i-1])
            sockets[i-1].close()
            del sockets[i-1]
            del startTimes[i-1]
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            length = service_connection(key, mask)
