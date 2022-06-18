from tkinter import font
from matplotlib import style
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from numpy.fft import rfftfreq


# b, a = signal.iirnotch(50, 60, 250)
# b, a = signal.butter(4, 1, 'high', fs=250)
b, a = signal.butter(4, (5,90), 'bandpass', fs=250)
# b, a = signal.butter(4, (48,52), 'bandstop', fs=250)

w,h = signal.freqz(b, a)
w *= (125 / np.pi) 

fig, ax1 = plt.subplots(figsize=(10,5))

ax1.plot(w[:], 20 * np.log10(abs(h[:])), linewidth=1, label='Transfer function')
ax1.set_ylabel('Amplitude [dB]', fontsize=13)
ax1.set_xlabel('Frequency [Hz]', fontsize=13)
ax1.axvline(5, linestyle="--", color="orange", label='Critical frequency')
ax1.axvline(90, linestyle="--", color="orange" )
# plt.title('4th order bandpass filter [5-90 Hz]', fontsize=13)
plt.title('4th order bandpass filter [5-90 Hz]', fontsize=13)
plt.legend(loc='upper right',fontsize=11)
plt.xticks(list(plt.xticks()[0]) + [5,90])
plt.xlim([0,125])
# plt.show(block=True)
plt.savefig('bandpass.png', dpi=400)