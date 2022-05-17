from pathlib import Path
import numpy as np
import os

# Global dictionary constructed from experiment file
RECORDINGS_CROP_DICTIONARY = {
        # M1
        'M1_CALIBRATION' : {
                'path' : Path('./recorded_data/recordings_numpy/M1_10_05_2022/OpenBCISession_Wessel_calibration.npy'),
                'crop' : (250*15, 250*75)
        },
        'M1_PSEUDO' : {
                'path' : Path('./recorded_data/recordings_numpy/M1_10_05_2022/OpenBCISession_Wessel_pseudo.npy'),
                'crop' : (1570, 62864)
        }, 
        # SAM
        'SAM_CALIBRATION' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_calibration.npy'),
                'crop' : (250*62, 250*122)
        },
        'SAM_PSEUDO' : {
                'path' : Path('./recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_pseudo.npy'),
                'crop' : (1186, 62532)
        }
}

def txt_to_numpy(recording_txt_path, filename, subject_name):
        BASE_PATH = Path('./recorded_data/recordings_numpy')
        subject_dir = BASE_PATH / Path(subject_name)
        try:
                os.makedirs(subject_dir)
        except FileExistsError:
                pass
        
        raw_txt_file = list(recording_txt_path.iterdir())[0]
        with open(raw_txt_file, 'r') as file:
                np_frame = np.loadtxt(fname=file, skiprows=5, delimiter=', ', usecols=(i for i in range(1,9)))
                save_path = Path(f'{subject_dir}/{filename}.npy')
                np.save(save_path, np_frame)


if __name__ == '__main__':
        # Raw recording path
        RAW_RECORDING_PATH = Path('./recorded_data/recordings_txt')

        # Iterate Test Subjects
        SUBJECTS = RAW_RECORDING_PATH.iterdir()
        for subject in SUBJECTS:
                subject_name = subject.stem
                base_path = RAW_RECORDING_PATH / Path(subject_name)
                # Iterate recordings
                RECORDINGS = base_path.iterdir()
                for recording in RECORDINGS:
                        recording_path = Path(recording)
                        folder_name = recording_path.stem
                        txt_to_numpy(recording_path, folder_name, subject_name)

        for recording_to_crop in RECORDINGS_CROP_DICTIONARY.values():
                numpy_data = np.load(recording_to_crop['path'])
                print(f"{recording_to_crop['path']} --- {numpy_data.shape}")
                cropped_numpy_data = numpy_data[recording_to_crop['crop'][0]:recording_to_crop['crop'][1]]
                np.save(recording_to_crop['path'], cropped_numpy_data)
                print(np.load(recording_to_crop['path']).shape)
                
        



