import numpy as np
from pathlib import Path
import sys
sys.path.append('..\Code\Preprocessing')
from prepare_data import crop
from Filters import Filter
from Pipeline import Pipeline
from Visualize import DataPlot
import matplotlib.pyplot as plt


def do_fft(data, fs, plot=True):
    fs = fs
    #
    fft_vals = np.absolute(np.fft.rfft(data))
    # Get frequencies for amplitudes in Hz
    fft_freq = np.fft.rfftfreq(len(data), 1.0/fs)
    if plot==True:
        plot_fft(fft_freq, fft_vals)
    return fft_vals, fft_freq

def plot_fft(freq, vals):
    plt.plot(freq, vals)
    plt.xlabel("frequency(Hz)")
    plt.ylabel("Amplitude")

def plot_bands(eeg_band_fft):
    values = [eeg_band_fft[band] for band in eeg_band_fft.keys()]
    plt.figure(2)
    plt.bar(eeg_band_fft.keys(), values)
    plt.xlabel("band")
    plt.ylabel("Energy")
    plt.show()


def extract_bands(fft_vals, fft_freq, plot=True):
    # Define EEG bands
    eeg_bands = {'Delta': (0, 4),
                'Theta': (4, 8),
                'Alpha': (8, 12),
                'Beta': (12, 30),
                'Gamma': (30, 45)}

    # Take the mean of the fft amplitude for each EEG band
    eeg_band_fft = dict()
    for band in eeg_bands:  
        freq_ix = np.where((fft_freq >= eeg_bands[band][0]) & 
                        (fft_freq <= eeg_bands[band][1]))[0]
        eeg_band_fft[band] = np.mean(fft_vals[freq_ix])
    if plot==True:
        plot_bands(eeg_band_fft)
    return eeg_band_fft
    
if __name__ == "__main__":
    data_path = Path('../Code/Data/recorded_data/recordings_numpy/OpenBCI-RAW-2022-05-02_15-07-38.npy')
    f_sampling = 250
    t_window = 10

    data = np.load(data_path)
    cropped_data = crop(data, t_window, f_sampling, skip=83)
    # DataPlot.eeg_channels_plot(cropped_data[0])

    # Prepare and start pipelines
    pipeline = Pipeline(cropped_data[1])
    filtered_data = pipeline.start(plot=False)
    print("filtered_data shape:", filtered_data.shape)
    one_channel = filtered_data[:, 0]
    print("one_channel shape:", one_channel.shape)
    vals, freq = do_fft(one_channel, f_sampling)
    eeg_band_fft = extract_bands(vals, freq)
    print("eeg_bands_dict:", eeg_band_fft)
