import sys
import platform
from matplotlib import style
import numpy as np
import csv
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import normalize
from numpy.fft import rfft, rfftfreq


if platform.system() == "Windows":
    sys.path.append(str(Path('PipelineComponents/Preprocessing').resolve()))
    sys.path.append(str(Path('PipelineComponents/FeatureExtraction').resolve()))
    sys.path.append(str(Path('Data/ExperimentResults').resolve()))
    sys.path.append(str(Path('Data').resolve()))
    sys.path.append(str(Path('PipelineComponents/Classification').resolve()))
else:
    sys.path.append(str(Path('./PipelineComponents/Preprocessing').resolve()))
    sys.path.append(str(Path('./PipelineComponents/FeatureExtraction').resolve()))
    sys.path.append(str(Path('./PipelineComponents/Classification').resolve()))
    sys.path.append(str(Path('./Data/ExperimentResults').resolve()))
    sys.path.append(str(Path('./Data').resolve()))

from ExperimentWrapper import ExperimentWrapper

from PreprocessingPipeline import PreprocessingPipeline
from Visualize import DataPlot 
from Filters import Filter
from crop import crop

# temp
from FeaturesLos import get_frequency_power_per_channel

def get_boundary_indexes(frequencies):
    start = np.abs(frequencies - 5.0).argmin()
    end = np.abs(frequencies - 50.0).argmin()
    return start, end

if __name__ == "__main__":
    data = np.load('./Data/ExperimentResults/recorded_data/recordings_numpy/Mirthe/OpenBCISession_Mirthe_exp_sam_6hz-60sec.npy')
    data_filtered = PreprocessingPipeline(data).start()
    data_cropped = crop(data_filtered, 1, 250)
    data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
    data_cropped = [x for x in data_cropped if x is not None]
    data_artifacts_removed = np.concatenate(data_cropped)
    # print(get_frequency_power_per_channel(data_artifacts_removed[:,6], (2,10)))
    y_fft = np.abs(rfft(data_artifacts_removed[:,6]))
    f = rfftfreq(data_artifacts_removed.shape[0], 1/250)

    start, end = get_boundary_indexes(f)
    plt.plot(f, y_fft, label="Fourier Transform of EEG signal")
    plt.xlim([0,40])
    plt.title('Frequency spectrum of EEG data tagged at 6 Hz', fontsize=11)
    plt.xlabel('Frequency [Hz]', fontsize=12)
    plt.ylabel('Amplitude [μV]', fontsize=12)
    plt.axvline(x=5, color='orange', linestyle="--")
    plt.axvline(x=7, color='orange', linestyle='--')
    plt.legend(fontsize=11)
    # plt.show(block=True)
    plt.savefig('ReportPlots/flashlight_6hz.png', dpi=400)
    
    # data = np.load('Data/ExperimentResults/recorded_data/recordings_numpy/sample/cyril_mind.npy')
    # data = np.load('./Data/ExperimentResults/recorded_data/recordings_numpy/Mirthe/OpenBCISession_Mirthe_exp_cyril_15hz-60sec.npy')
    # y_fft = np.abs(rfft(data[:,6]))[200:1000]
    # f = rfftfreq(data.shape[0], 1/250)[200:1000]
    # plt.plot(f, y_fft)
    # plt.show(block=True)
