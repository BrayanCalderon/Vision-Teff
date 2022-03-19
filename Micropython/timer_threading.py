import threading
import time
import socket

d = dict()

def test(*args):
    print(f"Hola pasaron {args[0]} segundos\n")
    s.send((str(1)+" "+str(args[0])).encode())

def enviar_pulso(id,tiempo,valvula):
    global d
    d[id] = threading.Timer(tiempo,test,args = [valvula])
    d[id].start()

#Realizo la conexión
s = socket.socket()
s.connect(("192.168.4.1",2020))

input("Da enter para comenzar :3")
#Envio pulsos de prueba
enviar_pulso(1,5,2)
enviar_pulso(2,3,2)
enviar_pulso(3,1,2)
