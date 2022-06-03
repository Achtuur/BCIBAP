import numpy as np
from numpy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt

from pathlib import Path
import platform
import sys

if platform.system() == "Windows":
    sys.path.append(str(Path('PipelineComponents/Preprocessing').resolve()))
    sys.path.append(str(Path('PipelineComponents/FeatureExtraction').resolve()))
    sys.path.append(str(Path('Data/ExperimentResults').resolve()))
    sys.path.append(str(Path('Data').resolve()))
    sys.path.append(str(Path('PipelineComponents/Classification').resolve()))
else:
    sys.path.append(str(Path('../Preprocessing').resolve()))
    sys.path.append(str(Path('./PipelineComponents/FeatureExtraction').resolve()))
    sys.path.append(str(Path('./PipelineComponents/Classification').resolve()))
    sys.path.append(str(Path('./Data/ExperimentResults').resolve()))
    sys.path.append(str(Path('./Data').resolve()))

from PreprocessingPipeline import PreprocessingPipeline
from crop import crop
from Filters import Filter

#--------------------Auxillary Functions--------------------
def freq_power(fft_data):
    # This creates a function which can square a numpy array
    square = np.vectorize(lambda x: x**2)

    # Power is calculated
    power = np.sum(square(fft_data)) / fft_data.shape[0] 
    return power

def get_boundary_indexes(frequencies, range: tuple):
    # frequencies is a list. range[0] is the first boundary.
    # argmin() finds the index of the lowest frequency. If 5 needs to be found,
    # 5-5 = 0 which is found by argmin.
    start = np.abs(frequencies - range[0]).argmin()
    end = np.abs(frequencies - range[1]).argmin()
    return start, end

#--------------------General Features--------------------
# This function assumes single channel data
def get_frequency_band_power_per_channel(signal):
    delta_range = (0.5, 4) 
    theta_range = (4, 8) 
    alpha_range = (8, 12) 
    beta_range = (12, 35) 
    gamma_range = (35, 100) 

    band_power = {
        'delta': get_frequency_power_per_channel(signal, delta_range),
        'theta': get_frequency_power_per_channel(signal, theta_range),
        'alpha': get_frequency_power_per_channel(signal, alpha_range),
        'beta': get_frequency_power_per_channel(signal, beta_range),
        'gamma': get_frequency_power_per_channel(signal, gamma_range)
    }

    return band_power

def get_frequency_band_power(signal):
    band_powers = dict()
    for channel in range(signal.shape[1]):
        band_powers[str(channel)] = get_frequency_band_power_per_channel(signal[:, channel])

    return band_powers



# This function assumes single channel data
def get_signal_power_per_channel(signal):
    square = np.vectorize(lambda x: x**2)
    signal_power = np.sum(square(signal))/signal.shape[0]
    
    return signal_power 

def get_signal_power(signal):
    signal_power = dict()

    for channel in range(signal.shape[1]):
        signal_power[str(channel)] = get_signal_power_per_channel(signal[:, channel])

    return signal_power


#--------------------FT--------------------
# This function assumes single channel data
def get_frequency_power_per_channel(signal, freq_range: tuple, fs=250):
    # The input data is filtered within the required frequency range specified by freq_range aka (5,7)
    signal = Filter.band_pass_filter(signal, 4, crit_range=freq_range, fs=fs)
    
    # The fft is calculated of the filtered data
    fft_data = np.abs(rfft(signal))

    # The frequency bins are determined. These are required to find the
    # range of values to include from the FFt
    frequencies = rfftfreq(signal.shape[0], 1/fs)

    # get_boundary_indexes finds the indexes of the frequency boundaries.
    # These are necessary to only include the specified range in the power calculation
    start, end = get_boundary_indexes(frequencies, freq_range)

    # The power range is calculated
    power = freq_power(fft_data[start:end])
    return power

def get_frequency_power(signal, freq_range: tuple):
    # This function calculates power for every channel (n x m)
    power_dictionary = dict()

    # For every channel, the power is calculated whithin the specified frequency range
    for channel in range(signal.shape[1]):
        power_dictionary[str(channel)] = get_frequency_power_per_channel(signal[:,channel], freq_range)
    return power_dictionary

def get_par_per_channel(signal, freq_range):
    frequency_power = get_frequency_power_per_channel(signal, freq_range)

    # f-axis used to skip frequency range
    f = rfftfreq(signal.shape[0], 1/250)
    start, end = get_boundary_indexes(f, freq_range)
    signal_fft = rfft(signal)

    left_over_spectrum = np.concatenate((signal_fft[:start], signal_fft[end:]))
    left_over_power = freq_power(left_over_spectrum)

    return frequency_power/left_over_power


def cross_channel_power_ratio(signal, num_set: list, denom_set: list):
    numerator_power = 0
    denominator_power = 0

    signal_channel_powers = get_signal_power(signal)

    for channel in num_set:
        numerator_power += signal_channel_powers[str(channel)]
    
    numerator_power /= len(num_set)
    
    for channel in denom_set:
        denominator_power += signal_channel_powers[str(channel)]
    
    denominator_power /= len(denom_set)

    return numerator_power / denominator_power

# PW specific
def left_hemisphere_difference_ratio(pw_signal: np.array, word_signal_list: list, freq_range: tuple): 
    left_channels = [0, 2, 4, 6]
    # right_channels = [1, 3, 5, 7]

    # Baseline is the average of the word signals 
    baseline = 0

    # Iterate all words to find the average 
    for word_signal in word_signal_list:
        average_word_power = 0
        word_power = get_frequency_power(word_signal, freq_range)

        # Only count the channels in the left hemisphere
        for channel in left_channels:
            average_word_power += word_power[str(channel)]
        
        baseline += (average_word_power / len(left_channels))

    # Find the average
    baseline /= len(word_signal_list)

    # Find frequency power of pw signal
    average_pw_power = 0
    pw_power = get_frequency_power(pw_signal, freq_range)

    # Only count the channels in the left hemisphere
    for channel in left_channels:
        average_pw_power += pw_power[str(channel)]

    # Get average
    average_pw_power /= len(left_channels)

    return average_pw_power / baseline


if __name__ == '__main__':
    # data = np.load('../../Data/ExperimentResults/recorded_data/recordings_numpy/Mirthe/OpenBCISession_Mirthe_exp_sam_6hz-60sec.npy')
    # data_filtered = PreprocessingPipeline(data).start()
    # data_cropped = crop(data_filtered, 2, 250)
    # data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
    # data_cropped = [x for x in data_cropped if x is not None]
    # data = np.concatenate(data_cropped)
    
    # # powers = get_frequency_power(data_artifacts_removed, (2,10))
    # # print(powers.items())
    # print(cross_channel_power_ratio(data, [6,7], [0,1,2,3,4,5]))
    t = np.arange(0, 2*np.pi, 0.001)
    y = 5*np.sin(2*np.pi*200*t)

    y_fft = np.abs(rfft(y))
    f = rfftfreq(len(y), 0.001)
    print(f[y_fft.argmax()])
    plt.plot(f, y_fft)
    plt.show(block=True)
    print(get_frequency_power_per_channel(y, (100,210), 1/0.001))