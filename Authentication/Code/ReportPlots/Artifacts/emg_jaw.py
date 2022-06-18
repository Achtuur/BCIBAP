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

    # # fig, axs, plt = DataPlot.eeg_channels_plot(data)
    # fig, axs = plt.subplots(8,1, figsize=(12,6))

    # # EEG
    # for i in range(8):
    #     if i == 0:
    #         label1, = axs[i].plot(data[:,i], linewidth=0.25, label="EEG signal")
    #         axs[i].set_ylim([-400, 400])
    #     else:
    #         axs[i].plot(data[:,i], linewidth=0.25)
    #         axs[i].set_ylim([-400, 400])

    #     # Channel label
    #     ax = axs[i].twinx()
    #     ax.set_ylabel(f'{i+1}')
    #     ax.set_yticks([])

    # # Lines
    # label2 = axs[2].axvline(x=110, linestyle='--', color='orange', label="Portion containing EMG artifact")
    # axs[2].axvline(x=450, linestyle='--', color='orange')
    # axs[3].axvline(x=480, linestyle='--', color='orange')
    # axs[3].axvline(x=880, linestyle='--', color='orange')
    # axs[4].axvline(x=110, linestyle='--', color='orange')
    # axs[4].axvline(x=450, linestyle='--', color='orange')
    # axs[5].axvline(x=480, linestyle='--', color='orange')
    # axs[5].axvline(x=880, linestyle='--', color='orange')
    # # handles, labels = axs[2].get_legend_handles_labels()
    # # fig.legend(handles, labels, loc='upper right') 
    # fig.legend([label1, label2], ['EEG signal', 'Portion containing EMG artifact'], fontsize=12)
    # fig.text(0.04, 0.5, 'Amplitude [$\mu V$]', va='center', rotation='vertical', fontsize=13)
    # fig.text(0.5, 0.04, 'Sample [n]', ha='center', fontsize=13)

    # plt.show(block=True)
    # plt.savefig('eeg_with_emg.png', dpi=400)

    y0 = np.abs(rfft(data[110:451,0]))
    y1 = np.abs(rfft(data[110:451,1]))
    y2 = np.abs(rfft(data[110:451,2]))
    y3 = np.abs(rfft(data[480:821,3]))
    y4 = np.abs(rfft(data[110:451,4]))
    y5 = np.abs(rfft(data[480:821,5]))
    y6 = np.abs(rfft(data[110:451,6]))
    y7 = np.abs(rfft(data[110:451,7]))
    f = rfftfreq(340,1/250)
    
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(f,y2, linewidth=0.5, color="orange", label="FFT of EMG artifact")
    # plt.plot(f,y3, linewidth=0.5, color="orange")
    # plt.plot(f,y4, linewidth=0.5, color="orange")
    # plt.plot(f,y5, linewidth=0.5, color="orange")
    ax.plot(f,y0, linewidth=0.5, color="blue", label="FFT of EEG")
    # plt.plot(f,y1, linewidth=0.5, color="blue")
    # plt.plot(f,y6, linewidth=0.5, color="blue")
    # plt.plot(f,y7, linewidth=0.5, color="blue")
    
    plt.xlabel('Frequency [Hz]', fontsize=13)
    plt.ylabel('Amplitude [$\mu V$]', fontsize=13)
    plt.legend(fontsize=12)
    plt.title('Comparison EEG signal with EMG artifact', fontsize=12)
    # plt.show(block=True)
    plt.savefig('fft_eeg_emg.png', dpi=400)

