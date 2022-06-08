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
from FeaturesLos import get_par_per_channel, cross_channel_power_ratio

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

    data_to_analyse = data_artifacts_removed[:]
    numerator = []
    results = np.empty((8,8))
    for i in range(8):
        numerator.append(i)
        denominator = []
        for j in range(8):
            denominator.append(j)
            results[i,j]

    # cross_channel_power = cross_channel_power_ratio(data_to_analyse, [0,1,2], [2,3,4])
    # print(cross_channel_power)