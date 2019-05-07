# -*- coding: utf-8 -*-
"""
Created on Mon May  6 16:34:37 2019

@author: m-far
"""
# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# %%
# cargo los datos
datos=np.loadtxt('0.01uFy1H.csv', delimiter=',',skiprows=1)

# %% Acomodo los datos para sacarles los offset de más
tiempoaux=datos[122:1500,0]
voltajeaux=datos[122:1500,1]
tiempo = tiempoaux - tiempoaux[0]
voltaje = voltajeaux - np.mean(voltajeaux)
error=voltaje*0.03
# %% Veo que pinta tienen los datos
plt.plot(tiempo,voltaje,'r.', label='Voltaje sobre capacitor')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.legend()
plt.grid()
#plt.savefig('datosadquiridos.pdf')
plt.show()

# %%
def transitorio_RLC(t,tini,Tau,A,Omega,offset):
    I= A * (np.exp(-(t-tini)/Tau)) * np.sin(Omega * (t-tini))+offset
    return I
 
# %%  Pongo a ojo los parámetros
R = 342
C = 0.01e-6
L = 1
tau=0.00422
t0=0
omega = (np.sqrt((1/(L*C)) - ((R/(2*L))**2)))
amp=6
b=0
modelo=transitorio_RLC(tiempo,t0,tau,amp,omega,b)

# %% ploteo a ver si tiene sentido
plt.figure(num=None, figsize=(8, 6))
plt.errorbar(tiempo,voltaje,yerr=error, fmt='r.', label='Carga Capacitor')
plt.plot(tiempo,modelo ,'-g', linewidth=2.5, label='Modelo')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.legend(loc='best')
plt.grid()
#plt.savefig('modelocarga.pdf')
plt.show()


# %%
# Hago el ajuste 
pini=[t0,tau,amp,omega,b]  
popt, pcov = curve_fit(transitorio_RLC, tiempo, voltaje, sigma = error, p0=pini)
#popt, pcov = curve_fit(transitorio_RLC, tiempo, voltaje, sigma = error_carga)
sigmas = [pcov[0,0],pcov[1,1],pcov[2,2],pcov[3,3],pcov[4,4]]
print(popt, sigmas)

# %%
# ploteo datos vs ajuste para la descarga
plt.figure(num=None, figsize=(8, 6))
plt.errorbar(tiempo,voltaje,yerr=error, fmt='r.-', label='Carga Capacitor')
plt.plot(tiempo, transitorio_RLC(tiempo,popt[0],popt[1],popt[2],popt[3],popt[4]),'-g', linewidth=2.5, label='Ajuste')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.legend(loc='best')
plt.grid()
#plt.savefig('ajustecarga.pdf')
plt.show()
