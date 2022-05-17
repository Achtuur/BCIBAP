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

        # ASR if pipeline has calibrated data
        if self.cal_data is not None:
            if v:
                print("Removing artifacts")
            clean_data = self.remove_artifacts(clean_data)
            if plot:
                DataPlot.eeg_channels_plot(clean_data)

        return clean_data
        

if __name__ == '__main__':
    pass
    # # Initialise config variables
    # f_sampling = 250
    # t_window = 10

    # # Calibration Data
    # cal_data_path = Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_calibration.npy')
    # cal_data = np.load(cal_data_path)
    # cropped_cal_data = crop(cal_data, t_window, f_sampling)
    # raw_cal = np.concatenate((cropped_cal_data[7], cropped_cal_data[8], cropped_cal_data[9], cropped_cal_data[10]))
    # cal_eeg_data = PreprocessingPipeline(raw_cal).start(plot=True)



    # # Regular data
    # data_path = Path('../Data/recorded_data/recordings_numpy/OpenBCI-RAW-2022-05-06_15-40-45.npy')
    # data = np.load(data_path)
    # cropped_data = crop(data, t_window, f_sampling)
    # raw = np.concatenate((cropped_data[2], cropped_data[3], cropped_data[4], cropped_data[5]))
    # eeg_data = PreprocessingPipeline(raw, cal_eeg_data).start()
