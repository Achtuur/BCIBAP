import sys
import platform
import numpy as np
import csv
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import normalize


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
from FeaturesLos import get_frequency_power

def average_power_per_interval(data, interval_duration, freq_range: tuple):
    frequency_power_list = []
    data_segments = crop(data, interval_duration, 250)
    for data_interval in data_segments:
        frequency_power = get_frequency_power(data_interval, freq_range)
        frequency_power_list.append(np.mean(np.array([x for x in frequency_power.values()])))
    return np.mean(np.array(frequency_power_list))

if __name__ == '__main__':
    EXPERIMENTS = []

    # EXPERIMENT_SAM_6HZ_2 = ExperimentWrapper("Sam_6hz_2", "ft2")
    # EXPERIMENT_SAM_6HZ_2.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_ft2_6hz_2.npy"))
    # EXPERIMENTS.append(EXPERIMENT_SAM_6HZ_2)

    # EXPERIMENT_SAM_6HZ_4 = ExperimentWrapper("Sam_6hz_4", "ft2")
    # EXPERIMENT_SAM_6HZ_4.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_ft2_6hz_4.npy"))
    # EXPERIMENTS.append(EXPERIMENT_SAM_6HZ_4)

    # EXPERIMENT_SAM_6HZ_6 = ExperimentWrapper("Sam_6hz_6", "ft2")
    # EXPERIMENT_SAM_6HZ_6.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_ft2_6hz_6.npy"))
    # EXPERIMENTS.append(EXPERIMENT_SAM_6HZ_6)

    # EXPERIMENT_SAM_6HZ_8 = ExperimentWrapper("Sam_6hz_8", "ft2")
    # EXPERIMENT_SAM_6HZ_8.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_ft2_6hz_8.npy"))
    # EXPERIMENTS.append(EXPERIMENT_SAM_6HZ_8)

    # EXPERIMENT_SAM_6HZ_10 = ExperimentWrapper("Sam_6hz_10", "ft2")
    # EXPERIMENT_SAM_6HZ_10.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_ft2_6hz_10.npy"))
    # EXPERIMENTS.append(EXPERIMENT_SAM_6HZ_10)

    EXPERIMENTS_SAM_FT2_CALIBRATION = ExperimentWrapper("Sam_ft2_calibration", "ft2")
    EXPERIMENTS_SAM_FT2_CALIBRATION.set_experiment_data(Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_ft2_calibration.npy'))
    EXPERIMENTS.append(EXPERIMENTS_SAM_FT2_CALIBRATION)

    average_power_dict = {} 
    for experiment in EXPERIMENTS:
        # Only the first 50 seconds are used
        data = experiment.get_experiment_data()[:50*250,:] 
        data_filtered = PreprocessingPipeline(data).start()
        data_cropped = crop(data_filtered, 1, 250)
        data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
        data_cropped = [x for x in data_cropped if x is not None]
        data_to_analyse = np.concatenate(data_cropped)
        average_power_dict = get_frequency_power(data_to_analyse, (11,13))
        # frequency_power = get_frequency_power(data_to_analyse, (11,13))
        # for index, power in frequency_power.items():
        #     average_power_dict[index].append(power)
        #     print(average_power_dict)
    
    # for index, powers in average_power_dict.items():
    #     average_power_dict[index] = np.mean(np.array(average_power_dict[index]))
        # frequency_power_list.append(np.mean(np.array([x for x in frequency_power.values()])))

    # average_12hz_power = np.mean(np.array(frequency_power_list))
    print(average_power_dict)
    EXPERIMENTS = []

    EXPERIMENT_SAM_12HZ_2 = ExperimentWrapper("Sam_12hz_2", "ft2")
    EXPERIMENT_SAM_12HZ_2.set_experiment_data(Path("../../Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_ft2_12hz_2.npy"))
    EXPERIMENTS.append(EXPERIMENT_SAM_12HZ_2)

    EXPERIMENT_SAM_12HZ_4 = ExperimentWrapper("Sam_12hz_4", "ft2")
    EXPERIMENT_SAM_12HZ_4.set_experiment_data(Path("../../Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_ft2_12hz_4.npy"))
    EXPERIMENTS.append(EXPERIMENT_SAM_12HZ_4)

    EXPERIMENT_SAM_12HZ_6 = ExperimentWrapper("Sam_12hz_6", "ft2")
    EXPERIMENT_SAM_12HZ_6.set_experiment_data(Path("../../Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_ft2_12hz_6.npy"))
    EXPERIMENTS.append(EXPERIMENT_SAM_12HZ_6)

    EXPERIMENT_SAM_12HZ_8 = ExperimentWrapper("Sam_12hz_8", "ft2")
    EXPERIMENT_SAM_12HZ_8.set_experiment_data(Path("../../Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_ft2_12hz_8.npy"))
    EXPERIMENTS.append(EXPERIMENT_SAM_12HZ_8)

    EXPERIMENT_SAM_12HZ_10 = ExperimentWrapper("Sam_12hz_10", "ft2")
    EXPERIMENT_SAM_12HZ_10.set_experiment_data(Path("../../Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_ft2_12hz_10.npy"))
    EXPERIMENTS.append(EXPERIMENT_SAM_12HZ_10)

    frequency_power_list = []
    for experiment in EXPERIMENTS:
        # Only the first 50 seconds are used
        data = experiment.get_experiment_data()[:50*250,:] 
        data_filtered = PreprocessingPipeline(data).start()
        data_cropped = crop(data_filtered, 1, 250)
        data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
        data_cropped = [x for x in data_cropped if x is not None]
        data_to_analyse = np.concatenate(data_cropped)

        frequency_power = get_frequency_power(data_to_analyse, (10,14))
        frequency_power_list.append(frequency_power)
        print(experiment.get_subject())
        for channel, power in frequency_power.items():
            print(f'Channel: {channel} - Higher than average: {power > average_power_dict[channel]} - Ratio: {power/average_power_dict[channel]}')

    # Plot for channel vs power
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'chartreuse', 'burlywood']
    for index, freq_power_dict in enumerate(frequency_power_list):
        for i, freq_power in freq_power_dict.items():
            if index == 4:
                plt.scatter(index, freq_power/average_power_dict[i], color=colors[int(i)], label=f'Channel {int(i) + 1}')
            else:
                plt.scatter(index, freq_power/average_power_dict[i], color=colors[int(i)],)
    plt.axhline(1)
    plt.xticks([0, 1, 2, 3, 4], ['1', '2', '3', '4', '5'])
    plt.rcParams["figure.figsize"] = (10,5)
    plt.legend(bbox_to_anchor=(0.98, 1.05))
    plt.title('Frequency power around tagging frequency compared to average channel power')
    plt.xlabel('Different experiment trials')
    plt.ylabel('Relative Power')
    plt.show(block=True)
    
