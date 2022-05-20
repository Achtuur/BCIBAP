from matplotlib import pyplot as plt
from scipy import signal
from scipy.signal import find_peaks
import numpy as np
from pathlib import Path

from Visualize import DataPlot

class Filter():
    @staticmethod
    def notch_filter(data: np.ndarray, f0: float, Q: float, fs: float) -> np.ndarray:
        b, a = signal.iirnotch(f0, Q, fs)
        notch_filtered_data = signal.filtfilt(b, a, data)
        return notch_filtered_data

    @staticmethod
    def high_pass_filter(data: np.ndarray, order: int, crit_freq: float, fs: float):
        b, a = signal.butter(order, crit_freq, 'high', fs=fs)
        high_pas_filtered_data = signal.filtfilt(b, a, data)
        return high_pas_filtered_data

    @staticmethod
    def band_pass_filter(data: np.ndarray, order: int, crit_range: tuple, fs: float):
        b, a = signal.butter(order, crit_range, 'bandpass', fs=fs)
        # Just discovered that you don't have to filter per channel, oops
        band_pass_filtered = signal.filtfilt(b, a, data, axis=0)
        return band_pass_filtered

    
if __name__ == '__main__':
    data_path = Path('../../Data/ExperimentResults/recorded_data/_unused/OpenBCI-RAW-2022-05-06_15-40-45.npy')
    data = np.load(data_path)[1000:3000]
    
    data_notch_filtered = np.empty(data.shape)
    for channel in range(data.shape[1]):
        result = np.array(Filter.notch_filter(data[:,channel], 50, 30, 250))
        data_notch_filtered[:, channel] = result 

    data_high_pass_filtered = np.empty(data_notch_filtered.shape)
    for channel in range(data_notch_filtered.shape[1]):
        result = np.array(Filter.high_pass_filter(data_notch_filtered[:, channel], 4, 1, 250))
        data_high_pass_filtered[:, channel] = result 

    DataPlot.eeg_channels_plot(data_high_pass_filtered)
    data_bp_filtered = Filter.band_pass_filter(data_high_pass_filtered, 4, (20,40), 250)
    DataPlot.eeg_spectrum_plot(data_bp_filtered)
        