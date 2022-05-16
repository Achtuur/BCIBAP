%% Creates labels for seizures based on summary file
%   Seizures are labelled as '1' and no seizure is labelled as 0

%% Inputs
%   path: path to "chbxx-summary.txt"
%   EpochDurationSeconds: duration of an epoch in seconds
%   FileIndices: indices of files in summary.txt to be labeled, starts at 1

%% Outputs
%   Fs: sampling frequency contained in summary.txt file
%   LabelsOut: vector containing labels for seizure in a cell array. Every row is structured as {filename, labels}
%   Channelsout: vector containing indices of channels to be used
function [Fs, LabelsOut, ChannelsOut] = Label_extract2(path, EpochDurationSeconds, FileIndices)
%% testvalues
%     dataset = 'chb04';
%     eegpath = AddPath();
%     path = eegpath + "\sample_data\" + dataset + "\";
%     FileIndices = [1 2 28 9];
%     path = path + dataset + "-summary.txt";
%     EpochDurationSeconds = 3;
%% Read txt file and create arrays with file and channel info
%Read summary as plain txt
Txt = fileread(path);
FileIndices = sort(FileIndices);

%split Txt by blank lines
blocks = strsplit(Txt, '\n\s*\n', 'DelimiterType', 'RegularExpression', 'CollapseDelimiters',false);
% blocks{1} has sampling rate
Fs = regexpnum(blocks{1}, '\d+(?=\s\Hz)'); %get sampling frequency from first block

%Files contains the blocks like:
% File Name: chb04_01.edf
% File Start Time: 18:01:25
% File End Time: 22:01:23
% Number of Seizures in File: 0
Files = cell(1); 
Channels = blocks{2}; %channel info is always in blocks{2}
i = 1;
for k = 2 : length(blocks)
    if contains(blocks{k}, ".edf", 'IgnoreCase', ispc) %add only strings that contain a file block
        Files{i} = blocks{k};
        i = i + 1;
    end
end
%% Get seizure labels
maxLoop = min(length(FileIndices), length(Files));
loop = FileIndices;
if length(loop) < 1
   loop = 1 : length(Files); 
end
LabelsOut = cell(maxLoop, 2);
i = 1; %index for labelsout
for k = loop
   fileblock = splitlines(Files{k});
   % fileblock{1} contains file name
   % fileblock{2} contains start time
   % fileblock{3} contains end time
   % fileblock{4} contains number of seizures
   % fileblock{5,} contains seizures
   % note that last entry is empty, so entries without seizures are 5 long, entries with 1 seizure are 7 long etc
   filename = cell2mat(regexp(fileblock{1}, '[a-zA-Z\_0-9]+\.edf', 'match'));
   
   startTimeHMS = cell2mat(regexp(fileblock{2}, '\d+:\d+:\d+', 'match'));
   endTimeHMS = cell2mat(regexp(fileblock{3}, '\d+:\d+:\d+', 'match'));
   timeDiff = calcTimeDiff(startTimeHMS, endTimeHMS);
   Epoch = zeros(1, floor(timeDiff / EpochDurationSeconds));
   
   nSeizures = regexpnum(fileblock{4}, '\d+'); %get number of seizures as a double
   if(nSeizures > 0)
      for n = 0 : nSeizures - 1
          startTime = regexpnum(fileblock{5 + 2*n}, '\d+(?=\s*seconds)');
          endTime = regexpnum(fileblock{6 + 2*n}, '\d+(?=\s*seconds)');
          startIndex = floor(startTime / EpochDurationSeconds);
          endIndex = floor(endTime / EpochDurationSeconds);
          Epoch(1, startIndex : endIndex) = 1; % change labels to 1
      end
   end
   LabelsOut(i, :) = {filename Epoch};
   i = i + 1;
end

%% Get channel info
Channels = strsplit(Channels, '\n');
Channels = Channels(3:end); %first two entries contain irrelevant text
% Channels now looks like this:
% Channels{x} = "Channel x: FP7-T4" (FP7 and T4 are example values)
EarLabels = {'FT9', 'FT7', 'T7', 'TP7', 'TP9', 'FC5', 'C5', 'CP5', ... %Left preauricular
             'FT10', 'FT8', 'T8', 'TP8', 'TP10', 'FC6', 'C6', 'CP6'}; %Right preauricular

ChannelsOut = [];
for k = 1:length(Channels)
    matches = regexp(Channels{k}, 'Channel\s\d+:\s(?<Electrode>[a-zA-Z0-9]+)\-(?<Reference>[a-zA-Z0-9]+)', 'names');
    % matches is struct containing:
    %   matches.Electrode: name of electrode (label left of the ':')
    %   matches.Reference: name of the reference electrode (label right of the ':')
    if any(contains(EarLabels, matches.Electrode, 'IgnoreCase', ispc)) %electrode is around ear
       ChannelsOut = [ChannelsOut k]; %append to channels
    end
end
end %func end
%% Helper functions

%calculate time difference in seconds
%input time should be in 'hh:mm:ss' format
function d = calcTimeDiff(startTimeHMS, endTimeHMS)
    %Split HMS time from 'hh:mm:ss' to cell array {'hh', 'mm', 'ss'}
    startTimeHMS = split(startTimeHMS, ':'); endTimeHMS = split(endTimeHMS, ':');
    d = zeros(0, 3);
    for i = 1 : 3
        d(i) = str2double(endTimeHMS{i}) - str2double(startTimeHMS{i}); %calculate difference in hours, minutes and seconds
    end
    d = d(1) * 3600 + d(2) * 60 + d(3); %add up differences
    
    if d < 0
       error('Time difference negative'); 
    end
end

%get resulting double from regular expression
%does the same as regexp(), but also does cell2mat and str2double so that a double comes out
%regular expression should give 1 result or unexpected behaviour could occur
function m = regexpnum(str, regular_expr)
    m = str2double(cell2mat(regexp(str, regular_expr, 'match')));
end