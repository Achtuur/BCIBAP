import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from sklearn.decomposition import FastICA
from pathlib import Path

from prepare_data import crop

class ICA():
    @staticmethod
    def construct_ic_sources(data: np.ndarray, n_components: int):
        ica = FastICA(n_components=n_components, max_iter=300, random_state=148)
        sources = ica.fit_transform(data)
        mixing_matrix = ica.mixing_
        ica_mean = ica.mean_
        return ica_mean, mixing_matrix, sources

    @staticmethod
    def plot_ica_sources(sources: np.ndarray):
        fig, axs = plt.subplots(sources.shape[1])
        axs[0].set_title(f"{sources.shape[1]} ICA components")
        for col in range(sources.shape[1]):
            axs[col].plot(sources[:, col])
        plt.show(block=True)

if __name__ == '__main__':
    # Initialise data
    data_path = Path('../Data/recorded_data/recordings_numpy/OpenBCI-RAW-2022-05-02_15-07-38.npy')
    f_sampling = 250
    t_window = 5
    data = np.load(data_path)
    cropped_data = crop(data, t_window, f_sampling)

    sources = ICA.construct_ic_sources(cropped_data[5], 7)
