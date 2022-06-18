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
    # fig, axs = plt.subplots(8,1, figsize=(11,6))
    # axs[0].plot(data[:,0], linewidth=0.25, label="EEG signal")
    # for i in range(1,8):
    #     axs[i].plot(data[:,i], linewidth=0.25)
    # fig.text(0.04, 0.5, 'Amplitude [$\mu V$]', va='center', rotation='vertical', fontsize=14)
    # fig.text(0.5, 0.04, 'Sample [n]', ha='center', fontsize=14)
    # handles, labels = axs[0].get_legend_handles_labels()
    # fig.legend(handles, labels, loc='upper right', fontsize=13)
    # for i in range(8):
    #     ax = axs[i].twinx()
    #     ax.set_yticks([])
    #     ax.set_ylabel(f'{i+1}')
    # # ax2 = axs[0].twinx()
    # # ax2.set_yticks([])
    # # ax2.set_ylabel('test')
    # axs[0].title.set_text('Unfiltered EEG signal')
    # plt.savefig('unfiltered_eeg.png', dpi=400)
    # plt.show(block=True)
    fig, axs = plt.subplots(figsize=(10,5))
    y = np.abs(rfft(data[:,0]))[1:]
    f = rfftfreq(1250,1/250)[1:]
    axs.plot(f,y, linewidth=0.5, label="Fourier transform")
    plt.title('Fourier Transform of unfiltered EEG signal channel 1')
    plt.xlabel('Frequency [Hz]', fontsize=14)
    plt.ylabel('Amplitude [$\mu V$]', fontsize=14)
    plt.legend(fontsize=13)
    # plt.show(block=True)
    plt.savefig('fft_raw_eeg.png', dpi=400)