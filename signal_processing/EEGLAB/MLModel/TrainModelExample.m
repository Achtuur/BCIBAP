eegpath = AddPath();
dataset = 'chb04';
path = eegpath + "\sample_data\" + dataset + "\";
nFiles = 1;
TrainModel(dataset, path, nFiles);