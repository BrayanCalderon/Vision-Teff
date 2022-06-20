import threading
import time
import socket

d = dict()

def test(*args):
    s = args[1]
    print(f"Valvula {args[0]} Activada\n")
    s.send((str(args[2])+"0"+str(args[0])).encode())
    
def test_(*args):
    print(f"Valvula {args} Activada\n")
    #s.send((str(1)+" "+str(args[0])).encode())

def enviar_pulso(id,tiempo,valvula,s):
    global d
    d[id] = threading.Timer(tiempo,test,args = [valvula,s,id])
    d[id].start()
    
def enviar_pulso_(id,tiempo,valvula):
    global d
    d[id] = threading.Timer(tiempo,test_,args = [valvula])
    d[id].start()

def conexion():
    try:
        s = socket.socket()
        s.connect(("192.168.4.1",2020))
        print("Conexión Exitosa")
    except:
        print("Intentando conectar de nuevo")
        conexion()
            

#Realizo la conexión
#

#input("Da enter para comenzar :3")
#Envio pulsos de prueba
#enviar_pulso(2,0,1)
#enviar_pulso(2,0,1)
#enviar_pulso(2,0,1)


#for i in range(10):
#    enviar_pulso(2)
