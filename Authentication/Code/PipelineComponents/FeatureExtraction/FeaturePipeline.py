# This is ugly
from pathlib import Path
import sys
import platform
from extract import do_fft, get_bands
from AnalysisMentalTaskCyril import average_power
from Filters import Filter
if platform.system() == "Windows":
    sys.path.append(str(Path('PipelineComponents/Preprocessing').resolve()))
else:
    sys.path.append(str(Path('../Preprocessing').resolve()))


from wavelet import Wavelet
import numpy as np
from PreprocessingPipeline import PreprocessingPipeline
from wavelet import Wavelet
from PreprocessingPipeline import PreprocessingPipeline
from pprint import pprint
class FeaturePipeline():

    def __init__(self, input_data, f_sampling):
        self.input_data = input_data
        self.f_sampling = f_sampling

    def perform_bands_power(self, eeg_data):
        vals, freq = do_fft(eeg_data, self.f_sampling, plot=False)
        eeg_bands = get_bands(vals, freq, plot=False)
        return eeg_bands


    def perform_wavelet(self, eeg_data, plot=False):
        data_dwt = []
        for channel in range(eeg_data.shape[1]):
            result = Wavelet.coefficients(eeg_data[:,channel], plot=plot)
            data_dwt.append(result) 
        return data_dwt  

    def perform_statistics_dwt(self, dwt_data):
        stats_dwt = []
        for channel in range(len(dwt_data)):
            _ , result_lst = Wavelet.stats_dwt(dwt_data[channel])
            stats_dwt.append(result_lst)
        return np.array(stats_dwt)
    
    def perform_statistics_raw(self, data):
        stats_dwt = []
        for channel in range(data.shape[1]):
            result_lst = Wavelet.stats(data[:, channel])
            stats_dwt.append(result_lst)
        return np.array(stats_dwt)
    
    def NormalizeData(self, data):
        return (data - np.min(data)) / (np.max(data) - np.min(data))

    def start(self, segment, plot=False):
        # for i, segment in enumerate(self.input_data):
            # bands = self.perform_bands_power(segment)
            # av_overall, av_per_channel = average_power(Filter.band_pass_filter(segment, 4, (12,  18), 250))
        dwt_data = self.perform_wavelet(segment, plot=plot)
        stats_dwt = self.perform_statistics_dwt(dwt_data).reshape(1, 320)
            # stats = self.perform_statistics_raw(segment).reshape(1, 64)
            # print(bands.shape)
            # vals, _ = do_fft(segment, self.f_sampling)
            # if i==0:
            # # #     # features = vals.reshape(1, vals.shape[0]*vals.shape[1])
            # #     # features = av_per_channel.reshape(1, 8)
            #     features = stats_dwt
            # else: 
            # # #     # features = np.vstack((features, vals.reshape(1, vals.shape[0]*vals.shape[1])))
            # #     # features = np.vstack((features, av_per_channel.reshape(1, 8)))
            #     features = np.vstack((features, stats_dwt))
        return stats_dwt

    def perform_fft(self, eeg_data):
        eeg_fft = np.fft(eeg_data)
        return eeg_fft



if __name__ == "__main__":
    # pass
    # Initialise config variables
    f_sampling = 250
    t_window = 10


    # # Calibration Data
    # cal_data_path = Path('Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_calibration.npy')
    # cal_data = np.load(cal_data_path)
    # cropped_cal_data = crop(cal_data, t_window, f_sampling)
    # raw_cal = np.concatenate((cropped_cal_data[4], cropped_cal_data[5], cropped_cal_data[6], cropped_cal_data[7]))
    # cal_eeg_data = PreprocessingPipeline(raw_cal).start()



    # # Regular data
    # data_path = Path('Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_music.npy')
    # data = np.load(data_path)
    # cropped_data = crop(data, t_window, f_sampling)
    # raw = np.concatenate((cropped_data[2], cropped_data[3], cropped_data[4], cropped_data[5]))
    # eeg_data = PreprocessingPipeline(raw, cal_eeg_data).start()

    # #Wavelet transform
    # stats_dwt = FeaturePipeline(eeg_data).start()
    # stats_dwt = np.array(stats_dwt).reshape(240, 1)
    # print(stats_dwt.shape)

