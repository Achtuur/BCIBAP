import numpy as np
import random
import sys
import platform
from pathlib import Path
from AnalysisPseudo import get_labels
from AnalysisMentalTaskCyril import average_power
from AnalysisMentalTaskCyril import gen_power_plot
from FeaturePipeline import FeaturePipeline
from Filters import Filter
from Visualize import DataPlot
from combine_data_and_labels import combine_data_and_labels
from sklearn.metrics import confusion_matrix
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
from Kfold_CV import Models
from crop import crop
import matplotlib.pyplot as plt
import matplotlib 

def pow_plot(data, labels):
    av = []
    result = []
    for block in data:
        av_once = average_power(Filter.band_pass_filter(block, 4, (12, 18), 250))
        for i in range(10):
            av.append(av_once)
        cropped_data = crop(block, 0.2, 250)
        for data_interval in cropped_data:
            data_interval = Filter.band_pass_filter(data_interval, 4, (12, 18), 250)
            result.append(average_power(data_interval))
    plt.plot(result, label="Power")
    plt.xlabel('Time [s]')
    plt.ylabel('Power [uV^2]')
    plt.title('Power vs Time')
    plt.plot(av, '--', label="Average Power over interval")
    # plt.plot(np.linspace(0, 400, len(labels)), labels, label="labels")
    plt.legend()
    plt.show(block=True)

def make_experiments_list():
    
    EXPERIMENTS = []

    EXPERIMENT_SIMON_TAKE_1 = ExperimentWrapper("Simon", "ft")
    EXPERIMENT_SIMON_TAKE_1.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_Simon_stage1_take1.npy"))
    EXPERIMENT_SIMON_TAKE_1.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Simon_2022-05-23_ft1_take1.csv"))
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_1)

    EXPERIMENT_SIMON_TAKE_2 = ExperimentWrapper("Simon", "ft")
    EXPERIMENT_SIMON_TAKE_2.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Simon/OpenBCISession_Simon_stage1_take2.npy"))
    EXPERIMENT_SIMON_TAKE_2.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Simon_2022-05-23_ft1_take2.csv"))
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_2)

    EXPERIMENT_JOOS_TAKE_1 = ExperimentWrapper("Joos", "ft")
    EXPERIMENT_JOOS_TAKE_1.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_stage1_take1.npy"))
    EXPERIMENT_JOOS_TAKE_1.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Joos_2022-05-23_ft1_take1.csv"))
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_1)

    EXPERIMENT_JOOS_TAKE_2 = ExperimentWrapper("Joos", "ft")
    EXPERIMENT_JOOS_TAKE_2.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_stage1_take2.npy"))
    EXPERIMENT_JOOS_TAKE_2.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Joos_2022-05-23_ft1_take2.csv"))
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_2)

    # EXPERIMENT_SAM_TAKE_1 = ExperimentWrapper("Sam", "ft")
    # EXPERIMENT_SAM_TAKE_1.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_stage1_take1.npy"))
    # EXPERIMENT_SAM_TAKE_1.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Sam_2022-05-23_ft1_take1.csv"))
    # EXPERIMENTS.append(EXPERIMENT_SAM_TAKE_1)

    EXPERIMENT_SAM_TAKE_2 = ExperimentWrapper("Sam", "ft")
    EXPERIMENT_SAM_TAKE_2.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_stage1_take2.npy"))
    EXPERIMENT_SAM_TAKE_2.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Sam_2022-05-23_ft1_take2.csv"))
    EXPERIMENTS.append(EXPERIMENT_SAM_TAKE_2)

    return EXPERIMENTS

if __name__ == "__main__":
    f_sampling = 250
    EXPERIMENTS = make_experiments_list()
    for index, experiment in enumerate(EXPERIMENTS):
        data = PreprocessingPipeline(experiment.get_experiment_data()).start()
        labels = get_labels(experiment.get_experiment_description_file())
        cropped_data = crop(data, 2, f_sampling)
        
        #filter bad channels
        filtered_data = []
        for segment in cropped_data:
            filtered_data.append(Filter.remove_bad_channels(segment))
        # pow_plot(filtered_data, labels)
        
        #feature extraction
        features_data = FeaturePipeline(filtered_data, f_sampling).start()

        #data with labels and concatenation
        setje = combine_data_and_labels(filtered_data, labels)
        if index==0:
            full = setje
        else:
            full = full + setje

    #randomize order
    # random.shuffle(full)

    #flatten data for ML
    data, labels = zip(*full)
    print(len(data), data[0])
    data = np.array(data).reshape(200, 4000)
    print(type(data), data.shape)

    #train test split
    X_train, X_test, Y_train, Y_test = Models.train_val_split(data, labels, 0.2)
    #train val split
    X_train, X_val, Y_train, Y_val = Models.train_val_split(X_train, Y_train, 0.2)

    #ML
    model = Models()
    gridsearch, acc = model.KFOLD_CV(X_train, Y_train, X_val, Y_val)
    for i in range(len(gridsearch)):
        best_model = gridsearch[i].best_estimator_
        Y_predict = best_model.predict(X_test)
        tn, fp, fn, tp = confusion_matrix(Y_test, Y_predict).ravel()
        print(((tn+tp)/(fp+fn+tp+tn))*100)
    

     
        