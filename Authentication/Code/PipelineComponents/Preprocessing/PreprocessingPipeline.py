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

    def start(self, plot=False, v=False):
        clean_data = self.raw_data
        # High pass filter
        if v:
            print("Apply High Pass Filter")
        clean_data = self.perform_high_pass_filter(clean_data, 4, 1, 250)
        if plot:
            DataPlot.eeg_channels_plot(clean_data)


        # Notch filter
        if v:
            print("Apply Notch Filter")
        clean_data = self.perform_notch_filter(clean_data, 50, 30, 250)
        if plot:
            DataPlot.eeg_channels_plot(clean_data)


 
        # ASR if pipeline has calibrated data
        # if self.cal_data is not None:
        #     if v:
        #         print("Removing artifacts")
        #     clean_data = self.remove_artifacts(clean_data)
        #     if plot:
        #         DataPlot.eeg_channels_plot(clean_data)


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

    