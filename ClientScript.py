import socket
import selectors

sel = selectors.DefaultSelector()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "95.91.247.164"
s.connect_ex((ip, 5000))
s.send(b'Data')
newDataA = s.recv(1024)
s.send(b'2ndData')
newDataB = s.recv(1024)
print(newDataA, " ", newDataB)