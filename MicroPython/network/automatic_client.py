import socket
import time 
s = socket.socket()
s.connect(("192.168.4.1",2020))
_=0
time.sleep(3)

#open = "1"
#s.send(open.encode())
print("Open")

while True and _ != 19:
        
    a = "201"
    b = "202" 
    c = "203"
    
    s.send(a.encode())
    print(a)
    time.sleep(0.2)
    s.send(b.encode())
    print(b)
    time.sleep(0.2)
    s.send(c.encode())
    print(c)
    time.sleep(0.2)
    
    _+=1


close = "4"    
s.send(close.encode())
print("Close")
s.close()

print("Fin programa")