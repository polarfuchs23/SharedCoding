import socket
import selectors
import time


def send(content, sock):
    sock.send(str(len(content.decode("ascii"))).encode("utf-8")+content)


def sendstring(content, sock):
    sock.send((str(len(content))+content).encode("utf-8"))


sel = selectors.DefaultSelector()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "mineburg.firewall-gateway.com"
#ip = "192.168.178.40"


print(sock.connect_ex((ip, 5000)))
sendstring("Data",sock)
print("received:  ", sock.recv(1024).decode("ascii"))

time.sleep(2)

while True:
    time.sleep(0.4)
    sendstring(1000*"---Test---", sock)
    #sock.recv(40240000).decode("ascii")
    print("runs")
    print("received:  ",sock.recv(40240000).decode("ascii"))
print("received:  ",sock.recv(1024).decode("ascii"))