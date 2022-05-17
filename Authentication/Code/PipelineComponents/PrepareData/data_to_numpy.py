from pathlib import Path
import numpy as np
import os
# This is to easily run the script from the command line
# [] = optional
# Usage: python data_to_numpy.py -folder folder_name


def data_to_numpy(RECORDINGS_PATH = Path(f'../../Data/ExperimentResults/recorded_data/recordings_txt')):
        #cwd = os.getcwd()[:-30] #Cut off 30 characters in order to delete last two folders
        dir_path = os.path.dirname(os.path.realpath(__file__))[:-30]
        for subdirs, dirs, files in os.walk(RECORDINGS_PATH):
            for file in files:
                newsubdir = os.path.basename(os.path.normpath(subdirs)) #create folder name to save converted data
                #oldpath = Path(f'{subdirs}/{file}') #The path to the txt file that will be converted
                #oldpath = Path(f'{cwd}/{file}')
                oldpath = dir_path + subdirs[5:] + '/' + file
                start_time = timestamps_recording(oldpath)
                if not os.path.exists(Path(f'./recorded_data/recordings_numpy/{newsubdir}/{file[:-4]}')): #The last 4 items are removed, which are .txt
                    os.makedirs(Path(f'./recorded_data/recordings_numpy/{newsubdir}/{file[:-4]}'))
                    with open(oldpath, 'r') as f:
                        np_frame = np.loadtxt(fname=f, skiprows=5, delimiter=', ', usecols=(i for i in range(1,9)))
                        save_npy = Path(f'./recorded_data/recordings_numpy/{newsubdir}/{file[:-4]}/{file[:-4]}.npy')
                        np.save(save_npy, np_frame)
                    save_text = Path(f'./recorded_data/recordings_numpy/{newsubdir}/{file[:-4]}/{file}')
                    with open(save_text, 'w') as f:
                        f.write(start_time)

        return 

if __name__ == '__main__':
        data_to_numpy()
# RECORDING_FOLDERS = list(RECORDINGS_PATH.iterdir())

# for recording in RECORDING_FOLDERS:
#         # This is weird code to get the value of the generator
#         path = list(recording.glob('*.txt'))[0]
#         with open(path, 'r') as file:
#                 np_frame = np.loadtxt(fname=file, skiprows=5, delimiter=', ', usecols=(i for i in range(1,9)))
#                 save_path = Path(f'./recorded_data/recordings_numpy/{newname}/{file}.npy')
#                 np.save(save_path, np_frame)