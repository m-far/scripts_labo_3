# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:11:13 2019

@author: m-far
"""
import numpy as np
import visa
import time
import matplotlib.pyplot as plt

#%%
#Creo la interfaz visa para comunicarme con equipos
rm = visa.ResourceManager()
#Pregunto que dispositvos están conectados
rm.list_resources()


rscfungen = 'USB::0x0699::0x0353::1625721::INSTR'
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
freq=np.logspace(np.log(10),np.log(1000),10)
amplitude=1
offset=0.0

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

def smooth(voltaje,cuanto):
    window = np.ones(cuanto)/cuanto
    out = np.convolve(voltaje,window,'same')
    return out
        

def vpp(tiempo, voltaje):
    out=max(voltaje)-min(voltaje)
    return out

def vrms(tiempo, voltaje):
    out = np.sqrt(np.mean(voltaje**2))
    return out

def frecuencia(tiempo, voltaje):
    a=np.array([])
    for i,t in enumerate(tiempo[:-1]):# para cada puntito
        if (voltaje[i]<0) and (voltaje[i+1]>=0): #si cruza el cero
            a=np.append(a,t) #agrego el tiempo de ese puntito al vector de cruces   
    out=1/(a[1]-a[0])
    return out

def desfasaje(tiempo, voltaje1,voltaje2):
    a1=np.array([])
    for i,t in enumerate(tiempo[:-1]):
        if (voltaje1[i]<0) and (voltaje1[i+1]>=0): #si cruza el cero
            a1=np.append(a1,t)    
    a2=np.array([])
    for i,t in enumerate(tiempo[:-1]):
        if (voltaje2[i]<0) and (voltaje2[i+1]>=0): #si cruza el cero
            a2=np.append(a2,t)    
                
    delay=a2[0]-a1[0]
    radianes=delay*frecuencia(tiempo, voltaje1)*2*np.pi
    grados=radianes*180/np.pi
    return grados

osci = rm.open_resource(rscosci)
fungen = rm.open_resource(rscfungen)

#Le pregunto al osciloscopio todas sus escalas
xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')

#Eligo el modo de transmisión de datos (binario)
osci.write('DAT:ENC RPB')
osci.write('DAT:WID 1')

frecuencias=[]
desfasajes=[]
voltaje_pp_ch1=[]
voltaje_pp_ch2=[]
voltaje_rms_ch1=[]
voltaje_rms_ch2=[]

#freq=np.array([500:100:2500])
freq=np.linspace(500,2500,10)
for i in range(len(freq)):
    #Creo un vector para guardar los datos
    datos=[]
    #elijo la frecuencia del generador
    fungen.write('SOUR1:FREQ %f' % freq[i])
    
    time.sleep(.1)
    #Elijo el canal 1 del osciloscopio
    osci.write('DATA:SOURCE CH1')
    #Le pido al osciloscopio los datos del canal 1
    data = osci.query_binary_values('CURV?', datatype='B', container=np.array)
    #Me armo el vector de tiempo con la escala apropiada
    tiempo1 = xze + np.arange(len(data)) * xin
    #Transformo el voltaje a la escala apropiada
    voltaje1 = (data-yoff)*ymu+yze
    #Elijo el canal 2 del osciloscopio
    osci.write('DATA:SOURCE CH2')
    #Le pido al osciloscopio los datos del canal 2
    data = osci.query_binary_values('CURV?', datatype='B', container=np.array)
    #Me armo el vector de tiempo con la escala apropiada
    tiempo2 = xze + np.arange(len(data)) * xin
    #Transformo el voltaje a la escala apropiada
    voltaje2 = (data-yoff)*ymu+yze


    cuanto = 10
    frec=frecuencia(tiempo1, smooth(voltaje1,cuanto))
    desfa=desfasaje(tiempo1, smooth(voltaje1,cuanto),smooth(voltaje2,cuanto))
    vpp1=vpp(tiempo1,voltaje1)
    vpp2=vpp(tiempo2,voltaje2)
    vrms1=vpp(tiempo1,voltaje1)
    vrms2=vpp(tiempo2,voltaje2)
    
    frecuencias=np.append(frecuencias,frec)
    desfasajes=np.append(desfasajes,desfa)
    voltaje_pp_ch1=np.append(voltaje_pp_ch1,vpp1)
    voltaje_pp_ch2=np.append(voltaje_pp_ch2,vpp2)
    voltaje_rms_ch1=np.append(voltaje_rms_ch1,vrms1)
    voltaje_rms_ch2=np.append(voltaje_rms_ch2,vrms2)    
    
    print('Freq %s' % freq[i])
    
 
#OJO QUE NO SE GUARDAN LOS DATOS. Decidan que vale la pena guardar   

#Cierro la comunicación con el equipo (Imortante!)

osci.close()
fungen.close()

#%%
plt.figure(1)
plt.clf()
plt.plot(tiempo1,voltaje1,'.-')
plt.plot(tiempo2,voltaje2,'.-')
plt.plot(tiempo2,smooth(voltaje2,10),'-k')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.grid()
plt.show()

plt.figure(2)
plt.clf()
plt.plot(frecuencias,voltaje_pp_ch1,'.-')
plt.plot(frecuencias,voltaje_pp_ch2,'.-')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.grid()
plt.show()

plt.figure(3)
plt.clf()
plt.plot(freq,desfasajes,'.-')
plt.xlabel('Tiempo [s]')
plt.ylabel('Desfasaje [grados]')
plt.grid()
plt.show()
