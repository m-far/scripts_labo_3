# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:52:19 2019

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
rscfungen = 'USB::0x0699::0x0353::1625695::INSTR'


#%%
#Abro la comunicación con el equipo (AFG Tektronik AFG1022)
fungen = rm.open_resource(rscfungen)

#defino los valores de las variables
freq=1000
amplitude=1
offset=0.5
'''
Le mando la instrucción al equipo.
SOUR = Source, y el numero que le sigue es el canal que queremos usar
 El %f lo que hace es "llamar" a un valor que esta afuera del comando.
 En el caso de la frecuencia, el %f va a ser reemplazado por el numero 
 cargado en la variable freq
'''
fungen.write('SOUR1:FREQ %f' % freq)
fungen.write('SOUR1:VOLT %f' % amplitude)
fungen.write('SOUR1:VOLT:OFFS %f' % offset)

fungen.close()
 