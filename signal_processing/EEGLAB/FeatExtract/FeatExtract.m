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
%s= spectrogram(epochs(2,:),hanning(L/3),L/6,nfft,'onesided','MinThreshold',-20,'yaxis');
s= spectrogram(epochs(2,:),hanning(L/3),L/6, f,Fs,'MinThreshold',-20,'yaxis');
spectrogram(epochs(2,:),hanning(L/3),L/6,f,Fs,'MinThreshold',-20,'yaxis');
%spectrogram(epochs(2,:),hanning(L/3),L/6,nfft,'onesided','MinThreshold',-20,'yaxis');

%% POWER SPECTRAL DENSITY
figure(4)
psd2 = pwelch(epochs(2,:),hanning(L/3),nfft/2,nfft,Fs, 'psd');  %[p,f]= pwelch(x,window,noverlap,nfft,fs) , outputs single sided
pwelch(epochs(2,:),hanning(L/3), nfft/2,nfft,Fs,'psd');
PdB_Hz= 10*log10(pxx);                  % dBW/Hz
figure(5)
power= pwelch(epochs(2,:),hanning(L/3),nfft/2,nfft, Fs,'power');  %[p,f]= pwelch(x,window,noverlap,nfft,fs) 
welch(epochs(2,:),hanning(L/3),nfft/2,nfft, Fs,'power'); 

%% AVERAGE BAND POWER FOR EEG EPOCHS
%compute average band power for each EEG channel
pxx = periodogram(epochs(2,:),hanning(L));

deltaPower = bandpower(epochs(2,:),Fs,[0.5,4]);
thetaPower= bandpower(epochs(2,:),Fs,[4,8]);
alphaPower= bandpower(epochs(2,:),Fs,[8,12]);
betaPower= bandpower(epochs(2,:),Fs,[12,30]);

f1=linspace(0,L/2,floor(nfft/2+1));


pdelta2= bandpower(pxx,f1,[0.5,4],'psd'); % pxx should be 

%f3= linspace(0,L/2,floor(L/2+1));
pdelta = bandpower(psd2,f1,[0.5,4],'psd')
ptheta = bandpower(psd2,f1,[4,8],'psd')
palpha = bandpower(psd2,f1,[8,12],'psd')
pbeta = bandpower(psd2,f1,[12,30],'psd')