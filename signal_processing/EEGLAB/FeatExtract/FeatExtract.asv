%% SIGNAL PARAMETERS 
addpath('./SPgroupfunc')
path2edf = './sample_data/chb10_01.edf';

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

%% TIME DOMAIN SIGNAL
t = (0:L-1)*T;        % Time vector
figure(1)
plot(1000*t,epochs(2,:));
title('EEG signal Epoch')
xlabel('t (milliseconds)')
ylabel('Epoch')

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

%short time fourier transform
figure(3)
s= spectrogram(epochs(2,:),hanning(L/3),L/6,2^nextpow2(L/3),Fs,'MinThreshold',-20,'yaxis');
spectrogram(epochs(2,:),hanning(L/3),L/6,2^nextpow2(L/3),Fs,'MinThreshold',-20,'yaxis');
[S,F,T] = stft(epochs(2,:),Fs,'Window',hanning(L/3),'OverlapLength',L/6,'FFTLength',2^nextpow2(L/3));


%% POWER SPECTRAL DENSITY
figure(4)
nfftWelch= 2^nextpow2(L/3); 
[psdWelch,fWelch] = pwelch(epochs(2,:),hanning(L/3),L/6,nfftWelch, Fs, 'psd');  %[p,f]= pwelch(x,window,noverlap,nfft,fs) , outputs single sided
pwelch(epochs(2,:),hanning(L/3), L/6,nfftWelch,Fs,'psd');
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


%% FEATURES
%TIME DOMAIN
%mean value
mean= sum(transpose(epochs))./length(epochs(1,:));

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
%variance
variance= var(transpose(epochs));


%FREQUENCY DOMAIN
%mean frequency(MNF)
powerSpectrum= power(1:40);
MNF=(sum(powerSpectrum.*(1:40)))/sum(powerSpectrum);
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





