from math import ceil
import csv
from pathlib import Path
import numpy as np
import os
from os import listdir
import glob

def crop(path_experiment, path_recording_numpy, t_window: int, f_sampling: float) -> list:
    sample_start, sample_end = start_data(f_sampling, path_experiment, path_recording_numpy)

    path = Path(path_recording_numpy)
    file = glob.glob(f'{path}/*.npy')
    data = np.load(file[0])
    data = data[sample_start:sample_end]
    array_length = data.shape[0]
    n_sub_samples = ceil(t_window * f_sampling)
    groups = array_length // n_sub_samples
    cropped_data = np.array_split(data, groups)
    return cropped_data


#This function gets labels from the timestamp file
def get_labels(path_experiment, label_column = 1):
    path = Path(path_experiment)
    
    with open(path, newline = '') as f:
        csv_reader = csv.reader(f, delimiter=',')
        data = list(csv_reader)

    labels = [0] * int((0.5 * len(data)))
    
    for index,label in enumerate(data): #This for loop gets the zeros and ones from the imported file and stores them as labels
        if not label: 
            continue
        else:
            labels[index] = int(label[label_column])
    return labels

#This function gets timestamps from the file timestamp file
def timestamps_experiment(path_experiment, time_column = 2):
    with open(path_experiment, newline = '') as f:
        csv_reader = csv.reader(f, delimiter=',')
        data = list(csv_reader)

    start_experiment = data[0][time_column].replace(':','').replace('.','')
    len_experiment = int(len(data))
    
    return start_experiment, len_experiment

#This function checks at what sample of the recorded data the experiment has started
def start_data(fs, path_experiment, path_recording, duration = 5): 
    # Hier mag dus een mooie input
    start_experiment, len_experiment = timestamps_experiment(path_experiment)

    #start_data = timestamps_data(path_recording, lines_to_skip, time_location, time_information)
    start_data = timestamps_recording(path_recording)
    time_diff = str(int(start_experiment) - int(start_data))
    time_diff = '0000000' + time_diff
    ms = time_diff[-3:]
    s = time_diff[-5:-3]
    m = time_diff[-7:-5]
    if s == '' and m == '':
        sample_start = int( int(ms)*(fs/1000)) #sample_start is an integer for at what sample the experiment started
    elif m == '':
        sample_start = int(int(s)*fs + int(ms)*(fs*0.001))
    else:
        sample_start = int(int(m)*fs*60 + int(s)*fs + int(ms)*(fs/1000))

    sample_end = len_experiment*fs*duration + sample_start
    return sample_start, sample_end


#This function takes data from the raw recording file and takes the timestamps from this, it removes the dates and turns the time into a string of only numbers
def timestamps_recording(path_recording):
    path = Path(path_recording)

    file = glob.glob(f'{path}/*.txt')
    with open(file[0], 'r') as f:
        data = f.readlines()
    
    data = str(data[0])
    start_data = data.split(':', 1)[1].replace(':','').replace('.','')
    return start_data

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
    path_experiment = Path('../../Data/Experiments/Pseudowords/results/data_2022-05-10_11-31-17.544482.csv') #path to file containing information on the experiment
    path_recordings_RAW = Path() #Path to raw recording, used for the data_to_numpy function
    path_recording_numpy = Path(f'.\\recorded_data\\recordings_numpy\OpenBCISession_Sam_ft_12\OpenBCI-RAW-2022-05-10_10-03-06') #path to folder containing the numpy data and timestampfile
    f_sampling = 250 #sampling frequency
    t_window = 5 #duration of experiment stimulations
    
    #data_to_numpy()
    

    cropped_data = crop(path_experiment, path_recording_numpy, t_window, f_sampling)
    print(cropped_data[0].shape)