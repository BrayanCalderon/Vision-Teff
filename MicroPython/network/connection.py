import network
import usocket
from machine import Pin
import time

p2 = Pin(2,Pin.OUT)

def enciende_led():
    cont = 0
    while(cont < 10):
        cont+=1
        p2.on()
        time.sleep_ms(500)
        p2.off()
        time.sleep_ms(500)
        

ap = network.WLAN(network.AP_IF) # create access-point interface
ap.config(essid='ESP-AP') # set the ESSID of the access point
ap.config(max_clients=10) # set how many clients can connect to the network
ap.active(True)
print(ap.ifconfig()[0])

s = usocket.socket()
s.bind(("192.168.4.1",2020))
s.listen(10)
print("Servidor Iniciado, esperando conexiones: ")

while True:
    (sc,addr) = s.accept()
    print(addr)
    continuar2 = True
    while True:
        mensaje = sc.recv(64).decode()
        if not mensaje:
            break
        if mensaje == "1":
            enciende_led()
            
        print(mensaje)
    sc.close()
    break

s.close()
print("Fin programa")
        