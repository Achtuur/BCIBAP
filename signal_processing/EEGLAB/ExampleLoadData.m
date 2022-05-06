
%Example of how to use LoadnFilter to get filtered data from an .edf file

addpath('./SPgroupfunc') %this folder should be in your EEGLAB folder as it contains the functions
path2edf = './sample_data/chb01_01.edf'; %path to .edf file
% filtered_data = LoadnFilter(path2edf, 'locutoff', 0.5, 'hicutoff', 30, 'showplots', 1); %call function and voila

epochs = 15;

feat1 = rand(epochs, 1); % per epoch 1 random value as example feature
feat2 = rand(epochs, 5); % per epoch 5 random values as example feature
feat3 = rand(3, epochs); % epochs are in columns instead of rows, function will attempt to fix this by transposing but results may not be expected

%use function with data/name pairs as below
[features, labels] = FeatureLabelsPerEpoch(feat1, 'feature 1', feat2, 'feature number 2', feat3, 'third feature');

%features now contains cell per epoch of features, labels contains the names