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
from PreprocessingPipeline import PreprocessingPipeline

if __name__ == '__main__':
    # To recreate this plot, the notch filter in the preprocess pipeline needs to be changed to 60 Hz
    data_path = Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/sample/artifacts.npy')
    data = np.load(data_path)[1950:2950]
    data = PreprocessingPipeline(data).start()#[110:450,:]
    
    # Before
    # Time series
    # plt = DataPlot.eeg_channels_plot(data[:,2])
    # plt.axvline(x=110, linestyle='--', color='red', label="Portion containing EMG artifact")
    # plt.axvline(x=450, linestyle='--', color='red')
    # axs[1].axvline(x=480, linestyle='--', color='orange')
    # axs[1].axvline(x=880, linestyle='--', color='orange')
    # axs[2].axvline(x=110, linestyle='--', color='orange')
    # axs[2].axvline(x=450, linestyle='--', color='orange')
    # axs[3].axvline(x=480, linestyle='--', color='orange')
    # axs[3].axvline(x=880, linestyle='--', color='orange')

    # fig.text(0.04, 0.5, 'Amplitude [uV]', va='center', rotation='vertical')
    # fig.text(0.5, 0.04, 'Sample [n]', ha='center')

    # handles, labels = axs[0].get_legend_handles_labels()
    # fig.legend(handles, labels, loc='upper right') 
    # plt.xlabel("Sample [n]")
    # plt.ylabel("Amplitude [μV]")
    # plt.legend()
    # plt.show(block=True)
    # # # Frequency
    # y_fft_1 = np.abs(rfft(data[110:451,2]))
    # f1 = rfftfreq(341, 1/250)

    # # After
    # # Time series
    artifact_split_1 = data[110:451,:]
    # artifact_split_2 =  data[480:881,:] 

    data[110:451,:] = Filter.remove_bad_channels(artifact_split_1)
    # data[480:881,:] = Filter.remove_bad_channels(artifact_split_2)
    plt = DataPlot.eeg_channels_plot(data[:,2])
    plt.axvline(x=110, linestyle='--', linewidth=1, color='red', label="Portion containing EMG artifact")
    plt.axvline(x=450, linestyle='--', linewidth=1,color='red')
    # axs[0].axvline(x=110, linestyle='--', color='orange', label="Portion containing EMG artifact")
    # axs[0].axvline(x=450, linestyle='--', color='orange')
    # axs[1].axvline(x=480, linestyle='--', color='orange')
    # axs[1].axvline(x=880, linestyle='--', color='orange')
    # axs[2].axvline(x=110, linestyle='--', color='orange')
    # axs[2].axvline(x=450, linestyle='--', color='orange')
    # axs[3].axvline(x=480, linestyle='--', color='orange')
    # axs[3].axvline(x=880, linestyle='--', color='orange')
    # fig.text(0.04, 0.5, 'Amplitude [uV]', va='center', rotation='vertical')

    plt.xlabel("Sample [n]")
    plt.ylabel("Amplitude [μV]")
    # plt.legend(loc="upper right")
    plt.show(block=True) 

    # handles, labels = axs[0].get_legend_handles_labels()
    # fig.legend(handles, labels, loc='upper right') 

    # # Frequency
    # data[110:451,2] = Filter.remove_bad_channels(artifact_split_1)[:,2]
    # y_fft_2 = np.abs(rfft(data[110:451,2]))
    
    # plt.plot(f1, y_fft_1, color="orange", linewidth=0.5, label="FFT of interval with artifact")
    # plt.plot(f1, y_fft_2, linewidth=0.5, label="FFT of interval after artifact removal")
    # plt.xlabel('Frequency [Hz]')
    # plt.ylabel('Amplitude [uV]')