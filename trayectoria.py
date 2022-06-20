from re import A
import numpy as np
import math
g =  9.77412            # Gravedad en Bogotá

#Seria el tiempo desde la banda hasta la valvula que es constante 
#menos el tiempo desde la posición encontrada, eso me da el tiempo restante

def trayec_simple(valv,posy):
    
    #if valv == 1:
    #    valv = 3
    #elif valv == 3:
    #    valv = 1
    
    a = -4.6345
    b = 2.4764
    c = -0.3345
    d = 0.0125*math.sin(80.1*math.pi/180)
    posy2 = -(posy/1000) - d - 0.057 
    print(posy2)
    t_pos = (((b/(2*a))**2) - ((c-posy2)/a))**(1/2) - b/(2*a)
    t_pos = t_pos
    t_valv = 0.492 #Tiempo constante desde la superficie de la banda hasta las valvulas 
    return t_valv-t_pos

    
