from machine import Pin, Timer
import network

print("Comenzando")
p18 = Pin(18, Pin.OUT)
p19 = Pin(19, Pin.OUT)
p21 = Pin(21, Pin.OUT)

p18.off()
p19.on()
p21.on()



ap = network.WLAN(network.AP_IF) # create access-point interface
ap.config(essid='ESP32-AP') # set the ESSID of the access point
ap.config(max_clients=2, authmode = 3, password = "12345678") # set how many clients can connect to the network
ap.active(True)         # activate the interface


def decorador(funcion):
    def wrapper():
        print("Hola cabron")
        funcion()
    return wrapper


@decorador
def printClients():
    clients = ap.status('stations')
    print("------------------------")
    print("Clientes Conectados"+ str(len(clients)))
    for item in clients:
        print(str(item))
    print("-------------------------")

    if len(clients) > 0:
        print('Hola2')
        p19.off() #on verde
        p18.on()
        p21.on()
    else:
        p21.off() #on rojo
        p18.on()
        p19.on()


tim1 = Timer(1)
tim1.init(period=10000, mode=Timer.PERIODIC, callback=lambda t:
    printClients()
)



