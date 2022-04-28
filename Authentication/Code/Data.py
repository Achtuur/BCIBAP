# Required
import numpy as np
import pandas as pd
import scipy
from scipy.io import loadmat
import matplotlib.pyplot as plt

# Temp
from scipy.fft import fft, ifft 

matlab_signal = loadmat('data/subject_00.mat')
data = np.array(matlab_signal['SIGNAL'])
dataset = pd.DataFrame.from_records(data)
dataset.rename(columns={dataset.columns[0]: 'Time'}, inplace=True)

electrodes = ['FP1', 'FP2', 'FC5', 'FC6', 'FZ', 'T7', 'CZ', 'T8', 'P7', 'P3', 'PZ', 'P4', 'P8', 'O1', 'Oz', 'O2']
for index, name in enumerate(electrodes):
    dataset.rename(columns={dataset.columns[index + 1]: name}, inplace=True)

# # FFT
# Fs = 512
# y = np.abs(fft(dataset['FP1'].to_numpy()))
# x = np.linspace(0, len(y), 1/Fs)
# fig = plt.figure()
# plt.plot(x,y)
# fig.savefig('fft.png')

# Plot the
fig, axs = plt.subplots(4,4, figsize=(15,15))
index = 0
for i in range(4):
    for j in range(4):
        axs[i,j].plot(dataset['Time'], dataset[electrodes[index]])
        axs[i,j].set_title(electrodes[index])
        index += 1


fig.savefig('Channels.png')
