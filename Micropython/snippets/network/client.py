import socket

s = socket.socket()
s.connect(("192.168.4.1",2020))
while True:
    a = input("Ingresa tu mensaje mamalon")
    if a == "fin":
        break
    else:
        s.send(a.encode())
s.close()

print("Fin programa")