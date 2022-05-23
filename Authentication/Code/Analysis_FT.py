import sys
import platform
from pathlib import Path 
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
from crop import crop
if __name__ == "__main__":

    EXPERIMENTS = []

    EXPERIMENT_SIMON_TAKE_1 = ExperimentWrapper("Simon", "ft", Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Simon_17_05_2022/OpenBCISession_Simon_Calibration.npy"))
    EXPERIMENT_SIMON_TAKE_1.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Simon_17_05_2022/OpenBCISession_Simon_ft_recognition.npy"))
    EXPERIMENT_SIMON_TAKE_1.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/simon_17-05-2022_ft_take1.csv"))
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_1)

    EXPERIMENT_SIMON_TAKE_2 = ExperimentWrapper("Simon", "ft", Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Simon_17_05_2022/OpenBCISession_Simon_Calibration.npy"))
    EXPERIMENT_SIMON_TAKE_2.set_experiment_data(Path("./Data/ExperimentResults/recorded_data/recordings_numpy/Simon_17_05_2022/OpenBCISession_Simon_ft_recognition_2.npy"))
    EXPERIMENT_SIMON_TAKE_2.set_experiment_description_file(Path("./Data/Experiments/Frequency_tagging/results/simon_17-05-2022_ft_take2.csv"))
    EXPERIMENTS.append(EXPERIMENT_SIMON_TAKE_2)

    for experiment in EXPERIMENTS:
        # print(experiment)
        # print(experiment.get_subject())
        # print(experiment.get_experiment_description_file())
        data = PreprocessingPipeline(experiment.get_experiment_data(), experiment.get_calibration_data()).start()
        