import socket
import selectors

sel = selectors.DefaultSelector()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "192.168.0.203"
print(s.connect_ex((ip, 5000)))

leftfor = 0

msg = "Teweffewfefewfwefefewefwfewfewfewewf"
if len(msg) > 16:
    for i in range(int(len(msg)/16)):
        s.send(msg[i*16:(i+1)*16].encode("utf-8"))
        print("send: ", msg[i*16:(i+1)*16], " ", msg[i*16:(i+1)*16].encode("utf-8"))
        leftfor = i+1
    s.send(msg[leftfor*16:].encode("utf-8"))
else:
    s.send(msg.encode("utf-8"))
print("send: ", msg[leftfor*16:], " ", msg[leftfor*16:].encode("utf-8"))
newDataA = s.recv(1024)
print(newDataA.decode("ascii"))
print(s.recv(1024).decode("ascii"))