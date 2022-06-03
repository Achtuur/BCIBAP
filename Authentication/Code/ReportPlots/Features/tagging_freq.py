import numpy as np
from numpy.fft import rfft, fftfreq
from scipy.fft import rfftfreq
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt

# This is an ugly hack to make imports work
from pathlib import Path
import sys
import platform
if platform.system() == "Windows":
    sys.path.append(str(Path('PipelineComponents/Preprocessing').resolve()))
    sys.path.append(str(Path('PipelineComponents/FeatureExtraction').resolve()))
    sys.path.append(str(Path('Data/ExperimentResults').resolve()))
else:
    sys.path.append(str(Path('../../PipelineComponents/Preprocessing').resolve()))
    sys.path.append(str(Path('../../PipelineComponents/FeatureExtraction').resolve()))
    sys.path.append(str(Path('../../PipelineComponents/Classification').resolve()))
    sys.path.append(str(Path('./Data').resolve()))
    sys.path.append(str(Path('./Data/ExperimentResults').resolve()))

# Preprocessing
from PreprocessingPipeline import PreprocessingPipeline
from Filters import Filter
from crop import crop
from Visualize import DataPlot

# Features
from FeaturesLos import *

if __name__ == '__main__':
    data_path = Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Mirthe/OpenBCISession_Mirthe_exp_sam_6hz-60sec.npy')
    data = np.load(data_path)

    data = Filter.notch_filter(data, 50, 30, 250)
    y_fft = np.abs(rfft(data[:,6]))
    freq = rfftfreq(data.shape[0], 1/250)
    plt.plot(freq[30:], y_fft[30:])
    
    plt.show(block=True)

    # data = np.load(data_path)
    # data = PreprocessingPipeline(data).start(v=True)
    # data_cropped = crop(data, 2, 250)
    # data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
    # data_cropped = [x for x in data_cropped if x is not None]
    # data_filtered = np.concatenate(data_cropped) 

    # y_fft = np.abs(rfft(data_filtered[:,6]))
    # freq = rfftfreq(data_filtered.shape[0], 1/250)
    # plt.plot(freq, y_fft)
    # plt.show(block=True)
    