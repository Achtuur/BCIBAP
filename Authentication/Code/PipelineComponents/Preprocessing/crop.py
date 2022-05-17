import numpy as np
from math import ceil

def crop(data: np.ndarray, t_window: int, f_sampling: int):
    array_length = data.shape[0]
    n_sub_samples = ceil(t_window * f_sampling)
    groups = array_length // n_sub_samples

    cropped_data = np.array_split(data, groups)
    return cropped_data