import os
import numpy as np
import mne
from mne.datasets import eegbci
from mne.io import concatenate_raws, read_raw_edf
import matplotlib.pyplot as plt
from mne.viz import plot_raw

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis_filt-0-40_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file)
raw.crop(tmax=60)
# raw.plot_psd(fmax=50)
eeg_channel_indices = mne.pick_types(raw.info, meg=False, eeg=True)
eeg_data, times = raw[eeg_channel_indices]
eeg_data_null = eeg_data[0,:]
# times_null = times[0,:]
print(eeg_data_null.shape)
print(times.shape)
plt.plot(times, eeg_data_null.T)
plt.show()
