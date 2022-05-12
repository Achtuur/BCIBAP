%% Trains model used to classify seizures

%% Inputs
%   dataset: name of dataset, eg 'chb04' or 'chb10'
%   path: path to folder containing dataset .edf files and summary.txt
%   nFiles: first n .edf files to be used to train model

%% Outputs
%   model.mat saved in same folder contains:
%       model: ML model which can be used to classify seizures
%       mu_train: mean of training data obtained from zscore test, used to normalise
%       sigma_train: std of training data obtained from zscore test, used to normalise
function [lab, predicted] = TrainModel(dataset, path2dataset, FileIndices, EpochLengthSec)
% test vars
% dataset = 'chb04';
% path2dataset = "C:\Users\Arthur\Desktop\Programming\BCIBAP\signal_processing\EEGLAB\sample_data\" + dataset + "\";
% FileIndices = 5;
%% get filtered data

filtered_data = LoadData(path2dataset, FileIndices, 'overwrite', 0);

%% Get labels of data
% EpochLengthSec = 2;
summarypath = path2dataset + dataset + "-summary.txt";
[Fs, labels] = Label_extract2(summarypath, EpochLengthSec, FileIndices); %get labels of where there are seizures


temp = [];
for k = 1 : size(labels, 1) %loop through rows of labels
    labelarr = labels{k, 2};
    labelarr = labelarr(:); %force column vector
    temp = [temp; labelarr]; %make labels 1 long column vector where every row is an epoch
end
labels = temp + 1; % +1 so that labels are '1' and '2' for no seizure / seizure respectively

%%

% normalise filtered_data
for k = 1 : size(filtered_data, 1) %loop through channels
    filtered_data(:,k) = (filtered_data(:,k) - mean(filtered_data(:,k))) / max(filtered_data(:,k));
end

[features, featurelabels] = FeatExtractFunc(filtered_data(1,:), Fs, EpochLengthSec);

starti = find(labels == 2,1, 'first');
endi = find(labels == 2,1, 'last');
di = floor((endi-starti) * 2);
features = features(starti - di : endi + di, :); %only take stuff around the epilepsy so data is 50/50
labels = labels(starti - di : endi + di, :);

[lab, predicted] = CreateModel(features, labels, featurelabels);

end