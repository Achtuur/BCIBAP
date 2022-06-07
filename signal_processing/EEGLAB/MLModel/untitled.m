%% please give this file a name

clc; clear;
eegpath = AddPath();
dataset = 'chb04';
path2dataset = eegpath + "sample_data\" + dataset + "\";
FileIndices = 5;
EpochLengthSec = 3;
% %% Get labels of data
% disp('Getting labels of data');
% t = tic;
% 
fac_downsample = 2; %downsa5mpling factor
summarypath = path2dataset + dataset + "-summary.txt";
[Fs, labels1, channellist, rounding_err] = Label_extract2(summarypath, EpochLengthSec, FileIndices, fac_downsample); %get labels of where there are seizures
channellist = channellist.index;
% temp = [];
% for k = 1 : size(labels1, 1) %loop through rows of labels
%     labelarr = labels1{k, 2};
%     labelarr = labelarr(:); %force column vector
%     temp = [temp; labelarr]; %make labels 1 long column vector where every row is an epoch
% end
% labels = temp + 1; % +1 so that labels are '1' and '2' for no seizure / seizure respectively
% if isempty(find(labels == 2, 1))
%    error("Input data contains no seizures"); 
% end
% 
% clear temp;
% save('MLModel/CNNmodel.mat', 'Fs', 'EpochLengthSec', '-append');
% fprintf("Got labels, took %.3f seconds", toc(t));

%% get filtered data
t = tic;
disp("Loading data...");
filtered_data = LoadData(path2dataset, FileIndices, 'overwrite', 1,...
    'channellist', channellist, 'rounding_err', rounding_err, 'ASR', 0, 'downsample', fac_downsample);
t = toc(t);
fprintf("Data loaded, took %.3f seconds\n", t);
%% Get features

disp('Getting features...');

epochs = DivideInEpochs(filtered_data, Fs, EpochLengthSec);
epochsmatrix=cell2mat(epochs);
seizureepochs= zeros(147,384);
nonseizureepochs=zeros(147,384);
j=1;
for i=2602:2749 
    seizureepochs1(j,:)=epochsmatrix(i,:);
    seizureepochs2(j,:)=epochsmatrix(i+3178,:);
    seizureepochs3(j,:)=epochsmatrix(i+2*3178,:);
    seizureepochs4(j,:)=epochsmatrix(i+3*3178,:);
    seizureepochs5(j,:)=epochsmatrix(i+4*3178,:);
    seizureepochs6(j,:)=epochsmatrix(i+5*3178,:);
    seizureepochs7(j,:)=epochsmatrix(i+6*3178,:);
    seizureepochs8(j,:)=epochsmatrix(i+7*3178,:);
    seizureepochs9(j,:)=epochsmatrix(i+8*3178,:);
    j=j+1;
end
seizureepochs=[seizureepochs1;seizureepochs2;seizureepochs3;seizureepochs4;seizureepochs5;seizureepochs6;seizureepochs7;seizureepochs8;seizureepochs9];
j=1;
for i=2:150
    nonseizureepochs1(j,:)=epochsmatrix(i,:);
    nonseizureepochs2(j,:)=epochsmatrix(i+3178,:);
    nonseizureepochs3(j,:)=epochsmatrix(i+2*3178,:);
    nonseizureepochs4(j,:)=epochsmatrix(i+3*3178,:);
    nonseizureepochs5(j,:)=epochsmatrix(i+4*3178,:);
    nonseizureepochs6(j,:)=epochsmatrix(i+5*3178,:);
    nonseizureepochs7(j,:)=epochsmatrix(i+6*3178,:);
    nonseizureepochs8(j,:)=epochsmatrix(i+7*3178,:);
    nonseizureepochs9(j,:)=epochsmatrix(i+8*3178,:);
    j=j+1;
end
nonseizureepochs=[nonseizureepochs1;nonseizureepochs2;nonseizureepochs3;nonseizureepochs4;nonseizureepochs5;nonseizureepochs6;nonseizureepochs7;nonseizureepochs8;nonseizureepochs9];
totalepochs=[seizureepochs;nonseizureepochs];
% [features, featurelabels] = FeatExtractFunc(epochs, Fs, EpochLengthSec);
%[features, featurelabels] = FeatExtractWavelet([seizureepochs;nonseizureepochs], Fs, EpochLengthSec);
%%
nEpochs=2673;

