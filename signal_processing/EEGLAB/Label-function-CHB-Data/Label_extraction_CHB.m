% Extract the seizure times and output them based on Epoch length

clearvars;

EpochLength = 3; % Length of epoch in seconds
[SmplRate,LabelOut] = Label_extract('chb01-summary.txt',EpochLength);

