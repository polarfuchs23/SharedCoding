import socket
import selectors
import time

sel = selectors.DefaultSelector()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "mineburg.firewall-gateway.com"
print(s.connect_ex((ip, 5000)))
tosend="Data"
s.send(str(len(tosend)).encode("utf-8"))
s.send(tosend.encode("utf-8"))
print(s.recv(1024).decode("ascii"))
time.sleep(2)

tosend=100*"2ndData"
s.send(str(len(tosend)).encode("utf-8"))
s.send(tosend.encode("utf-8"))

print(s.recv(1024).decode("ascii"))
print(s.recv(1024).decode("ascii"))