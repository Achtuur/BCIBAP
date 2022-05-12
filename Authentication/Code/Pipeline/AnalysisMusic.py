from pathlib import Path

# Add components and data to the path, str(Path()) to convert path to a string
import sys
sys.path.append(str(Path('../PipelineComponents/Preprocessing')))
sys.path.append(str(Path('../PipelineComponents/FeatureExtraction')))
sys.path.append(str(Path('../Data/ExperimentResults')))

# Experiments
from ExperimentWrapper import ExperimentWrapper

# Preprocessing
from PreprocessingPipeline import PreprocessingPipeline
from Visualize import DataPlot

# Feature Extraction

if __name__ == '__main__':
    EXPERIMENTS = []

    # Sam
    EXPERIMENT_SAM = ExperimentWrapper("SAM", 
        Path('../Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_calibration.npy')
    )

    EXPERIMENT_SAM = EXPERIMENT_SAM.set_m_data(
        Path('../Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_music.npy')
    )

    EXPERIMENTS.append(EXPERIMENT_SAM)

    # M1
    EXPERIMENT_M1 = ExperimentWrapper("M1",
        Path('../Data/ExperimentResults/recorded_data/recordings_numpy/M1_10_05_2022/OpenBCISession_M1_calibration.npy')
    )

    EXPERIMENT_M1 = EXPERIMENT_M1.set_m_data(
        Path('../Data/ExperimentResults/recorded_data/recordings_numpy/M1_10_05_2022/OpenBCISession_M1_music_2.npy')
    )
    
    EXPERIMENTS.append(EXPERIMENT_M1)

    for experiment in EXPERIMENTS:
        # Hier functie van Joos om automatisch data te croppen
        calibration_data = PreprocessingPipeline(experiment.get_calibration_data()).start()
        # DataPlot.eeg_channels_plot(calibration_data)
        experiment_data = PreprocessingPipeline(experiment.get_m_data(), calibration_data)

        # Do feature Extraction

        # Aggregate result(?)

