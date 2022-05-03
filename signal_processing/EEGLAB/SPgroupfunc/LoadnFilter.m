% Loads edf file using EEGLAB, uses a basic filter and returns the data from
% all channels
%
% !!! Important: EEGLAB must be in MATLAB path !!!

% INPUTS:
%       - path2edf: Path to edf file
%  OPTIONAL:
%       - locutoff: bottom cutoff frequency for filter on eeg data
%       - hicutoff: top cutoff frequency for filter on eeg data

% OUTPUTS:
%       - filtered_data: MATLAB matrix with a size of nChannels x
%       TimeRecorded * Fs
function filtered_data = LoadnFilter(path2edf, varargin)
    %check if eeglab is in path already or if eeglab.m is in current folder
    if ~strInPath("eeglab") && ~ScriptInCurrentFolder("eeglab", mfilename) 
%        error('EEGLAB not found in path')
       addpath(which('eeglab'));
    end

    %Test if biosig is in path, if not then launch eeglab to take care of
    %adding to path and stuff
    if ~strInPath('Biosig')
       eeglab nogui; %launch eeglab without gui
    end

    if nargin < 3
       g.locutoff = 0.5; %default values for locutoff and hicutoff
       g.hicutoff = 25;
    else
        g = finputcheck( varargin, { ...
            'locutoff' 'integer' [0 Inf] [];
            'hicutoff' 'integer' [0 Inf] [] %take lo/hi cutoff from function argument input
            }, 'LoadnFilter');
    end
    
    %read file using biosig
    EEG = pop_biosig(path2edf);
        
    %create EEGLAB set
    [ALLEEG, EEG, CURRENTSET] = pop_newset([], EEG, 1, 'setname', 'edfread', 'overwrite', 'on');
    
    %filter EEG data
    [EEG, com, filter_coeff] = pop_eegfiltnew(EEG, 'locutoff', g.locutoff, 'hicutoff', g.hicutoff);

    %create new EEGLAB set with filtered data
    [ALLEEG, EEG, CURRENTSET] = pop_newset(ALLEEG, EEG, CURRENTSET, 'setname', 'filtered', 'overwrite', 'on');

    filtered_data = EEG.data; %get data from EEG struct
end