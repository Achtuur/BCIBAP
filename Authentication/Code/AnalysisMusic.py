import numpy as np
import csv

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
    sys.path.append(str(Path('./Data/ExperimentResults').resolve()))

# Experiments
from ExperimentWrapper import ExperimentWrapper

# Preprocessing
from PreprocessingPipeline import PreprocessingPipeline
from prepare_data import crop
from Visualize import DataPlot

# Feature Extraction
from FeaturePipeline import FeaturePipeline

# Auxillary functions
def get_labels(path_experiment, label_column = 1):
    path = path_experiment
    
    with open(path, newline = '') as f:
        csv_reader = csv.reader(f, delimiter=',')
        data = list(csv_reader)

    labels = []
    
    for label in data: 
        if not label: 
            continue
        else:
            labels.append(int(label[label_column]))
    return labels

if __name__ == '__main__':
    EXPERIMENTS = []

    # Sam
    EXPERIMENT_SAM = ExperimentWrapper("SAM", 
        'music',
        Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_calibration.npy')
    )

    EXPERIMENT_SAM = EXPERIMENT_SAM.set_experiment_data(
        Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_music.npy')
    ).set_experiment_description_file(
        Path('./Data/Experiments/Music/experiment_song_order/songlist_2022-05-10_09-46-52.139.csv')
    )

    EXPERIMENTS.append(EXPERIMENT_SAM)

    # M1
    EXPERIMENT_M1 = ExperimentWrapper("M1",
        'music',
        Path('./Data/ExperimentResults/recorded_data/recordings_numpy/M1_10_05_2022/OpenBCISession_M1_calibration.npy')
    )

    EXPERIMENT_M1 = EXPERIMENT_M1.set_experiment_data(
        Path('./Data/ExperimentResults/recorded_data/recordings_numpy/M1_10_05_2022/OpenBCISession_M1_music_2.npy')
    ).set_experiment_description_file(
        Path('./Data/Experiments/Music/experiment_song_order/songlist_2022-05-10_11-41-15.987.csv')
    )
    
    EXPERIMENTS.append(EXPERIMENT_M1)

    features = []
    labels = []
    for experiment in EXPERIMENTS:
        print(f'\nAnalysing {experiment.get_subject()}')
        # Hier functie van Joos om automatisch data te croppen
        calibration_data = PreprocessingPipeline(experiment.get_calibration_data()).start()
        # DataPlot.eeg_channels_plot(calibration_data)
        experiment_data = PreprocessingPipeline(experiment.get_experiment_data(), calibration_data).start()
        data_portions = crop(experiment_data[8000:20000], 5, 250)
        
        for data in data_portions:
            features.append(np.array(FeaturePipeline(data).start()).reshape(240,1))

        labels.append(get_labels(experiment.get_experiment_description_file(), 2))

    # This converts list with sublist features into large list and reshapes it into 240x18
    # features = np.array([item for sublist in features for item in sublist]).reshape(18,240)
    # features_normalized = np.empty((240, 18))
    # for index, column in enumerate(features.T):
    #     features_normalized[index,:] = np.linalg.norm(column)
    
    # features_normalized = features_normalized.T
    # print(features_normalized.s)

        # Do feature Extraction
        # features = FeaturePipeline(experiment_data).start()
        
        # Aggregate result(?)