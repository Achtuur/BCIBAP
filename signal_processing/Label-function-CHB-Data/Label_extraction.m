function [SessMatch,SmplRate, Out] = Label_extraction(TxtLoc)
%LABEL_EXTRACTION Summary of this function goes here
% Label_extraction extracts the seizure and sample data from CHB EEG,
% the outputs are a matrix of size M x N, with M the amount of recordings
% for the given patient, and N the amount of samples in a recording.
% furthermore the sample rate is also returned.
%   Detailed explanation goes here
% Reads CHB summary text files and extracts the data which is required to 
% label the data for the machine learning modules. This is done through 
% use of regular expressions, to find the important values


% nargin zooi als nodig
Txt = fileread(TxtLoc);

SmpleExpr = '\d* Hz';  % Helps find the sampling rate in the txt file
Match = regexp(Txt,SmpleExpr,'match');
SmplRate = str2double(Match{1}(1:length(Match{1})-3));

SessExpr = 'File: ';
SessMatch = regexp(Txt,SessExpr,'end');

TimeExpr = ' \d* '; % Finds the start and end time of seizures in txt

Out = zeros(length(SessMatch),3600*SmplRate); % Output labels set to 0 (no seizure)

for i=1:(length(SessMatch)-1)
    if '0' < Txt(SessMatch(i)+1) % Check if seizure happened in session
        Match = regexp(Txt(SessMatch(i):SessMatch(i+1)),TimeExpr,'match');
        Out(i,str2double(Match{1})*SmplRate:str2double(Match{2})*SmplRate) = 1;
    end
%     if Out == 0
%         Out = 
%     end
end
    
end

