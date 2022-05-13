from math import ceil
import csv
from pathlib import Path
import numpy as np

def crop(data: np.ndarray, t_window: int, f_sampling: float) -> list:
    array_length = data.shape[0]
    n_sub_samples = ceil(t_window * f_sampling)
    groups = array_length // n_sub_samples

    cropped_data = np.array_split(data, groups)
    return cropped_data


#This function gets labels from the pseudoword timestamp file, which are a 1 for pseudoword and a 0 for a real word

# Deze functie moet een path als input hebben zodat het niet gehardcode hoeft te zijn
def get_labels():
    path = Path(r"..\Experiments\Pseudowords\timestamps\data_2022-05-10_09-51-54.724695.csv")
    
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
    j = 0
    for i in data: #This for loop gets the zeros and ones from the imported file and stores them as labels
        if not i: 
            i = ''
        else:
            # Het is nice als deze 1 ook een functie input is, mocht de format verwijderen gaat
            # het niet stuk dan
            labels[j] = i[1]
            # Dit zou dan weg kunnen
            j = j + 1 
        
    return labels

#This function gets timestamps from the file pseudoword timestamp file
# Deze functie moet een path als input hebben zodat het niet gehardcode hoeft te zijn
def timestamps_experiment():
    path = Path(r"..\Experiments\Pseudowords\timestamps\data_2022-05-10_09-51-54.724695.csv")
    with open(path, newline = '') as f:
        csv_reader = csv.reader(f, delimiter=',')
        data = list(csv_reader)

    #This for loop gets the timestamps from the experiment data and turns it into a string of only numbers
    # Het is onduidelijk wat j en i doen, ik denk dat je van een lijst
    # een index en een item wilt. Je moet dan for index, item in enumerate(data) doen,
    # dan hoef je niet op deze manier met letter variabelen te werken
    experiment_times = [0] * int((0.5 * len(data))) 

    # Het is onduidelijk wat j en i doen, ik denk dat je van een lijst
    # een index en een item wilt. Je moet dan for index, item in enumerate(data) doen,
    # dan hoef je niet op deze manier met letter variabelen te werken
    j = 0
    for i in data:
        if not i: 
            i = ''
        else:
            # Het is nice als deze 2 ook een functie input is, mocht de format verwijderen gaat
            # het niet stuk dan
            experiment_times[j] = i[2].replace(':','').replace('.','')
            # Dit kan dan weg
            j = j + 1 
        
    return experiment_times

#This function checks at what sample of the recorded data the experiment has started
# Is fs sampling rate?
def start_data(fs): 
    # Hier mag dus een mooie input
    experiment_times = timestamps_experiment()
    # Hier mag dus een mooie input
    data_times = timestamps_data()

    time_diff = str(int(experiment_times[0]) - int(data_times[0]))
    ms = time_diff[6:]
    s = time_diff[4:6]
    m = time_diff[2:4]
    sample_start = int(int(m)*fs*60 + int(s)*fs + int(ms)*(fs/1000)) #sample_start is an integer for at what sample the experiment started
    return sample_start


#This function takes data from the raw recording file and takes the timestamps from this, it removes the dates and turns the time into a strin of only numbers
# Hier ook een path input
def timestamps_data():
    path = Path(r"..\Data\recorded_data\_unused\OpenBCISession_Sam_take_5_pseudowords\OpenBCI-RAW-2022-05-06_15-53-11.txt")
    with open(path, newline = '') as f: 
        data = f.readlines()
        # Kan deze print weg?
        print(data[20])
        # Hier ook weer een list comprehension
        data_times = [0] * (len(data) - 5)

    # Hetzelfde met dit laatste loopje als de andere punten
    j = 0
    for i in data[5:]:
        i = i.split(",")
        data_times[j] = i[24].replace('\n','').replace(' ','').replace('-','').replace(':','').replace('.','')[8:]
        j = j + 1
    return data_times




if __name__ == '__main__':
    data_path = Path('../Data/recorded_data/recordings_numpy/OpenBCI-RAW-2022-05-02_15-07-38.npy')
    f_sampling = 250
    t_window = 5

    data = np.load(data_path)
    cropped_data = crop(data, t_window, f_sampling)
    print(cropped_data[0].shape)