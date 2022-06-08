import sys
import platform
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
    sys.path.append(str(Path('../../PipelineComponents/Preprocessing').resolve()))
    sys.path.append(str(Path('../../PipelineComponents/FeatureExtraction').resolve()))
    sys.path.append(str(Path('../../PipelineComponents/Classification').resolve()))
    sys.path.append(str(Path('../../Data/ExperimentResults').resolve()))
    sys.path.append(str(Path('../../Data').resolve()))

from PreprocessingPipeline import PreprocessingPipeline
from Visualize import DataPlot 
from Filters import Filter
from crop import crop

# temp
from FeaturesLos import get_par_per_channel

def get_boundary_indexes(frequencies, lim: tuple):
    start = np.abs(frequencies - lim[0]).argmin()
    end = np.abs(frequencies - lim[1]).argmin()
    return start, end

if __name__ == '__main__':
    data = np.load('../../Data/ExperimentResults/recorded_data/recordings_numpy/Mirthe/OpenBCISession_Mirthe_exp_sam_6hz-60sec.npy')
    data_filtered = PreprocessingPipeline(data).start()[500:-500]
    # data_filtered = Filter.band_pass_filter(data_filtered,4,(2,10),250)
    data_cropped = crop(data_filtered, 2, 250)
    data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
    data_cropped = [x for x in data_cropped if x is not None]
    data_artifacts_removed = np.concatenate(data_cropped)

    data_to_analyse = data_artifacts_removed[:,6]
    y_fft = np.abs(rfft(data_to_analyse))[:]
    f = rfftfreq(data_to_analyse.shape[0], 1/250)[:]

    start, end = get_boundary_indexes(f, (4,40))

    y_fft = y_fft[start:end]
    f = f[start:end]

    # Ugliest code i have ever written
    pars = []
    indexes = []

    left = 0
    right = 2
    for i in range(39): 
        left += 1
        right += 1
        indexes.append(left+1)
        _, par = get_par_per_channel(data_to_analyse, (left, right))
        pars.append(par)


    fig, ax = plt.subplots()

    line, = ax.plot(f, y_fft, label="FFT of EEG signal")
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplitude [μV]')
    ax2 = ax.twinx()
    line2, = ax2.plot(indexes, pars, color='orange', label="PAR of EEG signal")
    ax2.set_ylabel('Peak-Average-Ratio')
    ax.legend(handles=[line, line2])
    plt.title('PAR compared to FFT plot of EEG signal')
    plt.show(block=True)