# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 08:35:19 2022

@author: faramirez
"""

import matplotlib.pyplot as plt
import math as mt
import numpy as np
from IPython import get_ipython

get_ipython().magic('reset -sf')


#-----------------------------------------------------------------------------
# Creacion de variables
#-----------------------------------------------------------------------------

# Vector de tiempo, unidades en [s]

time_final = 0.35
time_delta = 0.001
time_initial = 0
time_vector = np.float64(np.arange(time_initial,time_final+time_delta,time_delta))

# Parametros de entrada

omega = 10.972          # Velocidad de la banda (RPM)
R = 55.7                # Radio del rodillo de la banda (mm)
rho_teff = 0.26/1000    # Densidad del teff (g/grano)
g = 9.81                # Gravedad (m/s^{2})

# Calculo del vector posicion P = xi + yj, con sus coordenadas respectivas, este
# calculo se realiza por coordenada 

P = np.float64(np.zeros([len(time_vector),2]))

for i in range(len(time_vector)):
    x = omega*R*time_vector[i]
    y = -0.5*g*mt.pow(time_vector[i], 2)*1000
    P[i,0] = x
    P[i,1] = y

#-----------------------------------------------------------------------------
# Para determinar un tiempo especifico a cierta posicion. Con posicion me refiero
# a la distancia entre el punto que se desea determinar el tiempo y la parte 
# superior de la banda
#-----------------------------------------------------------------------------
 
num_pos = 2

# Se inicializan vectores de posY (contiene la medida desde la parte superior de
# la banda hasta el punto1 y punto2 respectivamente), time (para almacenar los 
# tiempos) y posX (para determinar la posicion X en esos momentos, solo es pa'
# graficar)

posY = np.empty(num_pos)
time = np.empty(num_pos)
posX = np.empty(num_pos)
posY[0] = -100         # Unidades en [mm]
posY[1] = -240

time[0] = np.sqrt(-2*posY[0]/(1000*g))
time[1] = np.sqrt(-2*posY[1]/(1000*g))
posX[0] = omega*R*time[0]
posX[1] = omega*R*time[1]

print('--------------------------------------------------------------------')
print('El tiempo que tarda en llegar a la pos1 es de ',round(time[0],3),' segundos')
print('El tiempo que tarda en llegar a la pos2 es de ',round(time[1],3),' segundos')
print('Entre pos1 y pos2 hay ',round(time[1]-time[0],3),' s')
print('--------------------------------------------------------------------')

#-----------------------------------------------------------------------------
# Para graficar el rodillo de la banda
#-----------------------------------------------------------------------------

num_segmentos = 100
rad = R
cx = 0
cy = -R

angulo = np.linspace(0, 2*np.pi, num_segmentos+1)
x_rod = rad * np.cos(angulo) + cx
y_rod = rad * np.sin(angulo) + cy

#-----------------------------------------------------------------------------
# Grafica de la posición de la semilla
#-----------------------------------------------------------------------------

plt.figure(dpi=300)
plt.plot(P[:,0],P[:,1],'b-',label='Trayectoria')
plt.plot(x_rod,y_rod,'k--',label='Rodillo Banda')
plt.plot(posX,posY,'ro',label='Puntos')
plt.title('Posicion y vs x de la semilla en el tiempo')
plt.xlabel('x (mm)')
plt.ylabel('y (mm)')
xmin = -R-50
xmax = max(abs(P[:,1]))
plt.xlim(xmin,xmax)
# ymin = 10
# ymax = -max(P[:,0])
# plt.ylim(ymax,ymin)
plt.legend()
plt.grid()

plt.show()


    


