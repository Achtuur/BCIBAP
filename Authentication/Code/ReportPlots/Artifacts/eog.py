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
    data = np.load(data_path)[800:2000]
    data = PreprocessingPipeline(data).start()

    # # Artifacts
    # fig, axs, plt = DataPlot.eeg_channels_plot(data)
    
    # axs[0].axvline(x=230, linestyle='--', color='orange')
    # axs[0].axvline(x=330, linestyle='--', color='orange')
    # axs[1].axvline(x=230, linestyle='--', color='orange')
    # axs[1].axvline(x=330, linestyle='--', color='orange')

    # axs[0].axvline(x=400, linestyle='--', color='blue')
    # axs[0].axvline(x=800, linestyle='--', color='blue')
    # axs[1].axvline(x=400, linestyle='--', color='blue')
    # axs[1].axvline(x=800, linestyle='--', color='blue')
    # fig.text(0.04, 0.5, 'Amplitude [uV]', va='center', rotation='vertical')
    # fig.text(0.5, 0.04, 'Sample [n]', ha='center')
    # handles, labels = axs[0].get_legend_handles_labels()
    # fig.legend(handles, labels, loc='upper right') 
    # plt.show(block=True)

    data_eog = data[400:800]
    y0 = np.abs(rfft(data_eog[:,0]))
    y1 = np.abs(rfft(data_eog[:,1]))
    y2 = np.abs(rfft(data_eog[:,2]))
    y3 = np.abs(rfft(data_eog[:,3]))
    y4 = np.abs(rfft(data_eog[:,4]))
    y5 = np.abs(rfft(data_eog[:,5]))
    y6 = np.abs(rfft(data_eog[:,6]))
    y7 = np.abs(rfft(data_eog[:,7]))
    f = rfftfreq(400,1/250)
    plt.plot(f,y0, linewidth=0.5, color="orange", label="FFT of EOG artifact")
    plt.plot(f,y1, linewidth=0.5, color="orange")
    plt.plot(f,y2, linewidth=0.5, color="blue", label="FFT of EEG")
    plt.plot(f,y3, linewidth=0.5, color="blue")
    plt.plot(f,y4, linewidth=0.5, color="blue")
    plt.plot(f,y5, linewidth=0.5, color="blue")
    plt.plot(f,y6, linewidth=0.5, color="blue")
    plt.plot(f,y7, linewidth=0.5, color="blue")
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude [uV]')
    plt.legend()
    plt.show(block=True)
 