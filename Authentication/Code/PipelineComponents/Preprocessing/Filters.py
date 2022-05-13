from matplotlib import pyplot as plt
from scipy import signal
from scipy.signal import find_peaks
import numpy as np
from pathlib import Path

from meegkit.asr import ASR
from meegkit.utils.matrix import sliding_window


class Filter():
    @staticmethod
    def notch_filter(data: np.ndarray, f0: float, Q: float, fs: float) -> np.ndarray:
        b, a = signal.iirnotch(f0, Q, fs)
        notch_filtered_data = signal.filtfilt(b, a, data)
        return notch_filtered_data

    @staticmethod
    def high_pass_filter(data: np.ndarray, order: int, crit_freq: float):
        b, a = signal.butter(order, crit_freq, 'high', fs=250)
        high_pas_filtered_data = signal.filtfilt(b, a, data)
        return high_pas_filtered_data

    @staticmethod
    def filter_artifacts(data: np.ndarray, cal_data: np.ndarray):
        # This value is hardcoded for now
        f_sampling = 250

        # The data is transposed, because that is the required format for the ASR package
        data = data.T
        cal_data = cal_data.T

        asr = ASR(method='euclid')
        train_idx = np.arange(0, data.shape[1], dtype=int)
        _, sample_mask = asr.fit(cal_data)
    
        X = sliding_window(data, window=int(f_sampling), step=int(f_sampling))
        Y = np.zeros_like(X)
        for i in range(X.shape[1]):
            Y[:, i, :] = asr.transform(X[:, i, :])

        clean = Y.reshape(-1, 8)

        return clean

    
if __name__ == '__main__':
    data_path = Path('../Data/recorded_data/recordings_numpy/OpenBCI-RAW-2022-05-06_15-40-45.npy')
    f_sampling = 250
    t_window = 10
    data = np.load(data_path)
    cropped_data = crop(data, t_window, f_sampling)
    
    # ASR method
    asr = ASR(method='euclid')
    
    