from machine import Pin
import time
p18 = Pin(18, Pin.OUT)
p19 = Pin(19, Pin.OUT)
p21 = Pin(21, Pin.OUT)

#Se enciende con off
#Puedo imprimir en terminal con print
#18 Azul
#19 Verde
#21 Rojo

p18.on()
p19.on()
p21.on()
contador = 10

for i in range(30):
    time.sleep_ms(1000)
    print("Azul")
    p18.off()
    p19.on()
    p21.on()
    time.sleep_ms(1000)
    print("Verde")
    p18.on()
    p19.off()
    p21.on()
    time.sleep_ms(1000)
    print("Rojo")
    p18.on()
    p19.on()
    p21.off()

