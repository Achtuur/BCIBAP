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


def power_band(data_segment, band = 0):
    data_segment = Filter.remove_bad_channels(data_segment)
    power_band_per_channel = []
    if band == 0:
        lower_bound = int(0)
        upper_bound = int(len(data_segment[0])/2)
    else:
        lower_bound = int((band - 5) * (len(data_segment[0])/250))
        upper_bound = int((band + 5) * (len(data_segment[0])/250))
    for channel in data_segment:
        channel_fft = np.absolute(np.fft.fft(channel, len(channel)))
        channel_band = np.absolute(np.fft.ifft(np.append(np.zeros(lower_bound),np.append(channel_fft[lower_bound:upper_bound],np.zeros(len(channel) - upper_bound)))))
        power_band = np.mean(np.square(channel_band)) / (upper_bound - lower_bound)
        power_band_per_channel.append(power_band)

    return power_band_per_channel


def SVM_test(features, pca_components = 30, iterations = 200):
    accuracy_list = []
    features = np.asarray(features).T
    pca = PCA(n_components = 40)
    pca.fit(features) 
    features = pca.components_[:pca_components].T
    print(features.shape)

    for i in range(iterations):
        c = []
        features_shuffled = features
        labels_shuffled = labels
        c = list(zip(features_shuffled, labels_shuffled))

        random.shuffle(c)

        features_shuffled, labels_shuffled = zip(*c)
        features_shuffled = np.asarray(features_shuffled)

        labels_shuffled = np.array(labels_shuffled)

        training_data = features_shuffled[:int(len(features_shuffled)*(3/2))]
        training_labels = labels_shuffled[:int(len(features_shuffled)*(3/2))]
        test_data = features_shuffled[int(len(features_shuffled)*(3/2)):]
        test_labels = labels_shuffled[int(len(features_shuffled)*(3/2)):]
        SVM = svm_classifier(training_data, training_labels)
        
        accurate = 0
        for index, test_features in enumerate(test_data):
            result = SVM.predict([test_features])
            if result == test_labels[index]:
                accurate = accurate + 1

        accuracy_list.append(accurate/len(test_labels))
    return accuracy_list


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

    power_segment_channel = []
    figs, axs = plt.subplots(1,3)
    plot = 0 
    for experiment in EXPERIMENTS:
        power_segment_forheatmap = []
        experiment_data = experiment.get_experiment_data()

        data_filtered = PreprocessingPipeline(experiment_data).start().T
        data_chopped = cut(data_filtered, t_window = 20, f_sampling = 250)

 
        for data_segment in data_chopped:
            power_baseline_per_channel = power_band(data_segment, band = 0)
            power_20hz_per_channel = power_band(data_segment, band = 20)
            power_30hz_per_channel = power_band(data_segment, band = 30)
            power_40hz_per_channel = power_band(data_segment, band = 40)
            power_50hz_per_channel = power_band(data_segment, band = 50)
            power_60hz_per_channel = power_band(data_segment, band = 60)
            power_segment_channel.append([power_baseline_per_channel, power_20hz_per_channel, power_30hz_per_channel, power_40hz_per_channel, 
            power_50hz_per_channel, power_60hz_per_channel])
            power_segment_forheatmap.append([power_baseline_per_channel, power_20hz_per_channel, power_30hz_per_channel, power_40hz_per_channel, 
            power_50hz_per_channel, power_60hz_per_channel])


        heatmap = np.zeros((2,len(power_segment_forheatmap[0]),8))
        for e_index, experiment in enumerate(power_segment_forheatmap):
            for b_index, band in enumerate(experiment):
                for c_index, channel in enumerate(band):
                    heatmap[e_index, b_index, c_index] = channel
        

        for (j,i),label in np.ndenumerate(np.abs(heatmap[0] - heatmap[1])):
            axs[plot].text(i,j,round(label, 3),ha='center',va='center')
        axs[plot].imshow(np.abs(heatmap[0] - heatmap[1]))

        plot = plot + 1

    figs.supxlabel('channel')
    figs.supylabel('band')
    band_labels = ('baseline', '15-25 Hz', '25-35 Hz', '35-45 Hz', '45-55 Hz', '55-65 Hz')
    axs[0].set_yticks(np.arange(len(power_segment_channel[0])), labels=band_labels)
    axs[0].set_xticks(np.arange(8), np.linspace(1,8,8))
    axs[0].set_title('Experiment 1')
    axs[1].set_yticks(np.arange(len(power_segment_channel[0])), labels=[' ']*len(band_labels))
    axs[1].set_xticks(np.arange(8), np.linspace(1,8,8))
    axs[1].set_title('Experiment 2')
    axs[2].set_yticks(np.arange(len(power_segment_channel[0])), labels=[' ']*len(band_labels))
    axs[2].set_xticks(np.arange(8), np.linspace(1,8,8))
    axs[2].set_title('Experiment 3')
    figs.suptitle('Power difference for each band-channel combination, between control words and pseudo-words [\u03BCV^2 / Hz]')
    plt.show(block=True)


        

        


    #accuracy_list = SVM_test(features)
    








