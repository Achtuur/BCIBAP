%% SIGNAL PARAMETERS 
AddPath();
path2edf = 'FeatExtract\chb10_01.edf';

Fs = 256;            % Sampling frequency                    
T = 1/Fs;             % Sampling period  
filtered_data = LoadnFilter(path2edf, 'locutoff', 0.5, 'hicutoff', 40, 'showplots', 0);
EarData= filtered_data(1,:);
%L = 768;             % Length of signal
%t = (0:L-1)*T;        % Time vector
%% MAKE EPOCHS
EpochLengthSec=3; 
L = Fs*EpochLengthSec;
rowsEpoch= floor(length(EarData)/L);
epochs= zeros(rowsEpoch,L);
x=0;
for i=1:rowsEpoch
    epochs(i,:)= EarData(1,(x*L+1):L*(x+1));
    x=x+1;
end
epoch1= epochs(2,:);
epoch2= decimate(epoch1,2);

epochsDec=zeros(2406,384);
for i=1:2406
    epochsDec(i,:)=decimate(epochs(i,:),2);
end


%% TIME DOMAIN SIGNAL
t = (0:L-1)*T;        % Time vector
figure(1)
plot(1000*t,epochs(2,:));
title('EEG signal Epoch')
xlabel('t (milliseconds)')
%ylabel('Amplitude')
saveas(gcf,'EEG_Epoch','epsc')
%% FOURIER TRANSFORM
nfft = 2^nextpow2(L); %zerro padding
Y= fft(transpose(epochs),L);  % compute fft of each epoch , zero padding is an option in second argument
%Pxx = abs(fft(x,nfft)).^2/length(x)/Fs;
P2 = abs(Y/L); %normalize fft with length of signal
P1 = P2(1:L/2+1);  %take frequencies up until nyquist rate (L/2)
P1(2:end-1) = 2*P1(2:end-1); %times 2 because negative frequencies need to add up with positive ones
                                   %exclude DC folding frequency
psd=P1.^2; %(divide by Fs)?
%Plot Fourier Transform
figure(2)
f = Fs*(0:(L/2))/L;
plot(f,P1) 
title('Single-Sided Amplitude Spectrum of X(t)')
xlabel('f (Hz)')
ylabel('|P1(f)|')
%short time fourier transform (STFT)
%figure(3)
s= spectrogram(epochs(2,:),hanning(L/3),L/6,2^nextpow2(L/3),Fs,'MinThreshold',-20,'yaxis');
%spectrogram(epochs(2,:),hanning(L/3),L/6,2^nextpow2(L/3),Fs,'MinThreshold',-20,'yaxis');
[S,F,T] = stft(epochs(2,:),Fs,'Window',hanning(L/3),'OverlapLength',L/6,'FFTLength',2^nextpow2(L/3));
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
%% POWER SPECTRAL DENSITY
figure(4)
nfftWelch= 2^nextpow2(L/3); 
[psdWelch,fWelch] = pwelch(epochs(2,:),hanning(L/3),L/6,nfftWelch, Fs, 'psd');  %[p,f]= pwelch(x,window,noverlap,nfft,fs) , outputs single sided
pwelch(epochs(2,:),hanning(L/3), L/6, nfftWelch,Fs,'psd');
figure(5)
power= pwelch(epochs(2,:),hanning(L/3),L/6,nfftWelch, Fs,'power');  %[p,f]= pwelch(x,window,noverlap,nfft,fs) 
pwelch(epochs(2,:),hanning(L/3),L/6, nfftWelch,Fs,'power'); 
%% AVERAGE BAND POWER FOR EEG EPOCHS
%compute average band power for each EEG channel using 3 different methods
 
