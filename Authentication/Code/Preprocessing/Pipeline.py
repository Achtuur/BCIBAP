import numpy as np
from pathlib import Path

from prepare_data import crop
from Filters import Filter
from Visualize import DataPlot

class Pipeline():
    def __init__(self, data):
        self.data = data

    def perform_notch_filter(self):
        data_notch_filtered = np.empty(self.data.shape)
        for channel in range(self.data.shape[1]):
            result = np.array(Filter.notch_filter(self.data[:,channel], 50, 30, 250)).T
            data_notch_filtered[:, channel] = result 
        self.data = data_notch_filtered

    def perform_high_pass_filter(self):
        data_high_pass_filtered = np.empty(self.data.shape)
        for channel in range(self.data.shape[1]):
            result = np.array(Filter.notch_filter(self.data[:,channel], 50, 30, 250)).T
            data_high_pass_filtered[:, channel] = result 
        self.data = data_high_pass_filtered

    def remove_ecg(self):
        self.data = Filter.filter_ecg(self.data)
        


    def start(self):
        # Required for plotting differences
        raw_data = self.data
        # DataPlot.eeg_channels_plot(raw_data)

        # Notch filter
        self.perform_notch_filter()

        # High pass filter
        self.perform_high_pass_filter()

        # Remove ECG
        self.remove_ecg()

        DataPlot.eeg_channels_plot(self.data)
        # DataPlot.plot_difference(raw_data, self.data)
        

if __name__ == '__main__':
    # Initialise data
    data_path = Path('../Data/recorded_data/recordings_numpy/OpenBCI-RAW-2022-05-02_15-07-38.npy')
    f_sampling = 250
    t_window = 5
    data = np.load(data_path)
    cropped_data = crop(data, t_window, f_sampling)

    # Prepare and start pipeline
    pipeline = Pipeline(cropped_data[10])
    filtered_data = pipeline.start()


