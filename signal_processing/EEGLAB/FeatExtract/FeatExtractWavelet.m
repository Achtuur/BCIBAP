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
    meanDeltaEpochs = zeros(1,length(EarDataEpochs));
    meanThetaEpochs = zeros(1,length(EarDataEpochs));
    meanAlphaEpochs = zeros(1,length(EarDataEpochs));
    meanBetaEpochs = zeros(1,length(EarDataEpochs));
    meanAbsDeltaEpochs = zeros(1,length(EarDataEpochs));
    meanAbsThetaEpochs = zeros(1,length(EarDataEpochs));
    meanAbsAlphaEpochs = zeros(1,length(EarDataEpochs));
    meanAbsBetaEpochs = zeros(1,length(EarDataEpochs));
    stdDeltaEpochs= zeros(1,length(EarDataEpochs));
    stdThetaEpochs = zeros(1,length(EarDataEpochs));
    stdAlphaEpochs= zeros(1,length(EarDataEpochs));
    stdBetaEpochs= zeros(1,length(EarDataEpochs));
    
    energyDeltaEpochs= zeros(1,length(EarDataEpochs));
    energyThetaEpochs = zeros(1,length(EarDataEpochs));
    energyAlphaEpochs= zeros(1,length(EarDataEpochs));
    energyBetaEpochs= zeros(1,length(EarDataEpochs));
    
    entropyDeltaEpochs= zeros(1,length(EarDataEpochs));
    entropyThetaEpochs =zeros(1,length(EarDataEpochs));
    entropyAlphaEpochs= zeros(1,length(EarDataEpochs));
    entropyBetaEpochs= zeros(1,length(EarDataEpochs));
    
    powerDeltaEpochs= zeros(1,length(EarDataEpochs));
    powerThetaEpochs = zeros(1,length(EarDataEpochs));
    powerAlphaEpochs= zeros(1,length(EarDataEpochs));
    powerBetaEpochs= zeros(1,length(EarDataEpochs));
    
    skewnessDeltaEpochs=zeros(1,length(EarDataEpochs));
    skewnessThetaEpochs=zeros(1,length(EarDataEpochs));
    skewnessAlphaEpochs=zeros(1,length(EarDataEpochs));
    skewnessBetaEpochs=zeros(1,length(EarDataEpochs));
    
    kurtosisDeltaEpochs=zeros(1,length(EarDataEpochs));
    kurtosisThetaEpochs=zeros(1,length(EarDataEpochs));
    kurtosisAlphaEpochs=zeros(1,length(EarDataEpochs));
    kurtosisBetaEpochs=zeros(1,length(EarDataEpochs));
    
    varDeltaEpochs=zeros(1,length(EarDataEpochs));
    varThetaEpochs=zeros(1,length(EarDataEpochs));
    varAlphaEpochs=zeros(1,length(EarDataEpochs));
    varBetaEpochs=zeros(1,length(EarDataEpochs));

