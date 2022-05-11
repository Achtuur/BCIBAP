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
function TrainModel(dataset, path, nFiles)
%% test vars
% dataset = 'chb04';
% path = "C:\Users\Arthur\Desktop\Programming\BCIBAP\signal_processing\EEGLAB\sample_data\" + dataset + "\";
% nFiles = 5;
%% get filtered data

filtered_data = LoadData(path, nFiles);

%% Get labels of data
EpochLengthSec = 3;
summarypath = path + dataset + "-summary.txt";
[Fs, labels] = Label_extract2(summarypath, EpochLengthSec, nFiles); %get labels of where there are seizures

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

disp('Extracting features...');
[features, featurelabels] = FeatExtractFunc(filtered_data(1,:), Fs, EpochLengthSec);
disp('Done extracting features!');

%% Below follows some shameless copy paste stuff from EPO 4
percent_train_split = 70/100;

[train_id, test_id] = SplitTrainTest(labels, percent_train_split);

Xtrain = cell2mat(features(train_id, :));
Xtest = cell2mat(features(test_id, :));
Ytrain = labels(train_id, :);
Ytest = labels(test_id, :);

[Xtrain,mu_train,sigma_train] = zscore(Xtrain); % normalisation using zscore test
Xtest = (Xtest-mu_train)./sigma_train; %applying same normalisation to test data

fig = figure(1);
[idx,scores] = fscmrmr(Xtrain,Ytrain); % mRMR feature selection (selects most useful features)
bar(idx,scores(idx))%Create bar graph
xlabel('Feature')
set(gca,'TickLabelInterpreter','latex');
ylabel('Predictor Score'); hold off;
xticklabels(featurelabels);

% This makes sure we get the same results every time we run the code.
rng default

% How many trees do you want in the forest? 
nTrees = 100;

% Train the TreeBagger (Random Forest). could use a different model later
model = TreeBagger(nTrees,Xtrain,Ytrain, 'Method', 'classification','InBagFraction',0.5,'MaxNumSplits',15);

Ytest_pred_str = model.predict(Xtest); %fix this confusion matrix so the variable names make sense later
Ytest_pred = str2double(Ytest_pred_str);
num_classes=length(unique(labels));
Ytest_cat=zeros(num_classes,size(Ytest,1));
Ytest_pred_cat=zeros(num_classes,size(Ytest,1));

for i=1:num_classes
    Ytest_cat(i, Ytest==i) = 1;
    Ytest_pred_cat(i, Ytest_pred==i) = 1;
end
figure(2);
plotconfusion(Ytest_cat,Ytest_pred_cat); hold off;

%% Save model and relevant normalisation constants to ./model.mat

scriptpath = mfilename('fullpath'); %get path to current script
scriptpath = strrep(scriptpath, mfilename, ''); %remove filename to obtain path to folder where script is run
savepath = scriptpath + "model.mat";
save(savepath, 'model', 'mu_train', 'sigma_train');

end