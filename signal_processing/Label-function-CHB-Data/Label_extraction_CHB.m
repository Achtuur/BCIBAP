% Extract the seizure times and output them based on Epoch length

clear var;


% [RegexOut,SmplRate,LabelOut] = LabelOld('chb01-summary.txt');

EpochLength = 1; % Length of epoch in seconds
[SmplRate,LabelOut] = Label_extract('chb04-summary.txt',EpochLength);