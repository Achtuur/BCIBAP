from matplotlib import pyplot as plt
from scipy import signal
from scipy.signal import find_peaks
import numpy as np

from ICA import ICA

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
    def filter_ecg(data: np.ndarray, plot: bool):
        ica_mean, mixing_matrix, sources = ICA.construct_ic_sources(data, 7)
        
        # Keep track of which components to drop
        drop: list = []

        # Process each source individually
        for index, source in enumerate(sources.T):
            # 1. Emphasize spikes
            # Filter IC from 8 Hz
            b, a = signal.butter(1, 8, 'high', fs=250)
            filtered_source = signal.filtfilt(b, a, source)

            # Calculate energy according to Teager-Kaiser
            energy: list = []
            for i in range(1, len(filtered_source) - 1):
                E = filtered_source[i]**2 - filtered_source[i+1]*filtered_source[i-1]
                energy.append(E)

            # Add 0 at beginning and end so size is equal
            energy.insert(0,0)
            energy.append(0)

            # Determine Threshold
            q3, q1 = np.percentile(energy, [75, 25])
            iqr = q3 - q1
            threshold = 5.8*iqr + q3

            peaks, _ = find_peaks(energy, height=threshold, distance=220)
            
            # Determine frequency of peaks
            frequencies: list = []
            for i in range(1, len(peaks)):
                if len(peaks) > 1:
                    frequencies.append((peaks[i] - peaks[i-1])/ 250)
            
            # If frequency of peaks is within 1-2 Hz range, the component
            # Can be dropped
            freq = 0
            if len(frequencies) != 0:
                freq = np.median(frequencies)

            if freq != 0 and 1 <= freq <= 2:
                if plot:
                    print('IC to remove')
                    plt.plot(filtered_source)
                    plt.show(block=True)
                drop.append(index)

        # If ECG sources are detected, the component can be set to 0
        for i in drop:
            sources[:, i] = 0
        
        print(f'{len(drop)} IC components removed')
        return np.dot(sources, mixing_matrix.T) + ica_mean
        
