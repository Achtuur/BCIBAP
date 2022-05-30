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
from PreprocessingPipeline import PreprocessingPipeline

if __name__ == '__main__':
    # To recreate this plot, the notch filter in the preprocess pipeline needs to be changed to 60 Hz

    data_path = Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/sample/artifacts.npy')
    data = np.load(data_path)[1950:2950]
    data = PreprocessingPipeline(data).start()
    # fig, axs, plt = DataPlot.eeg_channels_plot(data)
    # axs[2].axvline(x=110, linestyle='--', color='orange', label="Portion containing EMG artifact")
    # axs[2].axvline(x=450, linestyle='--', color='orange')
    # axs[3].axvline(x=480, linestyle='--', color='orange')
    # axs[3].axvline(x=880, linestyle='--', color='orange')
    # axs[4].axvline(x=110, linestyle='--', color='orange')
    # axs[4].axvline(x=450, linestyle='--', color='orange')
    # axs[5].axvline(x=480, linestyle='--', color='orange')
    # axs[5].axvline(x=880, linestyle='--', color='orange')
    # handles, labels = axs[2].get_legend_handles_labels()
    # fig.legend(handles, labels, loc='upper right') 
    # fig.text(0.04, 0.5, 'Amplitude [uV]', va='center', rotation='vertical')
    # fig.text(0.5, 0.04, 'Sample [n]', ha='center')
    y0 = np.abs(rfft(data[110:451,0]))
    y1 = np.abs(rfft(data[110:451,1]))
    y2 = np.abs(rfft(data[110:451,2]))
    y3 = np.abs(rfft(data[480:821,3]))
    y4 = np.abs(rfft(data[110:451,4]))
    y5 = np.abs(rfft(data[480:821,5]))
    y6 = np.abs(rfft(data[110:451,6]))
    y7 = np.abs(rfft(data[110:451,7]))
    f = rfftfreq(340,1/250)
    
    plt.plot(f,y2, linewidth=0.5, color="orange", label="FFT of EMG artifact")
    # plt.plot(f,y3, linewidth=0.5, color="orange")
    # plt.plot(f,y4, linewidth=0.5, color="orange")
    # plt.plot(f,y5, linewidth=0.5, color="orange")
    plt.plot(f,y0, linewidth=0.5, color="blue", label="FFT of EEG")
    # plt.plot(f,y1, linewidth=0.5, color="blue")
    # plt.plot(f,y6, linewidth=0.5, color="blue")
    # plt.plot(f,y7, linewidth=0.5, color="blue")
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude [uV]')
    plt.legend()
    plt.show(block=True)

