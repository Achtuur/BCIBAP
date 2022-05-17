eegpath = AddPath();
dataset = 'chb03';
path2dataset = eegpath + "sample_data\" + dataset + "\";
FileIndices = [1:6];
Plot_CFNMatrix = 0;

epochs = 0.5 : 0.25 : 4;
final_results = cell(size(epochs, 2), 2);
i = 1;

for k = epochs

    [X,features,Y,featurelabels] = CNN(dataset, path2dataset, FileIndices, k);
    X = cell2mat(X);
    %Y = cell2mat(Y);
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
    
     if Plot_CFNMatrix
         figure(i)
         confusionchart(YTest,predict(Mdl,XTest),'Normalization','row-normalized')
     end
     models{i} = Mdl;
     i = i + 1;
%     fig = plotconfusion(lab, predicted);
%     fig.CurrentAxes.Title.String = sprintf("epochlengthsec = %0.1f", k);
%     plt.Title = sprintf("epochlengthsec = %s", k);
%     title(fig.axes, sprintf("epochlengthsec = %s", k));
end