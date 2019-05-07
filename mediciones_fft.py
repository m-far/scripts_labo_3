import numpy as np
from matplotlib import pyplot as plt


def fft_freq(time):
    # genera el vector de frecuencias de la transformada de fourier
    df = 1/np.max(time)
    L =len(time)//2
    f = np.linspace(0,L,L)*df
    return f

def fft(signal):
    # calcula la FFT de manera amigable
    L = len(signal)//2
    sf = np.fft.fft(signal)/L
    out = sf[0:L]
    return out

def fft_get_freq(time,signal):
    # Obtiene la frecuencia principal de una señal temporal
    sf = fft(signal)
    idx_max = np.argmax(np.abs(sf))
    freq = fft_freq(time)
    fmax = freq[idx_max]
    return fmax

def fft_get_amp(time,signal):
    # Obtiene la amplitud a la frecuencia principal
    sf = fft(signal)
    idx_max = np.argmax(np.abs(sf))
    Amp = np.abs(sf[idx_max])
    return Amp

def fft_get_phase_dif(time,signal1,signal2):
    # Calcula el desfasaje de signal2 respecto a signal1 en grados
    s1 = fft(signal1)
    s2 = fft(signal2)
    s = s2/s1
    idx_max = np.argmax(np.abs(s1))
    phase = np.angle(s[idx_max])*180/np.pi
    return phase

## Ejemplo: Genero dos señales oscilando a 100Hz y mido los tres parametros.

f = 100
tau = 1/f
N = 10
t = np.linspace(0,N*tau,1000)
w = 2*np.pi*f
p1 = np.pi/9
p2= np.pi/13
s1 = np.sin(w*t+p1)
s2 = 0.8*np.sin(w*t+p2)

dp_control = 180/3.14*(p2-p1)
fo = fft_get_freq(t,s1)
a1 = fft_get_amp(t,s1)
a2 = fft_get_amp(t,s2)
dp = fft_get_phase_dif(t,s1,s2)






