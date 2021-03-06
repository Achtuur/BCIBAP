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
    sys.path.append(str(Path('./PipelineComponents/Classification').resolve()))
    sys.path.append(str(Path('./Data').resolve()))
    sys.path.append(str(Path('./Data/ExperimentResults').resolve()))

# Experiments
from ExperimentWrapper import ExperimentWrapper

# Preprocessing
from PreprocessingPipeline import PreprocessingPipeline
from crop import crop
from Visualize import DataPlot

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

    # This Shouldn't Change unless you add experiments
    #-------------------------------------------------------------------- 
    EXPERIMENTS = []
    
    # Sam
    EXPERIMENT_SAM =ExperimentWrapper("Sam", 
        'Pseudo',
        Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_calibration.npy'),
    )

    EXPERIMENT_SAM = EXPERIMENT_SAM.set_experiment_data(
        Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_pseudo.npy')    
    ).set_experiment_description_file(
        Path('./Data/Experiments/Pseudowords/results/data_2022-05-10_09-51-54.724695.csv')
    )

    EXPERIMENTS.append(EXPERIMENT_SAM)

    # M1
    EXPERIMENT_M1 = ExperimentWrapper("M1", 
        'Pseudo',    
        Path('./Data/ExperimentResults/recorded_data/recordings_numpy/M1_10_05_2022/OpenBCISession_M1_calibration.npy'),
    )

    EXPERIMENT_M1 = EXPERIMENT_M1.set_experiment_data(
        Path('./Data/ExperimentResults/recorded_data/recordings_numpy/M1_10_05_2022/OpenBCISession_M1_pseudo.npy')
    ).set_experiment_description_file(
        Path('./Data/Experiments/Pseudowords/results/data_2022-05-10_11-31-17.544482.csv')
    )

    EXPERIMENTS.append(EXPERIMENT_M1)

    # Simon
    EXPERIMENT_SIMON = ExperimentWrapper("Simon", 
        'Pseudo',    
        Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Simon_17_05_2022/OpenBCISession_Simon_calibration.npy')
    )

    EXPERIMENT_SIMON = EXPERIMENT_SIMON.set_experiment_data(
        Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Simon_17_05_2022/OpenBCISession_Simon_pseudo.npy')
    ).set_experiment_description_file(
        Path('./Data/Experiments/Pseudowords/results/Simon_17-05-2022_pseudo_take1.csv')
    )

    EXPERIMENTS.append(EXPERIMENT_SIMON)

    # F1
    EXPERIMENT_F1 = ExperimentWrapper('F1',
        'Pseudo',    
        Path('./Data/ExperimentResults/recorded_data/recordings_numpy/F1_17_05_2022/OpenBCISession_F1_calibration.npy')
    )

    EXPERIMENT_F1 = EXPERIMENT_F1.set_experiment_data(
        Path('./Data/ExperimentResults/recorded_data/recordings_numpy/F1_17_05_2022/OpenBCISession_F1_pseudo.npy')
    ).set_experiment_description_file(
        Path('./Data/Experiments/Pseudowords/results/F1_17-05-2022_pseudo_take1.csv')
    )

    EXPERIMENTS.append(EXPERIMENT_F1)
    #-------------------------------------------------------------------- 
   

    # This can be changed, but you'll probably only need to change the lines 
    # where the Features are calculated and the PCA stuff
    #-------------------------------------------------------------------- 
    features = np.array([])
    labels = []
    for experiment in EXPERIMENTS:
        calibration_data = PreprocessingPipeline(experiment.get_calibration_data()).start()
        data = PreprocessingPipeline(experiment.get_experiment_data(), experiment.get_calibration_data()).start()
        
        # This is not correct
        cropped_data = crop(data, 5, 250)
                
        # Calculate Features, reshaped to 240x1 numpy array
        for data_interval in cropped_data:
            try:
                features = np.vstack([features, np.array(FeaturePipeline(data_interval).start()).reshape(1,240)])
            except ValueError:
                features = np.array(FeaturePipeline(data_interval).start()).reshape(1,240)

        
        labels = labels + get_labels(experiment.get_experiment_description_file())

    
    features_normalized = normalize(features, axis=0)

    # This is arbitrarily chosen and depends on how many features you have
    pca = PCA(n_components=80)
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
    #-------------------------------------------------------------------- 


    # Below can be changed freely
    #-------------------------------------------------------------------- 
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
    #-------------------------------------------------------------------- 