from signal import signal
import numpy as np
from pathlib import Path

from Filters import Filter
from Visualize import DataPlot

class PreprocessingPipeline():
    def __init__(self, raw_data, cal_data=None):
        self.raw_data = raw_data
        self.cal_data = cal_data

    def perform_notch_filter(self, eeg_data, f0, q, fs):
        data_notch_filtered = Filter.notch_filter(eeg_data, f0, q, fs)

        return data_notch_filtered 

    def perform_high_pass_filter(self, eeg_data, order, cutoff, fs):
        data_high_pass_filtered = Filter.high_pass_filter(eeg_data, order, cutoff, fs)
        
        return data_high_pass_filtered

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
            common_mode = np.zeros(data.shape[0])
            for key, value in bad_channels.items():
                if value == 0:
                    common_mode = np.add(common_mode, data[:, key])

            common_mode = common_mode / sum(list(bad_channels.values()))

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

        return clean_data


if __name__ == '__main__':
    
    # # Initialise config variables
    # f_sampling = 250
    # t_window = 10

    # # Regular data
    data_path = Path('../../Data/ExperimentResults/recorded_data/_unused/OpenBCI-RAW-2022-05-06_15-40-45.npy')
    data = np.load(data_path)[1000:3000, 0]
    # data = np.load(data_path)[1000:]
    data = PreprocessingPipeline(data).start(plot=True)
    data = PreprocessingPipeline.remove_bad_channels(data)
    DataPlot.eeg_channels_plot(data)

    