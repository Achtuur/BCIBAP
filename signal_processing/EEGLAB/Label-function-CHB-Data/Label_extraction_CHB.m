% Extract the seizure times and output them based on Epoch length

clearvars;

EpochLength = 2; % Length of epoch in seconds
[SmplRate,LabelOut] = Label_extract('chb10-summary.txt',EpochLength);

