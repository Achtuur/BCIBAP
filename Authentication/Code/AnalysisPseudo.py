import numpy as np
import csv
import random
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from math import floor


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
    sys.path.append(str(Path('./PipelineComponents/PrepareData').resolve()))
    sys.path.append(str(Path('./PipelineComponents/Classification').resolve()))
    sys.path.append(str(Path('./Data/ExperimentResults').resolve()))

# Experiments
from ExperimentWrapper import ExperimentWrapper

# Preprocessing
from PreprocessingPipeline import PreprocessingPipeline
from Visualize import DataPlot

# PrepareData
from prepare_data import crop

# Feature Extraction
from FeaturePipeline import FeaturePipeline

# Classification
from SVM import svm_classifier

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
    EXPERIMENT_SAM =ExperimentWrapper("Sam", 
        'Pseudo',
        Path('./PipelineComponents/PrepareData/recorded_data/recordings_numpy/OpenBCISession_Sam_calibration/OpenBCI-RAW-2022-05-10_09-35-30/OpenBCI-RAW-2022-05-10_09-35-30.npy'),
        (250*62, 250*122)
    )

    EXPERIMENT_SAM = EXPERIMENT_SAM.set_experiment_data_path(
        Path('./PipelineComponents/PrepareData/recorded_data/recordings_numpy/OpenBCISession_Sam_pseudo/OpenBCI-RAW-2022-05-10_09-51-49/')    
    ).set_experiment_description_file(
        Path('./Data/Experiments/Pseudowords/results/data_2022-05-10_09-51-54.724695.csv')
    )

    EXPERIMENTS.append(EXPERIMENT_SAM)

    # M1
    EXPERIMENT_M1 = ExperimentWrapper("M1", 
        'Pseudo',    
        Path('./PipelineComponents/PrepareData/recorded_data/recordings_numpy/OpenBCISession_Wessel_calibration/OpenBCI-RAW-2022-05-10_11-28-23/OpenBCI-RAW-2022-05-10_11-28-23.npy'),
        (250*15, 250*75)
    )
    EXPERIMENT_M1 = EXPERIMENT_M1.set_experiment_data_path(
        Path('./PipelineComponents/PrepareData/recorded_data/recordings_numpy/OpenBCISession_Wessel_pseudo/OpenBCI-RAW-2022-05-10_11-31-11/')
    ).set_experiment_description_file(
        Path('./Data/Experiments/Pseudowords/results/data_2022-05-10_11-31-17.544482.csv')
    )

    EXPERIMENTS.append(EXPERIMENT_M1)

    # Simon
    EXPERIMENT_SIMON = ExperimentWrapper("Simon",
        'Pseudo',
        Path('')
    )

    features = np.array([])
    labels = []
    for experiment in EXPERIMENTS:
        calibration_data = PreprocessingPipeline(experiment.get_calibration_data()).start()
        cropped_data = crop(experiment.get_experiment_description_file(), experiment.get_experiment_data_path(), 5, 250) 
        cropped_data = list(map(lambda x: PreprocessingPipeline(x, calibration_data).start(), cropped_data))
        
        # Calculate Features, reshaped to 240x1 numpy array
        for data_interval in cropped_data:
            try:
                features = np.vstack([features, np.array(FeaturePipeline(data_interval).start()).reshape(1,240)])
            except ValueError:
                features = np.array(FeaturePipeline(data_interval).start()).reshape(1,240)

        labels = labels + get_labels(experiment.get_experiment_description_file())

    
    features_normalized = normalize(features, axis=0)
    # This is arbitrarily chosen
    pca = PCA(n_components=40)
    principal_components = pca.fit_transform(features_normalized)
    principal_components = principal_components.tolist() 

    # Randomise data
    training_data = list(zip(principal_components, labels))
    random.shuffle(training_data)
    principal_components[:], labels[:] = zip(*training_data)

    # Create train and test data
    total_length = len(training_data)
    split_percentage = 0.6

    split = floor(split_percentage * total_length)
    train_data = principal_components[:split]
    train_labels = labels[:split]

    test_data = principal_components[split+1:]
    test_labels = labels[split+1:]

    # # Train classifier
    svm = svm_classifier(train_data, train_labels)

    result = []
    for test in test_data:
        result.append(svm.predict(np.array([test])))

    correct = 0
    for i,j in list(zip(test_labels, result)):
        if i == j[0]:
            correct += 1

    print(f'Number of test samples: {len(test_data)}\nTotal Correct: {correct}\nAccuracy: {correct/len(test_data)}')