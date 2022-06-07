from pathlib import Path
import numpy as np
from datetime import datetime

import os

# Global dictionary constructed from experiment file
RECORDINGS_CROP_DICTIONARY = {
        # Old
        # M1
        'Joos_ft1_take1' : {
                'path' : Path('./recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_stage1_take1.npy'),
                'crop' : (538, 538 + 20000)
        },
        'Joos_ft1_take2' : {
                'path' : Path('./recorded_data/recordings_numpy/Joos/OpenBCISession_Joos_stage1_take2.npy'),
                'crop' : (678, 678 + 20000)
        },
        'Sam_ft1_take1' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_stage1_take1.npy'),
                'crop' : (4984, 4984 + 20000)
        },
        'Sam_ft1_take2' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_stage1_take2.npy'),
                'crop' : (1393, 1393 + 20000)
        },
        'Simon_ft1_take1' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_Simon_stage1_take1.npy'),
                'crop' : (809, 809 + 20000)
        },
        'Simon_ft1_take2' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_Simon_stage1_take2.npy'),
                'crop' : (1168, 1168 + 20000)
        },
        'Simon_ft1_6hz' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_Simon_stage1_6hz.npy'),
                'crop' : (1828, 1828 + 20000)
        },
        # New
        'Sam_exp_cyril_10hz_60' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_cyril_10hz_60.npy'),
                'crop' : (7*250, 67*250)
        },
        'Sam_exp_cyril_10hz_50' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_cyril_10hz_50.npy'),
                'crop' : (2*250, 52*250)
        },
        'Sam_exp_cyril_10hz_40' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_cyril_10hz_40.npy'),
                'crop' : (2*250, 42*250)
        },
        'Sam_exp_cyril_10hz_30' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_cyril_10hz_30.npy'),
                'crop' : (3*250, 33*250)
        },
        'Sam_exp_cyril_10hz_20' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_cyril_10hz_20.npy'),
                'crop' : (2*250, 22*250)
        },
        'Sam_exp_cyril_10hz_10' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_cyril_10hz_10.npy'),
                'crop' : (2*250, 12*250)
        },
        'Sam_exp_cyril_10hz_5' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_cyril_10hz_5.npy'),
                'crop' : (2*250, 7*250)
        },
        'Sam_exp_cyril_6hz_60' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_cyril_6hz_60.npy'),
                'crop' : (1*250, 61*250)
        },
        'Sam_exp_cyril_6hz_50' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_cyril_6hz_50.npy'),
                'crop' : (1*250, 51*250)
        },
        'Sam_exp_cyril_6hz_40' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_cyril_6hz_40.npy'),
                'crop' : (1*250, 41*250)
        },
        'Sam_exp_cyril_6hz_30' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_cyril_6hz_30.npy'),
                'crop' : (1*250, 29*250)
        },
        'Sam_exp_cyril_6hz_20' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_cyril_6hz_20.npy'),
                'crop' : (4*250, 24*250)
        },
        'Sam_exp_cyril_6hz_10' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_cyril_6hz_10.npy'),
                'crop' : (2*250, 12*250)
        },
        'Sam_exp_cyril_6hz_5' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_cyril_6hz_5.npy'),
                'crop' : (3*250, 8*250)
        },
        'Simon_exp_cyril_10hz_60' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_10hz_60.npy'),
                'crop' : (3*250, 63*250)
        },
        'Simon_exp_cyril_10hz_50' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_10hz_50.npy'),
                'crop' : (2*250, 52*250)
        },
        'Simon_exp_cyril_10hz_40' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_10hz_40.npy'),
                'crop' : (3*250, 43*250)
        },
        'Simon_exp_cyril_10hz_30' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_10hz_30.npy'),
                'crop' : (3*250, 33*250)
        },
        'Simon_exp_cyril_10hz_20' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_10hz_20.npy'),
                'crop' : (4*250, 24*250)
        },
        'Simon_exp_cyril_10hz_10' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_10hz_10.npy'),
                'crop' : (3*250, 13*250)
        },
        'Simon_exp_cyril_10hz_5' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_10hz_5.npy'),
                'crop' : (5*250, 10*250)
        },
        'Simon_exp_cyril_6hz_60' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_6hz_60.npy'),
                'crop' : (5*250, 65*250)
        },
        'Simon_exp_cyril_6hz_50' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_6hz_50.npy'),
                'crop' : (4*250, 54*250)
        },
        'Simon_exp_cyril_6hz_40' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_6hz_40.npy'),
                'crop' : (4*250, 44*250)
        },
        'Simon_exp_cyril_6hz_30' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_6hz_30.npy'),
                'crop' : (4*250, 34*250)
        },
        'Simon_exp_cyril_6hz_20' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_6hz_20.npy'),
                'crop' : (3*250, 23*250)
        },
        'Simon_exp_cyril_6hz_10' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_6hz_10.npy'),
                'crop' : (3*250, 13*250)
        },
        'Simon_exp_cyril_6hz_5' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_6hz_5.npy'),
                'crop' : (5*250, 10*250)
        },
        'Simon_exp_cyril_6hz_10' : {
                'path' : Path('./recorded_data/recordings_numpy/Simon/OpenBCISession_simon_exp_cyril_6hz_10.npy'),
                'crop' : (3*250, 13*250)
        },
        'Sam_exp_ft2_12hz_2' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam/OpenBCISession_Sam_exp_ft2_12hz_2.npy'),
                'crop' : (2*250, 65*250)
        },

        'Joos_exp_pseudo2_take1' : {
                'path' : Path('.\\recorded_data\\recordings_numpy\Joos\OpenBCISession_Joos_exp_pseudo2_1s_take1.npy'),
                'crop' : (367, 367 + 40*250)
        },
        'Joos_exp_pseudo2_take2' : {
                'path' : Path('.\\recorded_data\\recordings_numpy\Joos\OpenBCISession_Joos_exp_pseudo2_1s_take2.npy'),
                'crop' : (649, 649 + 40*250)
        },
        'Joos_exp_pseudo2_take3' : {
                'path' : Path('.\\recorded_data\\recordings_numpy\Joos\OpenBCISession_Joos_exp_pseudo2_1s_take3.npy'),
                'crop' : (398, 398 + 40*250)
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
                
        



