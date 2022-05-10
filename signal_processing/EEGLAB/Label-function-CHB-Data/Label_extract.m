% Extracts classification labels from CHB summary file and returns labels
% based on epoch length in seconds
function [SmplRate, Out] = Label_extract(TxtLoc, EpochLength, nFiles)
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

SmpleExpr = '\d+ Hz';  % Helps find the sampling rate in the txt file
SmplMatch = regexp(Txt,SmpleExpr,'match');
SmplRate = str2double(SmplMatch{1}(1:length(SmplMatch{1})-3));


% if nargin < 2
%     EpochLength = 1;
% end

SessExpr = 'File Name: ';
SessMatch = regexp(Txt,SessExpr,'end');
SessMatch(length(SessMatch)+1) = length(Txt);


% Finds the start and end time of seizures in txt

NameExpr = 'chb\S*.edf';
HMSExpr = '(\d+):(\d+):(\d+)';
AmountExpr = ' \d+ ';
NameMatch = regexp(Txt,NameExpr,'match');
HMSMatch = regexp(Txt,HMSExpr,'tokens');

maxLoop = min(nFiles, length(SessMatch)-1); %take first n Files
for i=1:maxLoop
    % Findname of recording + amount of seizures + duration of recording
    % which is turned into epochs
    AmountMatch = regexp(Txt(SessMatch(i):SessMatch(i+1)),AmountExpr,'match');
    
    % Calc length of session
    SessLength = (str2double(HMSMatch{2*i}{1}) - str2double(HMSMatch{2*i-1}{1})) * 3600;
    SessLength = SessLength + (str2double(HMSMatch{2*i}{2}) - str2double(HMSMatch{2*i-1}{2})) * 60;
    SessLength = SessLength + (str2double(HMSMatch{2*i}{3}) - str2double(HMSMatch{2*i-1}{3}));
    Epoch = zeros(1,floor(SessLength/EpochLength));
    
    disp(Txt(SessMatch(i) + 1))
    if Txt(SessMatch(i)+1) == '1' % Check if seizure happened in session
        begin = ceil(str2double(AmountMatch{1})/EpochLength);
        finish = ceil(str2double(AmountMatch{2})/EpochLength);
        Epoch(begin:finish) = 1;
    elseif Txt(SessMatch(i)+1) > '1'
        for j=0:(length(AmountMatch)/4)-1
            begin = ceil(str2double(AmountMatch{2+4*j})/EpochLength);
            finish = ceil(str2double(AmountMatch{4+4*j})/EpochLength);
            Epoch(begin:finish) = 1;
        end
    end
    Out(i,:) = {NameMatch{i}, Epoch};
end

    
end
