function [TotalFeatures,TotalFeatureLabels] = FeatExtractWavelet(EarDataEpochs, Fs, EpochLengthSec)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
%%
disp('Extracting features...');
T = 1/Fs;             % Sampling period 
L = Fs*EpochLengthSec;
nEpochs = size(EarDataEpochs{1,1}, 1); % get amount of epochs (assume all entries in eardataepochs have same number of epochs)
nChannels = size(EarDataEpochs, 1);

%% Discrete Wavelet Transform (DWT)
% figure(1)
% [c,l]=wavedec(epoch1,5,'db4'); %second argument is level of decomposition and 3rd is vanishing level
% a5= appcoef(c,l,'db4');
% [d1,d2,d3,d4,d5]=detcoef(c,l,[1 2 3 4 5]);
% subplot(6, 1, 1)
% plot(a5);
% title('Approximation at Level 5') %0-4Hz
% subplot(6, 1, 2)
% plot(d1)
% title('Detail Coefficients at Level 1');%64-128Hz
% subplot(6, 1, 3)
% plot(d2)
% title('Detail Coefficients at Level 2');%32-64Hz
% subplot(6, 1, 4)
% plot(d3)
% title('Detail Coefficients at Level 3');%16-32Hz
% subplot(6, 1, 5)
% plot(d4)
% title('Detail Coefficients at Level 4');%8-16Hz
% subplot(6, 1, 6)
% plot(d5)
% title('Detail Coefficients at Level 5'); %4-8Hz
% 
% meanDelta= mean(a5); meanTheta = mean(d5); meanAlpha= mean(d4); meanBeta= mean(d3);
% 
% stdDelta= std(a5); stdTheta = std(d5); stdAlpha= std(d4); stdBeta= std(d3);
% 
% energyDelta= sum(a5.^2); energyTheta = sum(d5.^2); energyAlpha= sum(d4.^2); energyBeta= sum(d3.^2);
% 
% entropyDelta= approximateEntropy(a5);
% entropyTheta = approximateEntropy(d5);
% entropyAlpha= approximateEntropy(d4);
% entropyBeta= approximateEntropy(d3);
% 
% skewnessDelta=skewness(a5);skewnessTheta=skewness(d5);skewnessAlpha=skewness(d4);skewnessBeta=skewness(d3);
% 
% kurtosisDelta=kurtosis(a5);kurtosisTheta=kurtosis(d5);kurtosisAlpha=kurtosis(d4);kurtosisBeta=kurtosis(d3);


%% Discrete Wavelet Packet Transform
TotalFeatures = {};
TotalFeatureLabels = '';
for k = 1:nChannels
    fprintf('Extracting from channel %d...\n', k);
%initialize matrices 
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
    
    energyDeltaEpochs= zeros(nEpochs, 1);
    energyThetaEpochs = zeros(nEpochs, 1);
    energyAlphaEpochs= zeros(nEpochs, 1);
    energyBetaEpochs= zeros(nEpochs, 1);
    
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

    for i = 1:nEpochs %loop through epochs of current channel
        CurChannelEpochs = EarDataEpochs{k,1};
        wpt = wpdec(CurChannelEpochs(i,:)',5,'db4','shannon');
        %plot(wpt)

        signaldelta=read(wpt,'cfs',31);
        signaltheta=read(wpt,'cfs',32);
        signalalpha=read(wpt,'cfs',33);
        signalbeta=read(wpt,'cfs',34)+read(wpt,'cfs',35)+read(wpt,'cfs',36)+read(wpt,'cfs',37)+read(wpt,'cfs',38);

        meanDeltaEpochs(i,1)= mean(signaldelta);
        meanThetaEpochs(i,1) = mean(signaltheta);
        meanAlphaEpochs(i,1) = mean(signalalpha);
        meanBetaEpochs(i,1) = mean(signalbeta);

        meanAbsDeltaEpochs(i,1) = mean(abs(signaldelta));
        meanAbsThetaEpochs(i,1) = mean(abs(signaltheta));
        meanAbsAlphaEpochs(i,1) = mean(abs(signalalpha));
        meanAbsBetaEpochs(i,1) = mean(abs(signalbeta));

        stdDeltaEpochs(i,1)= std(signaldelta);
        stdThetaEpochs(i,1) = std(signaltheta);
        stdAlphaEpochs(i,1)= std(signalalpha);
        stdBetaEpochs(i,1)= std(signalbeta);

        energyDeltaEpochs(i,1)= sum(signaldelta.^2);
        energyThetaEpochs(i,1) = sum(signaltheta.^2);
        energyAlphaEpochs(i,1)= sum(signalalpha.^2);
        energyBetaEpochs(i,1)= sum(signalbeta.^2);

        entropyDeltaEpochs(i,1)= approximateEntropy(signaldelta);
        entropyThetaEpochs(i,1) = approximateEntropy(signaltheta);
        entropyAlphaEpochs(i,1)= approximateEntropy(signalalpha);
        entropyBetaEpochs(i,1)= approximateEntropy(signalbeta);

        powerDeltaEpochs(i,1)= sum(signaldelta.^2)/length(signaldelta);
        powerThetaEpochs(i,1) = sum(signaltheta.^2)/length(signaltheta);
        powerAlphaEpochs(i,1)= sum(signalalpha.^2)/length(signalalpha);
        powerBetaEpochs(i,1)= sum(signalbeta.^2)/length(signalbeta);

        skewnessDeltaEpochs(i,1)= skewness(signaldelta);
        skewnessThetaEpochs(i,1)= skewness(signaltheta);
        skewnessAlphaEpochs(i,1)= skewness(signalalpha);
        skewnessBetaEpochs(i,1)= skewness(signalbeta);

        kurtosisDeltaEpochs(i,1)= kurtosis(signaldelta);
        kurtosisThetaEpochs(i,1)= kurtosis(signaltheta);
        kurtosisAlphaEpochs(i,1)= kurtosis(signalalpha);
        kurtosisBetaEpochs(i,1)= kurtosis(signalbeta);

        varDeltaEpochs(i,1)= var(signaldelta);
        varThetaEpochs(i,1)= var(signaltheta);
        varAlphaEpochs(i,1)= var(signalalpha);
        varBetaEpochs(i,1)= var(signalbeta);
    end 
    
    %% label features
    
    fprintf('Labelling features from channel %d...\n', k);
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
     [TotalFeatures, TotalFeatureLabels] = CombineFeatureLabels(TotalFeatures, TotalFeatureLabels, features, labels); 
end
disp('Done extracting features');
end