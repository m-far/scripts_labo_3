# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 09:52:18 2019

@author: m-far
"""
import numpy as np
import matplotlib.pyplot as plt
#%%
datos=np.loadtxt('datos.txt')
data=datos[:,0:300:10]

#%%
sensibilidad=1
errory= abs(data[1,:])*0.03+0.00001*sensibilidad
x=data[0,:]
y=data[1,:]
plt.errorbar(x,y,errory)
plt.xlabel('Time')
plt.ylabel('Voltage')
plt.grid()
plt.show()

#%%
p,cov = np.polyfit(x,y,1,cov=True,w=1/errory)

#%%
plt.errorbar(x,y,errory,linestyle='',marker='s',markersize=5,capsize=3)
plt.plot(x, p[0]*(x)+p[1],'-')
plt.xlabel('Time')
plt.ylabel('Voltage')
plt.grid()
plt.show()