import numpy as np
from numpy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
# This is an ugly hack to make imports work
from pathlib import Path
import sys
import platform
if platform.system() == "Windows":
    sys.path.append(str(Path('PipelineComponents/Preprocessing').resolve()))
    sys.path.append(str(Path('PipelineComponents/FeatureExtraction').resolve()))
    sys.path.append(str(Path('Data/ExperimentResults').resolve()))
else:
    sys.path.append(str(Path('../../PipelineComponents/Preprocessing').resolve()))
    sys.path.append(str(Path('../../PipelineComponents/FeatureExtraction').resolve()))

from Visualize import DataPlot
from Filters import Filter

if __name__ == '__main__':
    data_path = Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_stage1_take1.npy')
    data = np.load(data_path)[3250:4500]
    data = Filter.band_pass_filter(data[:,0], 4, (49,51), 250)
    fig, axs = plt.subplots(1,2)
    axs[0].plot(data, linewidth=0.25, label="EEG signal")
    axs[0].set_xlabel('Sample [n]')
    axs[0].set_ylabel('Amplitude [uV]')

    y = np.abs(rfft(data))
    f = rfftfreq(1250,1/250)
    axs[1].plot(f,y,linewidth=0.5, label="Fourier Transform of EEG signal")
    axs[1].set_xlabel('Frequency [Hz]')
    axs[1].set_ylabel('Amplitude [uV]')
    plt.show(block=True)
    # plt = DataPlot.eeg_channels_plot(data)
    # plt.xlim(0, 1200)
    # plt.xlabel('Sample [n]')
    # plt.ylabel('Amplitude [uV]')
    # plt.legend()
    # plt.show(block=True)