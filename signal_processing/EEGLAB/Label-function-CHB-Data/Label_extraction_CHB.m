% Extract the seizure times and output them based on Epoch length

clearvars;



EpochLength = 1; % Length of epoch in seconds
[SmplRate,LabelOut] = Label_extract('chb04-summary.txt',EpochLength);