meanDeltaEpochs = zeros(nEpochs, 1);
    meanThetaEpochs = zeros(nEpochs, 1);
    meanAlphaEpochs = zeros(nEpochs, 1);
    meanBetaEpochs = zeros(nEpochs, 1);
    meanAbsDeltaEpochs = zeros(nEpochs, 1);
    meanAbsThetaEpochs = zeros(nEpochs, 1);
    meanAbsAlphaEpochs = zeros(nEpochs, 1);
    meanAbsBetaEpochs = zeros(nEpochs, 1);
    stdDeltaEpochs= zeros(nEpochs, 1);
    stdThetaEpochs = zeros(nEpochs, 1);
    stdAlphaEpochs= zeros(nEpochs, 1);
    stdBetaEpochs= zeros(nEpochs, 1);
    
    energyDeltaEpochs=zeros(nEpochs,1);
    energyThetaEpochs=zeros(nEpochs,1);
    energyAlphaEpochs=zeros(nEpochs,1);
    energyBetaEpochs=zeros(nEpochs,1);
    
    entropyDeltaEpochs= zeros(nEpochs, 1);
    entropyThetaEpochs =zeros(nEpochs, 1);
    entropyAlphaEpochs= zeros(nEpochs, 1);
    entropyBetaEpochs= zeros(nEpochs, 1);
    
    powerDeltaEpochs= zeros(nEpochs, 1);
    powerThetaEpochs = zeros(nEpochs, 1);
    powerAlphaEpochs= zeros(nEpochs, 1);
    powerBetaEpochs= zeros(nEpochs, 1);
    
    skewnessDeltaEpochs=zeros(nEpochs, 1);
    skewnessThetaEpochs=zeros(nEpochs, 1);
    skewnessAlphaEpochs=zeros(nEpochs, 1);
    skewnessBetaEpochs=zeros(nEpochs, 1);
    
    kurtosisDeltaEpochs=zeros(nEpochs, 1);
    kurtosisThetaEpochs=zeros(nEpochs, 1);
    kurtosisAlphaEpochs=zeros(nEpochs, 1);
    kurtosisBetaEpochs=zeros(nEpochs, 1);
    
    varDeltaEpochs=zeros(nEpochs, 1);
    varThetaEpochs=zeros(nEpochs, 1);
    varAlphaEpochs=zeros(nEpochs, 1);
    varBetaEpochs=zeros(nEpochs, 1);


for i = 1:nEpochs
  
    [c,l]=wavedec(totalepochs(i,:),4,'db4'); %second argument is level of decomposition and 3rd is vanishing level
    a4= appcoef(c,l,'db4');
    [d1,d2,d3,d4]=detcoef(c,l,[1 2 3 4]);
   
    meanDeltaEpochs(i,1)= mean(a4) ;
    meanThetaEpochs(i,1) = mean(d4);
    meanAlphaEpochs(i,1) = mean(d3);
    meanBetaEpochs(i,1) = mean(d2);

    meanAbsDeltaEpochs(i,1) = mean(abs(a4)) ;
    meanAbsThetaEpochs(i,1) = mean(abs(d4)) ;
    meanAbsAlphaEpochs(i,1) = mean(abs(d3)) ;
    meanAbsBetaEpochs(i,1) = mean(abs(d2)) ;

    stdDeltaEpochs(i,1)= std(a4);
    stdThetaEpochs(i,1) = std(d4);
    stdAlphaEpochs(i,1)= std(d3);
    stdBetaEpochs(i,1)=std(d2);

    energyDeltaEpochs(i,1)= sum(a4.^2);
    energyThetaEpochs(i,1) = sum(d4.^2);
    energyAlphaEpochs(i,1)= sum(d3.^2);
    energyBetaEpochs(i,1)= sum(d2.^2);
    
    entropyDeltaEpochs(i,1)= approximateEntropy(a4);
    entropyThetaEpochs(i,1) =approximateEntropy(d4);
    entropyAlphaEpochs(i,1)= approximateEntropy(d3);
    entropyBetaEpochs(i,1)= approximateEntropy(d2);
    
    powerDeltaEpochs(i,1)= sum(a4.^2)/length(a4);
    powerThetaEpochs(i,1) = sum(d4.^2)/length(d4);
    powerAlphaEpochs(i,1)= sum(d3.^2)/length(d3);
    powerBetaEpochs(i,1)= sum(d2.^2)/length(d2);
    
    skewnessDeltaEpochs(i,1)= skewness(a4);
    skewnessThetaEpochs(i,1)=skewness(d4);
    skewnessAlphaEpochs(i,1)=skewness(d3);
    skewnessBetaEpochs(i,1)=skewness(d2);
    
    kurtosisDeltaEpochs(i,1)=kurtosis(a4);
    kurtosisThetaEpochs(i,1)=kurtosis(d4);
    kurtosisAlphaEpochs(i,1)=kurtosis(d3);
    kurtosisBetaEpochs(i,1)=kurtosis(d2);
    
    varDeltaEpochs(i,1)=var(a4);
    varThetaEpochs(i,1)=var(d4);
    varAlphaEpochs(i,1)=var(d3);
    varBetaEpochs(i,1)=var(d2);   
