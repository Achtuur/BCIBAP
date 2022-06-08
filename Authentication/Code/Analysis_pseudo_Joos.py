import sys
import platform
from pathlib import Path 
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
from FeaturePipeline import FeaturePipeline
from crop import crop
from crop import cut
import scipy.signal as sig
from Filters import Filter
import matplotlib.pyplot as plt
from statistics import mean
from SVM import svm_classifier
import random
import sklearn
from sklearn.decomposition import PCA


def power_baseline(data_segment):
    data_segment = Filter.remove_bad_channels(data_segment)
    power_baseline_per_channel = []
    for channel in data_segment:
        channel_fft = np.absolute(np.fft.fft(channel, 250))
        channel = np.absolute(np.fft.ifft(np.append(channel_fft[:125],np.zeros(125))))
        power_baseline = np.mean(np.square(channel)) / 125
        power_baseline_per_channel.append(power_baseline)

    return power_baseline_per_channel

def power_20hz(data_segment):
    data_segment = Filter.remove_bad_channels(data_segment)
    power_20hz_per_channel = []
    for channel in data_segment:
        channel_fft = np.absolute(np.fft.fft(channel, 250))
        channel_20hz = np.absolute(np.fft.ifft(np.append(np.zeros(15),np.append(channel_fft[15:25],np.zeros(225)))))
        power_20hz = np.mean(np.square(channel_20hz)) / 10
        power_20hz_per_channel.append(power_20hz)
    
    return power_20hz_per_channel

def power_30hz(data_segment):
    data_segment = Filter.remove_bad_channels(data_segment)
    power_30hz_per_channel = []
    for channel in data_segment:
        channel_fft = np.absolute(np.fft.fft(channel, 250))
        channel_30hz = np.absolute(np.fft.ifft(np.append(np.zeros(25),np.append(channel_fft[25:35],np.zeros(215)))))
        power_30hz = np.mean(np.square(channel_30hz)) / 10
        power_30hz_per_channel.append(power_30hz)
    
    return power_30hz_per_channel

def power_40hz(data_segment):
    data_segment = Filter.remove_bad_channels(data_segment)
    power_40hz_per_channel = []
    for channel in data_segment:
        channel_fft = np.absolute(np.fft.fft(channel, 250))
        channel_40hz = np.absolute(np.fft.ifft(np.append(np.zeros(35),np.append(channel_fft[35:45],np.zeros(205)))))
        power_40hz = np.mean(np.square(channel_40hz)) / 10
        power_40hz_per_channel.append(power_40hz)
    
    return power_40hz_per_channel

def power_50hz(data_segment):
    data_segment = Filter.remove_bad_channels(data_segment)
    power_50hz_per_channel = []
    for channel in data_segment:
        channel_fft = np.absolute(np.fft.fft(channel, 250))
        channel_50hz = np.absolute(np.fft.ifft(np.append(np.zeros(45),np.append(channel_fft[45:55],np.zeros(195)))))
        power_50hz = np.mean(np.square(channel_50hz)) / 10
        power_50hz_per_channel.append(power_50hz)
    
    return power_50hz_per_channel



if __name__ == "__main__":

    features = [] #list of features per data segment. Each segment contains following features: [power in 30 hz band]
    labels = [0] * 20 + [1] *20 + [0] * 20 + [1] *20 + [0] * 20 + [1] *20

    EXPERIMENTS = []

    # EXPERIMENT_SIMON_6HZ = ExperimentWrapper("Simon", "ft")
    # EXPERIMENT_SIMON_6HZ.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Simon\OpenBCISession_Simon_stage1_6hz.npy"))
    # EXPERIMENT_SIMON_6HZ.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/simon_23-05-2022_ft1_take2.csv"))
    # EXPERIMENTS.append(EXPERIMENT_SIMON_6HZ)

    EXPERIMENT_JOOS_TAKE_1 = ExperimentWrapper("Joos", "pseudo")
    EXPERIMENT_JOOS_TAKE_1.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\Joos\OpenBCISession_Joos_exp_pseudo2_1s_take1.npy"))
    EXPERIMENT_JOOS_TAKE_1.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/simon_23-05-2022_ft1_take1.csv"))
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_1)

    EXPERIMENT_JOOS_TAKE_2 = ExperimentWrapper("Joos", "pseudo")
    EXPERIMENT_JOOS_TAKE_2.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\Joos\OpenBCISession_Joos_exp_pseudo2_1s_take2.npy"))
    EXPERIMENT_JOOS_TAKE_2.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/simon_23-05-2022_ft1_take2.csv"))
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_2)

    EXPERIMENT_JOOS_TAKE_3 = ExperimentWrapper("Joos", "pseudo")
    EXPERIMENT_JOOS_TAKE_3.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\Joos\OpenBCISession_Joos_exp_pseudo2_1s_take3.npy"))
    EXPERIMENT_JOOS_TAKE_3.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/simon_23-05-2022_ft1_take2.csv"))
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_3)

    for experiment in EXPERIMENTS:
        experiment_data = experiment.get_experiment_data()

        data_filtered = PreprocessingPipeline(experiment_data).start().T
        plt.show(block=True)
        data_chopped = cut(data_filtered, t_window = 1, f_sampling = 250)

        power_segment_channel = []
        for data_segment in data_chopped:
            power_baseline_per_channel = power_baseline(data_segment)
            power_20hz_per_channel = power_20hz(data_segment)
            power_30hz_per_channel = power_30hz(data_segment)
            power_40hz_per_channel = power_40hz(data_segment)
            power_50hz_per_channel = power_50hz(data_segment)
            features.append(power_baseline_per_channel + power_20hz_per_channel + power_30hz_per_channel + power_40hz_per_channel + power_50hz_per_channel)
            power_segment_channel.append(power_20hz_per_channel)


#for plotting something
        # print(len(power_segment_channel))
        # control = power_segment_channel[0:20]
        # pseudo = power_segment_channel[20:40]

        # power_per_band_control = np.zeros(8)
        # for segment in control:
        #     power_per_band_control = np.add(power_per_band_control, segment)
        # power_per_band_pseudo = np.zeros(8)
        # for segment in pseudo:
        #     power_per_band_pseudo = np.add(power_per_band_pseudo, segment)

        # x = np.linspace(1,8,8)
        # plt.title('power around 30 hz per channel')
        # plt.bar(x - 0.2, power_per_band_control,0.4, label = 'control word')
        # plt.bar(x + 0.2, power_per_band_pseudo, 0.4, label = 'pseudo-word')
        # plt.legend()
        # plt.show(block=True)

    #classify using svm
    accuracy_list = []
    features = np.asarray(features).T
    pca = PCA(n_components = 40)
    pca.fit(features) 
    features = pca.components_[:30].T
    print(features.shape)

    for i in range(200):
        c = []
        features_shuffled = features
        labels_shuffled = labels
        c = list(zip(features_shuffled, labels_shuffled))

        random.shuffle(c)

        features_shuffled, labels_shuffled = zip(*c)
        features_shuffled = np.asarray(features_shuffled)

        labels_shuffled = np.array(labels_shuffled)

        training_data = features_shuffled[:80]
        training_labels = labels_shuffled[:80]
        test_data = features_shuffled[80:]
        test_labels = labels_shuffled[80:]
        SVM = svm_classifier(training_data, training_labels)
        
        accurate = 0
        for index, test_features in enumerate(test_data):
            result = SVM.predict([test_features])
            if result == test_labels[index]:
                accurate = accurate + 1

        accuracy_list.append(accurate/40)
    print(mean(accuracy_list))
    








