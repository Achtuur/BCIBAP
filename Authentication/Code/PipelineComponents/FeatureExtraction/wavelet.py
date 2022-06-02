# This is ugly
from pathlib import Path
import sys
import platform
if platform.system() == "Windows":
    sys.path.append(str(Path('PipelineComponents/Preprocessing').resolve()))
else:
    sys.path.append(str(Path('../Preprocessing').resolve()))

from turtle import shape
from pprint import pprint
import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import pywt
from PreprocessingPipeline import PreprocessingPipeline
from Filters import Filter
from Visualize import DataPlot

class Wavelet():

    @staticmethod
    def coefficients(data, plot=False):
        # coeff = pywt.wavedec(data, 'db2', level=4)
        coeff = pywt.wavedec(data, "db2", level=4)
        if plot == True:
            Wavelet.plot_wavelet(data, coeff[0], coeff[1])
        return coeff
    
    @staticmethod
    def plot_wavelet(data, cA, cD):
        plt.plot(cA, label="approximation coefficients")
        plt.plot(cD, label="detail coefficients")
        plt.legend(loc="best")
        plt.show()

    @staticmethod
    def stats_dwt(coeff):
        statlib = {}
        statlist = []
        for i in range(len(coeff)):
            MAX = np.max(np.abs(coeff[i]))
            MIN = np.min(np.abs(coeff[i]))
            MAV = np.mean(np.abs(coeff[i]))
            AVP = np.mean(np.square(coeff[i]))
            SD = np.std(coeff[i])
            VAR = np.var(coeff[i])
            SKEW = sp.stats.skew(coeff[i])
            KURT = sp.stats.kurtosis(coeff[i])
            statlib[f'D{i}'] = [MAV, AVP, SD, VAR, SKEW, KURT, MAX, MIN]
            statlist.append([MAV, AVP, SD, VAR, SKEW, KURT, MAX, MIN])
        return statlib, statlist
    
    @staticmethod
    def stats(channel):
        statlist = []
        MAX = np.max(np.abs(channel))
        MIN = np.min(np.abs(channel))
        MAV = np.mean(np.abs(channel))
        AVP = np.mean(np.square(channel))
        SD = np.std(channel)
        VAR = np.var(channel)
        SKEW = sp.stats.skew(channel)
        KURT = sp.stats.kurtosis(channel)
        statlist.append([MAV, AVP, SD, VAR, SKEW, KURT, MAX, MIN])
        return statlist





        # print(np.shape(MAV))

if __name__ == "__main__":
# Initialise config variables
    f_sampling = 250
    t_window = 10

    # Calibration Data
    cal_data_path = Path('Data/recorded_data/recordings_numpy/OpenBCI-RAW-2022-05-02_15-07-38.npy')
    cal_data = np.load(cal_data_path)
    cropped_cal_data = crop(cal_data, t_window, f_sampling)
    raw_cal = np.concatenate((cropped_cal_data[10], cropped_cal_data[11], cropped_cal_data[12], cropped_cal_data[13]))
    cal_eeg_data = PreprocessingPipeline(raw_cal).start()


    # Regular data
    data_path = Path('Data/recorded_data/recordings_numpy/OpenBCI-RAW-2022-05-06_15-40-45.npy')
    data = np.load(data_path)
    cropped_data = crop(data, t_window, f_sampling)
    raw = np.concatenate((cropped_data[2], cropped_data[3], cropped_data[4], cropped_data[5]))
    # raw = np.concatenate((cropped_data[2], cropped_data[3]))
    eeg_data = PreprocessingPipeline(raw, cal_eeg_data).start(plot=False)
    print(eeg_data.shape)
    one_channel = eeg_data[:, 0]
    coefficients = Wavelet.coefficients(one_channel, plot=True)
    print(type(coefficients))
    statslib, statslist = Wavelet.stats(coefficients)
    pprint(statslist)