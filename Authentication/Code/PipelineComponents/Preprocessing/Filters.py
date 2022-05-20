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
        notch_filtered_data = signal.filtfilt(b, a, data, axis=0)
        return notch_filtered_data

    @staticmethod
    def high_pass_filter(data: np.ndarray, order: int, crit_freq: float, fs: float):
        b, a = signal.butter(order, crit_freq, 'high', fs=fs)
        high_pas_filtered_data = signal.filtfilt(b, a, data, axis=0)
        return high_pas_filtered_data

    @staticmethod
    def band_pass_filter(data: np.ndarray, order: int, crit_range: tuple, fs: float):
        b, a = signal.butter(order, crit_range, 'bandpass', fs=fs)
        band_pass_filtered = signal.filtfilt(b, a, data, axis=0)
        return band_pass_filtered

    
if __name__ == '__main__':
    data_path = Path('../../Data/ExperimentResults/recorded_data/_unused/OpenBCI-RAW-2022-05-06_15-40-45.npy')
    data = np.load(data_path)[1000:3000]
    DataPlot.eeg_channels_plot(data)
    data = Filter.high_pass_filter(data, 4, 1, 250)
    DataPlot.eeg_channels_plot(data)
    data = Filter.notch_filter(data, 50, 30, 250)
    DataPlot.eeg_channels_plot(data)
    data = Filter.band_pass_filter(data, 4, (10,30), 250)
    DataPlot.eeg_channels_plot(data)
        