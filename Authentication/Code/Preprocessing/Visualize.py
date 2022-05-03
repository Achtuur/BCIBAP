from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from prepare_data import crop

class DataPlot():
    @staticmethod
    def eeg_channels_plot(data: np.ndarray):
        # This programming method allows for multiple or singular EEG channel plots
        try:
            num_col = data.shape[1]
        except IndexError:
            num_col = 1
        
        try:
            fix, axs = plt.subplots(num_col,1)
            for i in range(num_col):
                axs[i].plot(data[:,i])
        except TypeError:
            plt.plot(data[:])

        plt.show(block=True)

    # @staticmethod
    # def eeg_combined_channels_plot(data: np.ndarray):
    #     try:
    #         num_col = data.shape[1]
    #     except IndexError:
    #         num_col = 1
        
    #     for i in range(num_col):
    #         plt.plot(np.linalg.norm(data[:, i]))

    #     plt.show(block=True)

if __name__ == '__main__':
    data_path = Path('../Data/recorded_data/recordings_numpy/OpenBCI-RAW-2022-05-02_15-07-38.npy')
    f_sampling = 250
    t_window = 10

    data = np.load(data_path)
    cropped_data = crop(data, t_window, f_sampling)
    DataPlot.eeg_channels_plot(cropped_data[8])
