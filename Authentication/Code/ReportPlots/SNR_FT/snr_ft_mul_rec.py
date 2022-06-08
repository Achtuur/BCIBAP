import sys
import platform
import numpy as np
import math
from math import ceil
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

from ExperimentWrapper import ExperimentWrapper 

from PreprocessingPipeline import PreprocessingPipeline
from Visualize import DataPlot 
from Filters import Filter
from crop import crop

from FeaturesLos import get_par_per_channel

if __name__ == '__main__':
    EXPERIMENTS = []

    sam_10hz_60 = ExperimentWrapper('sam_10hz_60', 'ft')
    sam_10hz_60.set_experiment_data(Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_10hz_60.npy'))

    EXPERIMENTS.append(sam_10hz_60)

    for experiment in EXPERIMENTS:
        data = PreprocessingPipeline(experiment.get_experiment_data()).start()
        # data_cropped = crop(data, 2, 250)
        # data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
        # data_cropped = [x for x in data_cropped if x is not None]
        # data = np.concatenate(data_cropped)

        data = data[:,5]
        par = get_par_per_channel(data, (5,7))
        # y_fft = np.abs(rfft(data))
        # f = rfftfreq(data.shape[0], 1/250)
        # plt.plot(f, y_fft)
        # plt.xlim(right=50)
        # plt.show(block=True)
        print(par)
        # power = get_frequency_power(data, (5,15))
        # temp = []

        # for i in range(8):
        #     temp.append(power[str(i)])

        # plt.plot(temp)
        # plt.show(block=True)
