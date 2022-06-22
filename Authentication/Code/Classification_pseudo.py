import sys
import platform
from pathlib import Path 
import csv
import numpy as np
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
    sys.path.append(str(Path('./Data').resolve()))
    sys.path.append(str(Path('./Data/ExperimentResults').resolve()))
from ExperimentWrapper import ExperimentWrapper
from PreprocessingPipeline import PreprocessingPipeline
from FeaturesLos import get_frequency_band_power, get_signal_power#, left_hemisphere_difference_ratio
from Filters import Filter
from crop import crop
from sklearn.decomposition import PCA
from combine_data_and_labels import combine_data_and_labels
import random
from SVM import svm_classifier
from sklearn import preprocessing
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt

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

    features = [] #list of features per data segment. Each segment contains following features: [power in 30 hz band]
    labels = []


    EXPERIMENTS = []

    EXPERIMENT_JOOS_TAKE_1 = ExperimentWrapper("Joos_1_1", "pseudo")
    EXPERIMENT_JOOS_TAKE_1.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_exp_pseudo2_1s_take1.npy"))
    EXPERIMENT_JOOS_TAKE_1.set_experiment_labels([1] * 20 + [0] * 20)
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_1)

    EXPERIMENT_JOOS_TAKE_2 = ExperimentWrapper("Joos_1_2", "pseudo")
    EXPERIMENT_JOOS_TAKE_2.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_exp_pseudo2_1s_take2.npy"))
    EXPERIMENT_JOOS_TAKE_2.set_experiment_labels([1] * 20 + [0] * 20)
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_2)

    EXPERIMENT_JOOS_TAKE_3 = ExperimentWrapper("Joos_1_3", "pseudo")
    EXPERIMENT_JOOS_TAKE_3.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_exp_pseudo2_1s_take3.npy"))
    EXPERIMENT_JOOS_TAKE_3.set_experiment_labels([1] * 20 + [0] * 20)
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_3)

    EXPERIMENT_SAM_TAKE_2 = ExperimentWrapper("Sam_2_1", "pseudo")
    EXPERIMENT_SAM_TAKE_2.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_pw_7juni_take2.npy"))
    EXPERIMENT_SAM_TAKE_2.set_experiment_labels([1] * 20 + [0] * 20)
    EXPERIMENTS.append(EXPERIMENT_SAM_TAKE_2)

    EXPERIMENT_SAM_TAKE_3 = ExperimentWrapper("Sam_2_2", "pseudo")
    EXPERIMENT_SAM_TAKE_3.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_pw_7juni_take3.npy"))
    EXPERIMENT_SAM_TAKE_3.set_experiment_labels([1] * 20 + [0] * 20)
    EXPERIMENTS.append(EXPERIMENT_SAM_TAKE_3)

    EXPERIMENT_SAM_TAKE_4 = ExperimentWrapper("Sam_2_3", "pseudo")
    EXPERIMENT_SAM_TAKE_4.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_pw_7juni_take4.npy"))
    EXPERIMENT_SAM_TAKE_4.set_experiment_labels([1] * 20 + [0] * 20)
    EXPERIMENTS.append(EXPERIMENT_SAM_TAKE_4)

    EXPERIMENT_SAM_TAKE_RANDOM_1 = ExperimentWrapper("Sam_2_4_rand", "pseudorandom")
    EXPERIMENT_SAM_TAKE_RANDOM_1.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_sam-pw-random-7-juni.npy"))
    EXPERIMENT_SAM_TAKE_RANDOM_1.set_experiment_labels(['1', '0', '1', '0', '1', '0', '1', '1', '0', '0', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '1', '0', '0', '0', '1', '1', '0', '0', '1', '1', '1', '1', '0', '1', '1', '0', '1', '0', '0', '0'])
    EXPERIMENTS.append(EXPERIMENT_SAM_TAKE_RANDOM_1)

    EXPERIMENT_SAM_TAKE_RANDOM_2 = ExperimentWrapper("Sam_2_5_rand", "pseudorandom")
    EXPERIMENT_SAM_TAKE_RANDOM_2.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_pw_7juni_take2.npy"))
    EXPERIMENT_SAM_TAKE_RANDOM_2.set_experiment_labels(['0', '1', '1', '0', '0', '0', '1', '1', '0', '0', '0', '1', '0', '0', '1', '1', '1', '1', '0', '1', '1', '1', '0', '1', '0', '0', '0', '0', '1', '1', '0', '1', '1', '1', '0', '0', '1', '0', '1', '0'])
    EXPERIMENTS.append(EXPERIMENT_SAM_TAKE_RANDOM_2)

    EXPERIMENT_SIMON_TAKE_RANDOM_1 = ExperimentWrapper("Simon_3_1_rand", "pseudorandom")
    EXPERIMENT_SIMON_TAKE_RANDOM_1.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_Simon_exp_pseudo_random_take1.npy"))
    EXPERIMENT_SIMON_TAKE_RANDOM_1.set_experiment_labels(['1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '1', '1', '0', '1', '0', '1', '1', '1', '1', '0', '1', '0', '1', '1', '1', '0', '1', '1', '1', '0', '1', '0', '0', '0', '0', '1', '0', '1', '0'])
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_RANDOM_1)

    EXPERIMENT_SIMON_TAKE_RANDOM_2 = ExperimentWrapper("Simon_3_2_rand", "pseudorandom")
    EXPERIMENT_SIMON_TAKE_RANDOM_2.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_Simon_exp_pseudo_random_take2.npy"))
    EXPERIMENT_SIMON_TAKE_RANDOM_2.set_experiment_labels(['1', '0', '1', '1', '1', '1', '0', '1', '0', '1', '1', '1', '0', '1', '0', '0', '0', '0', '1', '0', '1', '1', '1', '1', '1', '0', '0', '1', '0', '0', '0', '1', '0', '1', '0', '0', '0', '1', '0', '0'])
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_RANDOM_2)

    EXPERIMENT_SIMON_TAKE_RANDOM_3 = ExperimentWrapper("Simon_3_3_rand", "pseudorandom")
    EXPERIMENT_SIMON_TAKE_RANDOM_3.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_Simon_exp_pseudo_random_take3.npy"))
    EXPERIMENT_SIMON_TAKE_RANDOM_3.set_experiment_labels(['1', '0', '1', '0', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '0', '1', '0', '1', '0', '1', '0', '1', '0', '0', '1', '1', '0', '0', '1', '0', '1', '1', '0', '0', '1', '1', '1', '0', '1'])
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_RANDOM_3)

    EXPERIMENT_SIMON_TAKE_RANDOM_4 = ExperimentWrapper("Simon_3_4_rand", "pseudorandom")
    EXPERIMENT_SIMON_TAKE_RANDOM_4.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_Simon_exp_pseudo_random_take4.npy"))
    EXPERIMENT_SIMON_TAKE_RANDOM_4.set_experiment_labels(['0', '0', '1', '1', '1', '0', '1', '0', '1', '0', '0', '1', '1', '1', '1', '1', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '1', '1', '1', '1', '1', '0', '1', '1', '0', '1', '0', '0', '0', '0'])
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_RANDOM_4)

    EXPERIMENT_SIMON_TAKE_RANDOM_5 = ExperimentWrapper("Simon_3_5_rand", "pseudorandom")
    EXPERIMENT_SIMON_TAKE_RANDOM_5.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_Simon_exp_pseudo_random_take5.npy"))
    EXPERIMENT_SIMON_TAKE_RANDOM_5.set_experiment_labels(['0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '1', '1', '1', '0', '1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '1', '0', '1', '0', '1', '1', '1', '1', '0'])
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_RANDOM_5)

    EXPERIMENT_JOOS_TAKE_RANDOM_1 = ExperimentWrapper("Joos_4_1_rand", "pseudorandom")
    EXPERIMENT_JOOS_TAKE_RANDOM_1.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_exp_pseudo_random_take1.npy"))
    EXPERIMENT_JOOS_TAKE_RANDOM_1.set_experiment_labels(['0', '1', '0', '1', '1', '0', '1', '1', '0', '1', '1', '0', '1', '1', '0', '1', '0', '0', '0', '1', '0', '1', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '1', '0', '1', '1', '0', '0', '1'])
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_RANDOM_1)

    EXPERIMENT_JOOS_TAKE_RANDOM_2 = ExperimentWrapper("Joos_4_2_rand", "pseudorandom")
    EXPERIMENT_JOOS_TAKE_RANDOM_2.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_exp_pseudo_random_take2.npy"))
    EXPERIMENT_JOOS_TAKE_RANDOM_2.set_experiment_labels(['1', '1', '1', '0', '0', '1', '1', '1', '0', '1', '1', '0', '0', '0', '0', '0', '1', '0', '1', '1', '1', '0', '1', '0', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0', '1', '0', '1', '0', '0', '0'])
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_RANDOM_2)

    EXPERIMENT_JOOS_TAKE_RANDOM_3 = ExperimentWrapper("Joos_4_3_rand", "pseudorandom")
    EXPERIMENT_JOOS_TAKE_RANDOM_3.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_exp_pseudo_random_take3.npy"))
    EXPERIMENT_JOOS_TAKE_RANDOM_3.set_experiment_labels(['0', '1', '1', '1', '0', '1', '1', '1', '1', '0', '0', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '1', '1', '1', '0', '0', '1', '1', '1', '0', '1', '0', '0', '1', '0', '1'])
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_RANDOM_3)

    EXPERIMENT_JOOS_TAKE_RANDOM_4 = ExperimentWrapper("Joos_4_4_rand", "pseudorandom")
    EXPERIMENT_JOOS_TAKE_RANDOM_4.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_exp_pseudo_random_take4.npy"))
    EXPERIMENT_JOOS_TAKE_RANDOM_4.set_experiment_labels(['1', '0', '0', '0', '0', '0', '1', '1', '0', '0', '1', '0', '1', '1', '0', '1', '0', '1', '1', '1', '1', '0', '1', '1', '0', '0', '0', '1', '0', '0', '0', '0', '1', '1', '1', '0', '1', '1', '0', '1'])
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_RANDOM_4)

    # EXPERIMENT_SIMON_LONG_PSEUDO_1 = ExperimentWrapper("Simon", "pseudorandom")
    # EXPERIMENT_SIMON_LONG_PSEUDO_1.set_experiment_data(Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_Simon_long_pseudo_take1.npy'))
    # EXPERIMENT_SIMON_LONG_PSEUDO_1.set_experiment_labels(get_labels(Path('./Data/Experiments/Pseudowords/simon_long_pseudo_take1.csv')))
    # EXPERIMENTS.append(EXPERIMENT_SIMON_LONG_PSEUDO_1)

    # EXPERIMENT_SIMON_LONG_PSEUDO_2 = ExperimentWrapper("Simon", "pseudorandom")
    # EXPERIMENT_SIMON_LONG_PSEUDO_2.set_experiment_data(Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_simon_long_pseudo_take2.npy'))
    # EXPERIMENT_SIMON_LONG_PSEUDO_2.set_experiment_labels(get_labels(Path('./Data/Experiments/Pseudowords/simon_long_pseudo_take2.csv')))
    # EXPERIMENTS.append(EXPERIMENT_SIMON_LONG_PSEUDO_2)

    # EXPERIMENT_SIMON_LONG_PSEUDO_3 = ExperimentWrapper("Simon", "pseudorandom")
    # EXPERIMENT_SIMON_LONG_PSEUDO_3.set_experiment_data(Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_simon_long_pseudo_take3.npy'))
    # EXPERIMENT_SIMON_LONG_PSEUDO_3.set_experiment_labels(get_labels(Path('./Data/Experiments/Pseudowords/simon_long_pseudo_take3.csv')))
    # EXPERIMENTS.append(EXPERIMENT_SIMON_LONG_PSEUDO_3)

    # # EXPERIMENT_SIMON_LONG_PSEUDO_4 = ExperimentWrapper("Simon", "pseudorandom")
    # # EXPERIMENT_SIMON_LONG_PSEUDO_4.set_experiment_data(Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_simon_long_pseudo_take4.npy'))
    # # EXPERIMENT_SIMON_LONG_PSEUDO_4.set_experiment_labels(get_labels(Path('./Data/Experiments/Pseudowords/simon_long_pseudo_take4.csv')))
    # # EXPERIMENTS.append(EXPERIMENT_SIMON_LONG_PSEUDO_4)

    # EXPERIMENT_SIMON_LONG_PSEUDO_5 = ExperimentWrapper("Simon", "pseudorandom")
    # EXPERIMENT_SIMON_LONG_PSEUDO_5.set_experiment_data(Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_simon_long_pseudo_take5.npy'))
    # EXPERIMENT_SIMON_LONG_PSEUDO_5.set_experiment_labels(get_labels(Path('./Data/Experiments/Pseudowords/simon_long_pseudo_take5.csv')))
    # EXPERIMENTS.append(EXPERIMENT_SIMON_LONG_PSEUDO_5)

    # EXPERIMENT_SIMON_LONG_PSEUDO_6 = ExperimentWrapper("Simon", "pseudorandom")
    # EXPERIMENT_SIMON_LONG_PSEUDO_6.set_experiment_data(Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_simon_long_pseudo_take6.npy'))
    # EXPERIMENT_SIMON_LONG_PSEUDO_6.set_experiment_labels(get_labels(Path('./Data/Experiments/Pseudowords/simon_long_pseudo_take6.csv')))
    # EXPERIMENTS.append(EXPERIMENT_SIMON_LONG_PSEUDO_6)


    # EXPERIMENT_SIMON_LONG_PSEUDO_7 = ExperimentWrapper("Simon", "pseudorandom")
    # EXPERIMENT_SIMON_LONG_PSEUDO_7.set_experiment_data(Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_simon_long_pseudo_take7.npy'))
    # EXPERIMENT_SIMON_LONG_PSEUDO_7.set_experiment_labels(get_labels(Path('./Data/Experiments/Pseudowords/simon_long_pseudo_take7.csv')))
    # EXPERIMENTS.append(EXPERIMENT_SIMON_LONG_PSEUDO_7)


    # EXPERIMENT_SIMON_LONG_PSEUDO_8 = ExperimentWrapper("Simon", "pseudorandom")
    # EXPERIMENT_SIMON_LONG_PSEUDO_8.set_experiment_data(Path('./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_simon_long_pseudo_take8.npy'))
    # EXPERIMENT_SIMON_LONG_PSEUDO_8.set_experiment_labels(get_labels(Path('./Data/Experiments/Pseudowords/simon_long_pseudo_take8.csv')))
    # EXPERIMENTS.append(EXPERIMENT_SIMON_LONG_PSEUDO_8)

    # average_score = []
    # for _ in range(20):
    features_total = np.array([])
    labels = []
    for experiment in EXPERIMENTS:
        labels += experiment.get_experiment_labels()
        data = experiment.get_experiment_data()
        data_filtered = PreprocessingPipeline(data).start()
        data_cropped = crop(data_filtered, 2, 250)
        data_cropped = list(map(lambda x: Filter.remove_bad_channels(x), data_cropped))
        data_cropped = [x for x in data_cropped if x is not None]
        data_artifacts_removed = np.concatenate(data_cropped)

        data_intervals = crop(data_artifacts_removed, 1, 250)
        average_power = []
        for channel in ['0', '1', '2', '3', '4', '5', '6', '7']:
            for index,data_interval in enumerate(data_intervals):
                band_powers = list(get_frequency_band_power(data_interval)[channel].values())
                average_power.append(band_powers)
        average_power = np.array(average_power)
        # plt.bar([1,2,3,4,5] ,np.mean(average_power, axis=0))
        # plt.title(f'{experiment.get_subject()}')
        # plt.xlabel('hello')
        # plt.show(block=True)
        print(f'Experiment: {experiment.get_subject()} - Channel: {int(channel) + 1} - Average Power: {np.mean(average_power, axis=0)}')
            # band_power_list = []

            # for channel_band_power in band_powers.values():
            #     for band_power in channel_band_power.values():
            #         band_power_list.append(band_power)

            # signal_powers = get_signal_power(data_interval)
            # signal_power_list = list(signal_powers.values()) 

            # features_interval = band_power_list + signal_power_list
            # try:
            #     features = np.vstack((np.array(features), np.array(features_interval)))
            # except:
            #     features = np.array(features_interval)
        # features = normalize(features, axis=1)
        # try:
        #     features_total = np.vstack((np.array(features_total), np.array(features)))
        # except:
        #     features_total = np.array(features)

    # features = features_total
    # print(features.shape)
    # print(len(labels))
    # scaler = preprocessing.StandardScaler().fit(features)
    # features = scaler.transform(features)
    # pca = PCA(n_components=20).fit(features.T)

    # pca_components = pca.components_[:]
    # pca_components_list = []
    # for i in range(pca_components.shape[1]): 
    #     pca_components_list.append(pca_components[:,i].tolist())

    # data_and_labels = combine_data_and_labels(pca_components_list, labels)
    # random.shuffle(data_and_labels)

    # split = int(0.6 * len(data_and_labels))
    # train_data = data_and_labels[:split]
    # test_data = data_and_labels[split:]

    # train_features = [x[0] for x in train_data]
    # train_labels = [x[1] for x in train_data]
    # svm = svm_classifier(train_features, train_labels)

    # test_features = [x[0] for x in test_data]
    # test_labels = [x[1] for x in test_data]

    # predictions = []
    # for test_data_point in test_features:
    #     predictions.append(svm.predict(np.array(test_data_point).reshape(1,-1)))

    # total = len(test_labels)
    # correct = 0
    # for prediction, test_label in zip(predictions, test_labels):
    #     if int(prediction) == int(test_label):
    #         correct += 1

    # average_score.append(correct/total)
    # print(np.mean(np.array(average_score)))
        # print(correct/total)