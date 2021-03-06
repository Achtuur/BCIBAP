import numpy as np
from math import ceil

def crop(data: np.ndarray, t_window: int, f_sampling: int, mask: tuple = False):
    array_length = data.shape[0]
    n_sub_samples = ceil(t_window * f_sampling)
    groups = array_length // n_sub_samples

    cropped_data = np.array_split(data, groups)

    if mask:
        cropped_data = list(map(lambda x: x[mask[0]:mask[1]], cropped_data))

    return cropped_data

if __name__ == '__main__':
    data = np.arange(0,2000)
    # cropped_data = crop(data, 2, 250)
    cropped_data = crop(data, 2, 250, (50,400))

    print(f'Length data: {len(data)}\nIntervals: {len(cropped_data)}\nPoints in interval: {len(cropped_data[0])}\nData: {cropped_data[0]}')