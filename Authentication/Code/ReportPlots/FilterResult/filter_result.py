import numpy as np
from numpy.fft import rfft, rfftfreq
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
    sys.path.append(str(Path('../../Data/ExperimentResults').resolve()))


# Preprocessing
from PreprocessingPipeline import PreprocessingPipeline
from Filters import Filter
from Visualize import DataPlot
from prepare_data import crop

def get_fft(data: np.ndarray, title: str):
    fig, axs = plt.subplots(data.shape[1])
    axs[0].title.set_text(title)
    # Calc values for x-axis 
    f = rfftfreq(data.shape[0], 1/250)

    # Calc fft
    for index in range(data.shape[1]):
        y = rfft(data[:,index])
        axs[index].plot(f, y)
    plt.show(block=True)


if __name__ == '__main__':
    cal_path = Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_calibration.npy')
    calibration_data = np.load(cal_path)
    # The calibration interval is 1:02 - 2:02
    calibration_data = calibration_data[250*62:250*122]
    calibration_data = PreprocessingPipeline(calibration_data).start()
    
    experiment_data_path = Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_pseudo.npy')
    experiment_data = np.load(experiment_data_path)
    experiment_data = experiment_data[8*250:240*250]
    get_fft(experiment_data, 'FFT of raw data')

    # Highpass filter
    data_high_pass_filtered = np.empty(experiment_data.shape)
    for channel in range(experiment_data.shape[1]):
        result = np.array(Filter.high_pass_filter(experiment_data[:, channel], 4, 1))
        data_high_pass_filtered[:, channel] = result

    get_fft(data_high_pass_filtered, 'FFT of data after High Pass Filter')

    # Notch Filter
    data_notch_filtered = np.empty(data_high_pass_filtered.shape)
    for channel in range(data_high_pass_filtered.shape[1]):
        result = np.array(Filter.notch_filter(data_high_pass_filtered[:,channel], 50, 30, 250))
        data_notch_filtered[:, channel] = result 

    get_fft(data_notch_filtered, 'FFT of data after Notch Filter')

    data_artifact_filtered = Filter.filter_artifacts(data_notch_filtered, calibration_data)
    
    # The Artifact removal introduces spikes between 0-1 Hz so it is HP filtered again
    data_high_pass_filtered = np.empty(data_artifact_filtered.shape)
    for channel in range(data_artifact_filtered.shape[1]):
        result = np.array(Filter.high_pass_filter(data_artifact_filtered[:, channel], 4, 1))
        data_high_pass_filtered[:, channel] = result

    get_fft(data_high_pass_filtered, 'FFT of data after ASR')
    