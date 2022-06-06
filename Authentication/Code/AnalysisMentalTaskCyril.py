import numpy as np
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
    sys.path.append(str(Path('./PipelineComponents/Preprocessing').resolve()))
    sys.path.append(str(Path('./PipelineComponents/FeatureExtraction').resolve()))
    sys.path.append(str(Path('./PipelineComponents/Classification').resolve()))
    sys.path.append(str(Path('./Data').resolve()))
    sys.path.append(str(Path('./Data/ExperimentResults').resolve()))


# Preprocessing
from PreprocessingPipeline import PreprocessingPipeline
from Filters import Filter
from crop import crop
from Visualize import DataPlot

def average_power(data):
    square = np.vectorize(lambda x: x**2)
    powers = []
    for channel in range(data.shape[1]):
        powers.append(np.sum(square(data[:, channel]) / data.shape[0]))
    
    return np.mean(np.array(powers))

def gen_average_power_plot(data):
    affected_channels = np.concatenate([data[:,0:2], data[:,6:8]], axis=1)
    # # print(affected_channels.shape)
    unaffected_channels = data[:,2:4]
    # # print(unaffected_channels.shape)
    affected_channel_alpha_band = Filter.band_pass_filter(affected_channels, 4, (7.5, 12.5), 250)
    power_affected_channel = average_power(affected_channel_alpha_band)

    unaffected_channel_alpha_band = Filter.band_pass_filter(unaffected_channels, 4, (7.5, 12.5), 250)
    power_unaffected_channel = average_power(unaffected_channel_alpha_band)

    return power_affected_channel, power_unaffected_channel

    # # Calculate powers
    # alpha_band_1 = Filter.band_pass_filter(data_task_1, 4, (7.5, 12.5), 250)
    # alpha_band_1_power = average_power(alpha_band_1) 

    # alpha_band_2 = Filter.band_pass_filter(data_rest_1, 4, (7.5, 12.5), 250)
    # alpha_band_2_power = average_power(alpha_band_2) 

    # alpha_band_3 = Filter.band_pass_filter(data_task_2, 4, (7.5, 12.5), 250)
    # alpha_band_3_power = average_power(alpha_band_3) 

    # alpha_band_4 = Filter.band_pass_filter(data_rest_2, 4, (7.5, 12.5), 250)
    # alpha_band_4_power = average_power(alpha_band_4) 

    # print(f"""
    #     Mental Task period 1: {alpha_band_1_power}\n
    #     Resting period 1: {alpha_band_2_power}\n
    #     Mental Task period 2: {alpha_band_3_power}\n
    #     Resting period 2: {alpha_band_4_power}

    # """)

    # plt.bar([1,2,3,4], [alpha_band_1_power,alpha_band_2_power,alpha_band_3_power,alpha_band_4_power], color=['blue', 'orange', 'blue', 'orange'])
    # plt.title('Average Alpha Bands Power during mental tasks and resting periods')
    # plt.xlabel('Time period')
    # plt.xticks([])
    # plt.ylabel('Power [μV^2]')
    # plt.show(block=True)
    
def gen_power_plot(data_blocks):
    av0 = average_power(Filter.band_pass_filter(data_blocks[0], 4, (7.5, 12.5), 250))
    av1 = average_power(Filter.band_pass_filter(data_blocks[1], 4, (7.5, 12.5), 250))
    av2 = average_power(Filter.band_pass_filter(data_blocks[2], 4, (7.5, 12.5), 250))
    av3 = average_power(Filter.band_pass_filter(data_blocks[3], 4, (7.5, 12.5), 250))

    result = []
    for data in data_blocks:
        data = data[:,2:]
        cropped_data = crop(data, 2, 250)
        for data_interval in cropped_data:
            data_interval = Filter.band_pass_filter(data_interval, 4, (7.5, 12.5), 250)
            result.append(average_power(data_interval))
    plt.plot(result, label="Power")
    plt.xlabel('Time [s]')
    plt.ylabel('Power [uV^2]')
    plt.title('Power vs Time')
    av = []
    for i in range(10):
        av.append(av0)
    for i in range(10):
        av.append(av1)
    for i in range(10):
        av.append(av2)
    for i in range(10):
        av.append(av3)
    plt.plot(av, '--', label="Average Power over interval")
    plt.legend()
    plt.show(block=True)
    

if __name__ == '__main__':
    data_path = Path('./Data/ExperimentResults/recorded_data/recordings_numpy/sample/alpha_waves.npy')
    # The relevant data interval is 1:23 - 2:42
    data = np.load(data_path)[250*83:250*163]
    _,_, plt = DataPlot.eeg_channels_plot(data)
    plt.show(block=True)
    # Processing
    # data = PreprocessingPipeline(data).start()
    # data_cropped = crop(data, 2, 250)
    # data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
    # data_cropped = [x for x in data_cropped if x is not None]
    # data = np.concatenate(data_cropped) 

    # # Split intervals
    data_task_1 = data[:20*250]
    data_rest_1 = data[20*250:40*250]
    data_task_2 = data[40*250:60*250]
    data_rest_2 = data[60*250:]
    
    data_list = [data_task_1, data_rest_1, data_task_2, data_rest_2]

    powers = []
    for data_interval in data_list:
        powers.append(gen_average_power_plot(data_interval))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    interval = ['Arithmetic 1', 'Rest 1', 'Arithmetic 2', 'Rest 2']
    values = [(powers[0][0]+powers[0][1])/2,(powers[1][0]+powers[1][1])/2, (powers[2][0]+powers[2][1])/2, (powers[3][0]+powers[3][1])/2]
    ax.bar(interval, values)
    plt.title('Average alpha band power during tasks')
    plt.xlabel('Interval')
    plt.ylabel('Average Power [μV^2]')
    plt.show(block=True)
    # # gen_power_plot([data_task_1, data_rest_1, data_task_2, data_rest_2])
    

    