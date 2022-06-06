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

if __name__ == "__main__":

    EXPERIMENTS = []

    # EXPERIMENT_SIMON_6HZ = ExperimentWrapper("Simon", "ft")
    # EXPERIMENT_SIMON_6HZ.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Simon\OpenBCISession_Simon_stage1_6hz.npy"))
    # EXPERIMENT_SIMON_6HZ.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/simon_23-05-2022_ft1_take2.csv"))
    # EXPERIMENTS.append(EXPERIMENT_SIMON_6HZ)

    EXPERIMENT_SIMON_TAKE_1 = ExperimentWrapper("Simon", "ft")
    EXPERIMENT_SIMON_TAKE_1.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Simon\OpenBCISession_Simon_stage1_take1.npy"))
    EXPERIMENT_SIMON_TAKE_1.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/simon_23-05-2022_ft1_take1.csv"))
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_1)

    EXPERIMENT_SIMON_TAKE_2 = ExperimentWrapper("Simon", "ft")
    EXPERIMENT_SIMON_TAKE_2.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Simon\OpenBCISession_Simon_stage1_take2.npy"))
    EXPERIMENT_SIMON_TAKE_2.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/simon_23-05-2022_ft1_take2.csv"))
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_2)

    EXPERIMENT_SAM_TAKE_1 = ExperimentWrapper("Sam", "ft")
    EXPERIMENT_SAM_TAKE_1.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Sam\OpenBCISession_Sam_stage1_take1.npy"))
    EXPERIMENT_SAM_TAKE_1.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Sam_23-05-2022_ft1_take1.csv"))
    EXPERIMENTS.append(EXPERIMENT_SAM_TAKE_1)

    EXPERIMENT_SAM_TAKE_2 = ExperimentWrapper("Sam", "ft")
    EXPERIMENT_SAM_TAKE_2.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Sam\OpenBCISession_Sam_stage1_take2.npy"))
    EXPERIMENT_SAM_TAKE_2.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Sam_23-05-2022_ft1_take2.csv"))
    EXPERIMENTS.append(EXPERIMENT_SAM_TAKE_2)

    EXPERIMENT_JOOS_TAKE_1 = ExperimentWrapper("Joos", "ft")
    EXPERIMENT_JOOS_TAKE_1.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Joos\OpenBCISession_Joos_stage1_take1.npy"))
    EXPERIMENT_JOOS_TAKE_1.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Sam_23-05-2022_ft1_take1.csv"))
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_1)

    EXPERIMENT_JOOS_TAKE_2 = ExperimentWrapper("Joos", "ft")
    EXPERIMENT_JOOS_TAKE_2.set_experiment_data(Path(".\Data\ExperimentResults\\recorded_data\\recordings_numpy\\Joos\OpenBCISession_Joos_stage1_take2.npy"))
    EXPERIMENT_JOOS_TAKE_2.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/Step1/Sam_23-05-2022_ft1_take2.csv"))
    EXPERIMENTS.append(EXPERIMENT_JOOS_TAKE_2)