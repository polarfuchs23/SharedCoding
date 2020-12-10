#
#
#       fix infinite loop at line 40 when server is closed while sending
#
#

import socket
import time
import FileInterface


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "mineburg.firewall-gateway.com"
ip = "192.168.0.203"

def send(content, sock):
    try:
        sock.send(str(len(content.decode("ascii"))).encode("utf-8") + b'a' + content)
    except:
        return -1


def sendstring(content, sock):
    try:
        sock.send((str(len(content)) + "a" + content).encode("utf-8"))
    except:
        return -1


def awaitdata(sock):
    recievedlength = sock.recv(15)  # Should be ready to read

    print("Received:", recievedlength)
    length = ""
    recv_data = b''

    recv = recievedlength.split(b'a', 1)

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


def awaitfile(sock):

    recv_data = awaitdata(sock)

    filename = -1

    recv = recv_data.split(b'qyz', 1)
    if len(recv) == 2:
        filename = recv[0].decode("ascii")
        recv_data = recv[1]

    return recv_data, filename


print(sock.connect_ex((ip, 5000)))
print("Sending")

print(sendstring("Data", sock))
print("Received:  ", sock.recv(1024).decode("ascii"))

time.sleep(1)

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
fileamount, rubbish = awaitfile(sock)
fileamount = int(fileamount)
print()
print()
print("fileamount:", fileamount)
for i in range(fileamount):
    f, name = awaitfile(sock)

    sock.send(b'/mRJ|M+@m&')

#   print("File:", f)
    FileInterface.writefilebytes(name, f)


sock.send("g3i3Nf8320".encode("utf-8"))
time.sleep(1)
print()
print("done")
