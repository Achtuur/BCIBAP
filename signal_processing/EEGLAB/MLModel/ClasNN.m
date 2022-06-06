close all;
eegpath = AddPath();
% dataset = 'chb03';
% path2dataset = eegpath + "sample_data\" + dataset + "\";
% FileIndices = SeizFileIndices(dataset);
Plot_CFNMatrix = 1;

epochs = 0.5 : 0.25 : 4;
epochs = 3;
final_results = cell(size(epochs, 2), 2);
i = 1;
numFolds = 10;
% "04" "05" "06" "07" "08" "09" "10"

datasets = ["01" "03" "04" "05" "06" "07" "08" "09" "10"];
temp = 0;
save(eegpath + "\MLModel\CNNmodel.mat", 'temp');
clear temp;
for i = 1:length(datasets)
    dataset = append("chb",datasets(i));
    path2dataset = eegpath + "sample_data\" + dataset + "\";
    FileIndices = SeizFileIndices(dataset);
    [featuresTemp,YTemp,featurelabelsTemp, epochsTemp] = getFeatures(dataset, path2dataset, FileIndices, epochs);
    featuresTemp = NormalizeFeat(featuresTemp);
%     if i ~= 1
%         features = [features; featuresTemp];
%         Y = [Y; YTemp];
%         featurelabels = [featurelabels; featurelabelsTemp];
%         epochdata = [epochdata; epochsTemp];
%     else
    features = FeatSelectionPCA(featuresTemp,95);
    Y = YTemp;
    featurelabels = featurelabelsTemp;
    epochdata = epochsTemp;
%     end
% end

X = features;

HyperTune = 0;
HyperEvalNum = 50;
%matfile('MLModel/CNNmodel.mat', 'Writable', true);
%for k = epochs

    % [X,features,Y,featurelabels, mu_train, sigma_train] = getFeatures(dataset, path2dataset, FileIndices, k);
    
    %% train model
    %X = cell2mat(X);
    %Y = cell2mat(Y);
    % Train CNN here
    rng("default") % For reproducibility of the partition
    idx = find(Y == 2);
    rows = randperm(length(X),length(idx)*4);
    rows = sort(unique([idx;rows']));
    Xfifty = X(rows,:);
    Yfifty = Y(rows,:);
%     cvp = cvpartition(Yfifty,"Holdout",0.1);
%     XTrain = Xfifty(training(cvp),:);
%     YTrain = Yfifty(training(cvp));
%     XTest = Xfifty(test(cvp),:);
%     YTest = Yfifty(test(cvp));
    cvp = cvpartition(Y,"KFold",numFolds);
%     XTrain = X(training(cvp),:);
%     YTrain = Y(training(cvp));
%     XTest = X(test(cvp),:);
%     YTest = Y(test(cvp));
acclist = zeros(numFolds,1);
senslist = zeros(numFolds,1);
TPlist = zeros(numFolds,1);
TNlist = zeros(numFolds,1);
FPlist = zeros(numFolds,1);
FNlist = zeros(numFolds,1);
    if HyperTune
        Mdl = fitcsvm(XTrain,YTrain,"OptimizeHyperparameters","auto", ...
        "HyperparameterOptimizationOptions", ...
        struct("AcquisitionFunctionName","expected-improvement-plus", ...
        "MaxObjectiveEvaluations",HyperEvalNum))
    else
        for j = 1:numFolds
        Mdl = fitcnet(X(cvp.training(j),:),Y(cvp.training(j)),"Layersizes",300,"Activations","none",...
            "Standardize",true,"Lambda",9.7118e-05);
%           Mdl = fitcsvm(XTrain,YTrain,"KernelFunction","rbf","KernelScale",3.4575,...
%             "Standardize",true,"BoxConstraint",211.68);
            figure()
            predictions = predict(Mdl,X(cvp.test(j),:));
            cm = confusionchart(Y(cvp.test(j)),predictions,'RowSummary','row-normalized');
            TPlist(j) = cm.NormalizedValues(2,2);
            TNlist(j) = cm.NormalizedValues(1,1);
            FPlist(j) = cm.NormalizedValues(1,2);
            FNlist(j) = cm.NormalizedValues(2,1);
            acclist(j) = (TPlist(j)+TNlist(j))/(TPlist(j)+TNlist(j)+FPlist(j)+FNlist(j))*100;
            senslist(j) = TPlist(j)/(TPlist(j)+FNlist(j))*100;
        end
    end
    
    %acclist = acclist(:,1);
    averageacc(i) = sum(acclist)/numFolds;
    
    %senslist = senslist(:,1);
    averagesens(i) = sum(senslist)/numFolds;
     final_results(i, :) = {features featurelabels};
end    
     if Plot_CFNMatrix
         %figure()
         %confusionchart(YTest,predict(Mdl,XTest),'RowSummary','row-normalized')
     end
     models{i} = Mdl;
     i = i + 1;
%     fig = plotconfusion(lab, predicted);
%     fig.CurrentAxes.Title.String = sprintf("epochlengthsec = %0.1f", k);

disp("Accuracy is "+  averageacc + "%")
disp("Sensitivity is "+ averagesens + "%")
model = Mdl;
save('MLModel/CNNmodel.mat', 'model', '-append');
