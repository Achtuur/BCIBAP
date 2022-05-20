eegpath = AddPath();
dataset = 'chb03';
path2dataset = eegpath + "sample_data\" + dataset + "\";
FileIndices = [1:6];

% epochs = 0.5 : 0.25 : 4;
epochs = 2.75;
final_results = cell(size(epochs, 2), 2);
i = 1;
for k = epochs
    [X,features,Y,featurelabels] = CNN(dataset, path2dataset, FileIndices, k);
    X = cell2mat(X);
    %Y = cell2mat(Y);
    % Train CNN here
    rng("default") % For reproducibility of the partition
    cvp = cvpartition(Y,"Holdout",0.3);
    Xtrain = X(training(cvp),:);
    Ytrain = Y(training(cvp));
    Xtest = X(test(cvp),:);
    Ytest = Y(test(cvp));
    
    [feature_idx,scores] = fscmrmr(Xtrain,Ytrain); % mRMR feature selection (selects most useful features)
    [sortedscores, feature_idx] = sort(scores);
    feature_idx = feature_idx(1:8);
    size(Xtrain)
    Xtrain = Xtrain(:, feature_idx);
    Xtest = Xtest(:, feature_idx);
    
    nTrees = 100;

    % Train the TreeBagger (Random Forest). could use a different model later
    model = TreeBagger(nTrees,Xtrain,Ytrain, 'Method', 'classification', 'InBagFraction', 0.5, 'MaxNumSplits',15);

    Ytest_pred_str = model.predict(Xtest); %fix this confusion matrix so the variable names make sense later
    Ytest_pred = str2double(Ytest_pred_str);
    num_classes=length(unique(Ytest));
    Ytest_cat=zeros(num_classes,size(Ytest,1));
    Ytest_pred_cat=zeros(num_classes,size(Ytest,1));
    size(find(Ytest == 2))

    for i=1:num_classes
        Ytest_cat(i, Ytest==i) = 1;
        Ytest_pred_cat(i, Ytest_pred==i) = 1;
    end

%     figure(i)
%     i = i + 1;
%     fig = plotconfusion(lab, predicted);
%     fig.CurrentAxes.Title.String = sprintf("epochlengthsec = %0.1f", k);
%     plt.Title = sprintf("epochlengthsec = %s", k);
%     title(fig.axes, sprintf("epochlengthsec = %s", k));
end
