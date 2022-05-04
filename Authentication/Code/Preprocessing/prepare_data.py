from math import ceil
from pathlib import Path
import numpy as np

<<<<<<< HEAD
def crop(data: np.ndarray, t_window: int, f_sampling: float) -> list:
    array_length = data.shape[0]
=======
def crop(data: np.ndarray, t_window: int, f_sampling: float, skip: float = None) -> list:
    if skip is not None:
        data = data[ceil(skip * f_sampling):]
    
    array_length = data.shape[0]

>>>>>>> Authentication_Branch
    n_sub_samples = ceil(t_window * f_sampling)
    groups = array_length // n_sub_samples

    cropped_data = np.array_split(data, groups)
    return cropped_data

if __name__ == '__main__':
    data_path = Path('../Data/recorded_data/recordings_numpy/OpenBCI-RAW-2022-05-02_15-07-38.npy')
    f_sampling = 250
    t_window = 5

    data = np.load(data_path)
<<<<<<< HEAD
    cropped_data = crop(data, t_window, f_sampling)
=======
    cropped_data = crop(data, t_window, f_sampling, skip=5)
>>>>>>> Authentication_Branch
    print(cropped_data[0].shape)