for i = 1:length(EarDataEpochs)

    wpt = wpdec(EarDataEpochs(i,:),5,'db4','shannon');
    %plot(wpt)
    
    signaldelta=read(wpt,'cfs',31);
    signaltheta=read(wpt,'cfs',32);
    signalalpha=read(wpt,'cfs',33);
    signalbeta=read(wpt,'cfs',34)+read(wpt,'cfs',35)+read(wpt,'cfs',36)+read(wpt,'cfs',37)+read(wpt,'cfs',38);
    
    meanDeltaEpochs(1,i)= mean(signaldelta) ;
    meanThetaEpochs(1,i) = mean(signaltheta);
    meanAlphaEpochs(1,i) = mean(signalalpha);
    meanBetaEpochs(1,i) = mean(signalbeta);

    meanAbsDeltaEpochs(1,i) = mean(abs(signaldelta)) ;
    meanAbsThetaEpochs(1,i) = mean(abs(signaltheta) ;
    meanAbsAlphaEpochs(1,i) = mean(abs(signalalpha)) ;
    meanAbsBetaEpochs(1,i) = mean(abs(signalbeta)) ;

    stdDeltaEpochs(1,i)= std(signaldelta);
    stdThetaEpochs(1,i) = std(signaltheta);
    stdAlphaEpochs(1,i)= std(signalalpha);
    stdBetaEpochs(1,i)=std(signalbeta);

    energyDeltaEpochs(1,i)= sum(signaldelta.^2);
    energyThetaEpochs(1,i) = sum(signaltheta.^2);
    energyAlphaEpochs(1,i)= sum(signalalpha.^2);
    energyBetaEpochs(1,i)= sum(signalbeta.^2);
    
    entropyDeltaEpochs(1,i)= approximateEntropy(signaldelta);
    entropyThetaEpochs(1,i) =approximateEntropy(signaltheta);
    entropyAlphaEpochs(1,i)= approximateEntropy(signalalpha);
    entropyBetaEpochs(1,i)= approximateEntropy(signalbeta);
    
    powerDeltaEpochs(1,i)= sum(signaldelta.^2)/length(signaldelta);
    powerThetaEpochs(1,i) = sum(signaltheta.^2)/length(signaltheta);
    powerAlphaEpochs(1,i)= sum(signalalpha.^2)/length(signalalpha);
    powerBetaEpochs(1,i)= sum(signalbeta.^2)/length(signalbeta);
    
    skewnessDeltaEpochs(1,i)= skewness(signaldelta);
    skewnessThetaEpochs(1,i)=skewness(signaltheta);
    skewnessAlphaEpochs(1,i)=skewness(signalalpha);
    skewnessBetaEpochs(1,i)=skewness(signalbeta);
    
    kurtosisDeltaEpochs(1,i)=kurtosis(signaldelta);
    kurtosisThetaEpochs(1,i)=kurtosis(signaltheta);
    kurtosisAlphaEpochs(1,i)=kurtosis(signalalpha);
    kurtosisBetaEpochs(1,i)=kurtosis(signalbeta);
    
    varDeltaEpochs(1,i)=var(signaldelta);
    varThetaEpochs(1,i)=var(signaltheta);
    varAlphaEpochs(1,i)=var(signalalpha);
    varBetaEpochs(1,i)=var(signalbeta);   
end 
    
    
disp('labelling features');
[features, labels] = FeatureLabelsPerEpoch( ...
     varDeltaEpochs, 'VarianceDelta',  varThetaEpochs, 'VarianceTheta',varAlphaEpochs, 'VarianceAlpha', varBetaEpochs, 'VarianceBeta', ...
    kurtosisDeltaEpochs, 'kurtosisDelta', kurtosisThetaEpochs, 'kurtosisTheta', kurtosisAlphaEpochs, 'kurtosisAlpha', kurtosisBetaEpochs, 'kurtosisBeta', ...
    skewnessDeltaEpochs, 'skewnessDelta', skewnessThetaEpochs, 'skewnessTheta', skewnessAlphaEpochs, 'skewnessAlpha', skewnessBetaEpochs, 'skewnessBeta', ...
     powerDeltaEpochs, 'powerDelta',  powerThetaEpochs, 'powerTheta', powerAlphaEpochs, 'powerAlpha',  powerBetaEpochs, 'powerBeta',  ...
   entropyDeltaEpochs, 'entropyDelta', entropyThetaEpochs, 'entropyTheta', entropyAlphaEpochs, 'entropyAlpha',entropyBetaEpochs, 'entropyBeta', ...
    energyDeltaEpochs, 'energyDelta', energyThetaEpochs, 'energyTheta', energyAlphaEpochs, 'energyAlpha',energyBetaEpochs,'energyBeta', ...
    stdDeltaEpochs, 'stdDelta',stdThetaEpochs, 'stdTheta', stdAlphaEpochs, 'stdAlpha',stdBetaEpochs,'stdBeta',...
    meanDeltaEpochs, 'meanDelta',meanThetaEpochs, 'meanTheta', meanAlphaEpochs, 'meanAlpha',meanBetaEpochs,'meanBeta'...
    meanAbsDeltaEpochs, 'meanAbsDelta',meanAbsThetaEpochs, 'meanAbsTheta', meanAbsAlphaEpochs, 'meanAbsAlpha',meanAbsBetaEpochs,'meanAbsBeta'...);%, ...
%    epochs, 'epochs');
       
disp('Done extracting features');


end