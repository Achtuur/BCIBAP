% Extract the seizure times and output them based on Epoch length

clearvars;
eegpath = AddPath();
dataset = 'chb03';
path2dataset = eegpath + "\sample_data\" + dataset + "\";
FileIndices = 1:6;

EpochLength = 3.25; % Length of epoch in seconds
[SmplRate,LabelOut, channellist, rounding_err] = Label_extract2(path2dataset + dataset + "-summary.txt", EpochLength, FileIndices);


%% Use rounding_err to make filtered_data a few samples shorter per loaded file
filtered_data = LoadData(path2dataset, FileIndices, 'overwrite', 0, 'channellist', channellist, 'rounding_err', rounding_err);
epochs = DivideInEpochs(filtered_data, SmplRate, EpochLength);


%% Test lengths of labels and epochs
labels = [];
for k = 1:size(LabelOut, 1)
   labels = [labels; LabelOut{k ,2}']; 
end

if size(epochs, 1) == size(labels, 1)
   disp('Same length!');
else
   error('not same length');
end