
%Example of how to use LoadnFilter to get filtered data from an .edf file

addpath('./SPgroupfunc') %this folder should be in your EEGLAB folder as it contains the functions
path2edf = './sample_data/chb01_01.edf'; %path to .edf file
filtered_data = LoadnFilter(path2edf, 'locutoff', 0.5, 'hicutoff', 30, 'showplots', 1); %call function and voila


