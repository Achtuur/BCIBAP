from pathlib import Path
import numpy as np

class ExperimentWrapper():
    def __init__(self, subject: str, experiment_type: str, calibration_path, cal_bounds: tuple):
        self.subject = subject
        self.cal_bounds = cal_bounds
        self.calibration_data = np.load(calibration_path)[cal_bounds[0]:cal_bounds[1]]
        self.experiment_type = experiment_type
        self.experiment_data_path = None
        self.experiment_description_file = None
        

    def get_subject(self):
        return self.subject

    def get_calibration_data(self):
        return self.calibration_data

    def set_experiment_data_path(self, exp_path: Path):
        self.experiment_data = exp_path
        return self

    def get_experiment_data_path(self):
        return self.experiment_data

    def set_experiment_description_file(self, description_path: Path):
        self.experiment_description_file = description_path
        return self

    def get_experiment_description_file(self):
        return self.experiment_description_file