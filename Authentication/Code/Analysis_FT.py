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

    # EXP = ExperimentWrapper('Simon', 'ft')
    # EXP.set_experiment_data(Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_Simon_stage1_6hz.npy'))
    # EXP.set_experiment_description_file(Path('./Data/Experiments/Frequency_tagging/results/Step1/Simon6hz_2022-05-23_ft1_take1.csv'))

    # EXPERIMENTS.append(EXP)

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
        data_filtered = Filter.band_pass_filter(data_filtered, 4, (1,10), 250)

        data_intervals = crop(data_filtered, 2, 250, v=True)
        print(data_intervals[0].shape)
        powers = []
        for data_interval in data_intervals:
            data = Filter.remove_bad_channels(data_interval)
            if data is not None:
                powers.append(average_power(data))
                # powers.append(front_back_ratio(data))
            else:
                print('Interval deleted')
                powers.append(-1000)
            
        labels = get_labels(experiment.get_experiment_description_file())

        powers = normalize(np.array(list(map(lambda x: [x], powers))), axis=0).tolist()

        # Dit is voor nu nog heel gebeund allemaal
        # Calculate means
        mean_no_flash = 0
        mean_flash = 0
        for label, power in zip(labels, powers):
            if label == 0:
                mean_no_flash += power[0]
            else:
                mean_flash += power[0]
        mean_no_flash /= 20
        mean_flash /= 20
        print(f'Average no flash: {mean_no_flash} Average flash: {mean_flash}')

        powers_new = []
        for label, power in zip(labels, powers):
            if label == 0:
                powers_new.append(power[0]/mean_no_flash)
            else:
                powers_new.append(power[0]/mean_flash)

        powers = powers_new

        # # relate powers to the average surrounding it.
        # old_powers = powers
        # for i in range(1,len(powers)-1):
        #     powers[i] = (powers[i-1] + powers[i+1]) / (2 *  np.mean(old_powers))
        # powers[0] = powers[0] / np.mean(old_powers)
        # powers[-1] = powers[-1] / np.mean(old_powers)
        
        experiment_powers.append(powers)
        experiment_labels.append(labels)
    
    fig, axs = plt.subplots(2,3)
    for index, (powers, labels) in enumerate(zip(experiment_powers, experiment_labels)):

        # Some index magic to get the right subplot
        row = index // 3
        if index <= 2:
            col = index
        else:
            col = index - 3

        for i, label in enumerate(labels):
            if label == 0:
                axs[row, col].axvline(x=i, color="orange", linestyle='--')
            else:
                axs[row, col].axvline(x=i, color="blue", linestyle='--')
        
        axs[row, col].plot(powers)
        
        axs[row, col].axvline(x=-10, color="orange", linestyle='--', label='No flash')
        axs[row, col].axvline(x=-10, color="blue", linestyle='--', label='Flash')
        
        axs[row, col].set_xlim(left=0)

    handles, labels = axs[0,0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right') 

    plt.show(block=True)