from cProfile import label
import numpy as np
from numpy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt

def get_fft(data: np.ndarray):
    y_fft = rfft(data)
    f = rfftfreq(data.shape[0], 1/250) 
    return f, y_fft

class DataPlot():
    @staticmethod
    def eeg_channels_plot(data: np.ndarray):
        # This programming method allows for multiple or singular EEG channel plots
        try:
            num_col = data.shape[1]
        except IndexError:
            num_col = 1
        
        try:
            fig, axs = plt.subplots(num_col,1)
            for i in range(num_col):
                axs[i].plot(data[:,i], linewidth=0.25, label="EEG signal")
            return fig, axs, plt
        except TypeError:
            plt.plot(data[:], linewidth=1, label="EEG signal")
            return plt

    @staticmethod
    def eeg_spectrum_plot(data: np.ndarray):
        # This programming method allows for multiple or singular EEG channel plots
        try:
            num_col = data.shape[1]
        except IndexError:
            num_col = 1

        try:
            fig, axs = plt.subplots(num_col, 1)
            for i in range(num_col):
                f, y = np.abs(get_fft(data[:,i]))
                axs[i].plot(f, y)

        except IndexError:
            f, y = np.abs(get_fft(data[:]))
            plt.plot(f, y)

        plt.show(block=True)
        

    @staticmethod
    def plot_difference(data: np.ndarray, filtered_data: np.ndarray):
        # If the shape is not the same, it can't be guaranteed that the same channels are used
        # if data.shape != filtered_data.shape:
        #     raise ValueError

        try:
            num_col = data.shape[1]
        except IndexError:
            num_col = 1

        try:
            fix, axs = plt.subplots(num_col,1)
            for i in range(num_col):
                axs[i].plot(data[:,i])
                axs[i].plot(filtered_data[:,i])
                plt.legend(['Original', 'Filtered'])
        except TypeError:
            plt.plot(data[:])
            plt.plot(filtered_data[:])
            plt.legend(['Original', 'Filtered'])

        plt.show(block=True)

if __name__ == '__main__':
    pass
    # import platform
    # import sys
    # from pathlib import Path
    # if platform.system() == "Windows":
    #     sys.path.append(str(Path('PipelineComponents/Preprocessing').resolve()))
    #     sys.path.append(str(Path('PipelineComponents/FeatureExtraction').resolve()))
    #     sys.path.append(str(Path('Data/ExperimentResults').resolve()))
    # else:
    #     sys.path.append(str(Path('./PipelineComponents/Preprocessing').resolve()))
    #     sys.path.append(str(Path('./PipelineComponents/FeatureExtraction').resolve()))
    #     sys.path.append(str(Path('./Data/ExperimentResults').resolve()))

    # from PreprocessingPipeline import PreprocessingPipeline

    # data_path = Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_music.npy')
    
    # f_sampling = 250
    # t_window = 10

    # data = np.load(data_path)
    # cropped_data = crop(data, t_window, f_sampling)
    # data = PreprocessingPipeline(cropped_data[10]).start()
    # DataPlot.eeg_spectrum_plot(data)
