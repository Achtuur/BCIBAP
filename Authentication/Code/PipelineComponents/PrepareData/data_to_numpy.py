from pathlib import Path
import numpy as np
import os
# This is to easily run the script from the command line
# [] = optional
# Usage: python data_to_numpy.py -folder folder_name
import argparse


RECORDINGS_PATH = Path(f'../../Data/ExperimentResults/recorded_data/recordings_txt')

for subdirs, dirs, files in os.walk(RECORDINGS_PATH):
        for file in files:
                newsubdir = os.path.basename(os.path.normpath(subdirs))
                oldpath = Path(f'{subdirs}/{file}')
                print(oldpath)
                if not os.path.exists(Path(f'./recorded_data/recordings_numpy/{newsubdir}/{file}')):
                        os.makedirs(Path(f'./recorded_data/recordings_numpy/{newsubdir}/{file}'))
                with open(oldpath, 'r') as f:
                        np_frame = np.loadtxt(fname=f, skiprows=5, delimiter=', ', usecols=(i for i in range(1,9)))
                        print(np_frame)
                        save_path = Path(f'./recorded_data/recordings_numpy/{newsubdir}/{file}.npy')
                        np.save(save_path, np_frame)


# RECORDING_FOLDERS = list(RECORDINGS_PATH.iterdir())

# for recording in RECORDING_FOLDERS:
#         # This is weird code to get the value of the generator
#         path = list(recording.glob('*.txt'))[0]
#         with open(path, 'r') as file:
#                 np_frame = np.loadtxt(fname=file, skiprows=5, delimiter=', ', usecols=(i for i in range(1,9)))
#                 save_path = Path(f'./recorded_data/recordings_numpy/{newname}/{file}.npy')
#                 np.save(save_path, np_frame)