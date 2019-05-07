# -*- coding: utf-8 -*-
"""
Created on Mon May  6 16:15:05 2019

@author: m-far
"""
# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# %%
# cargo los datos
datos=np.loadtxt('datos_carga.txt')
# %%
# separo las columnas en vectores independientes
tiempocarga=datos[:,0]
voltaje=datos[:,1]

# %% Veo que pinta tienen los datos
plt.plot(tiempocarga,voltaje,'r.', label='Voltaje sobre capacitor')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.legend()
plt.grid()
#plt.savefig('datosadquiridos.pdf')
plt.show()

# %%
# Para que el ajuste no tire error nesecito tener todos los datos mayores a 
# cero, por lo que le resto el más negativo y le sumo un cachito
voltajecarga=(voltaje-voltaje[0]+0.1)
error_carga = voltajecarga*0.03

# %%
# me armo la funcion del voltaje transitorio sobre el capacitor
def transitorio_RC(t,Tau,Vinicial,Vfuente):
    Vc=Vinicial + (Vfuente-Vinicial)* (1-np.exp(-t/(Tau)))
    return Vc

# %%
# ploteo los datos vs la funcion con parametros a ojo para la carga
tau=0.008
vinicial=0
vfuente=6.5
plt.figure(num=None, figsize=(8, 6))
plt.errorbar(tiempocarga,voltajecarga,yerr=error_carga, fmt='r.-', label='Carga Capacitor')
plt.plot(tiempocarga, transitorio_RC(tiempocarga,tau,vinicial,vfuente),'-g', linewidth=2.5, label='Modelo')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.legend(loc='best')
plt.grid()
#plt.savefig('modelocarga.pdf')
plt.show()

# %%
# Hago el ajuste para la carga
#pini=[0.008,6,0]
popt_carga, pcov_carga = curve_fit(transitorio_RC, tiempocarga, voltajecarga, sigma = error_carga)
sigmas_carga = [pcov_carga[0,0],pcov_carga[1,1],pcov_carga[2,2]]
print(popt_carga, sigmas_carga)

# %%
# ploteo datos vs ajuste para la descarga
plt.figure(num=None, figsize=(8, 6))
plt.errorbar(tiempocarga,voltajecarga,yerr=error_carga, fmt='r.-', label='Carga Capacitor')
plt.plot(tiempocarga, transitorio_RC(tiempocarga,popt_carga[0],popt_carga[1],popt_carga[2]),'-g', linewidth=2.5, label='Ajuste')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')
plt.legend(loc='best')
plt.grid()
#plt.savefig('ajustecarga.pdf')
plt.show()