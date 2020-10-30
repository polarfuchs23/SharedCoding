import socket
import selectors
import time


sel = selectors.DefaultSelector()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "mineburg.firewall-gateway.com"
#ip = "192.168.178.40"


print(s.connect_ex((ip, 5000)))
tosend="Data"
s.send((str(len(tosend))+tosend).encode("utf-8"))
print("received:  ",s.recv(1024).decode("ascii"))

time.sleep(2)

while True:
    time.sleep(0.4)
    tosend=1000*"---Test---"
    s.send((str(len(tosend))+tosend).encode("utf-8"))
    s.recv(40240000).decode("ascii")
    print("runs")
print("received:  ",s.recv(40240000).decode("ascii"))
print("received:  ",s.recv(1024).decode("ascii"))