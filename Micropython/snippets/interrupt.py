from machine import  Pin
import time
p2 = Pin(2,Pin.OUT)
p27 = Pin(27, Pin.IN)

p2.off()
count = 0

def setLed(pin):
    p2.value(not p2.value())
    
p27.irq(handler=setLed, trigger=Pin.IRQ_RISING)

while count < 20:
    p2.on()
    print("1 ")
    time.sleep_ms(1500)
    p2.off()
    time.sleep_ms(1500)
    print(count)
    count += 1