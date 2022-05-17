function [Ytest_cat,Ytest_pred_cat, savepath] = CreateModel(features, labels, featurelabels)
%% Below follows some shameless copy paste stuff from EPO 4
percent_train_split = 70/100;

[train_id, test_id] = SplitTrainTest(labels, percent_train_split);

Xtrain = cell2mat(features(train_id, :));
Xtest = cell2mat(features(test_id, :));
Ytrain = labels(train_id, :);
Ytest = labels(test_id, :);

[Xtrain,mu_train,sigma_train] = zscore(Xtrain); % normalisation using zscore test
Xtest = (Xtest-mu_train)./sigma_train; %applying same normalisation to test data

% fig = figure(1);
[feature_idx,scores] = fscmrmr(Xtrain,Ytrain); % mRMR feature selection (selects most useful features)
% bar(idx,scores(idx))%Create bar graph
% xlabel('Feature')
% set(gca,'TickLabelInterpreter','latex');
% ylabel('Predictor Score'); hold off;
% xticks(1:1:length(featurelabels));
% xticklabels(featurelabels);

[sortedscores, feature_idx] = sort(scores);
feature_idx = feature_idx(1:8);
size(Xtrain)
Xtrain = Xtrain(:, feature_idx);
Xtest = Xtest(:, feature_idx);

% This makes sure we get the same results every time we run the code.
rng default

% How many trees do you want in the forest? 
nTrees = 100;

% Train the TreeBagger (Random Forest). could use a different model later
model = TreeBagger(nTrees,Xtrain,Ytrain, 'Method', 'classification', 'InBagFraction', 0.5, 'MaxNumSplits',15);

Ytest_pred_str = model.predict(Xtest); %fix this confusion matrix so the variable names make sense later
Ytest_pred = str2double(Ytest_pred_str);
num_classes=length(unique(labels));
Ytest_cat=zeros(num_classes,size(Ytest,1));
Ytest_pred_cat=zeros(num_classes,size(Ytest,1));
size(find(Ytest == 2))

for i=1:num_classes
    Ytest_cat(i, Ytest==i) = 1;
    Ytest_pred_cat(i, Ytest_pred==i) = 1;
end
% figure(2);
% plotconfusion(Ytest_cat,Ytest_pred_cat); hold off;

%% Save model and relevant normalisation constants to ./model.mat

scriptpath = mfilename('fullpath'); %get path to current script
scriptpath = strrep(scriptpath, mfilename, ''); %remove filename to obtain path to folder where script is run
savepath = scriptpath + "model.mat";
save(savepath, 'model', 'mu_train', 'sigma_train', 'feature_idx');
end