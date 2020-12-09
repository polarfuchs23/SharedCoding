#
#
#       fix infinite loop at line 40 when server is closed while sending
#
#

import socket
import time
import FileInterface


def send(content, sock):
    try:
        sock.send(str(len(content.decode("ascii"))).encode("utf-8") + "a".encode("utf-8") + content)
    except:
        return -1


def sendstring(content, sock):
    try:
        sock.send((str(len(content)) + "a" + content).encode("utf-8"))
    except:
        return -1


def awaitdata(sock):
    #try:
    recievedlength = sock.recv(80)  # Should be ready to read


    print("Received:", recievedlength)
    length = ""
    recv_data = b''

    recv=recievedlength.split(b'qyz', 2)

    print("Splited received: ", recv)
    filename = -1
    for s in recv[0].decode("ascii"):
        length += s
    if len(recv) == 3:
        length = str(int(length)-3-len(recv[1]))

    if len(recv) == 2:
        recv_data += recv[1]
    else:
        filename = recv[1].decode("ascii")
        recv_data += recv[2]

    print("length ", length)
    while len(recv_data) < int(length):
        run = True
        while run:
            try:
                recv_data += (sock.recv(int(length)))
                run = False
            except:
                run = True
    return recv_data, filename
#except Exception as e:
#    print(e)
#    return -1


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "192.168.0.203"


print(sock.connect_ex((ip, 5000)))
print("sending")

print(sendstring("Data", sock))
print("received:  ", sock.recv(1024).decode("ascii"))

time.sleep(2)

"""
while True:
    time.sleep(0.4)
    if keyboard.is_pressed('esc'):
        sock.send("g3i3Nf8320".encode("utf-8"))
        break
    sendstring(500000 * "b", sock)
    print("received:  ", awaitdata(sock))
"""

sock.send("=)vjq0eVnd".encode("utf-8"))
fileamount, rubbish = awaitdata(sock)
fileamount = int(fileamount)
print()
print()
print("fileamount:", fileamount)
for i in range(fileamount):
    f, name = awaitdata(sock)
    print("File:", f)
    FileInterface.writeFileBytes("_"+name, f)


sock.send("g3i3Nf8320".encode("utf-8"))
time.sleep(1)
print()
print("done")