import socket
import selectors
import time
import types

sel = selectors.DefaultSelector()
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "192.168.188.21"
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
    print("Accepted:", sock)
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    global startTime
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
            print("Received data:", recv_data, "from", sock)
            if sock not in sockets:
                startTimes.append(time.time())
                print(startTimes)
                sockets.append(sock)
            else:
                print("First: ", startTimes)
                startTimes[sockets.index(sock)] = time.time()
                print(startTimes)
                pass
    '''
        else:
            sel.unregister(sock)
            print("Disconnected connection to", sock)
            sock.close()
        '''
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

while True:
    events = sel.select(timeout=None)
    for i in range(len(startTimes)):
        if time.time()-startTimes[i] > 10:
            sockets[i-1].send(b'Your were disconnected')
            sel.unregister(sockets[i])
            print("Disconnected connection to", sockets[i-1])
            sockets[i-1].close()
            del sockets[i-1]
            del startTimes[i-1]
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)
