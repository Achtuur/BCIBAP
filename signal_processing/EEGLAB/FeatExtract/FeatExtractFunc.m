%% SIGNAL PARAMETERS 
% addpath('./SPgroupfunc')
% path2edf = './sample_data/chb10_01.edf';
% 
% Fs = 256;            % Sampling frequency                    
 
% filtered_data = LoadnFilter(path2edf, 'locutoff', 0.5, 'hicutoff', 40, 'showplots', 0);
% EarData = filtered_data(1,:);
% %L = 768;             % Length of signal
% %t = (0:L-1)*T;        % Time vector

%Note that in most of the extraction paths 'epochs' is transposed because then the return value is per epoch instead of per sample of epoch

function [features, labels] = FeatExtractFunc(EarDataEpochs, Fs, EpochLengthSec)
%% Test variables
%     path2edf = 'FeatExtract\chb10_01.edf';
%     Fs = 256;            % Sampling frequency                    
%     T = 1/Fs;             % Sampling period  
%     filtered_data = LoadnFilter(path2edf, 'locutoff', 0.5, 'hicutoff', 40, 'showplots', 0);
%     EarData = filtered_data(1,:) ;
%     EpochLengthSec = 3;
%%
disp('Extracting features...');
T = 1/Fs;             % Sampling period 
L = Fs*EpochLengthSec;
%% FOURIER TRANSFORM
nfft = 2^nextpow2(L); %zero padding
Y = fft(EarDataEpochs', L);  % compute fft of each epoch , zero padding is an option in second argument
%Pxx = abs(fft(x,nfft)).^2/length(x)/Fs;

P2 = abs(Y/L); %normalize fft with length of signal
P1 = P2(1 : L/2+1);  %take frequencies up until nyquist rate (L/2)
P1(2:end-1) = 2*P1(2:end-1); %times 2 because negative frequencies need to add up with positive ones
                                   %exclude DC folding frequency
psd = P1.^2; %(divide by Fs)?


f = Fs*(0:(L/2))/L;

%% POWER SPECTRAL DENSITY
nfftWelch = 2^nextpow2(L/3); 
[psdWelch,fWelch] = pwelch(EarDataEpochs',hanning(L/3),L/6,nfftWelch, Fs, 'psd');  %[p,f] = pwelch(x,window,noverlap,nfft,fs) , outputs single sided

power = pwelch(EarDataEpochs',hanning(L/3),L/6, Fs,'power');  %[p,f] = pwelch(x,window,noverlap,nfft,fs) 

%% AVERAGE BAND POWER FOR EEG EPOCHS
%compute average band power for each EEG channel using 3 different methods

%using the time series input 
deltaTime = bandpower(EarDataEpochs',Fs,[0.5,4])';
thetaTime = bandpower(EarDataEpochs',Fs,[4,8])';
alphaTime = bandpower(EarDataEpochs',Fs,[8,12])';
betaTime = bandpower(EarDataEpochs',Fs,[12,30])';

%using Pwelch algorithm
deltaPwelch = bandpower(psdWelch,fWelch,[0.5,4],'psd')';
thetaPwelch = bandpower(psdWelch,fWelch,[4,8],'psd')';
alphaPwelch = bandpower(psdWelch,fWelch,[8,12],'psd')';
betaPwelch = bandpower(psdWelch,fWelch,[12,30],'psd')';
totalPwelch = bandpower(psdWelch,fWelch,'psd')';

%using Periodogram algorithm
[psdPerio,fPerio] = periodogram(EarDataEpochs',hanning(L),nfft,Fs);
deltaPerio = bandpower(psdPerio,fPerio,[0.5,4],'psd')';
thetaPerio = bandpower(psdPerio,fPerio,[4,8],'psd')';
alphaPerio = bandpower(psdPerio,fPerio,[8,12],'psd')';
betaPerio = bandpower(psdPerio,fPerio,[12,30],'psd')';
    
%% FEATURES
%TIME DOMAIN
%mean value
% mean = sum(epochs') ./ length(epochs(1,:));
disp('Calculating mean');
Mean = mean(EarDataEpochs')';

%maximum value
% posEpoch=epochs;
% posEpoch(posEpoch < 0) = 0; %take rid of negative values (this is extremely slow and unnecessary)
% maxValue= max(transpose(posEpoch)); 
disp('Calculating max value');
maxValue = max(EarDataEpochs')';

%minimum value
% negEpoch=epochs;
% negEpoch (negEpoch>0) = 0; %take rid of positive values (this is extremely slow and unnecessary)
% minValue = min(transpose(abs(negEpoch)));
disp('Calculating min value');
minValue = min(EarDataEpochs')';

%energy
disp('Calculating energy');
energy = sum(abs(transpose(EarDataEpochs).^2));
%variance
disp('Calculating variance');
variance = var(transpose(EarDataEpochs));


%FREQUENCY DOMAIN
%mean frequency(MNF)
% disp('Calculating MNF');
% powerSpectrum = power(1:40, :); %rows is 1Hz, columns is 1 epoch
% MNF = (sum( powerSpectrum .* (1:1:40)' )) / sum(powerSpectrum); % fix later to work per epoch
%relative powers
disp('Calculating relative powers');
totalPwelch = mean(totalPwelch);
Pdelta = deltaPwelch / totalPwelch;
Ptheta = thetaPwelch / totalPwelch;
Palpha = alphaPwelch / totalPwelch;
Pbeta  = betaPwelch  / totalPwelch;

%power ratios
disp('Calculating power ratios');
delta_theta = Pdelta ./ Ptheta;
delta_alpha = Pdelta ./ Palpha;
delta_beta =  Pdelta ./ Pbeta;
theta_alpha = Ptheta ./ Palpha;
theta_beta =  Ptheta ./ Pbeta;
alpha_beta =  Palpha ./ Pbeta;
    
disp('labelling features');
[features, labels] = FeatureLabelsPerEpoch( ...
    deltaTime, 'deltaTime', thetaTime, 'thetaTime', alphaTime, 'alphaTime', betaTime, 'betaTime', ...
    deltaPwelch, 'deltaPwelch', thetaPwelch, 'thetaPwelch', alphaPwelch, 'alphaPwelch', betaPwelch, 'betaPwelch', ...
    deltaPerio, 'deltaPerio', thetaPerio, 'thetaPerio', alphaPerio, 'alphaPerio', betaPerio, 'betaPerio', ...
    Mean, 'mean', maxValue, 'maxValue', minValue, 'minValue', energy, 'energy', variance, 'variance', ...
    Pdelta, 'Pdelta', Ptheta, 'Ptheta', Palpha, 'Palpha', Pbeta, 'Pbeta', ...
    delta_theta, 'delta_theta', delta_alpha, 'delta_alpha', delta_beta, 'delta_beta', ...
    theta_alpha, 'theta_alpha', theta_beta, 'theta_beta', alpha_beta, 'alpha_beta');
       
disp('Done extracting features');
end


