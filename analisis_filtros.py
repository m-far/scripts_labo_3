# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 09:13:39 2019

@author: m-far
"""
#%%
import numpy as np
import matplotlib.pyplot as plt

#defino escala horizontal lineal
x=np.linspace(0,20,100)

# defino las funciones transferencia, desfasaje y atenuacion
def transferencia(x):
    T=1./np.sqrt(1+(x)**2)
    return T
    

def fase(x):
    phi=-np.arctan(x)*180/np.pi
    return phi
    
def atenuacion(x):
    A=20*np.log10(transferencia(x))
    return A

# Then I plot it all toghether (data and calibration)
plt.figure(1)
plt.subplot(211)
plt.ylabel('T')
plt.plot(x, transferencia(x), 'ro')
plt.subplot(212)
plt.xlabel('w/w0')
plt.ylabel('\phi [grados]')
plt.plot(x, fase(x), 'bo')
plt.grid()
plt.show()

# diagrama de bode, en atenuacion y desfasaje en escala logaritmica
#defino escala horizontal logaritmica

y=np.logspace(-2,4,100);

plt.figure(2)
plt.subplot(211)
plt.semilogx(x,atenuacion(x))
plt.xlabel('\omega/\omega_0')
plt.ylabel('A')
plt.grid()
plt.subplot(212)
plt.semilogx(x,fase(x))
plt.xlabel('\omega/\omega_0')
plt.ylabel('\phi [grados]')
plt.grid()
plt.show()

# valores en la frecuencia de corte
#fprintf('T(wc)=#f\n',T(1))
#fprintf('phi(wc)=#f\n',phi(1))
#fprintf('A(wc)=#f\n',A(1))