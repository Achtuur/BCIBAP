from pathlib import Path
import numpy as np

class ExperimentWrapper():
    def __init__(self, subject, calibration_path):
        self.subject = subject
        self.calibration_data = np.load(calibration_path)
        self.frequency_tagging_data = None
        self.pseudo_words_data = None
        self.music_data = None

    def get_subject(self):
        return self.subject

    def get_calibration_data(self):
        return self.calibration_data

    def set_ft_data(self, ft_path: Path):
        self.frequency_tagging_data = np.load(ft_path)
        return self

    def get_ft_data(self):
        return self.frequency_tagging_data

    def set_pw_data(self, pw_path: Path):
        self.pseudo_words_data = np.load(pw_path)
        return self

    def get_pw_data(self):
        return self.pseudo_words_data

    def set_m_data(self, m_path: Path):
        self.music_data = np.load(m_path)
        return self 

    def get_m_data(self):
        return self.music_data