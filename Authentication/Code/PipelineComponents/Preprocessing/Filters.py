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

    @staticmethod
    def remove_bad_channels(data: np.ndarray, threshold_val=False):
        """
            This function finds bad channels based on the signal power.
            If there is at least one good channel, the bad channels are
            replaced by the average of the good channels.
            Otherwise, the data is set to None so it is later dropped.
        """
        # This dictionary keeps track of the bad channels. 
        # If the input data is a vector, this is not necessary.
        try:
            bad_channels = {i:0 for i in range(data.shape[1])}
        except IndexError:
            pass

        # Value was empirically chosen
        threshold = threshold_val if threshold_val else 1500

        try:
            channels = data.shape[1]
            for channel in range(channels):
                square = np.vectorize(lambda x: x**2)
                signal_power = np.sum(square(data[:, channel])) / len(data[:, channel])

                if signal_power > threshold:
                    bad_channels[channel] = 1

            # Determine the average of the good channels
            # This line filters the bad_channels dictionary for the number of good channels
            num_good_channels: int = len(list(filter(lambda x: x==0, bad_channels.values())))
            
            common_mode = np.zeros(data.shape[0])
            for key, value in bad_channels.items():
                if value == 0:
                    common_mode = np.add(common_mode, data[:, key])

            common_mode = common_mode / num_good_channels

            # Set bad channels to the average
            if sum(list(bad_channels.values())) == data.shape[1]:
                data = None
            else:
                for key, value in bad_channels.items():
                    if value == 1:
                        data[:, key] = common_mode
                        
        except IndexError:
            square = np.vectorize(lambda x: x**2)
            signal_power = np.sum(square(data)) / data.shape[0]
            if signal_power > threshold:
                data = None

        return data

    
if __name__ == '__main__':
    data_path = Path('../../Data/ExperimentResults/recorded_data/_unused/OpenBCI-RAW-2022-05-06_15-40-45.npy')
    data = np.load(data_path)[1000:3000]
    DataPlot.eeg_channels_plot(data)
    data = Filter.high_pass_filter(data, 4, 1, 250)
    DataPlot.eeg_channels_plot(data)
    data = Filter.notch_filter(data, 50, 30, 250)
    DataPlot.eeg_channels_plot(data)
    data = Filter.remove_bad_channels(data)
    DataPlot.eeg_channels_plot(data)
    # data = Filter.band_pass_filter(data, 4, (10,30), 250)
    # DataPlot.eeg_channels_plot(data)
        