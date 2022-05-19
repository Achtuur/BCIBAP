function [features,labels] = FeatExtractWavelet(EarDataEpochs, Fs, EpochLengthSec)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
%%
disp('Extracting features...');
T = 1/Fs;             % Sampling period 
L = Fs*EpochLengthSec;

%%
%% WAVELET TRANSFORM
%DWT
% figure(3)
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
% DWT packet decomposition

wpt = wpdec(epoch1,5,'db4','shannon');
%plot(wpt)
signaldelta=read(wpt,'cfs',31);
signaltheta=read(wpt,'cfs',32);
signalalpha=read(wpt,'cfs',33);
signalbeta=read(wpt,'cfs',34)+read(wpt,'cfs',35)+read(wpt,'cfs',36)+read(wpt,'cfs',37)+read(wpt,'cfs',38);

meandelta= mean(signaldelta);
meantheta= mean(signaltheta);
meanalpha= mean(signalalpha);
meanbeta= mean(signalbeta);

meanAbsdelta= mean(abs(signaldelta));
meanAbstheta= mean(abs(signaltheta));
meanAbsalpha= mean(abs(signalalpha));
meanAbsbeta= mean(abs(signalbeta));

stdDelta= std(signaldelta);
stdTheta = std(signaltheta);
stdAlpha= std(signalalpha);
stdBeta= std(signalbeta);

energyDelta= sum(signaldelta.^2);
energyTheta = sum(signaltheta.^2);
energyAlpha= sum(signalalpha.^2);
energyBeta= sum(signalbeta.^2);

entropyDelta= approximateEntropy(signaldelta);
entropyTheta = approximateEntropy(signaltheta);
entropyAlpha= approximateEntropy(signalalpha);
entropyBeta= approximateEntropy(signalbeta);

powerDelta= sum(signaldelta.^2)/length(signaldelta);
powerTheta = sum(signaltheta.^2)/length(signaltheta);
powerAlpha= sum(signalalpha.^2)/length(signalalpha);
powerBeta= sum(signalbeta.^2)/length(signalbeta);

skewnessDelta=skewness(signaldelta);
skewnessTheta=skewness(signaltheta);
skewnessAlpha=skewness(signalalpha);
skewnessBeta=skewness(signalbeta);

kurtosisDelta=kurtosis(signaldelta);
kurtosisTheta=kurtosis(signaltheta);
kurtosisAlpha=kurtosis(signalalpha);
kurtosisBeta=kurtosis(signalbeta); 

varDelta=var(signaldelta);
varTheta=var(signaltheta);
varAlpha=var(signalalpha);
varBeta=var(signalbeta); 















end