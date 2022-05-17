%% Trains model used to classify seizures

%% Inputs
%   dataset: name of dataset, eg 'chb04' or 'chb10'
%   path: path to folder containing dataset .edf files and summary.txt
%   FileIndices: indices of files in summary.txt to be labeled, starts at 1

%% Outputs
%   model.mat saved in same folder contains:
%       model: ML model which can be used to classify seizures
%       mu_train: mean of training data obtained from zscore test, used to normalise
%       sigma_train: std of training data obtained from zscore test, used to normalise
%%
% function [lab, predicted] = TrainModel(dataset, path2dataset, FileIndices, EpochLengthSec)
%% test vars
clc; clear;
eegpath = AddPath();
dataset = 'chb04';
path2dataset = eegpath + "sample_data\" + dataset + "\";
FileIndices = 5;
EpochLengthSec = 3.25;
%% Get labels of data
summarypath = path2dataset + dataset + "-summary.txt";
[Fs, labels1, channellist, rounding_err] = Label_extract2(summarypath, EpochLengthSec, FileIndices); %get labels of where there are seizures

temp = [];
for k = 1 : size(labels1, 1) %loop through rows of labels
    labelarr = labels1{k, 2};
    labelarr = labelarr(:); %force column vector
    temp = [temp; labelarr]; %make labels 1 long column vector where every row is an epoch
end
labels = temp + 1; % +1 so that labels are '1' and '2' for no seizure / seizure respectively

if isempty(find(labels == 2, 1))
   error("Input data contains no seizures"); 
end

%% get filtered data
filtered_data = LoadData(path2dataset, FileIndices, 'overwrite', 1, 'channellist', channellist, 'rounding_err', rounding_err);

%% Get features
% normalise filtered_data
% for k = 1 : size(filtered_data, 1) %loop through channels
%     filtered_data(:,k) = (filtered_data(:,k) - mean(filtered_data(:,k))) / max(filtered_data(:,k));
% end

epochs = DivideInEpochs(filtered_data, Fs, EpochLengthSec);
[features, featurelabels] = FeatExtractFunc(epochs, Fs, EpochLengthSec);

starti = find(labels == 2,1, 'first');
endi = find(labels == 2,1, 'last');
di = floor((endi-starti) * 1);
features = features(starti - di : endi + di, :); %only take stuff around the epilepsy so data is 50/50
labels = labels(starti - di : endi + di, :);

%% Create model
[lab, predicted, savepath] = CreateModel(features, labels, featurelabels);

save(savepath, 'Fs', 'EpochLengthSec', '-append');
% end