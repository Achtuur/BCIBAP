from pathlib import Path
import numpy as np
from datetime import datetime

import os

# Global dictionary constructed from experiment file
RECORDINGS_CROP_DICTIONARY = {
        # M1
        'M1_CALIBRATION' : {
                'path' : Path('./recorded_data/recordings_numpy/M1_10_05_2022/OpenBCISession_M1_calibration.npy'),
                'crop' : (250*15, 250*75)
        },
        'M1_PSEUDO' : {
                'path' : Path('./recorded_data/recordings_numpy/M1_10_05_2022/OpenBCISession_M1_pseudo.npy'),
                'crop' : (1570, 1570+(250*50*5))
        }, 
        # SAM
        'SAM_CALIBRATION' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_calibration.npy'),
                'crop' : (250*62, 250*122)
        },
        'SAM_PSEUDO' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_pseudo.npy'),
                'crop' : (1186, 1186+(250*50*5))
        },
        'SIMON_CALIBRATION' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon_17_05_2022/OpenBCISession_Simon_calibration.npy'),
                'crop' : (250*10, 250*70)
        },
        'SIMON_PSEUDO' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon_17_05_2022/OpenBCISession_Simon_pseudo.npy'),
                'crop' : (5511, 5511+(250*50*5))
        },
        'MIRTHE_CALIBRATION' : {
                'path' : Path('./recorded_data/recordings_numpy/Mirthe_17_05_2022/OpenBCISession_Mirthe_calibration.npy'),
                'crop' : (250*10, 250*70)
        },
        'MAXIM_CALIBRATION' : {
                'path' : Path('./recorded_data/recordings_numpy/M2_17_05_2022/OpenBCISession_M2_calibration.npy'),
                'crop' : (250*10, 250*70)
        },
        'F1_CALIBRATION' : {
                'path' : Path('./recorded_data/recordings_numpy/F1_17_05_2022/OpenBCISession_F1_calibration.npy'),
                'crop' : (250*10, 250*70)
        },
        'F1_PSEUDO' : {
                'path' : Path('./recorded_data/recordings_numpy/F1_17_05_2022/OpenBCISession_F1_pseudo.npy'),
                'crop' : (2570, 2570+(250*5*50))
        },
        'F3_CALIBRATION' : {
                'path' : Path('./recorded_data/recordings_numpy/F3_17_05_2022/OpenBCISession_F3_calibration.npy'),
                'crop' : (250*10, 250*70)
        }
}

def txt_to_numpy(recording_txt_path, filename, subject_name):
        # This is the path to numpy recordings folder
        BASE_PATH = Path('./recorded_data/recordings_numpy')

        # This is the path to the folder that will be created for the different npy files
        subject_dir = BASE_PATH / Path(subject_name)

        # If the folder doesn't exist yet, it is created
        try:
                os.makedirs(subject_dir)
        except FileExistsError:
                pass
        
        # The raw recording folders only have one file, so this gets the txt file 
        raw_txt_file = list(recording_txt_path.iterdir())[0]
        
        # These lines open the txt file, skip the first 5 rows, and save the 1-8 columns as a npy file
        with open(raw_txt_file, 'r') as file:
                np_frame = np.loadtxt(fname=file, skiprows=5, delimiter=', ', usecols=(i for i in range(1,9)))
                save_path = Path(f'{subject_dir}/{filename}.npy')
                np.save(save_path, np_frame)


if __name__ == '__main__':
        # Raw recording path to folder containing subjects
        RAW_RECORDING_PATH = Path('./recorded_data/recordings_txt')

        # Iterate Test Subjects
        SUBJECTS = RAW_RECORDING_PATH.iterdir()
        for subject in SUBJECTS:
                # Name of folder in recordings_txt
                subject_name = subject.stem

                # Path to the upper folder
                base_path = RAW_RECORDING_PATH / Path(subject_name)
                
                # Iterate recording folders in the subject folder
                RECORDINGS = base_path.iterdir()
                for recording in RECORDINGS:
                        # This is the path to the recording txt file
                        recording_path = Path(recording)

                        # This is the name of the folder the npy file will be created in
                        folder_name = recording_path.stem
                        txt_to_numpy(recording_path, folder_name, subject_name)

        # This code iterates the global dictionary and uses it to crop all the recordings which must be cropped
        for recording_to_crop in RECORDINGS_CROP_DICTIONARY.values():
                numpy_data = np.load(recording_to_crop['path'])
                cropped_numpy_data = numpy_data[recording_to_crop['crop'][0]:recording_to_crop['crop'][1]]
                print(f"File: {recording_to_crop['path'].stem}\nOld shape: {numpy_data.shape}\nNew shape: {cropped_numpy_data.shape}")
                np.save(recording_to_crop['path'], cropped_numpy_data)
                
        



