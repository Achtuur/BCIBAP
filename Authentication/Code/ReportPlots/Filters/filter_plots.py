import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from numpy.fft import rfftfreq


# b, a = signal.iirnotch(50, 30, 250)
# b, a = signal.butter(4, 1, 'high', fs=250)
b, a = signal.butter(4, (1,100), 'bandpass', fs=250)

w,h = signal.freqz(b, a)
w *= (125 / np.pi) 

fig, ax1 = plt.subplots()

ax1.plot(w, 20 * np.log10(abs(h)), linewidth=1)
ax1.set_ylabel('Amplitude [dB]')
ax1.set_xlabel('Frequency [Hz]')

plt.show(block=True)