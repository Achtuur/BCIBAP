import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from numpy.fft import rfftfreq


# b, a = signal.iirnotch(50, 30, 250)
# b, a = signal.butter(4, 1, 'high', fs=250)
b, a = signal.butter(4, (5,50), 'bandpass', fs=250)

w,h = signal.freqz(b, a)
w *= (125 / np.pi) 

fig, ax1 = plt.subplots()

ax1.plot(w[:300], 20 * np.log10(abs(h[:300])), linewidth=1)
ax1.set_ylabel('Amplitude [dB]')
ax1.set_xlabel('Frequency [Hz]')
plt.title('4th order bandpass filter [5-50 Hz]')

plt.show(block=True)