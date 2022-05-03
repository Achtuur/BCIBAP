% Loads edf file using EEGLAB, uses a basic filter and returns the data from
% all channels
%
% !!! Important: EEGLAB must be in MATLAB path !!!
% INPUTS:
%       - path2edf: Path to edf file
%       - locutoff: bottom cutoff frequency for filter on eeg data
%       - hicutoff: top cutoff frequency for filter on eeg data
% OUTPUTS:
%       - filtered_data: MATLAB matrix with a size of nChannels x
%       TimeRecorded * Fs
function filtered_data = LoadnFilter(path2edf, locutoff, hicutoff)
    %read file using biosig
    EEG = pop_biosig(path2edf);
    
    %create EEGLAB set
    [ALLEEG, EEG, CURRENTSET] = pop_newset([], EEG, 1, 'setname', 'edfread', 'overwrite', 'on');
    
    %filter EEG data
    [EEG, com, filter_coeff] = pop_eegfiltnew(EEG, 'locutoff', locutoff, 'hicutoff', hicutoff);

    %create new EEGLAB set with filtered data
    [ALLEEG, EEG, CURRENTSET] = pop_newset(ALLEEG, EEG, CURRENTSET, 'setname', 'filtered', 'overwrite', 'on');

    filtered_data = EEG.data; %get data from EEG struct
end