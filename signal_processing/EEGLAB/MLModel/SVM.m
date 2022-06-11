%% Train Support Vector Machine

%% Important variables
%  epochs: decides epoch length
%  numFolds: decides amount of folds in cross validation
%  datasets: hold array of the datasets to be trained on
%  



close all;

eegpath = AddPath();

Plot_CFNMatrix = 0;
Waveleton = 1;
epochlength = 3;
final_results = cell(size(epochlength, 2), 2);
i = 1;
numFolds = 10;
% "01" "03" "04" "05" "06" "07" "08" "09" "10"

datasets = ["01" "03" "04" "05" "06" "07" "08" "09" "10"];
temp = 0;
save(eegpath + "\MLModel\SVMmodel.mat", 'temp');
clear temp;
components = zeros(length(datasets),1);
for i = 1:length(datasets)
    dataset = append("chb",datasets(i));
    path2dataset = eegpath + "sample_data\" + dataset + "\";
    FileIndices = SeizFileIndices(dataset);
    [featuresTemp,featurelabelsTemp,YTemp] = getFeatures(dataset, path2dataset, FileIndices, epochlength, Waveleton);
    featuresTemp = NormalizeFeat(featuresTemp);
%     if i ~= 1
%         features = [features; featuresTemp];
%         Y = [Y; YTemp];
%         featurelabels = [featurelabels; featurelabelsTemp];
%     else
    %[features,components(i),coeff,latent] = FeatSelectionPCA(featuresTemp,99);
    features = featuresTemp;
    Y = YTemp;
    featurelabels = featurelabelsTemp;
%     end
% end

X = featuresTemp;

HyperTune = 0;
HyperEvalNum = 50;
%matfile('MLModel/CNNmodel.mat', 'Writable', true);
%for k = epochs

    
    %% train model
    % Train CNN here
    rng("default") % For reproducibility of the partition and other random decisions such as training
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
          Mdl = fitcsvm(X(cvp.training(j),:),Y(cvp.training(j)),"KernelFunction","rbf","KernelScale",0.0177,...
            "Standardize",true,"BoxConstraint",0.001);
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
     %final_results(i, :) = {features featurelabels};
end


disp("Accuracy is "+  averageacc + "%")
disp("Sensitivity is "+ averagesens + "%")
model = Mdl;
disp("accmean is "+ mean(averageacc))
disp("sensmean is "+ mean(averagesens))
save('MLModel/CNNmodel.mat', 'model', '-append');
