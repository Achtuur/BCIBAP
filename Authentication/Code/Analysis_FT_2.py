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
    sys.path.append(str(Path('./PipelineComponents/Preprocessing').resolve()))
    sys.path.append(str(Path('./PipelineComponents/FeatureExtraction').resolve()))
    sys.path.append(str(Path('./PipelineComponents/Classification').resolve()))
    sys.path.append(str(Path('./Data/ExperimentResults').resolve()))
    sys.path.append(str(Path('./Data').resolve()))

from ExperimentWrapper import ExperimentWrapper

from PreprocessingPipeline import PreprocessingPipeline
from Visualize import DataPlot 
from Filters import Filter
from crop import crop


def average_power(data):
    square = np.vectorize(lambda x: x**2)
    powers = []
    for channel in range(data.shape[1]):
        powers.append(np.sum(square(np.abs(data[:, channel])) / data.shape[0]))
    
    return np.mean(np.array(powers))

def front_back_ratio(data):
    square = np.vectorize(lambda x: x**2)

    front_power = []
    back_power = []

    back_power.append(np.sum(square(np.abs(data[:, 6])) / data.shape[0]))
    back_power.append(np.sum(square(np.abs(data[:, 7])) / data.shape[0]))

    for i in range(6):
        front_power.append(np.sum(square(np.abs(data[:, i])) / data.shape[0]))

    return np.mean(np.array(back_power))/np.mean(np.array(front_power))

def get_labels(path_experiment, label_column = 1):
    path = path_experiment
    
    with open(path, newline = '') as f:
        csv_reader = csv.reader(f, delimiter=',')
        data = list(csv_reader)

    labels = []
    
    for label in data: 
        if label == [] or ' ' in label:
            label = None
        else: 
            label = label

        if label is None: 
            continue
        else:
            labels.append(int(label[label_column]))
    return labels

if __name__ == "__main__":

    EXPERIMENTS = []

    EXPERIMENT_SAM_TAKE_1 = ExperimentWrapper('Sam1', 'ft')
    EXPERIMENT_SAM_TAKE_1.set_experiment_data(Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_stage1_take1.npy'))
    EXPERIMENT_SAM_TAKE_1.set_experiment_description_file(Path('./Data/Experiments/Frequency_tagging/results/Step1/Sam_2022-05-23_ft1_take1.csv'))

    EXPERIMENTS.append(EXPERIMENT_SAM_TAKE_1)

    EXPERIMENT_SAM_TAKE_2 = ExperimentWrapper('Sam2', 'ft')
    EXPERIMENT_SAM_TAKE_2.set_experiment_data(Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_stage1_take2.npy'))
    EXPERIMENT_SAM_TAKE_2.set_experiment_description_file(Path('./Data/Experiments/Frequency_tagging/results/Step1/Sam_2022-05-23_ft1_take2.csv'))

    EXPERIMENTS.append(EXPERIMENT_SAM_TAKE_2)

    # EXPERIMENT_JOOS_TAKE_1 = ExperimentWrapper('Joos', 'ft')
    # EXPERIMENT_JOOS_TAKE_1.set_experiment_data(Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_stage1_take1.npy'))
    # EXPERIMENT_JOOS_TAKE_1.set_experiment_description_file(Path('./Data/Experiments/Frequency_tagging/results/Step1/Joos_2022-05-23_ft1_take1.csv'))

    # EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_1)

    EXPERIMENT_JOOS_TAKE_2 = ExperimentWrapper('Joos2', 'ft')
    EXPERIMENT_JOOS_TAKE_2.set_experiment_data(Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_stage1_take2.npy'))
    EXPERIMENT_JOOS_TAKE_2.set_experiment_description_file(Path('./Data/Experiments/Frequency_tagging/results/Step1/Joos_2022-05-23_ft1_take2.csv'))

    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_2)

    EXPERIMENT_SIMON_TAKE_1 = ExperimentWrapper("Simon1", "ft")
    EXPERIMENT_SIMON_TAKE_1.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_Simon_stage1_take1.npy"))
    EXPERIMENT_SIMON_TAKE_1.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Simon_2022-05-23_ft1_take1.csv"))
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_1)

    EXPERIMENT_SIMON_TAKE_2 = ExperimentWrapper("Simon2", "ft")
    EXPERIMENT_SIMON_TAKE_2.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_Simon_stage1_take2.npy"))
    EXPERIMENT_SIMON_TAKE_2.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Simon_2022-05-23_ft1_take2.csv"))
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_2)

    experiment_powers = []
    experiment_labels = []
    for experiment in EXPERIMENTS:
        experiment_data = experiment.get_experiment_data()
        
        # Standard Filtering 
        data_filtered = PreprocessingPipeline(experiment_data).start()

        # Specific experiment Filtering
        data_filtered = Filter.band_pass_filter(data_filtered, 4, (10,20), 250)

        data_intervals = crop(data_filtered, 2, 250, (0,250))

        data_intervals = map(lambda x: Filter.remove_bad_channels(x), data_intervals)  
        labels = get_labels(experiment.get_experiment_description_file())

        for interval, label in zip(data_intervals, labels):
            if interval is not None:
                y = rfft(interval[:,6])
                if label == 0:
                    plt.plot(y, color="blue")
                else:
                    plt.plot(y, color="orange")
        plt.show(block=True)
