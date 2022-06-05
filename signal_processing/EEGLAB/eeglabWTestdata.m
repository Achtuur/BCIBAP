clear; clc;
eegpath = AddPath();
dataset = 'chb04';
path2dataset = eegpath + "sample_data\" + dataset + "\";
FileIndices = 4;
indexstr = sprintf("%d", FileIndices);
if length(indexstr) == 1
   indexstr = "0" + indexstr; 
end
path2edf = sprintf("%s%s_%s.edf", path2dataset, dataset, indexstr);

summarypath = path2dataset + dataset + "-summary.txt";
[~, ~, channellist, ~] = Label_extract2(summarypath, 1, FileIndices); %get labels of where there are seizures

path2edf = convertStringsToChars(path2edf); % make char array so that path can be indexed
path2edf = strrep(path2edf,'/', filesep); %make sure every dash in path works for os
path2edf = strrep(path2edf, '\', filesep);

eeglab;
EEG = pop_biosig(path2edf, 'channels', channellist.index);
        
%create EEGLAB set
[ALLEEG, EEG, CURRENTSET] = pop_newset([], EEG, 1, 'setname', 'edfread', 'overwrite', 'on');

%% After this is run, select "load existing dataset" and then exit the file select menu