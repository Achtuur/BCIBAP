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

if __name__ == '__main__':
    data_path = Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/sample/meditation.npy')
    data = np.load(data_path)[10000:50000,4]
    data = PreprocessingPipeline(data).start(v=True)
    y = np.abs(rfft(data))[:17000]
    f = rfftfreq(40000,1/250)[:17000]
    fig, axs = plt.subplots(figsize=(10,6))
    axs.plot(f,y, linewidth=0.2, label="FFT of EEG signal")
    # axs.xlim(left=0, right=100)
    axs.axvline(x=1, linestyle='--', color='orange')
    axs.axvline(x=4, linestyle='--', color='orange')
    axs.axvline(x=8, linestyle='--', color='orange')
    axs.axvline(x=14, linestyle='--', color='orange')
    axs.axvline(x=30, linestyle='--', color='orange')
    axs.axvline(x=100, linestyle='--', color='orange')
    # This is to create extra ticks of vertical line
    plt.xticks(list(plt.xticks()[0]) + [4,8,14,30])
    # plt.xticks([3, 6, 11, 22, 50], ['a', 'b', 'c', 'd', 'g'])
    
    plt.xlabel('Frequency [Hz]', fontsize=14)
    plt.ylabel('Amplitude [$\mu V$]', fontsize=14)
    plt.title("Frequency spectrum of EEG signal", fontsize=13)
    plt.xlim([0,80])
    
    plt.legend(fontsize=13)
    # plt.show(block=True)
    plt.savefig('eeg_spectrum_plot.png', dpi=400)
