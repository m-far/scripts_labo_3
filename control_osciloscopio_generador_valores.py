# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:11:13 2019

@author: m-far
"""
import numpy as np
import pyvisa as visa
#import visa
import time
import matplotlib.pyplot as plt

#%%
#Creo la interfaz visa para comunicarme con equipos
rm = visa.ResourceManager()
#Pregunto que dispositvos están conectados
rm.list_resources()

#%%
rscfungen = 'USB0::0x0699::0x0353::1625721::INSTR'
rscosci = 'USB0::0x0699::0x0368::C017060::INSTR'

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
freq=np.logspace(np.log10(10),np.log10(100),5)
amplitude=1
offset=amplitude/2

'''
Le mando la instrucción al equipo.
SOUR = Source, y el numero que le sigue es el canal que queremos usar
El %f lo que hace es "llamar" a un valor que esta afuera del comando.
En el caso de la frecuencia, el %f va a ser reemplazado por el numero 
cargado en la variable freq
'''

fungen.write('SOUR1:VOLT %f' % amplitude)
fungen.write('SOUR1:VOLT:OFFS %f' % offset)


datos=np.zeros((len(freq),6))
for i in range(len(freq)):
    #Creo un vector para guardar los datos
    #elijo la frecuencia del generador
    fungen.write('SOUR1:FREQ %f' % freq[i])
    #espero 1 segundo para darle tiempo al equipo de responder
    time.sleep(1)
    #Elijo el canal 1 del osciloscopio
    osci.write('MEASU:IMMED:SOURCE CH1')
    #Le pido al osciloscopio los datos del canal 1
    osci.write('MEASU:IMMED:TYPE FREQ')
    freq1=osci.query('MEASU:IMMED:VALUE?')
    osci.write('MEASU:IMMED:TYPE AMPLITUDE')
    voltaje1=osci.query('MEASU:IMMED:VALUE?')
    osci.write('MEASU:IMMED:TYPE PHA')
    fase1=osci.query('MEASU:IMMED:VALUE?')
    #elijo el canal 2 del equipo
    osci.write('MEASU:IMMED:SOURCE CH2')
    #Le pido al osciloscopio los datos del canal 2
    osci.write('MEASU:IMMED:TYPE FREQ')
    freq2=osci.query('MEASU:IMMED:VALUE?')
    osci.write('MEASU:IMMED:TYPE AMPLITUDE')
    voltaje2=osci.query('MEASU:IMMED:VALUE?')
    osci.write('MEASU:IMMED:TYPE PHA')
    fase2=osci.query('MEASU:IMMED:VALUE?')
    #Me armo un vector con los datos de tiempo y voltaje
    datos[i,:]=np.array([freq1,voltaje1,fase1, freq2,voltaje2,fase2])
#Guardo los datos en formato python.
np.save('datos' %i,datos)
#Guardo los datos en formato txt
np.savetxt('datos.txt' %i,datos)
#Cierro la comunicación con el equipo (Imortante!)

osci.close()
fungen.close()

#%%
freq1=datos[:,0]
voltaje1=datos[:,1]
fase1=datos[:,2]
freq2=datos[:,3]
voltaje2=datos[:,4]
fase2=datos[:,5]

plt.figure(3)
plt.clf()
plt.subplot(2,1,1)
plt.plot(freq,voltaje1,'.-r')
plt.plot(freq,voltaje2,'.-b')
plt.subplot(2,1,2)
plt.plot(freq,fase1,'.-r')
plt.plot(freq,fase2,'.-b')
