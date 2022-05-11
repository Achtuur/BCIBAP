import numpy as np
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
    def doppler(freqs, dt, amp_inc=10, t0=0, f0=np.pi*2):
        t = np.arange(len(freqs)) * dt + t0
        amp = np.linspace(1, np.sqrt(amp_inc), len(freqs))**2
        sig = amp * np.sin(freqs * f0 * t)
        return t,sig

    @staticmethod 
    def noisify(sig, noise_amp=1):
        return sig + (np.random.random(len(sig))-0.5)*2*noise_amp
    

    
    @staticmethod
    def coeff(data, plot=False):
        # coeff = pywt.wavedec(data, 'db2', level=4)
        cA, cD = pywt.dwt(data, "sym12", mode="zero")
        if plot == True:
            Wavelet.plot_wavelet(data, cA, cD)
        return coeff
    
    @staticmethod
    def plot_wavelet(data, cA, cD):
        plt.plot(data, label="raw_data")
        plt.plot(cA, label="approximation coefficients")
        plt.plot(cD, label="detail coefficients")
        plt.legend(loc="best")
        plt.show()


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
    one_channel = eeg_data[:, 0]
    coefficients = Wavelet.coeff(one_channel, plot=True)
    # t_dop, sig_dop = doppler(np.arange(10,20,0.01)[::-1], 0.002)
    # sig_dop_n2 = noisify(sig_dop, noise_amp=2)