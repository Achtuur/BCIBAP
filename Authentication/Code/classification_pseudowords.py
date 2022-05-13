from sklearn import svm
from SVM import svm_classifier
from pathlib import Path
import csv

#This function gets labels from the pseudoword timestamp file, which are a 1 for pseudoword and a 0 for a real word
def get_labels():
    path = Path(r"..\Experiments\Pseudowords\timestamps\data_2022-05-10_09-51-54.724695.csv")
    with open(path, newline = '') as f:
        csv_reader = csv.reader(f, delimiter=',')
        data = list(csv_reader)

    labels = [0] * int((0.5 * len(data)))
    j = 0
    for i in data: #This for loop gets the zeros and ones from the imported file and stores them as labels
        if not i: 
            i = ''
        else:
            labels[j] = i[1]
            j = j + 1 
        
    return labels

#This function gets timestamps from the file pseudoword timestamp file
def timestamps_experiment():
    #
    path = Path(r"..\Experiments\Pseudowords\timestamps\data_2022-05-10_09-51-54.724695.csv")
    with open(path, newline = '') as f:
        csv_reader = csv.reader(f, delimiter=',')
        data = list(csv_reader)

    #This for loop gets the timestamps from the experiment data and turns it into a string of only numbers
    experiment_times = [0] * int((0.5 * len(data))) 
    j = 0
    for i in data:
        if not i: 
            i = ''
        else:
            experiment_times[j] = i[2].replace(':','').replace('.','')
            j = j + 1 
        
    return experiment_times

#This function checks at what sample of the recorded data the experiment has started
def start_data(fs): 
    experiment_times = timestamps_experiment()
    data_times = timestamps_data()
    time_diff = str(int(experiment_times[0]) - int(data_times[0]))
    ms = time_diff[6:]
    s = time_diff[4:6]
    m = time_diff[2:4]
    sample_start = int(int(m)*fs*60 + int(s)*fs + int(ms)*(fs/1000)) #sample_start is an integer for at what sample the experiment started
    return sample_start


#This function takes data from the raw recording file and takes the timestamps from this, it removes the dates and turns the time into a strin of only numbers
def timestamps_data():
    path = Path(r"..\Data\recorded_data\_unused\OpenBCISession_Sam_take_5_pseudowords\OpenBCI-RAW-2022-05-06_15-53-11.txt")
    with open(path, newline = '') as f: 
        data = f.readlines()
        print(data[20])
        data_times = [0] * (len(data) - 5)
        j = 0
    for i in data[5:]:
        i = i.split(",")
        data_times[j] = i[24].replace('\n','').replace(' ','').replace('-','').replace(':','').replace('.','')[8:]
        j = j + 1
    return data_times

if __name__ == '__main__':
    # labels = get_labels()
    # print(labels)
    # print(len(labels))
    # timestamps = get_timestamps()
    # print(timestamps)
    # print(len(labels))
    
    start = start_data(250)
    print(start)
