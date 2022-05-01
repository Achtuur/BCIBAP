import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import mne
from mne.preprocessing import (ICA, create_eog_epochs, create_ecg_epochs,
                               corrmap)

def is_ecg(independent_component: list):
    # 1. Emphasize spikes
    # Calculate energy according to Teager-Kaiser
    energy: list = []
    for i in range(1, len(independent_component) - 1):
        E = independent_component[i]**2 - independent_component[i+1]*independent_component[i-1]
        energy.append(E)
    
    # Add 0 at beginning and end so size is equal
    energy.insert(0, 0)
    energy.append(0)

    # Determine Threshold
    q3, q1 = np.percentile(independent_component, [75, 25])
    iqr = q3 - q1
    threshold = 5.8*iqr + q3

    # Determine peaks
    peaks, _ = find_peaks(energy, height=threshold, distance=100)
  
    # Plot
    fig = plt.figure()
    plt.plot(independent_component)
    plt.axhline(y=threshold)
    for peak in peaks:
        plt.plot(peak, independent_component[peak], marker="o", markeredgecolor="red")
    fig.savefig('test.png')


sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file).pick_types(meg=False, eeg=True, eog=False).crop(tmax=10)

filt_raw = raw.load_data().copy().filter(l_freq=1, h_freq=None)

ica = ICA(n_components=15, max_iter='auto', random_state=97)
ica.fit(filt_raw)

ica_components = ica._transform(filt_raw.get_data())
is_ecg(ica_components[0,:])

