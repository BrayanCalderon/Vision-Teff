import socket
import time 
s = socket.socket()
s.connect(("192.168.4.1",2020))
_=0
while True and _ != 19:
    #a = input("Ingresa tu mensaje mamalon")
    
    a = "201"    
    print("mandé 201")
    s.send(a.encode())
    time.sleep(5)
    #a = "202"
    #print("mande 202")
    #s.send(a.encode())
    #time.sleep(2)
    
    _+=1
    
s.close()

print("Fin programa")