%using the time series input 
deltaTime = bandpower(epochs(2,:),Fs,[0.5,4]);
thetaTime= bandpower(epochs(2,:),Fs,[4,8]);
alphaTime= bandpower(epochs(2,:),Fs,[8,12]);
betaTime= bandpower(epochs(2,:),Fs,[12,30]);
%using Pwelch algorithm
deltaPwelch = bandpower(psdWelch,fWelch,[0.5,4],'psd');
thetaPwelch = bandpower(psdWelch,fWelch,[4,8],'psd');
alphaPwelch = bandpower(psdWelch,fWelch,[8,12],'psd');
betaPwelch = bandpower(psdWelch,fWelch,[12,30],'psd');
totalPwelch= bandpower(psdWelch,fWelch,'psd');
%using Periodogram algorithm
figure(6)
periodogram(epochs(2,:),hanning(L),nfft,Fs);
[psdPerio,fPerio] = periodogram(epochs(2,:),hanning(L),nfft,Fs);
deltaPerio = bandpower(psdPerio,fPerio,[0.5,4],'psd');
thetaPerio = bandpower(psdPerio,fPerio,[4,8],'psd');
alphaPerio= bandpower(psdPerio,fPerio,[8,12],'psd');
betaPerio= bandpower(psdPerio,fPerio,[12,30],'psd');
figure(7)
subplot(2,2,1);
pwelch(epochs(2,:),hanning(L/3), L/6,nfftWelch,Fs,'psd');
subplot(2,2,2);
periodogram(epochs(2,:),hanning(L),nfft,Fs);
saveas(gcf,'Pwelch_Periodogram_plot','epsc')
saveas(gcf,'Pwelch_Periodogram_plot', 'jpg')
%% FEATURES
%TIME DOMAIN
%mean value
mean1= sum(transpose(epochs))./length(epochs(1,:));
%maximum value
posEpoch=epochs;
posEpoch(posEpoch < 0) = 0; %take rid of negative values
maxValue= max(transpose(posEpoch)); 
%minimum value
negEpoch=epochs;
negEpoch(negEpoch>0)=0; %take rid of positive values
minValue = min(transpose(abs(negEpoch)));
%energy
energy= sum(abs(transpose(epochs).^2));
%energy of every subband
%variance
variance= var(transpose(epochs));
%skewness
%skewness= skewness(transpose(epochs));
%FREQUENCY DOMAIN
%mean frequency(MNF)
powerSpectrum= transpose(power(1:40));
MNF=(sum(powerSpectrum.*(1:40)))/sum(powerSpectrum);
%spectral entropy
PSscaled= powerSpectrum-min(powerSpectrum);
normPower=PSscaled/norm(PSscaled,1);
SE=sum(transpose(normPower(:)).*log(1/normPower(:)));
%renyi entropy
RE=-log(sum(normPower.^2));
%relative powers
Pdelta= deltaPwelch/totalPwelch;
Ptheta= thetaPwelch/totalPwelch;
Palpha= alphaPwelch/totalPwelch;
Pbeta= betaPwelch/totalPwelch;
%power ratios
delta_theta= Pdelta/Ptheta;
delta_alpha=Pdelta/Palpha;
delta_beta=Pdelta/Pbeta;
theta_alpha=Ptheta/Palpha;
theta_beta=Ptheta/Pbeta;
alpha_beta= Palpha/Pbeta;
%energy per frequency band
%time instance1
sumenergyDelta=0;
sumenergyTheta=0;
sumenergyAlpha=0;
sumenergyBeta=0;
for i=1:5
    freq= abs(S(:,i))/length(S(:,1));
    freq1=freq(1:length(S(:,1))/2+1); 
    freq1(2:end-1)=2*freq1(2:end-1);
    energyDelta= sum(freq1(1:5).^2)/5; 
    energyTheta= sum(freq1(5:9).^2)/5; 
    energyAlpha= sum(freq1(9:13).^2)/5; 
    energyBeta = sum(freq1(13:31).^2)/19; 
    
    sumenergyDelta=sumenergyDelta+energyDelta;
    sumenergyTheta=sumenergyTheta+energyTheta;
    sumenergyAlpha=sumenergyAlpha+energyAlpha;
    sumenergyBeta=sumenergyBeta+energyBeta;
end 
avgEnergyDelta= sumenergyDelta/5;
avgEnergyTheta= sumenergyTheta/5;
avgEnergyAlpha= sumenergyAlpha/5;
avgEnergyBeta=  sumenergyBeta/5;