eegpath = AddPath();
dataset = 'chb03';
path2dataset = eegpath + "sample_data\" + dataset + "\";
FileIndices = [1:6];

epochs = 0.5 : 0.25 : 4;
final_results = cell(size(epochs, 2), 2);
i = 1;
for k = epochs

    [X,features,Y,featurelabels] = CNN(dataset, path2dataset, FileIndices, k);
    
    % Train CNN here
    rng("default") % For reproducibility of the partition
    cvp = cvpartition(Y,"Holdout",0.3);
    XTrain = X(training(cvp),:);
    YTrain = Y(training(cvp));
    XTest = X(test(cvp),:);
    YTest = Y(test(cvp));

    Mdl = fitcnet(XTrain,YTrain, ...
    "LayerSizes",[35 20]);

    
     final_results(i, :) = {features featurelabels};
    
     figure(i)
     confusionchart(YTest.Rating,predict(Mdl,Ytest))
     i = i + 1;
%     fig = plotconfusion(lab, predicted);
%     fig.CurrentAxes.Title.String = sprintf("epochlengthsec = %0.1f", k);
%     plt.Title = sprintf("epochlengthsec = %s", k);
%     title(fig.axes, sprintf("epochlengthsec = %s", k));
end