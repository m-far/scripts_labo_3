# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 08:58:27 2019

@author: m-far
"""

import numpy as np
import visa
#import time
import matplotlib.pyplot as plt

#%%
#Creo la interfaz visa para comunicarme con equipos
rm = visa.ResourceManager()
#Pregunto que dispositvos están conectados
rm.list_resources()

#Copio la dirección del equipo
rscosci = 'USB0::0x0699::0x0368::C017067::INSTR'
#%%
#Abro la comunicación con el equipo (Osc Tektronik TBS 1052B-EDU)
osci = rm.open_resource(rscosci)
print(osci.query('IDN*?'))

#Le pregunto al osciloscopio todas sus escalas
xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')

#Eligo el modo de transmisión de datos (binario)
osci.write('DAT:ENC RPB')
osci.write('DAT:WID 1')

#Creo un vector para guardar los datos
data=[]

#Elijo el canal 1
osci.write('DATA:SOURCE CH1')
#Le pido al osciloscopio los datos del canal 1
data = osci.query_binary_values('CURV?', datatype='B', container=np.array)
#Me armo el vector de tiempo con la escala apropiada
tiempo = xze + np.arange(len(data)) * xin
#Transformo el voltaje a la escala apropiada
voltaje = (data-yoff)*ymu+yze
#Me armo un vector con los datos de tiempo y voltaje
datos=np.array([tiempo[700:1000],voltaje[700:1000]])
#Guardo los datos en formato python
np.save('E:\PruebasAdquisiscion\datos',datos)
#Guardo los datos en formato txt
np.savetxt('E:\PruebasAdquisiscion\datos.txt',datos)
#Cierro la comunicación con el equipo (Imortante!)
osci.close()

#%%
errory= datos[1,:]*0.03
plt.errorbar(datos[0,:], datos[1,:],errory)
plt.xlabel('Time')
plt.ylabel('Voltage')
plt.grid()
plt.show()

#%%

p,cov = np.polyfit(datos[0,:],datos[1,:],1,cov=True,w=errory)
def linear(x):
    lin=p[0]*x+p[1]
    return lin
#%%
plt.plot(datos[0,:], datos[1,:],'b-')
plt.plot(datos[0,:], linear(datos[0,:]),'r-')
plt.xlabel('Time')
plt.ylabel('Voltage')
plt.grid()
plt.show()