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

from PreprocessingPipeline import PreprocessingPipeline
from Visualize import DataPlot
from Filters import Filter

if __name__ == '__main__':
    data_path = Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_stage1_take1.npy')
    data = np.load(data_path)[3250:4500]
    data_powerline = Filter.band_pass_filter(data[:,0], 4, (48,52), 250)
    data = PreprocessingPipeline(data[:, 0]).start(v=True)
    fig, axs = plt.subplots(2,1, figsize=(11,6))
    axs[0].title.set_text('Powerline noise compared to EEG signal')
    axs[0].plot(data_powerline, linewidth=0.25, label="Powerline noise")
    axs[0].plot(data, linewidth=0.5, color="orange", label="Filtered data")
    axs[0].set_xlim([100,1100])
    axs[0].set_ylim([-200, 200])
    axs[0].legend(loc='upper right', fontsize=13)
    axs[0].set_ylabel('Amplitude [$\mu V$]', fontsize=14)
    # axs[0].set_xlabel('Sample [n]')
    # axs[0].set_ylabel('Amplitude [uV]')

    y1 = np.abs(rfft(data_powerline))
    y2 = np.abs(rfft(data))
    f = rfftfreq(1250,1/250)
    axs[1].plot(f,y1,linewidth=0.5, label="Fourier transform of Powerline noise")
    axs[1].plot(f,y2,linewidth=0.5, color="orange", label="Fourier transform of EEG signal")
    axs[1].legend(loc="upper right", fontsize=13)
    axs[1].set_ylabel('Amplitude [$\mu V$]', fontsize=14)
    axs[1].set_xlabel('Frequency [Hz]', fontsize=14)
    # plt.title('Comparison EEG signal to Powerline noise')
    plt.savefig('comparison_powerline_eeg.png', dpi=400)
    # plt.show(block=True)
    # axs[1].set_xlabel('Frequency [Hz]')
    # axs[1].set_ylabel('Amplitude [uV]')
    # plt.show(block=True)
    # plt = DataPlot.eeg_channels_plot(data)
    # plt.xlim(0, 1200)
    # plt.xlabel('Sample [n]')
    # plt.ylabel('Amplitude [uV]')
    # plt.legend()
    # plt.show(block=True)