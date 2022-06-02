eegpath = AddPath();
% dataset = 'chb03';
% path2dataset = eegpath + "sample_data\" + dataset + "\";
% FileIndices = SeizFileIndices(dataset);
Plot_CFNMatrix = 1;

epochs = 0.5 : 0.25 : 4;
epochs = 3;
final_results = cell(size(epochs, 2), 2);
i = 1;

datasets = ["03"];
temp = 0;
save(eegpath + "\MLModel\CNNmodel.mat", 'i');
clear temp;
for i = 1:length(datasets)
    dataset = append("chb",datasets(i));
    path2dataset = eegpath + "sample_data\" + dataset + "\";
    FileIndices = SeizFileIndices(dataset);
    [featuresTemp,YTemp,featurelabelsTemp] = getFeatures(dataset, path2dataset, FileIndices, epochs);
    if i == 1
        features = featuresTemp;
        Y = YTemp;
        featurelabels = featurelabelsTemp;
    else
        features = [features; featuresTemp];
        Y = [Y; YTemp];
        featurelabels = [featurelabels; featurelabelsTemp];
    end
end

[X, mu_train, sigma_train] = NormalizeFeat(features);

HyperTune = 0;
HyperEvalNum = 100;
%matfile('MLModel/CNNmodel.mat', 'Writable', true);
for k = epochs

    % [X,features,Y,featurelabels, mu_train, sigma_train] = getFeatures(dataset, path2dataset, FileIndices, k);
    
    %% train model
    %X = cell2mat(X);
    %Y = cell2mat(Y);
    % Train CNN here
    rng("default") % For reproducibility of the partition
    cvp = cvpartition(Y,"Holdout",0.3);
    XTrain = X(training(cvp),:);
    YTrain = Y(training(cvp));
    XTest = X(test(cvp),:);
    YTest = Y(test(cvp));

    if HyperTune
        Mdl = fitcnet(XTrain,YTrain,"OptimizeHyperparameters","auto", ...
        "HyperparameterOptimizationOptions", ...
        struct("AcquisitionFunctionName","expected-improvement-plus", ...
        "MaxObjectiveEvaluations",HyperEvalNum))
    else
        Mdl = fitcnet(XTrain,YTrain,"Layersizes",300,"Activations","none",...
            "Standardize",true,"Lambda",0.00024864);
    end
     final_results(i, :) = {features featurelabels};
    
     if Plot_CFNMatrix
         figure()
         confusionchart(YTest,predict(Mdl,XTest),'RowSummary','row-normalized')
     end
     models{i} = Mdl;
     i = i + 1;
%     fig = plotconfusion(lab, predicted);
%     fig.CurrentAxes.Title.String = sprintf("epochlengthsec = %0.1f", k);
end
model = Mdl;
save('MLModel/CNNmodel.mat', 'model', 'mu_train', 'sigma_train', '-append');
