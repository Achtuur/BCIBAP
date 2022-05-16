%% Train Classification Neural Network

%% Inputs
%   dataset: name of dataset, eg 'chb04' or 'chb10'
%   path: path to folder containing dataset .edf files and summary.txt
%   FileIndices: indices of files in summary.txt to be labeled, starts at 1

%% Outputs
% uhh

%% Function start
function [features,labels,featurelabels] = CNN(dataset, path2dataset, FileIndices, EpochLengthSec)
%% Test variables
EegFeature = 0;

%% Get filtered data

filtered_data = LoadData(path2dataset, FileIndices, 'overwrite', 0);

%% Get labels of data

summarypath = path2dataset + dataset + "-summary.txt";
[Fs, labels] = Label_extract2(summarypath, EpochLengthSec, FileIndices); %get labels of where there are seizures

temp = [];
for k = 1 : size(labels, 1) %loop through rows of labels
    labelarr = labels{k, 2};
    labelarr = labelarr(:); %force column vector
    temp = [temp; labelarr]; %make labels 1 long column vector where every row is an epoch
end
labels = temp + 1; % +1 so that labels are '1' and '2' for no seizure / seizure respectively

%% Get features

[features, featurelabels] = FeatExtractFunc(filtered_data(1,:), Fs, EpochLengthSec);

for k = 1 : size(features, 2) %loop through channels
    features(:,k) = zscore([features{:,k}]);
end

%% Normalizes EEG data and adds it to features, TODO
if EegFeature
    for k = 1 : size(filtered_data, 1) %loop through channels
        filtered_data(:,k) = zcore(filtered_data(:,k));
    end
end



end

