from pathlib import Path
import numpy as np

RECORDINGS_PATH = Path('./recorded_data/recordings_txt')

RECORDING_FOLDERS = list(RECORDINGS_PATH.iterdir())

for recording in RECORDING_FOLDERS:
        path = list(recording.glob('*.txt'))[0]
        with open(path, 'r') as file:
                np_frame = np.loadtxt(fname=file, skiprows=5, delimiter=', ', usecols=(i for i in range(1,9)))
                save_path = Path(f'./recorded_data/recordings_numpy/{path.stem}.npy')
                np.save(save_path, np_frame)