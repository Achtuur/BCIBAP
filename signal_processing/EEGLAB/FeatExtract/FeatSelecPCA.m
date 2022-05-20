%% test vars
clc; clear;
eegpath = AddPath();
dataset = 'chb04';
path2dataset = eegpath + "sample_data\" + dataset + "\";
FileIndices = 5;
EpochLengthSec = 3;
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
[features, featurelabels] = FeatExtractWavelet(epochs, Fs, EpochLengthSec);
feature_out = features;

%% normalise features
%for k = 1 : size(features, 2) %loop through features
%    [temp(:,k), mus(:,k), stds(:,k)] = zscore([features{:,k}]);
%   features_norm = num2cell(temp);
%end
%features_norm=cell2mat(features_norm);
feature_out=cell2mat(feature_out);
features_norm = zscore(feature_out);

%% pca
[coeff,score,latent,~,explained,mu]= pca(features_norm);
FeatVector=coeff(:,1:18)'*features_norm'; %take first 18 principal components since they account for 95%variance


