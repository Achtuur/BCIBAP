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

if __name__ == '__main__':
    # To recreate this plot, the notch filter in the preprocess pipeline needs to be changed to 60 Hz
    
    data_path = Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_stage1_take1.npy')
    data = np.load(data_path)[3250:4500]
    # fig, axs, plt = DataPlot.eeg_channels_plot(data)
    # fig.text(0.04, 0.5, 'Amplitude [uV]', va='center', rotation='vertical')
    # fig.text(0.5, 0.04, 'Sample [n]', ha='center')
    # handles, labels = axs[0].get_legend_handles_labels()
    # fig.legend(handles, labels, loc='upper right') 
    # plt.show(block=True)
    y = np.abs(rfft(data[:,0]))[1:]
    f = rfftfreq(1250,1/250)[1:]
    plt.plot(f,y, linewidth=0.5, label="FFT of EEG signal")
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude [uV]')
    plt.legend()
    plt.show(block=True)