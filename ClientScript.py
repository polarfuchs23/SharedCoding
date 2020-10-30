import socket
import selectors
import time

sel = selectors.DefaultSelector()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "ip"
print(s.connect_ex((ip, 5000)))
s.send(b'Data')
newDataA = s.recv(1024)
print(newDataA.decode("ascii"))
time.sleep(4)
s.send(b'2ndData')
newDataB = s.recv(1024)
answers = []
#for i in range(100):
 #   s.send(bytes([i]))
  #  answers.append(s.recv(1024))
print(newDataB.decode("ascii"))
print(answers)
print(s.recv(1024).decode("ascii"))