end 


figure(1)
% 
scatter(energyDeltaEpochs(1:148*9,1),energyAlphaEpochs(1:148*9,1));
% 
figure(2)
scatter(energyDeltaEpochs(148*9:2673,1),energyAlphaEpochs(148*9:2673,1));
    %% label features
    %fprintf('Labelling features from channel %d...\n', k);
    [features, labels] = FeatureLabelsPerEpoch( ...
         varDeltaEpochs, 'VarianceDelta',  varThetaEpochs, 'VarianceTheta',varAlphaEpochs, 'VarianceAlpha', varBetaEpochs, 'VarianceBeta', ...
        kurtosisDeltaEpochs, 'kurtosisDelta', kurtosisThetaEpochs, 'kurtosisTheta', kurtosisAlphaEpochs, 'kurtosisAlpha', kurtosisBetaEpochs, 'kurtosisBeta', ...
        skewnessDeltaEpochs, 'skewnessDelta', skewnessThetaEpochs, 'skewnessTheta', skewnessAlphaEpochs, 'skewnessAlpha', skewnessBetaEpochs, 'skewnessBeta', ...
         powerDeltaEpochs, 'powerDelta',  powerThetaEpochs, 'powerTheta', powerAlphaEpochs, 'powerAlpha',  powerBetaEpochs, 'powerBeta',  ...
       entropyDeltaEpochs, 'entropyDelta', entropyThetaEpochs, 'entropyTheta', entropyAlphaEpochs, 'entropyAlpha',entropyBetaEpochs, 'entropyBeta', ...
        energyDeltaEpochs, 'energyDelta', energyThetaEpochs, 'energyTheta', energyAlphaEpochs, 'energyAlpha',energyBetaEpochs,'energyBeta', ...
        stdDeltaEpochs, 'stdDelta',stdThetaEpochs, 'stdTheta', stdAlphaEpochs, 'stdAlpha',stdBetaEpochs,'stdBeta',...
        meanDeltaEpochs, 'meanDelta',meanThetaEpochs, 'meanTheta', meanAlphaEpochs, 'meanAlpha',meanBetaEpochs,'meanBeta', ...
        meanAbsDeltaEpochs, 'meanAbsDelta', meanAbsThetaEpochs, 'meanAbsTheta', meanAbsAlphaEpochs, 'meanAbsAlpha', meanAbsBetaEpochs,'meanAbsBeta'); ...
    %    epochs, 'epochs');
% [FeatVector] = FeatSelectionPCA(features)  

 %% normalise features
features=cell2mat(features);
features_norm = zscore(features);
features_norm2=normalize(features);
%% pca
[coeff,score,latent,~,explained,mu]= pca(features_norm);
for i=2:35
    if (sum(explained(1:i))<95) %take the principal components with cumulative variance of 95%
        continue;
    else
        FeatVector=coeff(:,1:i)'*features_norm'; 
        break;
    end
end
figure(3)
bar(explained);
%% LDA
%X = [features_norm(1:148*9,:); features_norm(148*9:2)];  Y = [zeros(148*9,36); ones(149*9,36)] ;
%W=LDA(X,Y);

%% mRMR
% figure(4)
% %idx = fscmrmr(features_norm,'1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36') ;
% Y=[ones(148*9,1); ones(149*9,1)*2] ;
% [idx,scores]=fscmrmr(features,Y);
% bar (idx, scores( idx ));
% xlabel ( ' Feature ')
% ylabel ( ' Predictor Score ')