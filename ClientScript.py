import socket
import selectors
import time

sel = selectors.DefaultSelector()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "192.168.188.21"
s.connect_ex((ip, 5000))
s.send(b'Data')
newDataA = s.recv(1024)
print(newDataA.decode("ascii"))
time.sleep(4)
s.send(b'2ndData')
newDataB = s.recv(1024)
print(newDataB.decode("ascii"))
print(s.recv(1024).decode("ascii"))