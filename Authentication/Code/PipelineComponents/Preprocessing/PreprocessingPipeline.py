from signal import signal
import numpy as np
from pathlib import Path

from Filters import Filter
from Visualize import DataPlot

class PreprocessingPipeline():
    def __init__(self, raw_data, cal_data=None):
        self.raw_data = raw_data
        self.cal_data = cal_data

    def perform_notch_filter(self, eeg_data):
        data_notch_filtered = np.empty(eeg_data.shape)
        for channel in range(eeg_data.shape[1]):
            result = np.array(Filter.notch_filter(eeg_data[:,channel], 50, 30, 250))
            data_notch_filtered[:, channel] = result 

        return data_notch_filtered 

    def perform_high_pass_filter(self, eeg_data):
        data_high_pass_filtered = np.empty(eeg_data.shape)
        for channel in range(eeg_data.shape[1]):
            result = np.array(Filter.high_pass_filter(eeg_data[:, channel], 4, 1))
            data_high_pass_filtered[:, channel] = result 
        
        return data_high_pass_filtered

    def remove_artifacts(self, eeg_data):
        data_artifacts_removed = Filter.filter_artifacts(eeg_data, self.cal_data)

        return data_artifacts_removed

    @staticmethod
    def remove_bad_channels(data: np.ndarray, threshold_val=False):
        # Empirically chosen
        threshold = threshold_val if threshold_val else 2000

        try:
            channels = data.shape[1]
            for channel in range(channels):
                square = np.vectorize(lambda x: x**2)
                signal_power = np.sum(square(data[:, channel])) / data.shape[0]
                data[:, channel] = 0 if signal_power > threshold else data[:, channel]
        except:
            square = np.vectorize(lambda x: x**2)
            signal_power = np.sum(square(data)) / data.shape[0]
            data = 0 if signal_power > threshold else data

        return data 

    def start(self, plot=False, v=False):
        clean_data = self.raw_data
        # High pass filter
        if v:
            print("Apply High Pass Filter")
        clean_data = self.perform_high_pass_filter(clean_data)
        if plot:
            DataPlot.eeg_channels_plot(clean_data)


        # Notch filter
        if v:
            print("Apply Notch Filter")
        clean_data = self.perform_notch_filter(clean_data)
        if plot:
            DataPlot.eeg_channels_plot(clean_data)

        # # ASR if pipeline has calibrated data
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
    data = PreprocessingPipeline(data).start()
    DataPlot.eeg_channels_plot(data)
    data_bad_channels = PreprocessingPipeline.remove_bad_channels(data)
    DataPlot.eeg_channels_plot(data_bad_channels)