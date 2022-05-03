
%Example of how to use LoadnFilter to get filtered data from an .edf file

addpath('H:\My Documents\eeglab\SPgroupfunc') %this folder should be in your EEGLAB folder as it contains the functions
path2edf = 'H:\My Documents\eeglab\sample_data\chb01_01.edf'; %path to .edf file
filtered_data = LoadnFilter(path2edf, 'locutoff', 0.5, 'hicutoff', 30); %call function and voila


