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
from FeaturesLos import get_frequency_power_per_channel, get_par_per_channel

if __name__ == "__main__":
    data = np.load('../../Data/ExperimentResults/recorded_data/recordings_numpy/Mirthe/OpenBCISession_Mirthe_exp_sam_6hz-60sec.npy')[5*250:,:]
    data_filtered = PreprocessingPipeline(data).start()[5*250:,:]
    data_cropped = crop(data_filtered, 2, 250)
    data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
    data_cropped = [x for x in data_cropped if x is not None]
    data_artifacts_removed = np.concatenate(data_cropped)
    
    # durations = [50,40,30,20,10]
    durations = list(reversed(range(2,50)))
    
    powers_db = []
    pars = []

    for duration in durations:
        data_to_analyse = data_artifacts_removed[:duration*250,:]
        # print(get_frequency_power_per_channel(data_to_analyse[:,6], (2,10)))
        # y_fft = np.abs(rfft(data_to_analyse[:,6]))
        # f = rfftfreq(data_to_analyse.shape[0], 1/250)

        power = get_frequency_power_per_channel(data_to_analyse[:,6], (5,7), 250)
        db = 20*np.log10(power)
        powers_db.append(db)

        par = get_par_per_channel(data_to_analyse[:,6], (5,7))
        pars.append(20*np.log10(par))

    fig, ax = plt.subplots()

    line = ax.scatter(list(range(2,50)), powers_db, label="Frequency Power")
    ax.set_xlabel('Duration [s]')
    ax.set_ylabel('Frequency power [dB]')
    ax2 = ax.twinx()
    line2, = ax2.plot(list(range(2,50)), pars, color='orange', label="PAR of EEG signal")
    ax2.set_ylabel('Peak-Average-Ratio')
    ax.legend(handles=[line, line2])
    plt.xticks(durations)
    plt.title('PAR compared to Frequency power of EEG signal')
    plt.show(block=True)

    # print(pars)

    # plt.scatter([10,20,30,40,50], powers_db)
    # plt.xticks(durations)
    # plt.xlabel('Recording duration [s]')
    # plt.ylabel('Power [dB]')
    # plt.show(block=True)
        # plt.plot(f, y_fft)
        # plt.xlim([3,45])
        # plt.title('Frequency spectrum of EEG data during frequency tagging experiment.')
        # plt.xlabel('Frequency [Hz]')
        # plt.ylabel('Amplitude [μV]')
        # plt.show(block=True)

        # data = np.load('Data/ExperimentResults/recorded_data/recordings_numpy/sample/cyril_mind.npy')
        # data = np.load('./Data/ExperimentResults/recorded_data/recordings_numpy/Mirthe/OpenBCISession_Mirthe_exp_cyril_15hz-60sec.npy')
        # y_fft = np.abs(rfft(data[:,6]))[200:1000]
        # f = rfftfreq(data.shape[0], 1/250)[200:1000]
        # plt.plot(f, y_fft)
        # plt.show(block=True)
