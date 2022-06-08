from pathlib import Path
import numpy as np

class ExperimentWrapper():
    def __init__(self, subject: str, experiment_type: str):
        self.subject = subject
        self.experiment_type = experiment_type
        self.experiment_data = None
        self.experiment_description_file = None
        self.experiment_labels = None
        

    def get_subject(self):
        return self.subject

    def set_experiment_data(self, exp_path: Path):
        self.experiment_data = np.load(exp_path)
        return self

    def get_experiment_data(self):
        return self.experiment_data

    def set_experiment_description_file(self, description_path: Path):
        self.experiment_description_file = description_path
        return self

    def get_experiment_description_file(self):
        return self.experiment_description_file    
        
    def set_experiment_labels(self, labels: list):
        self.experiment_labels = labels
        return self

    def get_experiment_labels(self):
        return self.experiment_labels