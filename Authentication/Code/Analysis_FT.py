import numpy as np
import seaborn as sns
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
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA 
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
    fig, ax = plt.subplots(constrained_layout=True)
    ax.plot(result, label="Power")
    ax.set_xticks(np.arange(5, 405, step = 10), labels)
    secax = ax.secondary_xaxis("top")
    secax.set_xticks(np.arange(0, 401, step = 25), np.arange(0, 81, step=5))
    secax.set_xlabel('Time [s]')
    ax.set_xlabel('data_labels')
    ax.set_ylabel('Power [uV^2]')
    ax.set_title('Power vs Time')
    ax.set_xlim(-1, 400)
    ax.plot(av, '--', label="Average Power over interval")
    # plt.plot(np.linspace(0, 400, len(labels)), labels, label="labels")
    plt.legend()
    plt.show(block=True)

def confusion(gridsearch):
    # fig, axs = plt.subplots(2, 2)
    cf_matrix = []
    for i in range(len(gridsearch)):
        best_model = gridsearch[i].best_estimator_
        Y_predict = best_model.predict(X_test)
        cf_matrix.append(confusion_matrix(Y_test, Y_predict))
    return cf_matrix

def plot_confusion(cf_matrix, gridsearch):
    fig, axs = plt.subplots(2, 2)
    one = sns.heatmap(cf_matrix[0], annot=True, cmap='Blues', ax=axs[0, 0])
    one.set_title(f'Decision Tree')
    # axs[0, 0].set_xlabel('Predicted Values')
    axs[0, 0].set_ylabel('Actual Values ')
    #     ## Ticket labels - List must be in alphabetical order
    axs[0, 0].xaxis.set_ticklabels([' ',' '])
    axs[0, 0].yaxis.set_ticklabels(['False','True'])

    two = sns.heatmap(cf_matrix[1], annot=True, cmap='Blues', ax=axs[0, 1])
    two.set_title(f'KNN')
    # axs[0, 1].set_xlabel('Predicted Values')
    # axs[0, 1].set_ylabel('Actual Values ')
    #     ## Ticket labels - List must be in alphabetical order
    axs[0, 1].xaxis.set_ticklabels([' ',' '])
    axs[0, 1].yaxis.set_ticklabels([' ',' '])

    three =  sns.heatmap(cf_matrix[2], annot=True, cmap='Blues', ax=axs[1, 0])
    three.set_title(f'SVM')
    axs[1, 0].set_xlabel('Predicted Values')
    axs[1, 0].set_ylabel('Actual Values ')
    #     ## Ticket labels - List must be in alphabetical order
    axs[1, 0].xaxis.set_ticklabels(['False','True'])
    axs[1, 0].yaxis.set_ticklabels(['False','True'])

    four = sns.heatmap(cf_matrix[3], annot=True, cmap='Blues', ax=axs[1, 1])
    four.set_title(f'Logistic Regression')
    axs[1, 1].set_xlabel('Predicted Values')
    # axs[1, 1].set_ylabel('Actual Values ')
    #     ## Ticket labels - List must be in alphabetical order
    axs[1, 1].xaxis.set_ticklabels(['False','True'])
    axs[1, 1].yaxis.set_ticklabels([' ',' '])
        ## Display the visualization of the Confusion Matrix.
    for ax in axs.flat:
    #     ax.set(xlabel='Predicted Values', ylabel='Actual Values')
        ax.label_outer()
# Hide x labels and tick labels for top plots and y ticks for right plots.
        
    plt.show()

def plot_parameter_tuning(gridsearch):
    kernel = gridsearch[2].cv_results_['param_kernel']
    Cs = gridsearch[2].cv_results_['param_C']
    neighbors = gridsearch[1].cv_results_['param_n_neighbors']
    plt.plot(kernel, gridsearch[2].cv_results_['split0_test_score'], label='split0')
    plt.plot(kernel, gridsearch[2].cv_results_['split1_test_score'], label='split1')
    plt.plot(kernel, gridsearch[2].cv_results_['split2_test_score'], label='split2')
    plt.plot(kernel, gridsearch[2].cv_results_['split3_test_score'], label='split3')
    plt.plot(kernel, gridsearch[2].cv_results_['split4_test_score'], label='split4')
    plt.plot(kernel, gridsearch[2].cv_results_['mean_test_score'], c='black', label = 'mean')
    plt.title("cross validation scores of kernel for SVM(C=1)")
    plt.xlabel("kernel")
    plt.ylabel("accuracy score")
    # plt.xscale("log")
    plt.legend()
    

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
        setje = combine_data_and_labels(features_data, labels)
        if index==0:
            full = setje
        else:
            full = full + setje

    #randomize order
    # random.shuffle(full)

    #flatten data for ML
    data, labels = zip(*full)
    print(len(data), data[0].shape)
    data = np.array(data)#.reshape(200, data[0].shape[0]*data[0].shape[1])
    print(type(data), data.shape)

    #PCA
    pca = PCA(n_components=40)
    pca.fit(data.T)
    for i in range(len(pca.components_)):
        print(sum(pca.explained_variance_ratio_[:i]))
    print(f"exp_variance_ratio: {pca.explained_variance_ratio_}")
    data = pca.components_[:, 10] 
    print(data.shape)
    #train test split
    X_train, X_test, Y_train, Y_test = Models.train_val_split(data, labels, 42, 0.3)
    #train val split
    # X_train, X_val, Y_train, Y_val = Models.train_val_split(X_train, Y_train, 0.3)

    #ML
    model = Models()
    gridsearch, acc = model.KFOLD_CV(X_train, Y_train, X_test, Y_test)
    for i in range(len(gridsearch)):
        best_model = gridsearch[i].best_estimator_
        Y_predict = best_model.predict(X_test)
        tn, fp, fn, tp = confusion_matrix(Y_test, Y_predict).ravel()
        TPR = tn/(tn+fp)
        FAR = fp/(fp+tn)
        acc = (tp+tn)/(tp+tn+fp+fn)
        print(f"For algorithm {gridsearch[i].best_estimator_}: TPR = {TPR}, FAR = {FAR}, acc = {acc}.\n")
    cf_matrix1 = confusion(gridsearch)
    plot_confusion(cf_matrix1, gridsearch)
    # print(isinstance(gridsearch[2].cv_results_['param_C'][1], float))
    # plt.plot(gridsearch[2].cv_results_['param_C'])
    # plt.show()
    # plt.plot(gridsearch[2].cv_results_['mean_test_score'])
    # plt.show()
    

    # plt.show()
        # tn, fp, fn, tp = confusion_matrix(Y_test, Y_predict).ravel()
        # print(((tn+tp)/(fp+fn+tp+tn))*100)
    # print(gridsearch[3].cv_results_["split4_test_score"])

     
        