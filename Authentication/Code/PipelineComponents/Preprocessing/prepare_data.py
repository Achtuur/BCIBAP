from math import ceil
import csv
from pathlib import Path
import numpy as np
import os

def crop(sample_start, sample_end, data: np.ndarray, t_window: int, f_sampling: float) -> list:
    print(len(data))
    data = data[sample_start:sample_end]
    print(len(data))
    array_length = data.shape[0]
    n_sub_samples = ceil(t_window * f_sampling)
    groups = array_length // n_sub_samples
    print(groups)

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
    len_experiment = int(len(data)*0.5)
    
    return start_experiment, len_experiment

#This function checks at what sample of the recorded data the experiment has started
def start_data(fs, path_experiment, path_recording, duration = 5): 
    # Hier mag dus een mooie input
    start_experiment, len_experiment = timestamps_experiment(path_experiment)

    #start_data = timestamps_data(path_recording, lines_to_skip, time_location, time_information)
    start_data = timestamps_recording(path_recording)
    time_diff = str(int(start_experiment) - int(start_data))
    time_diff = '00000' + time_diff
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
def timestamps_recording(path_recording, lines_to_skip = 5, time_location = 24, time_information = 9):
    path = Path(path_recording)
    with open(path, newline = '') as f: 
        data = f.readlines()

    time_information = len(data[5]) - time_information
    start_data = data[lines_to_skip[time_location]][:time_information]   
    return start_data




if __name__ == '__main__':
    data_path = Path('../../Data/ExperimentResults/recorded_data/recordings_numpy/Sam_10_05_2022/OpenBCISession_Sam_pseudo.npy')
    path_experiment = Path('../../Data/Experiments/Pseudowords/results/data_2022-05-10_11-31-17.544482.csv')
    path_recording = Path()
    f_sampling = 250
    t_window = 5
    
    sample_start, sample_end = start_data(f_sampling, path_experiment, path_recording)

    data = np.load(data_path)
    cropped_data = crop(sample_start, sample_end, data, t_window, f_sampling)
    print(cropped_data[0].shape)