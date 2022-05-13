import numpy as np
from pathlib import Path
import sys
sys.path.append('Preprocessing')
sys.path.append('../Data/ExperimentResults/recorded_data/recordings_numpy')
from prepare_data import crop
from wavelet import Wavelet
from PreprocessingPipeline import PreprocessingPipeline
from pprint import pprint
class FeaturePipeline():

    def __init__(self, input_data):
        self.input_data = input_data

    def perform_wavelet(self, eeg_data, plot=False):
        data_dwt = []
        for channel in range(eeg_data.shape[1]):
            result = Wavelet.coefficients(eeg_data[:,channel], plot=plot)
            data_dwt.append(result) 
        return data_dwt  

    def perform_statistics(self, dwt_data):
        stats_dwt = []
        for channel in range(len(dwt_data)):
            _ , result_lst = Wavelet.stats(dwt_data[channel])
            stats_dwt.append(result_lst)
        return stats_dwt

    def start(self, plot=False):
        eeg_data = self.input_data
        dwt_data = self.perform_wavelet(eeg_data, plot=plot)
        stats_dwt = self.perform_statistics(dwt_data)
        return stats_dwt



if __name__ == "__main__":
    # Initialise config variables
    f_sampling = 250
    t_window = 10

    # Calibration Data
    cal_data_path = Path('Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_calibration.npy')
    cal_data = np.load(cal_data_path)
    cropped_cal_data = crop(cal_data, t_window, f_sampling)
    raw_cal = np.concatenate((cropped_cal_data[10], cropped_cal_data[11], cropped_cal_data[12], cropped_cal_data[13]))
    cal_eeg_data = PreprocessingPipeline(raw_cal).start()



    # Regular data
    data_path = Path('Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_music.npy')
    data = np.load(data_path)
    cropped_data = crop(data, t_window, f_sampling)
    raw = np.concatenate((cropped_data[2], cropped_data[3], cropped_data[4], cropped_data[5]))
    eeg_data = PreprocessingPipeline(raw, cal_eeg_data).start()

    #Wavelet transform
    stats_dwt = FeaturePipeline(eeg_data).start()

    print(len(stats_dwt),stats_dwt[0], stats_dwt[0][0])

