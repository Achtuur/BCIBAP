function [features,labels] = FeatExtractWavelet(EarDataEpochs, Fs, EpochLengthSec)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
%%
disp('Extracting features...');
T = 1/Fs;             % Sampling period 
L = Fs*EpochLengthSec;

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
%initialize matrices 
    meanDeltaEpochs = zeros(size(EarDataEpochs, 1), 1);
    meanThetaEpochs = zeros(size(EarDataEpochs, 1), 1);
    meanAlphaEpochs = zeros(size(EarDataEpochs, 1), 1);
    meanBetaEpochs = zeros(size(EarDataEpochs, 1), 1);
    meanAbsDeltaEpochs = zeros(size(EarDataEpochs, 1), 1);
    meanAbsThetaEpochs = zeros(size(EarDataEpochs, 1), 1);
    meanAbsAlphaEpochs = zeros(size(EarDataEpochs, 1), 1);
    meanAbsBetaEpochs = zeros(size(EarDataEpochs, 1), 1);
    stdDeltaEpochs= zeros(size(EarDataEpochs, 1), 1);
    stdThetaEpochs = zeros(size(EarDataEpochs, 1), 1);
    stdAlphaEpochs= zeros(size(EarDataEpochs, 1), 1);
    stdBetaEpochs= zeros(size(EarDataEpochs, 1), 1);
    
    energyDeltaEpochs= zeros(size(EarDataEpochs, 1), 1);
    energyThetaEpochs = zeros(size(EarDataEpochs, 1), 1);
    energyAlphaEpochs= zeros(size(EarDataEpochs, 1), 1);
    energyBetaEpochs= zeros(size(EarDataEpochs, 1), 1);
    
    entropyDeltaEpochs= zeros(size(EarDataEpochs, 1), 1);
    entropyThetaEpochs =zeros(size(EarDataEpochs, 1), 1);
    entropyAlphaEpochs= zeros(size(EarDataEpochs, 1), 1);
    entropyBetaEpochs= zeros(size(EarDataEpochs, 1), 1);
    
    powerDeltaEpochs= zeros(size(EarDataEpochs, 1), 1);
    powerThetaEpochs = zeros(size(EarDataEpochs, 1), 1);
    powerAlphaEpochs= zeros(size(EarDataEpochs, 1), 1);
    powerBetaEpochs= zeros(size(EarDataEpochs, 1), 1);
    
    skewnessDeltaEpochs=zeros(size(EarDataEpochs, 1), 1);
    skewnessThetaEpochs=zeros(size(EarDataEpochs, 1), 1);
    skewnessAlphaEpochs=zeros(size(EarDataEpochs, 1), 1);
    skewnessBetaEpochs=zeros(size(EarDataEpochs, 1), 1);
    
    kurtosisDeltaEpochs=zeros(size(EarDataEpochs, 1), 1);
    kurtosisThetaEpochs=zeros(size(EarDataEpochs, 1), 1);
    kurtosisAlphaEpochs=zeros(size(EarDataEpochs, 1), 1);
    kurtosisBetaEpochs=zeros(size(EarDataEpochs, 1), 1);
    
    varDeltaEpochs=zeros(size(EarDataEpochs, 1), 1);
    varThetaEpochs=zeros(size(EarDataEpochs, 1), 1);
    varAlphaEpochs=zeros(size(EarDataEpochs, 1), 1);
    varBetaEpochs=zeros(size(EarDataEpochs, 1), 1);

for i = 1:size(EarDataEpochs, 1)

    wpt = wpdec(EarDataEpochs(i,:)',5,'db4','shannon');
    %plot(wpt)
    
    signaldelta=read(wpt,'cfs',31);
    signaltheta=read(wpt,'cfs',32);
    signalalpha=read(wpt,'cfs',33);
    signalbeta=read(wpt,'cfs',34)+read(wpt,'cfs',35)+read(wpt,'cfs',36)+read(wpt,'cfs',37)+read(wpt,'cfs',38);
    
    meanDeltaEpochs(i,1)= mean(signaldelta) ;
    meanThetaEpochs(i,1) = mean(signaltheta);
    meanAlphaEpochs(i,1) = mean(signalalpha);
    meanBetaEpochs(i,1) = mean(signalbeta);

    meanAbsDeltaEpochs(i,1) = mean(abs(signaldelta)) ;
    meanAbsThetaEpochs(i,1) = mean(abs(signaltheta)) ;
    meanAbsAlphaEpochs(i,1) = mean(abs(signalalpha)) ;
    meanAbsBetaEpochs(i,1) = mean(abs(signalbeta)) ;

    stdDeltaEpochs(i,1)= std(signaldelta);
    stdThetaEpochs(i,1) = std(signaltheta);
    stdAlphaEpochs(i,1)= std(signalalpha);
    stdBetaEpochs(i,1)=std(signalbeta);

    energyDeltaEpochs(i,1)= sum(signaldelta.^2);
    energyThetaEpochs(i,1) = sum(signaltheta.^2);
    energyAlphaEpochs(i,1)= sum(signalalpha.^2);
    energyBetaEpochs(i,1)= sum(signalbeta.^2);
    
    entropyDeltaEpochs(i,1)= approximateEntropy(signaldelta);
    entropyThetaEpochs(i,1) =approximateEntropy(signaltheta);
    entropyAlphaEpochs(i,1)= approximateEntropy(signalalpha);
    entropyBetaEpochs(i,1)= approximateEntropy(signalbeta);
    
    powerDeltaEpochs(i,1)= sum(signaldelta.^2)/length(signaldelta);
    powerThetaEpochs(i,1) = sum(signaltheta.^2)/length(signaltheta);
    powerAlphaEpochs(i,1)= sum(signalalpha.^2)/length(signalalpha);
    powerBetaEpochs(i,1)= sum(signalbeta.^2)/length(signalbeta);
    
    skewnessDeltaEpochs(i,1)= skewness(signaldelta);
    skewnessThetaEpochs(i,1)=skewness(signaltheta);
    skewnessAlphaEpochs(i,1)=skewness(signalalpha);
    skewnessBetaEpochs(i,1)=skewness(signalbeta);
    
    kurtosisDeltaEpochs(i,1)=kurtosis(signaldelta);
    kurtosisThetaEpochs(i,1)=kurtosis(signaltheta);
    kurtosisAlphaEpochs(i,1)=kurtosis(signalalpha);
    kurtosisBetaEpochs(i,1)=kurtosis(signalbeta);
    
    varDeltaEpochs(i,1)=var(signaldelta);
    varThetaEpochs(i,1)=var(signaltheta);
    varAlphaEpochs(i,1)=var(signalalpha);
    varBetaEpochs(i,1)=var(signalbeta);   
end 
    
%% label features
    
disp('labelling features');
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
       
disp('Done extracting features');
end