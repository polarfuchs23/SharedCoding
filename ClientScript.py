#
#
#       fix infinite loop at line 40 when server is closed while sending
#
#

import socket
import time
import keyboard
import FileInterface


def send(content, sock):
    try:
        sock.send(str(len(content.decode("ascii"))).encode("utf-8") + content)
    except:
        return -1


def sendstring(content, sock):
    try:
        sock.send((str(len(content)) + content).encode("utf-8"))
    except:
        return -1


def awaitdata(sock):
    try:
        recievedlength = sock.recv(10).decode("ascii")  # Should be ready to read
        print("Received1:", recievedlength, " ", recievedlength.encode("utf-8"))
        length = ""
        recv_data = b''
        for s in recievedlength:
            if s.isdigit():
                length += s
            else:
                recv_data += s.encode("utf-8")

        print(length)
        while len(recv_data) < int(length):
            run = True
            while run:
                try:
                    recv_data += (sock.recv(int(length)))
                    run = False
                except:
                    run = True
        return recv_data.decode("ascii")
    except:
        return -1


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "mineburg.firewall-gateway.com"


print(sock.connect_ex((ip, 5000)))
sendstring("Data", sock)
print("received:  ", sock.recv(1024).decode("ascii"))

time.sleep(2)
"""
while True:
    time.sleep(0.4)
    if keyboard.is_pressed('esc'):
        sock.send("g3i3Nf8320".encode("utf-8"))
        break
    sendstring(10000000 * "a", sock)
    print("received:  ", awaitdata(sock)
"""
sock.send("=)vjq0eVnd".encode("utf-8"))
fileamount = int(awaitdata(sock))
print("fileamount:", fileamount)
for i in range(fileamount-1):
    f = awaitdata(sock)
    print("File:", f)
    FileInterface.writeFile("output"+i+".txt", f)

sock.send("g3i3Nf8320".encode("utf-8"))
print()
print("done")
