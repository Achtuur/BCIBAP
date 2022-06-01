%% Get seizures from file and test prediction

% function TestFileSeizures(dataset, path2dataset, FileIndices, path2model)
%% test vars
    dataset = 'chb04';
    eegpath = AddPath();
    path2dataset = eegpath + "\sample_data\" + dataset + "\";
    FileIndices = [5];
    path2model = eegpath + "\MLModel\CNNmodel.mat";

%% get labels
EpochLengthSec = load(path2model, 'EpochLengthSec').EpochLengthSec;
summarypath = path2dataset + dataset + "-summary.txt";
[Fs, labels, channellist, rounding_err] = Label_extract2(summarypath, EpochLengthSec, FileIndices); %get labels of where there are seizures
channellist = channellist.index;
temp = [];
for k = 1 : size(labels, 1) %loop through rows of labels
    labelarr = labels{k, 2};
    labelarr = labelarr(:); %force column vector
    temp = [temp; labelarr]; %make labels 1 long column vector where every row is an epoch
end
labels = temp + 1; % +1 so that labels are '1' and '2' for no seizure / seizure respectively

SeizureEpochs = find(labels == 2); %indices of epochs with seizure
if length(SeizureEpochs) == 0
   error('No seizures detected in selected file(s)'); 
end

%% get filtered data
filtered_data = LoadData(path2dataset, FileIndices, 'overwrite', 1, 'channellist', channellist, 'rounding_err', rounding_err, 'ASR', 1);
epochs = DivideInEpochs(filtered_data, Fs, EpochLengthSec);
for k = 1:size(epochs,1) %only take epochs with seizures
    temp = epochs{k,1};
    epochs(k,1) = {temp(SeizureEpochs,:)};
end
% epochs = epochs(SeizureEpochs, :);
[feat, ~] = FeatExtractWavelet(epochs, Fs, EpochLengthSec);


%% Classify
disp('Classifying data...');
outputclass = Classify(path2model, cell2mat(feat)); %classify all epochs
TN = length(find(outputclass == 2));
FP = length(find(outputclass ~= 2));
sensitivity = TN/(TN+FP);

disp("Done classifying");
disp("TN: " + TN + ", FP: " + FP);
disp("Sensitivity = " + 100 * sensitivity + "%");
% end