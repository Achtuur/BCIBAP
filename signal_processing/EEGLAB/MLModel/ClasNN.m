eegpath = AddPath();
dataset = 'chb03';
path2dataset = eegpath + "sample_data\" + dataset + "\";
FileIndices = [1:6];
Plot_CFNMatrix = 1;

epochs = 0.5 : 0.25 : 4;
epochs = 3;
final_results = cell(size(epochs, 2), 2);
i = 1;

matfile('MLModel/CNNmodel.mat', 'Writable', true);
for k = epochs

    [X,features,Y,featurelabels, mu_train, sigma_train] = getFeatures(dataset, path2dataset, FileIndices, k);
    %% train model
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
    "LayerSizes",[55 30]);

     final_results(i, :) = {features featurelabels};
    
     if Plot_CFNMatrix
         figure(i)
         confusionchart(YTest,predict(Mdl,XTest),'Normalization','row-normalized')
     end
     models{i} = Mdl;
     i = i + 1;
%     fig = plotconfusion(lab, predicted);
%     fig.CurrentAxes.Title.String = sprintf("epochlengthsec = %0.1f", k);
end
model = Mdl;
save('MLModel/CNNmodel.mat', 'model', 'mu_train', 'sigma_train', '-append');
