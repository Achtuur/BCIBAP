from turtle import shape
from pprint import pprint
import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import pywt
from pathlib import Path
import sys
sys.path.append('..\Code\Preprocessing')
from prepare_data import crop
from Filters import Filter
from Pipeline import Pipeline
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
    def stats(coeff):
        statlib = {}
        for i in range(len(coeff)):
            MAV = np.mean(np.abs(coeff[i]))
            AVP = np.mean(np.square(coeff[i]))
            SD = np.std(coeff[i])
            VAR = np.var(coeff[i])
            SKEW = sp.stats.skew(coeff[i])
            KURT = sp.stats.kurtosis(coeff[i])
            statlib[f'D{i}'] = [MAV, AVP, SD, VAR, SKEW, KURT]
        return statlib




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
    cal_eeg_data = Pipeline(raw_cal).start()


    # Regular data
    data_path = Path('Data/recorded_data/recordings_numpy/OpenBCI-RAW-2022-05-06_15-40-45.npy')
    data = np.load(data_path)
    cropped_data = crop(data, t_window, f_sampling)
    raw = np.concatenate((cropped_data[2], cropped_data[3], cropped_data[4], cropped_data[5]))
    # raw = np.concatenate((cropped_data[2], cropped_data[3]))
    eeg_data = Pipeline(raw, cal_eeg_data).start(plot=False)
    print(eeg_data.shape)
    one_channel = eeg_data[:, 0]
    coefficients = Wavelet.coefficients(one_channel, plot=True)
    stats = Wavelet.stats(coefficients)
    pprint(stats)


