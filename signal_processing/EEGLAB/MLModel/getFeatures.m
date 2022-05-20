%% Train Classification Neural Network

%% Inputs
%   dataset: name of dataset, eg 'chb04' or 'chb10'
%   path: path to folder containing dataset .edf files and summary.txt
%   FileIndices: indices of files in summary.txt to be labeled, starts at 1
%   EpochLengthSec: length of each epoch in seconds

%% Outputs
%   features_norm: normalised features from input dataset(s)
%   features: unnormalised features from input dataset
%   labels: label for each epoch indicating class (yes/no/incoming seizure)
%   mus, stds: mean and std per feature for normalisation
%% Todo
%   maybe remove features from output?

%% Function start
% function [features_norm,features,labels,featurelabels, mus, stds] = getFeatures(dataset, path2dataset, FileIndices, EpochLengthSec)
%% test vars
    clc; clear;
    eegpath = AddPath();
    dataset = 'chb04';
    path2dataset = eegpath + "sample_data\" + dataset + "\";
    FileIndices = 5;
    EpochLengthSec = 3.25;
%% Get labels of data
disp('Getting labels of data');
tic

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
t = toc;
clear temp;
save('MLModel/CNNmodel.mat', 'Fs', 'EpochLengthSec', '-append');
fprintf("Got labels, took %.3f seconds\n", t);

%% get filtered data
tic;
disp("Loading data...");
filtered_data = LoadData(path2dataset, FileIndices, 'overwrite', 0, 'channellist', channellist, 'rounding_err', rounding_err);
t = toc;
fprintf("Data loaded, took %.3f seconds\n", t);
%% Get features

disp('Getting features...');
tic;

epochs = DivideInEpochs(filtered_data, Fs, EpochLengthSec);
% [features, featurelabels] = FeatExtractFunc(epochs, Fs, EpochLengthSec);
[features, featurelabels] = FeatExtractWavelet(epochs, Fs, EpochLengthSec);

t = toc;
fprintf("Got features, took %.3f seconds\n", t);

%% Normalize features
disp('Normalising features...');
tic;
for k = 1 : size(features, 2) %loop through features
    [temp(:,k), mus(:,k), stds(:,k)] = zscore([features{:,k}]);
    features_norm = num2cell(temp);
end
t = toc;
fprintf("Normalised features, took %.3f seconds\n", t);

%% Normalizes EEG data and adds it to features, TODO
if 0 && EegFeature %remove '0 &&' when finished
    for k = 1 : size(filtered_data, 1) %loop through channels
        filtered_data(:,k) = zscore(filtered_data(:,k));
    end
end

% end

