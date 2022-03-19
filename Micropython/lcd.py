from machine import Pin, I2C
import utime 
from lcd_api import LcdApi
from i2c_lcd import I2cLcd


#Direccion I2C y tamaño LCD

I2C_ADDR =  0X27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16




i2c = I2C(0, sda=Pin(21), scl = Pin(22), freq =  400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS,I2C_NUM_COLS)
cont  = 20
while cont < 20:
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("Esperando conexiones")
    utime.sleep(1)
    lcd.move_to(0,1)
    lcd.putstr("Conexion realizada")
    utime.sleep(1)
    cont += 1