import os
import numpy as np
import matplotlib.pyplot as plt
import mne
from mne.preprocessing import (ICA, create_eog_epochs, create_ecg_epochs,
                               corrmap)

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file).pick_types(meg=False, eeg=True, eog=False).crop(tmax=10)

filt_raw = raw.load_data().copy().filter(l_freq=1, h_freq=None)

ica = ICA(n_components=15, max_iter='auto', random_state=97)
ica.fit(filt_raw)

raw.load_data()
ica.plot_sources(raw, show_scrollbars=False)
input()

# test = ica._transform(filt_raw.get_data())
# plt.plot(test[1,:])
# plt.show()
# input()