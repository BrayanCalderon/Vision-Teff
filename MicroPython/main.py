from machine import Pin,PWM, Timer, I2C
import time
import network
import usocket
###from lcd_api import LcdApi
###from pico_i2c_lcd import I2cLcd

"""
Código encargado de realizar el control de las valvulas conectadas al microcontrolador ESP32,
se encuentra planeado para trabajar con exactamente 3 distintas valvulas por medio de un control ON-OFF,
realizando la comunicación por medio de un modulo WIFI a través de un protocolo de comunicación TCP via sockets
la red inalambrica creada en el propio ESP32 está nombrada como ESP-AP. Permite utilizar una pantalla LCD como interfaz 
para conocer el estado del sistema pero no es esencial para su funcionamiento.
La información compartida en la comunicación está compuesta por paquetes de 3 bytes conformados por 3 números dispuestos de la
siguiente forma [id,tiempo,valvula] donde id es el código de la acción, el tiempo de activación  y finalmente la valvula a accionar.
"""

#Información LCD
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16


#Pines del ESP32 conectados a EN del driver
EN_M1_PIN_0 = 12 
EN_M1_PIN_1 = 27
EN_M2_PIN_0 = 13

#Pines del ESP32 conectados a CW del driver
CW_M1_1 = 14
CW_M1_2 = 26
CW_M2_1 = 18

#Pines del ESP32 conectados a PWM del driver
PMW_M1_1 = 32
PMW_M1_2 = 33
PMW_M2_1 = 19


###i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
###lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
###lcd.clear()

#Cola de accionamiento valvulas, estas determinan el orden en que llegan los mensajes y el orden de accionamiento de las valvulas
queue_valvulas = []
valvulas_dict = dict()
contador2 = 0




#Parada de Emergencia
def emergency_stop():
    valvula1.init(freq = 20000, duty = 0)
    valvula2.init(freq = 20000, duty = 0)
    valvula3.init(freq = 20000, duty = 0)
    #valvula4.init(freq = 20000, duty = 1023)
    while True:
        pass
    

#Crea la red en el esp32 para conectarse via wifi el pc 
def create_network():
    ap = network.WLAN(network.AP_IF) # Crea la interfaz de conexión Acces Point
    ap.config(essid='ESP-AP', channel =13) # Configura el nombre de la Red y asigna una banda de comunicación WIFI
    ap.config(max_clients=10) # Configura la cantidad máxima de clientes que se pueden conectar a la ESP32
    ap.active(True)
    
    print(ap.ifconfig()[0])
    
    
    
 # La valvula es normalmente cerrada por tanto para activarla necesito pwm de 1023 lo que son 24v en teoria y para
 # apagarla necesito 214 maso menos para tener una tensión de 5V en teoria   
def desactivar_valvula():
    global queue_valvulas
    if queue_valvulas:
        valvula = int(queue_valvulas.pop(0))
        valvulas_dict["valvula"+str(valvula)].duty(0)


    
    
def activar_valvula(valv):
    global queue_valvulas #tengo que ponerlo porque la modificaré :c
    continuar = True
    if continuar:
        #valvula = int(queue_valvulas.pop(0))
        valvula = valv
        print("valvula activada: ", valvula)
        valvulas_dict["valvula"+str(valvula)].duty(1023)
        time.sleep(0.001)
        valvulas_dict["valvula"+str(valvula)].duty(0)
        
        #print("valvula activada:", valvula)
        


    
if __name__ == '__main__':
    
    
    create_network()
    #Creo la variable p27 como entrada
    p27 = Pin(27, Pin.IN)
    
    
    #Activación PINES SALIDA

    ##Siempre en ON
    en_m1_1 = Pin(EN_M1_PIN_0, Pin.OUT)
    en_m1_2 = Pin(EN_M1_PIN_1, Pin.OUT)
    en_m2_1 = Pin(EN_M2_PIN_0, Pin.OUT)
    cw_m1_1 = Pin(CW_M1_1, Pin.OUT)
    cw_m1_2 = Pin(CW_M1_2, Pin.OUT)
    cw_m2_1 = Pin(CW_M2_1, Pin.OUT)
    
    en_m1_1.on()
    en_m1_2.on()
    en_m2_1.on()
    cw_m1_1.on()
    cw_m1_2.on()
    cw_m2_1.on()
    
    #Si el pin27 recibe una señal alta, se acciona y activa la función parada de emergencia
    p27.irq(handler=emergency_stop, trigger=Pin.IRQ_RISING)
    
    #Asignación Pines PWM
    valvula1 = PWM(Pin(PMW_M1_1), freq = 20000, duty = 0) 
    valvula2 = PWM(Pin(PMW_M1_2), freq = 20000, duty = 0)         
    valvula3 = PWM(Pin(PMW_M2_1), freq = 20000, duty = 0)         
    #valvula4 = PWM(Pin(15), freq = 20000, duty = 1023)     
    
    #Agrego a diccionario de valvulas
    valvulas_dict["valvula1"] = valvula1
    valvulas_dict["valvula2"] = valvula2
    valvulas_dict["valvula3"] = valvula3
    #valvulas_dict["valvula4"] = valvula4    
    
    #Creo el punto de acceso AP
    s = usocket.socket()
    s.bind(("192.168.4.1",2020))
    s.listen(10)
    control = 0
    
    ###lcd.putstr("Esperando conexiones")
    #time.sleep(1)
    print("Servidor Iniciado, esperando conexiones:")
    #Inicia el loop
    while True:
        
        #Información LCD
        (sc,addr) = s.accept() 
        if addr:
            ###lcd.clear()
            ###lcd.putstr("Conectado "+str(addr))
            time.sleep(1)
        ###else:
            ###lcd.clear()
            ###lcd.putstr("No se encontraron conexiones")
        ###lcd.clear()
        ###lcd.putstr("En funcionamiento: ")
            
        while True:
            codigo = sc.recv(3).decode()
            #print("codigo:", codigo)
            
            try:
            #Recibo mensaje de 3 bytes
                mensaje = codigo
            except:
                continue
            
            if mensaje[0] == "1":
                #print("Control")
                control += 1
                pass

            #composición mensaje [función,tiempo,zona]
            if mensaje[0] == "2":
                #queue_valvulas.append(int(mensaje[2])) 
                
                #queue_valvulas.append(int(mensaje[2])) 
                activar_valvula(int(mensaje[2]))
                time.sleep(0.001)
                #desactivar_valvula()
                #contador2 += 1
                #time.sleep(0.03)
                

            elif mensaje[0] == "4":
                print("Se recibieron", contador2, "senales")
                sc.close()
                break

        print("Sali del primer while")
    print("sali del segundo while")
        
