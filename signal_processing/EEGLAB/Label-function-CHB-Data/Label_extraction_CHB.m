% Extract the seizure times and output them based on Epoch length

clearvars;

dataset = 'chb04';
path = "C:\Users\Arthur\Desktop\Programming\BCIBAP\signal_processing\EEGLAB\sample_data\" + dataset + "\";
nFiles = 28;

EpochLength = 3; % Length of epoch in seconds
[SmplRate,LabelOut] = Label_extract2(path + dataset + "-summary.txt",EpochLength, nFiles);

t = [];
for k = 1:size(LabelOut, 1)
%     t(k, :) = find(LabelOut{k,2} == 1);
end
a = LabelOut{5,2};
b = find(a == 1);