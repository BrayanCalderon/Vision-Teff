from machine import Pin,PWM, Timer, I2C
import time
import network
import usocket
###from lcd_api import LcdApi
###from pico_i2c_lcd import I2cLcd

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

#Cola de accionamiento valvulas
queue_valvulas = []
valvulas_dict = dict()




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
    ap = network.WLAN(network.AP_IF) # create access-point interface
    ap.config(essid='ESP-AP') # set the ESSID of the access point
    ap.config(max_clients=10) # set how many clients can connect to the network
    ap.active(True)
    print(ap.ifconfig()[0])
    
    
    
 # La valvula es normalmente cerrada por tanto para activarla necesito pwm de 1023 lo que son 24v en teoria y para
 # apagarla necesito 214 maso menos para tener una tensión de 5V en teoria   
def desactivar_valvula():
    global queue_valvulas
    if queue_valvulas:
        valvula = int(queue_valvulas.pop(0))
        valvulas_dict["valvula"+str(valvula)].duty(0)
        print("valvula des:", valvula)
        print("El duty es:",valvulas_dict["valvula"+str(valvula)].duty())

    
    
def activar_valvula():
    global queue_valvulas #tengo que ponerlo porque la modificaré :c
    if queue_valvulas:
        valvula = int(queue_valvulas.pop(0))
        valvulas_dict["valvula"+str(valvula)].duty(1023)
        print("valvula act:", valvula)
        print("El duty act es:",valvulas_dict["valvula"+str(valvula)].duty())

        
        
        
        
        #Prueba con led esp32
        #pin  = "p"+str(valvula)
        #print(pin)
        #if valvulas_dict[pin].value():
        #   valvulas_dict[pin].off()
        #else:
        #    valvulas_dict[pin].on()
        

    
    
if __name__ == '__main__':
    
    
    create_network()
    print("Comence")
    #Creo la variable p27 como entrada
    p27 = Pin(27, Pin.IN)
    
    #Prueba
    #p2 = Pin(2, Pin.OUT)
    #valvulas_dict["p2"] = p2
    
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
    
    
    print("comencé2")

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
            
        #Parte de network    
        print(addr)
        continuar2 = True
        while True:
            #Recibo mensaje de 64 bits 
            mensaje = sc.recv(64).decode()
            #composición mensaje [función,tiempo,zona]
            if not mensaje:
                print("Not message")
                #break
            
            elif mensaje[0] == "1":
                #tupla de posiciones
                queue_valvulas.append(int(mensaje[2])) 
                activar_valvula()
            elif mensaje[0] == "2":
                print("entredos")
                queue_valvulas.append(int(mensaje[2])) 
                queue_valvulas.append(int(mensaje[2])) 
                activar_valvula()
                print("entredos.1")
                time.sleep(0.2)
                desactivar_valvula()
                print("entredos.2")

                print("salidos")


            elif mensaje[0] == "3":
                break

            print(mensaje)
        sc.close()
        break