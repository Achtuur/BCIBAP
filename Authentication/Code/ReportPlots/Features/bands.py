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

def get_average_bandpower(power):
    # Dictionary to hold averages
    average_bandpower = {
        'delta': 0,
        'theta': 0,
        'alpha': 0,
        'beta': 0,
        'gamma': 0
    }

    # Iterate over every channel and add power to 
    # corresponding average band
    for channel_bandpower in power.values():
        for band in channel_bandpower.keys():
            average_bandpower[band] += channel_bandpower[band]
    
    # Divide every value by the amount of channels
    # to get the average
    for band in average_bandpower.keys():
        average_bandpower[band] /= len(power.items())

    return average_bandpower

if __name__ == '__main__':
    data_path = Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/sample/alpha_waves.npy')
    # The relevant data interval is 1:23 - 2:42
    data = np.load(data_path)[250*83:250*163]
    data = PreprocessingPipeline(data).start()
    # _,_, plt = DataPlot.eeg_channels_plot(data)
    # plt.show(block=True)

    # # Split intervals
    data_task_1 = data[:20*250]
    data_rest_1 = data[20*250:40*250]
    data_task_2 = data[40*250:60*250]
    data_rest_2 = data[60*250:]
    
    # data_list = [data_task_1, data_rest_1, data_task_2, data_rest_2]
    power = get_frequency_band_power(data_task_1)
    power_task_1 = get_average_bandpower(power)

    power = get_frequency_band_power(data_rest_1)
    power_rest_1 = get_average_bandpower(power)


    power = get_frequency_band_power(data_task_2)
    power_task_2 = get_average_bandpower(power)

    power = get_frequency_band_power(data_rest_2)
    power_rest_2 = get_average_bandpower(power)


    # task 1
    plt.bar(['Theta', 'Alpha', 'Beta', 'Gamma'], list(power_task_1.values())[1:], color=('#1f77b4', 'green', '#1f77b4', '#1f77b4'))
    plt.xlabel('Frequency bands')
    plt.ylabel('Power [μV^2]')
    plt.title('Band powers during 1st task period')
    plt.show(block=True)
    
    # rest 1
    plt.bar(['Theta', 'Alpha', 'Beta', 'Gamma'], list(power_rest_1.values())[1:], color=('#1f77b4', 'green', '#1f77b4', '#1f77b4'))
    plt.xlabel('Frequency bands')
    plt.ylabel('Power [μV^2]')
    plt.title('Band powers during 1st rest period')
    plt.show(block=True)

    # task 2 
    plt.bar(['Theta', 'Alpha', 'Beta', 'Gamma'], list(power_task_2.values())[1:], color=('#1f77b4', 'green', '#1f77b4', '#1f77b4'))
    plt.xlabel('Frequency bands')
    plt.ylabel('Power [μV^2]')
    plt.title('Band powers during 2nd task period')
    plt.show(block=True)

    # rest 2 
    plt.bar(['Theta', 'Alpha', 'Beta', 'Gamma'], list(power_rest_2.values())[1:], color=('#1f77b4', 'green', '#1f77b4', '#1f77b4'))
    plt.xlabel('Frequency bands')
    plt.ylabel('Power [μV^2]')
    plt.title('Band powers during 2nd rest period')
    plt.show(block=True)
