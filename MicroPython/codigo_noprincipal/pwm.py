from machine import Pin, PWM
from machine import Timer

frecuency = 500
duty = 1023
dutyOff = 1023

pwm18 = PWM(Pin(18))
pwm19 = PWM(Pin(19))
pwm21 = PWM(Pin(21))

pwm18.freq(frecuency) 
pwm19.freq(frecuency) 
pwm21.freq(frecuency) 

pwm18.duty(dutyOff) 
pwm19.duty(dutyOff) 
pwm21.duty(dutyOff) 




#variables
led = 1
period = 50

#set timer
tim1 = Timer(1)
tim1.init(period=period, mode=Timer.PERIODIC, callback=lambda t:
    setLed()
)

def setLed():
    global led
    global duty
    global dutyOff

    duty -= 10
    if duty < 0:
        duty = dutyOff
        led += 1
        if led > 3:
            led = 1
        
    
    if led == 1:
        pwm18.duty(duty) 
        pwm19.duty(dutyOff) 
        pwm21.duty(dutyOff) 
        

    if led == 2:
        pwm18.duty(dutyOff) 
        pwm19.duty(duty) 
        pwm21.duty(dutyOff) 
        

    if led == 3:
        pwm18.duty(dutyOff) 
        pwm19.duty(dutyOff) 
        pwm21.duty(duty) 
        

    
    