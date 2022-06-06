%% Loads edf file using EEGLAB, uses a basic filter and returns the data from
% all channels
%
% !!! Important: EEGLAB must be in MATLAB path !!!

%% INPUTS:
%       - path2edf: Path to edf file
%  OPTIONAL:
%       - locutoff: [number], bottom cutoff frequency (Hz) for filter on eeg data, default 0.5
%       - hicutoff: [number], top cutoff frequency (Hz) for filter on eeg data, default 50
%       - forder: filter order, default 1000
%       - showplots: [true/false], show plots of before/after filtering, default 'false'
%       - channellist: [number], vector with channels to be included, use 0 to include all channels, default 0
%       - ASR: [true/false], do ASR, default 'true'
%       - TestSinWave: [period, phase, randrange] replace EEG data with a sin wave with certain period and phase and random variance, default []
%% OUTPUTS:
%       - filtered_data: MATLAB matrix with a size of nChannels x
%       TimeRecorded * Fs
function [filtered_data, unfiltered_data] = LoadnFilter(path2edf, varargin)
%% test vars (comment out nargin/varargin stuff)
%     eegpath = AddPath();
%     dataset = 'chb04';
%     filenum = '05';
%     file = sprintf("%s_%s.edf", dataset, filenum); %chb0x_0y.edf
%     path2edf = eegpath + "/sample_data/" + dataset + "/" + file;
%     g.locutoff = 0.5; %default values for locutoff and hicutoff
%     g.hicutoff = 40;
%     g.showplots = 0;
%     g.channellist = [1 2 5 4];
%%
path2edf = convertStringsToChars(path2edf); % make char array so that path can be indexed
path2edf = strrep(path2edf,'/', filesep); %make sure every dash in path works for os
path2edf = strrep(path2edf, '\', filesep);
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
%% varargin
    if nargin < 3
       g.locutoff = 0.5; %default values for locutoff and hicutoff
       g.hicutoff = 30;
       g.showplots = 0;
       g.channellist = 0;
       g.forder = 1000;
       g.ASR = 0;
       g.TestSinWave = [];
       g.downsample = 1;
    else
        g = finputcheck( varargin, { ...
            'channellist' 'integer' [0 inf] [];
            'locutoff' 'integer' [0 Inf] 0.5;
            'hicutoff' 'integer' [0 Inf] 30; %take lo/hi cutoff from function argument input
            'forder' 'integer' [0 inf] 30;
            'showplots' 'integer' [0 inf] 0;
            'ASR' 'integer' [0 inf] 0
            'TestSinWave' 'integer' [0 inf] [];
            'downsample' 'integer' [0 inf] 1;
            }, 'LoadnFilter');
    end
%% Read and filter data
g.channellist = sort(g.channellist);
if ~isfile(path2edf)
   error(path2edf + " not found"); 
end
%% read file using biosig
path2edf = convertStringsToChars(path2edf);
EEG = pop_biosig(path2edf, 'channels', g.channellist);

%% Replace sin wave (if enabled) doesnt work
if ~isempty(g.TestSinWave)
   T = g.TestSinWave(1); %period
   phi = g.TestSinWave(2); %phase
   rnd = g.TestSinWave(3); %rand range
   x = linspace(0, 10*pi, size(EEG.data, 2)); % x vector same length as loaded eeg data
   EEG.data = 0.1*sin(2*pi/T * x + phi) + rnd * [zeros(size(EEG.data, 1), 10000), rand(size(EEG.data, 1), size(EEG.data, 2)-10000) - rnd];
end


%% create EEGLAB set
[ALLEEG, EEG, CURRENTSET] = pop_newset([], EEG, 1, 'setname', 'edfread', 'overwrite', 'on');
unfiltered_data = EEG.data;

%% Plot raw EEG data
if g.showplots
    pop_eegplot( EEG, 1, 1, 1);
end

%% filter EEG data
%     [EEG, ~, ~] = pop_eegfiltnew(EEG, 'locutoff', g.locutoff, 'hicutoff', g.hicutoff);%, 'filtorder', g.forder);
if g.locutoff == 0 %low cutoff 0 -> use lowpass
    [EEG, ~, ~] = pop_firws(EEG, 'fcutoff', g.hicutoff, 'forder', g.forder, 'wtype', 'hamming', 'ftype', 'lowpass');
else %low cutoff ~= 0 -> use bandpass
    [EEG, ~, ~] = pop_firws(EEG, 'fcutoff', [g.hicutoff, g.locutoff], 'forder', g.forder, 'wtype', 'hamming', 'ftype', 'bandpass');
end


%% ASR
if g.ASR
    [EEG, ~, ~] = clean_artifacts(EEG, 'WindowCriterion', 'off', 'ChannelCriterion','off', 'LineNoiseCriterion', 'off');
end

%% Plot filtered EEG data
if g.showplots
    pop_eegplot( EEG, 1, 1, 1);
end

%% create new EEGLAB set with filtered data
[ALLEEG, EEG, CURRENTSET] = pop_newset(ALLEEG, EEG, CURRENTSET, 'setname', 'filtered', 'overwrite', 'on');

filtered_data = EEG.data; %get data from EEG struct
filtered_data = downsample(filtered_data', g.downsample)';
end