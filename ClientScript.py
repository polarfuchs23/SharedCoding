import socket
import selectors

sel = selectors.DefaultSelector()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect_ex(('192.168.0.203', 8080))
s.send(b'Data')
newData = s.recv(1024)
print(newData)