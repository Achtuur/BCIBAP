# This is ugly
from pathlib import Path
import sys
import platform
if platform.system() == "Windows":
    sys.path.append(str(Path('PipelineComponents/Preprocessing').resolve()))
else:
    sys.path.append(str(Path('../Preprocessing').resolve()))


import numpy as np
from crop import crop
from Filters import Filter
from PreprocessingPipeline import PreprocessingPipeline
from Visualize import DataPlot
import matplotlib.pyplot as plt

def do_fft(data, fs, plot=False):
    fs = fs
    #
    fft_vals = np.absolute(np.fft.rfft(data, axis=0))
    # Get frequencies for amplitudes in Hz
    fft_freq = np.fft.rfftfreq(len(data), 1.0/fs)
    if plot==True:
        plot_fft(fft_freq, fft_vals)
    return fft_vals, fft_freq

def plot_fft(freq, vals):
    fig, axs = plt.subplots(vals.shape[1],1)
    for i in range(vals.shape[1]):
        axs[i].plot(freq, vals[:,i], linewidth=0.25)
    # plt.plot(freq, vals)
    plt.xlabel("frequency(Hz)")
    plt.ylabel("Amplitude")
    plt.show()

def plot_bands(data):
    eeg_bands = {'Delta': (0, 4),
                'Theta': (4, 8),
                'Alpha': (8, 12),
                'Beta': (12, 30),
                'Gamma': (30, 45)
                }
    fig, axs = plt.subplots(1, data.shape[1])
    for i in range(data.shape[1]):
        axs[i].bar(eeg_bands.keys(), data[:,i])
        plt.xlabel("band")
    plt.ylabel("Energy")
    plt.show()

def get_bands(fft_vals, fft_freq, plot=False):
    for i in range(fft_vals.shape[1]):
        try:
            eeg_bands_channel = np.vstack([eeg_bands_channel, np.array(extract_bands(fft_vals[:,i], fft_freq))])
        except (ValueError, NameError):
            eeg_bands_channel = np.array(extract_bands(fft_vals[:,i], fft_freq))
    if plot==True:
        plot_bands(np.mean(eeg_bands_channel, axis=0))
    return eeg_bands_channel
    

def extract_bands(fft_vals, fft_freq, plot=False):
    # Define EEG bands
    eeg_bands = {'Delta': (0, 4),
                'Theta': (4, 8),
                'Alpha': (8, 12),
                'Beta': (12, 30),
                'Gamma': (30, 45)
                }

    # Take the mean of the fft amplitude for each EEG band
    eeg_band_fft = []
    for i, band in enumerate(eeg_bands):  
        freq_ix = np.where((fft_freq >= eeg_bands[band][0]) & 
                        (fft_freq <= eeg_bands[band][1]))[0]
        eeg_band_fft.append(np.mean(fft_vals[freq_ix]))
    return eeg_band_fft

    
if __name__ == "__main__":
    # Initialise config variables
    f_sampling = 250
    # t_window = 10

    # Regular data
    data_path = Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_first_mental_experiment.npy')
    # The relevant data interval is 1:23 - 2:42
    data = np.load(data_path)[250*83:250*163]
    data = PreprocessingPipeline(data).start()
    
    # Split intervals
    data_task_1 = data[:20*250]
    data_rest_1 = data[20*250:40*250]
    data_task_2 = data[40*250:60*250]
    data_rest_2 = data[60*250:]

    #task1:
    vals, freq = do_fft(data_task_2, f_sampling, plot=False)
    eeg_bands_avg = np.mean(get_bands(vals, freq, plot=False), axis=0)
    #task2:
    vals, freq = do_fft(data_rest_2, f_sampling, plot=False)
    eeg_bands_avg_2 = np.mean(get_bands(vals, freq, plot=False), axis=0)
    print(eeg_bands_avg[2], eeg_bands_avg_2[2])
    data = np.vstack([eeg_bands_avg, eeg_bands_avg_2])
    plot_bands(data.T)
