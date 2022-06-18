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
    average_power_dict = {
        '0' : [],
        '1' : [],
        '2' : [],
        '3' : [],
        '4' : [],
        '5' : [],
        '6' : [],
        '7' : [],
    }
    frequency_power_list = []
    data_segments = crop(data, interval_duration, 250)
    for data_interval in data_segments:
        frequency_power = get_frequency_power(data_interval, freq_range)
        frequency_power_list.append(frequency_power)
    
    for power_dict in frequency_power_list:
        for index, value in power_dict.items():
            average_power_dict[index].append(value)

    for index, value in average_power_dict.items():
        average_power_dict[index] = np.mean(np.array(average_power_dict[index]))
    
    return average_power_dict
    # return np.mean(np.array(frequency_power_list))

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

    EXPERIMENT_INTERVALS = [1, 1.5,2,2.5,3,3.5,4,4.5]

    # Dit is lelijk
    final_results = {
        '1' : [],
        '1.5' : [],
        '2' : [],
        '2.5' : [],
        '3' : [],
        '3.5' : [],
        '4' : [],
        '4.5' : [],
    }

    for EXPERIMENT_INTERVAL in EXPERIMENT_INTERVALS:
        average_power_dict = {} 
        for experiment in EXPERIMENTS:
            # Only the first 50 seconds are used
            data = experiment.get_experiment_data()[:50*250,:] 
            data_filtered = PreprocessingPipeline(data).start()
            data_cropped = crop(data_filtered, 0.5, 250)
            data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
            data_cropped = [x for x in data_cropped if x is not None]
            data_to_analyse = np.concatenate(data_cropped)
            average_power_dict = average_power_per_interval(data_to_analyse, EXPERIMENT_INTERVAL, (10,14))

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

        # Dit is heel beun
        skip = [2,4,6,8,10]
        for index, experiment in enumerate(EXPERIMENTS):
            # Only the first 50 seconds are used
            range_to_check = (50*250 + skip[index]*250)
            data = experiment.get_experiment_data()[range_to_check:(int(range_to_check + EXPERIMENT_INTERVAL*250)),:] 
            data_filtered = PreprocessingPipeline(data).start()
            data_cropped = crop(data_filtered, EXPERIMENT_INTERVAL, 250)
            data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
            data_cropped = [x for x in data_cropped if x is not None]
            data_to_analyse = np.concatenate(data_cropped)

            frequency_power = get_frequency_power(data_to_analyse, (10,14))
            for key in frequency_power.keys():
                frequency_power[key] /= average_power_dict[key]
            frequency_power_list.append(frequency_power)
        final_results[str(EXPERIMENT_INTERVAL)] = frequency_power_list

    test = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
    colors = ['b', 'g', 'r', 'c', 'm', 'orange']
    fig, axs = plt.subplots()
    for index, (key, interval_results) in enumerate(final_results.items()):
        for index_2, power_dict in enumerate(interval_results):
            axs.scatter(test[index], power_dict['6'], color=colors[index_2])
            # plt.scatter(test[index], power_dict['7'], color=colors[index_2], marker='+')

    fig.text(0.04, 0.5, 'Relative Power', va='center', rotation='vertical', fontsize=15)
    fig.text(0.5, 0.04, 'Measure period [s]', ha='center', fontsize=15) 
    
    y = [
        [],
        [],
        [],
        [],
        []
    ]
    for interval_results in final_results.values(): 
        for index, power_dict in enumerate(interval_results):
            y[index].append(power_dict['6'])

    p0 = np.polyfit(test, y[0], 2)
    p1 = np.polyfit(test, y[1], 2)
    p2 = np.polyfit(test, y[2], 2)
    p3 = np.polyfit(test, y[3], 2)
    p4 = np.polyfit(test, y[4], 2)

    y = np.mean(np.array(y), axis=0)
    pav = np.polyfit(test, y, 2)

    # pav = np.polyfit(test,)

    axs.plot(test, np.multiply(p0[0], np.power(test,2)) + np.multiply(p0[1], test) + p0[2], color=colors[0], label='2 sec')
    axs.plot(test, np.multiply(p1[0], np.power(test,2)) + np.multiply(p1[1], test) + p1[2], color=colors[1], label='4 sec')
    axs.plot(test, np.multiply(p2[0], np.power(test,2)) + np.multiply(p2[1], test) + p2[2], color=colors[2], label='6 sec')
    axs.plot(test, np.multiply(p3[0], np.power(test,2)) + np.multiply(p3[1], test) + p3[2], color=colors[3], label='8 sec')
    axs.plot(test, np.multiply(p4[0], np.power(test,2)) + np.multiply(p4[1], test) + p4[2], color=colors[4], label='10 sec')
    axs.plot(test, np.multiply(pav[0], np.power(test,2)) + np.multiply(pav[1], test) + pav[2], color=colors[5], label='average')
    
    axs.legend(bbox_to_anchor=(0.97,1), fontsize=13)
    # axs.legend(['2 sec', '4 sec', '6 sec', '8 sec', '10 sec', 'average'], bbox_to_anchor=(1,1))

    # for index, (key, interval_results) in enumerate(final_results.items()):
    #     for index_2, power_dict in enumerate(interval_results):
    #         axs[1].scatter(test[index], power_dict['7'], color=colors[index_2])

    # y = [
    #     [],
    #     [],
    #     [],
    #     [],
    #     []
    # ]
    # for interval_results in final_results.values(): 
    #     for index, power_dict in enumerate(interval_results):
    #         y[index].append(power_dict['7'])

    # p0 = np.polyfit(test, y[0], 2)
    # p1 = np.polyfit(test, y[1], 2)
    # p2 = np.polyfit(test, y[2], 2)
    # p3 = np.polyfit(test, y[3], 2)
    # p4 = np.polyfit(test, y[4], 2)

    # y = np.mean(np.array(y), axis=0)
    # pav = np.polyfit(test, y, 2)

    # # axs[1].plot(test, np.multiply(p0[0], np.power(test,2)) + np.multiply(p0[1], test) + p0[2], color=colors[0])
    # # axs[1].plot(test, np.multiply(p1[0], np.power(test,2)) + np.multiply(p1[1], test) + p1[2], color=colors[1])
    # # axs[1].plot(test, np.multiply(p2[0], np.power(test,2)) + np.multiply(p2[1], test) + p2[2], color=colors[2])
    # # axs[1].plot(test, np.multiply(p3[0], np.power(test,2)) + np.multiply(p3[1], test) + p3[2], color=colors[3])
    # # axs[1].plot(test, np.multiply(p4[0], np.power(test,2)) + np.multiply(p4[1], test) + p4[2], color=colors[4])
    # # axs[1].plot(test, np.multiply(pav[0], np.power(test,2)) + np.multiply(pav[1], test) + pav[2], color=colors[5])
    

    axs.set_title('Relative Tagged frequency Power for different measuring intervals', fontsize=14)
    axs.set_ylabel('Channel 6', fontsize=13)
    # axs[1].set_ylabel('Channel 7', fontsize=13)
    
    plt.show(block=True)


 