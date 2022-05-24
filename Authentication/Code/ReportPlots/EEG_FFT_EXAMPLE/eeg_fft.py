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
    plt.plot(f,y, linewidth=0.25, label="FFT of EEG signal")
    plt.xlim(left=0, right=100)
    plt.axvline(x=1, linestyle='--', color='orange')
    plt.axvline(x=4, linestyle='--', color='orange')
    plt.axvline(x=8, linestyle='--', color='orange')
    plt.axvline(x=14, linestyle='--', color='orange')
    plt.axvline(x=30, linestyle='--', color='orange')
    plt.axvline(x=100, linestyle='--', color='orange')
    # This is to create extra ticks of vertical line
    plt.xticks(list(plt.xticks()[0]) + [4,8,14,30])
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude [uV]')
    plt.legend()
    plt.show(block=True)
