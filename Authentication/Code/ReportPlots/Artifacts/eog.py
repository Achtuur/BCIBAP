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
    # fig, axs = plt.subplots(8,1, figsize=(12,6))
    # for i in range(8):
    #     axs[i].set_ylim([-200,200])
    #     axs[i].plot(data[:,i], linewidth=0.25, label="EEG signal")
    #     ax = axs[i].twinx()
    #     ax.set_ylabel(f'{i + 1}')
    #     ax.set_yticks([])
    
    # axs[0].axvline(x=230, linestyle='--', color='orange', label="Single EOG artifact boundary")
    # axs[0].axvline(x=330, linestyle='--', color='orange')
    # axs[1].axvline(x=230, linestyle='--', color='orange')
    # axs[1].axvline(x=330, linestyle='--', color='orange')

    # axs[0].axvline(x=400, linestyle='--', color='blue', label="Multiple EOG artifact boundary ")
    # axs[0].axvline(x=800, linestyle='--', color='blue')
    # axs[1].axvline(x=400, linestyle='--', color='blue')
    # axs[1].axvline(x=800, linestyle='--', color='blue')
    # fig.text(0.04, 0.5, 'Amplitude [$\mu V$]', va='center', rotation='vertical', fontsize=13)
    # fig.text(0.5, 0.04, 'Sample [n]', ha='center', fontsize=13)
    # handles, labels = axs[0].get_legend_handles_labels()
    # fig.legend(handles, labels, loc='upper right', fontsize=12) 
    # axs[0].title.set_text('EEG signal containing EOG artifacts')
    # # plt.show(block=True)
    # plt.savefig('eog_artifact.png', dpi=400)

    fig, ax = plt.subplots(figsize=(12,6))
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
    ax.plot(f,y0, linewidth=0.5, color="orange", label="FFT of EOG artifact")
    ax.plot(f,y1, linewidth=0.5, color="orange")
    ax.plot(f,y2, linewidth=0.5, color="blue", label="FFT of EEG")
    ax.plot(f,y3, linewidth=0.5, color="blue")
    # plt.plot(f,y4, linewidth=0.5, color="blue")
    # plt.plot(f,y5, linewidth=0.5, color="blue")
    # plt.plot(f,y6, linewidth=0.5, color="blue")
    # plt.plot(f,y7, linewidth=0.5, color="blue")
    plt.xlabel('Frequency [Hz]', fontsize=12)
    plt.ylabel('Amplitude [uV]', fontsize=12)
    plt.title('Frequency spectrum comparison between EEG signal and EOG artifact', fontsize=12)
    plt.legend(fontsize=12)
    # plt.show(block=True)
    plt.savefig('fft_eog.png', dpi=400)
 