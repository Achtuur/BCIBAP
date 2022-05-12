from pathlib import Path
import numpy as np
import os
# This is to easily run the script from the command line
# [] = optional
# Usage: python data_to_numpy.py -folder folder_name
import argparse

# Create parser
my_parser = argparse.ArgumentParser(description="Code to convert BCI txt to numpy data")
my_parser.add_argument('-folder',
                        metavar='-folder name',
                        type=str,
                        help='The name of the folder'    
                    )
args = my_parser.parse_args()

folder_name = args.folder 
RECORDINGS_PATH = Path(f'./recorded_data/recordings_txt/{folder_name}')

# Create folder to store .npy files
os.makedirs(Path(f'./recorded_data/recordings_numpy/{folder_name}'))

RECORDING_FOLDERS = list(RECORDINGS_PATH.iterdir())

for recording in RECORDING_FOLDERS:
        # This is weird code to get the value of the generator
        path = list(recording.glob('*.txt'))[0]
        with open(path, 'r') as file:
                np_frame = np.loadtxt(fname=file, skiprows=5, delimiter=', ', usecols=(i for i in range(1,9)))
                save_path = Path(f'./recorded_data/recordings_numpy/{folder_name}/{path.parent.name}.npy')
                np.save(save_path, np_frame)