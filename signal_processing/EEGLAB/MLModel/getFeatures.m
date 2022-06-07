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
%function [features,labels,featurelabels] = getFeatures(dataset, path2dataset, FileIndices, EpochLengthSec)
 %function [features_norm,features,labels,featurelabels, mus, stds] = getFeatures(dataset, path2dataset, FileIndices, EpochLengthSec)
function [featuresWavelet,features,labels,featurelabels,featurelabelsWavelet] = getFeatures()
% test vars
    clc; clear;
    eegpath = AddPath();
    dataset = 'chb08';
    path2dataset = eegpath + "sample_data\" + dataset + "\";
    FileIndices = SeizFileIndices(dataset);
    EpochLengthSec = 3;
%% Get labels of data
disp('Getting labels of data');
t = tic;

fac_downsample = 2; %downsa5mpling factor
summarypath = path2dataset + dataset + "-summary.txt";
[Fs, labels1, channellist, rounding_err] = Label_extract2(summarypath, EpochLengthSec, FileIndices, fac_downsample); %get labels of where there are seizures
channellist = channellist.index;
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

clear temp;
%save('MLModel/CNNmodel.mat', 'Fs', 'EpochLengthSec', '-append');
fprintf("Got labels, took %.3f seconds", toc(t));

%% get filtered data
t = tic;
disp("Loading data...");

filtered_data = LoadData(path2dataset, FileIndices, 'overwrite', 1,...
    'channellist', channellist, 'rounding_err', rounding_err, 'ASR', 0, 'downsample', fac_downsample);
t = toc(t);
fprintf("Data loaded, took %.3f seconds\n", t);
%% Get features

disp('Getting features...');
t = tic;

epochs = DivideInEpochs(filtered_data, Fs, EpochLengthSec);
 [features, featurelabels] = FeatExtractFunc(epochs, Fs, EpochLengthSec);
[featuresWavelet, featurelabelsWavelet] = FeatExtractWavelet(epochs,Fs,EpochLengthSec);


t = toc(t);
fprintf("Got features, took %.3f seconds\n", t);

%% Normalize features
% disp('Normalising features...');
% t = tic;
% 
% matfeat = cell2mat(features);
% idx = isnan(matfeat);
% NaNrows = unique(rem(find(idx==1),length(features)));
% NaNrows(NaNrows == 0) = length(features); %fix bottom column
% matfeat(NaNrows,:) = NaN;
% for k = NaNrows'
%     matfeat(k, :) = mean(matfeat,'omitnan');
% end
% 
% % makes wrong measurements means
% for k = 1:size(matfeat, 2)
%     i = isnan(matfeat(:,k));
%     j = ~i;
%     matfeat(i, k) = mean(matfeat(j,k), 'omitnan');
% end
% 
% [temp, mus, stds] = zscore(matfeat);
% features_norm = num2cell(temp);
% 
% t = toc(t);
% fprintf("Normalised features, took %.3f seconds\n", t);

%% Normalizes EEG data and adds it to features, TODO

features = cell2mat(features);
featuresWavelet=cell2mat(featuresWavelet);
%features_norm = cell2mat(features_norm);
%end

