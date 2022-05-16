from math import ceil
import csv
from pathlib import Path
import numpy as np

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


#This function gets labels from the pseudoword timestamp file, which are a 1 for pseudoword and a 0 for a real word

# Deze functie moet een path als input hebben zodat het niet gehardcode hoeft te zijn
def get_labels(path_experiment, label_column = 1):
    path = Path(path_experiment)
    
    with open(path, newline = '') as f:
        csv_reader = csv.reader(f, delimiter=',')
        data = list(csv_reader)

    # Het is onduidelijk wat j en i doen, ik denk dat je van een lijst
    # een index en een item wilt. Je moet dan for index, item in enumerate(data) doen,
    # dan hoef je niet op deze manier met letter variabelen te werken
    labels = [0] * int((0.5 * len(data)))

    # Het is onduidelijk wat j en i doen, ik denk dat je van een lijst
    # een index en een item wilt. Je moet dan for index, item in enumerate(data) doen,
    # dan hoef je niet op deze manier met letter variabelen te werken
    
    for j,i in enumerate(data): #This for loop gets the zeros and ones from the imported file and stores them as labels
        if not i: 
            i = ''
        else:
            # Het is nice als deze 1 ook een functie input is, mocht de format verwijderen gaat
            # het niet stuk dan
            labels[j] = i[label_column]
            # Dit zou dan weg kunnen
        
    return labels

#This function gets timestamps from the file pseudoword timestamp file
# Deze functie moet een path als input hebben zodat het niet gehardcode hoeft te zijn
# time_column is 2
def timestamps_experiment(path_experiment, time_column = 2):
    
    with open(path_experiment, newline = '') as f:
        csv_reader = csv.reader(f, delimiter=',')
        data = list(csv_reader)

    start_experiment = data[0][time_column].replace(':','').replace('.','')
    len_experiment = int(len(data)*0.5)
    # #This for loop gets the timestamps from the experiment data and turns it into a string of only numbers
    # # Het is onduidelijk wat j en i doen, ik denk dat je van een lijst
    # # een index en een item wilt. Je moet dan for index, item in enumerate(data) doen,
    # # dan hoef je niet op deze manier met letter variabelen te werken
    # experiment_times = [0] * int((0.5 * len(data))) 

    # # Het is onduidelijk wat j en i doen, ik denk dat je van een lijst
    # # een index en een item wilt. Je moet dan for index, item in enumerate(data) doen,
    # # dan hoef je niet op deze manier met letter variabelen te werken
    
    # for j,i in enumerate(data):
    #     if not i: 
    #         i = ''
    #     else:
    #         # Het is nice als deze 2 ook een functie input is, mocht de format verwijderen gaat
    #         # het niet stuk dan
    #         experiment_times[j] = i[time_column].replace(':','').replace('.','')

    return start_experiment, len_experiment

#This function checks at what sample of the recorded data the experiment has started
# Is fs sampling rate? yep
# RAW tells if the data used is raw
def start_data(fs, path_experiment, path_recording, duration = 5): 
    # Hier mag dus een mooie input
    start_experiment, len_experiment = timestamps_experiment(path_experiment)
    print(len_experiment)

    #start_data = timestamps_data(path_recording, lines_to_skip, time_location, time_information)
    start_data = '113023148'
    time_diff = str(int(start_experiment) - int(start_data))
    time_diff = '00000' + time_diff
    ms = time_diff[-3:]
    s = time_diff[-5:-3]
    m = time_diff[-7:-5]
    if s == '' and m == '':
        sample_start = int( int(ms)*(fs/1000)) #sample_start is an integer for at what sample the experiment started
        print('dit gaat niet goed')
    elif m == '':
        sample_start = int(int(s)*fs + int(ms)*(fs*0.001))
        print('test')
    else:
        sample_start = int(int(m)*fs*60 + int(s)*fs + int(ms)*(fs/1000))
        print('heel raar dit')

    sample_end = len_experiment*fs*duration + sample_start
    print(sample_start)
    print(sample_end)
    return sample_start, sample_end


#This function takes data from the raw recording file and takes the timestamps from this, it removes the dates and turns the time into a string of only numbers
# lines to skip is in principe 5, voor de rauwe data
# time_location is in principe 24, voor rauwe data
# time information geeft aantal getallen aan met tijd informatie 3 = miliseconde, 5 = seconde , 7 = minuten, 9 = uren. Uren is standaard
def timestamps_data(path_recording, lines_to_skip = 5, time_location = 24, time_information = 9):
    path = Path(path_recording)
    with open(path, newline = '') as f: 
        data = f.readlines()

    time_information = len(data[5]) - time_information
    start_data = data[lines_to_skip[time_location]][:time_information]   
        # Hier ook weer een list comprehension
        # data_times = [0] * (len(data) - 5)

    # for j, i in enumerate(data[lines_to_skip:]):
    #     i = i.split(",")
    #     data_times[j] = i[time_location].replace('\n','').replace(' ','').replace('-','').replace(':','').replace('.','')
    #     time_information = len(data_times[j]) - time_information
    #     data_times[j] = data_times[j][:time_information]
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