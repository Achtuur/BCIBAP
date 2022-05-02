from pathlib import Path
import csv
import numpy as np

TXT_PATH = ".\\recorded_data\\recordings_txt\OpenBCISession_Sam_take_2\OpenBCI-RAW-2022-05-02_15-07-38.txt"
test = np.array([])
with open(TXT_PATH, 'r') as f:
        np_frame = np.loadtxt(fname=f, skiprows=5, delimiter=', ', usecols=(i for i in range(1,9)))
        np.save('.\\recorded_data\\recordings_numpy\\test.npy', np_frame)