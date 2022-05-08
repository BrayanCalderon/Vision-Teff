from machine import Pin,PWM, Timer, I2C
import time
import network
import usocket
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

#Información LCD
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
lcd.clear()

queue_valvulas = []
valvulas_dict = dict()





    

def create_network():
    ap = network.WLAN(network.AP_IF) # create access-point interface
    ap.config(essid='ESP-AP') # set the ESSID of the access point
    ap.config(max_clients=10) # set how many clients can connect to the network
    ap.active(True)
    print(ap.ifconfig()[0])
    
def desactivar_valvula():
    global queue_valvulas
    if queue_valvulas:
        valvula = int(queue_valvulas.pop(0))
        valvulas_dict["valvula"+str(valvula)].duty(1024)
    
    
def activar_valvula():
    global queue_valvulas #tengo que ponerlo porque la modificaré :c
    if queue_valvulas:
        valvula = int(queue_valvulas.pop(0))
        #214 Es duty cycle de 5V
        valvulas_dict["valvula"+str(valvula)].duty(214)

def parada_valvulas():
    valvulas_dict["valvula1"].duty(1024)
    valvulas_dict["valvula2"].duty(1024)
    valvulas_dict["valvula3"].duty(1024)
    valvulas_dict["valvula4"].duty(1024)
    while True:
        lcd.clear()
        lcd.putstr("PARADA EMERGENCIA, REINICIE")
        
        
        
        
        #Prueba con led esp32
        #pin  = "p"+str(valvula)
        #print(pin)
        #if valvulas_dict[pin].value():
        #   valvulas_dict[pin].off()
        #else:
        #    valvulas_dict[pin].on()
        

    
    
if __name__ == '__main__':
    
    
    
    print("Comence")
    #Asigno la interrupción al pin 27
    p27 = Pin(27, Pin.IN)
    p35 = Pin(35,Pin.OUT)
    P35.on()
    #p2 = Pin(2, Pin.OUT)
    #valvulas_dict["p2"] = p2 #Pin de prueba LED 
    p27.irq(handler=parada_valvulas, trigger=Pin.IRQ_RISING)
    
    #Asignación Pines PWM
    valvula1 = PWM(Pin(12), freq = 20000, duty = 1023) 
    valvula2 = PWM(Pin(13), freq = 20000, duty = 1023)         
    valvula3 = PWM(Pin(14), freq = 20000, duty = 1023)         
    valvula4 = PWM(Pin(15), freq = 20000, duty = 1023)    
     
    #Agrego a diccionario de valvulas
    valvulas_dict["valvula1"] = valvula1
    valvulas_dict["valvula2"] = valvula2
    valvulas_dict["valvula3"] = valvula3
    valvulas_dict["valvula4"] = valvula4    
    
    #Creo el punto de acceso AP
    s = usocket.socket()
    s.bind(("192.168.4.1",2020))
    s.listen(10)
    lcd.putstr("Esperando conexiones")
    print("Servidor Iniciado, esperando conexiones:")

    #Inicia el loop de funcionamiento
    while True:
        
        #Realiza conexión con el computador mediante WiFi
        (sc,addr) = s.accept()
        
        #Si se logra una conexión lo imprime en la pantalla LCD
        if addr:
            lcd.clear()
            lcd.putstr("Conectado "+str(addr))
            time.sleep(1)
        else:
            lcd.clear()
            lcd.putstr("No se encontraron conexiones")
            
        #Limpia LCD e indica que está en funcionamiento
        lcd.clear()
        lcd.putstr("En funcionamiento: ")
            
        print(addr)
        while True:
            #Recibo mensaje de 64 bits 
            mensaje = sc.recv(64).decode()
            
            #composición mensaje [tiempo,zona]
            if not mensaje:
                break
            elif mensaje[0] == "1":
                queue_valvulas.append(int(mensaje[1])) 
                activar_valvula()
            elif mensaje[0] == "2":
                queue_valvulas.append(int(mensaje[1])) 
                desactivar_valvula()
            elif mensaje[0] == "3":
                parada_valvulas()
                break
                
            print(mensaje)
        #Cierro la conexión
        sc.close()
        
        lcd.clear()
        lcd.putstr("Se ha interrumpido el proceso")
        time.sleep(1)
        break