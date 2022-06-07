from signal import signal
import numpy as np
from pathlib import Path

from Filters import Filter
from Visualize import DataPlot

class PreprocessingPipeline():
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def perform_notch_filter(self, eeg_data, f0, q, fs):
        data_notch_filtered = Filter.notch_filter(eeg_data, f0, q, fs)

        return data_notch_filtered 

    def perform_high_pass_filter(self, eeg_data, order, cutoff, fs):
        data_high_pass_filtered = Filter.high_pass_filter(eeg_data, order, cutoff, fs)
        
        return data_high_pass_filtered

    def perform_band_pass_filter(self, eeg_data, order, crit_range, fs):
        data_band_pass_filtered = Filter.band_pass_filter(eeg_data, order, crit_range, fs)

        return data_band_pass_filtered

    def perform_band_stop_filter(self, eeg_data, order, crit_range, fs):
        data_band_stop_filtered = Filter.band_stop_filter(eeg_data, order, crit_range, fs)

        return data_band_stop_filtered

    def start(self, plot=False, v=False):
        clean_data = self.raw_data
        if v:
            print("Apply Band Pass Filter")
        clean_data = self.perform_band_pass_filter(clean_data, 4, (4,90), 250)
        if plot:
            DataPlot.eeg_channels_plot(clean_data)

        if v:
            print("Apply Bandstop filter")
        clean_data = self.perform_band_stop_filter(clean_data, 4, (48,52),250)

        return clean_data


if __name__ == '__main__':
    
    # # Initialise config variables
    # f_sampling = 250
    # t_window = 10

    # # Regular data
    data_path = Path('../../Data/ExperimentResults/recorded_data/_unused/OpenBCI-RAW-2022-05-06_15-40-45.npy')
    data = np.load(data_path)[1000:3000]
    # data = np.load(data_path)[1000:]
    data = PreprocessingPipeline(data).start(plot=True)
    DataPlot.eeg_channels_plot(data)

    