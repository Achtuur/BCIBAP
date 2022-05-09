% Extracts classification labels from CHB summary file and returns labels
% based on epoch length in seconds
function [SmplRate, Out] = Label_extract2(TxtLoc, EpochLength)
%LABEL_EXTRACTION Summary of this function goes here
% Label_extraction extracts the seizure and sample data from CHB EEG,
% the outputs are a matrix of size M x N, with M the amount of recordings
% for the given patient, and N the amount of samples in a recording.
% furthermore the sample rate is also returned.
%   Detailed explanation goes here
% Reads CHB summary text files and extracts the data which is required to 
% label the data for the machine learning modules. This is done through 
% use of regular expressions, to find the important values

Txt = fileread(TxtLoc);

SmpleExpr = '\d* Hz';  % Helps find the sampling rate in the txt file
Match = regexp(Txt,SmpleExpr,'match');
SmplRate = str2double(Match{1}(1:length(Match{1})-3));


if nargin < 2
    EpochLength = 1;
end

SessExpr = 'File Name: ';
SessMatch = regexp(Txt,SessExpr,'end');
SessMatch(length(SessMatch)+1) = length(Txt);


% Finds the start and end time of seizures in txt

NameExpr = 'chb\S*.edf';
TimeExpr = ' \d* ';

% Made assuming all recordings are of length an hour
% Output labels set to 0 (no seizure)

for i=1:(length(SessMatch)-1)
    % Findname of recording + amount of seizures + duration of recording
    % which is turned into epochs
    NameMatch = regexp(Txt(SessMatch(i):SessMatch(i+1)),NameExpr,'match');
    Match = regexp(Txt(SessMatch(i):SessMatch(i+1)),TimeExpr,'match');
    
    if Txt(SessMatch(i)+1) == '1' % Check if seizure happened in session
        begin = ceil(str2double(Match{1})/EpochLength);
        finish = ceil(str2double(Match{2})/EpochLength);
    elseif Txt(SessMatch(i)+1) > '1'
        for j=0:(length(Match)/4)-1
            begin = ceil(str2double(Match{2+4*j})/EpochLength);
            finish = ceil(str2double(Match{4+4*j})/EpochLength);
        end
    end
    Out(i,:) = {NameMatch{1}, 3};
end
    
end
