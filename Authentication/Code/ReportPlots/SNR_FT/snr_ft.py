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


from PreprocessingPipeline import PreprocessingPipeline
from Visualize import DataPlot 
from Filters import Filter
from crop import crop

def get_boundary_indexes(frequencies):
    start = np.abs(frequencies - 5.0).argmin()
    end = np.abs(frequencies - 50.0).argmin()
    return start, end

def get_snr(spectrum, peak_index):
    peak_power = spectrum[peak_index]**2
    spectrum[peak_index] = 0
    square = np.vectorize(lambda x: x**2)
    mean_power = np.sum(square(spectrum)) / len(spectrum)

    return 10*math.log(peak_power / mean_power, 10)


if __name__ == "__main__":
    data = np.load('../../Data/ExperimentResults/recorded_data/recordings_numpy/Mirthe/OpenBCISession_Mirthe_exp_sam_6hz-60sec.npy')
    tagged_frequency = 6
    data_filtered = PreprocessingPipeline(data).start()[:]
    data_cropped = crop(data_filtered, 2, 250)
    data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
    data_cropped = [x for x in data_cropped if x is not None]
    data = np.concatenate(data_cropped)
    SNR_DICTIONARY = {
        '0': [],
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': [],
        '6': [],
        '7': []
    }
    length_recording = int(data.shape[0] / 250)
    for channel in range(8):
        # signal_to_noise_per_length = []
        for duration in reversed(range(1,length_recording)):
            print(f'channel: {channel+1} - duration: {duration}')
            data_intervals = crop(data,duration,250)
            signal_to_noise_per_interval = []
            for index, data_interval in enumerate(data_intervals):
                y_fft = np.abs(rfft(data_interval[:,channel]))
                f = rfftfreq(data_interval.shape[0], 1/250)
                start, end = get_boundary_indexes(f)
                y_fft = y_fft[start:end]
                peak_index = y_fft.argmax()
                if math.isclose(f[start+peak_index], tagged_frequency, rel_tol=0.02) and y_fft[peak_index] >= 2*np.mean(y_fft):
                    # plt.plot(f[start:end],y_fft)
                    # plt.title(f'interval len: {duration} - data index: {index} - peak: {y_fft[peak_index]}')
                    # plt.show(block=True)
                    signal_to_noise_per_interval.append(get_snr(y_fft, peak_index))
                else:
                    signal_to_noise_per_interval.append(None)
            # SNR_DICTIONARY[f'{channel}'] += 1
            SNR_DICTIONARY[f'{channel}'].append(np.mean(np.array([x for x in signal_to_noise_per_interval if x is not None])))

    X = [x for x in reversed(range(1,length_recording))]
    # Scatter plot
    plt.scatter(X, SNR_DICTIONARY['0'], color="#1f77b4", label='Channel 1', marker='o', s=20.0)
    plt.scatter(X, SNR_DICTIONARY['1'], color="#ff7f0e", label='Channel 2', marker='o', s=20.0)
    plt.scatter(X, SNR_DICTIONARY['2'], color="#2ca02c", label='Channel 3', marker='o', s=20.0)
    plt.scatter(X, SNR_DICTIONARY['3'], color="#d62728", label='Channel 4', marker='o', s=20.0)
    plt.scatter(X, SNR_DICTIONARY['4'], color="#9467bd", label='Channel 5', marker='o', s=20.0)
    plt.scatter(X, SNR_DICTIONARY['5'], color="#8c564b", label='Channel 6', marker='o', s=20.0)
    plt.scatter(X, SNR_DICTIONARY['6'], color="#e377c2", label='Channel 7', marker='o', s=20.0)
    plt.scatter(X, SNR_DICTIONARY['7'], color="#7f7f7f", label='Channel 8', marker='o', s=20.0)
    
    # Polyfit
    # p1 = np.polyfit(X, SNR_DICTIONARY['1'], 3)
    # p4 = np.polyfit(X, [x for x in SNR_DICTIONARY['4'] if not np.isnan(x)], 3)
    # print(p4)
    p5 = np.polyfit(X, SNR_DICTIONARY['5'], 3)
    p6 = np.polyfit(X, SNR_DICTIONARY['6'], 3)
    p7 = np.polyfit(X, SNR_DICTIONARY['7'], 3)

    # plt.plot(X, np.multiply(p1[0],np.power(X, 3)) + np.multiply(p1[1], np.power(X, 2)) + np.multiply(p1[2], X) + p1[3], color="#ff7f0e")
    # plt.plot(X, np.multiply(p4[0],np.power(X, 3)) + np.multiply(p4[1], np.power(X, 2)) + np.multiply(p4[2], X) + p4[3], color="#9467bd")
    plt.plot(X, np.multiply(p5[0],np.power(X, 3)) + np.multiply(p5[1], np.power(X, 2)) + np.multiply(p5[2], X) + p5[3], color="#8c564b")
    plt.plot(X, np.multiply(p6[0],np.power(X, 3)) + np.multiply(p6[1], np.power(X, 2)) + np.multiply(p6[2], X) + p6[3], color="#e377c2")
    plt.plot(X, np.multiply(p7[0],np.power(X, 3)) + np.multiply(p7[1], np.power(X, 2)) + np.multiply(p7[2], X) + p7[3], color="#7f7f7f")
    plt.title(f'Peak-Average-Ratio of tagged frequency power [{tagged_frequency}Hz]')
    plt.xlabel('Interval Duration [s]')
    plt.ylabel('PAR [dB]')
    plt.xlim(left=0)
    plt.legend(loc="lower right")
    plt.show(block=True)



 









    
    # # snr_averages = []
    # # for sec in reversed(range(1,50)):
    # #     data = crop(data_artifacts_removed, sec, 250)
    # #     snrs = []
    # #     for index, data_interval in enumerate(data):
    # #         y_fft = np.abs(rfft(data_interval[:,7]))
    #         f = rfftfreq(data_interval.shape[0], 1/250)
    #         start, end = get_boundary_indexes(f)
    #         peak_index = y_fft.argmax()
    #         print(y_fft[peak_index])
    #         plt.plot(f[start:end],y_fft[start:end])
    #         plt.title(f'interval len: {sec} - data index: {index} - peak: {y_fft[peak_index]}')
    #         plt.show(block=True)

    #         snrs.append(get_snr(y_fft[start:end], peak_index - start))
    #     snr_averages.append(np.mean(np.array(snrs)))
    # plt.scatter([x for x in reversed(range(1,50))], snr_averages, marker='x')
    # plt.show(block=True)

    # y_fft = np.abs(rfft(data_artifacts_removed[:,7]))[:]
    # f = rfftfreq(data_artifacts_removed.shape[0], 1/250)[:]
    # start, end = get_boundary_indexes(f)
    # peak_index = y_fft.argmax()
    # print(get_snr(y_fft, peak_index)) 
    # # plt.plot(f[start:end],y_fft[start:end])
    # # plt.show(block=True)