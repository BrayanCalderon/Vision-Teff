import threading
import time
import socket

d = dict()
id = 0

def test(*args):
    print(f"Hola pasaron {args[0]} segundos\n")
    s.send((str(args[1])+" "+str(args[0])).encode())

def enviar_pulso(id,tiempo,valvula):
    global d
    delta = 0.5 #Tiempo que estará encendido la valvula
    d[id] = threading.Timer(tiempo,test,args = [valvula,1])
    d[id].start()
    d[id + 1] = threading.Timer(tiempo+delta, test, args = [valvula,2])

#Realizo la conexión
s = socket.socket()
s.connect(("192.168.4.1",2020))

input("Da enter para comenzar :3")
#Envio pulsos de prueba
# id es el identificador del thread va aumentando con cada ocasión
# tiempo es el tiempo en el cual se activará la valvula
# valvula es la valvula que se accionará
while id < 10:
    enviar_pulso(id,1,1)
    id +=2
    enviar_pulso(id,3,2)
    id += 2
    enviar_pulso(id,5,3)
    id +=2
    enviar_pulso(id,7,4)
    id +=2
