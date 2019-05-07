# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:11:13 2019

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


rscfungen = 'USB::0x0699::0x0353::1625697::INSTR'
rscosci = 'USB0::0x0699::0x0368::C017067::INSTR'

#%%
#Abro la comunicación con los equipos (Osc Tektronik TBS 1052B-EDU  +  Tektronik AFG1022)
osci = rm.open_resource(rscosci)
fungen = rm.open_resource(rscfungen)


#Le pregunto al osciloscopio todas sus escalas
xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')

#Eligo el modo de transmisión de datos (binario)
osci.write('DAT:ENC RPB')
osci.write('DAT:WID 1')

#defino los valores de las variables del generador de funciones
freq=np.logspace(np.log(10),np.log(1000),10)
amplitude=1
offset=0.5

'''
Le mando la instrucción al equipo.
SOUR = Source, y el numero que le sigue es el canal que queremos usar
El %f lo que hace es "llamar" a un valor que esta afuera del comando.
En el caso de la frecuencia, el %f va a ser reemplazado por el numero 
cargado en la variable freq
'''

fungen.write('SOUR1:VOLT %f' % amplitude)
fungen.write('SOUR1:VOLT:OFFS %f' % offset)
#%%

for i in range(len(freq)):
    #Creo un vector para guardar los datos
    datos=[]
    #elijo la frecuencia del generador
    fungen.write('SOUR1:FREQ %f' % freq[i])
    #Elijo el canal 1 del osciloscopio
    osci.write('DATA:SOURCE CH1')
    #Le pido al osciloscopio los datos del canal 1
    data = osci.query_binary_values('CURV?', datatype='B', container=np.array)
    #Me armo el vector de tiempo con la escala apropiada
    tiempo = xze + np.arange(len(data)) * xin
    #Transformo el voltaje a la escala apropiada
    voltaje = (data-yoff)*ymu+yze
    #Me armo un vector con los datos de tiempo y voltaje
    datos=np.array([tiempo,voltaje])
    #Guardo los datos en formato python. el %02d lo que hace es donde lo 
    #escribo, me reemplaza con dos digitos el valor que esta afuera con el % (i)
    np.save('D:\PythonScripts\datos%02d' %i,datos)
    #Guardo los datos en formato txt
    np.savetxt('D:\PythonScripts\datos%02d.txt' %i,datos)
#Cierro la comunicación con el equipo (Imortante!)

osci.close()
fungen.close()