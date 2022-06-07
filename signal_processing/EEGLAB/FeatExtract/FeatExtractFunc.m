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

disp('Extracting features...');
T = 1/Fs;             % Sampling period 
L = Fs*EpochLengthSec;
nEpochs = size(EarDataEpochs{1,1}, 1); % get amount of epochs (assume all entries in eardataepochs have same number of epochs)
nChannels = size(EarDataEpochs, 1);
                 
%epochsDec=zeros(2406,384);

%%
TotalFeatures = {};
TotalFeatureLabels = '';

%% extracting efatures

% For testing purposes only !!!!
warning('For testing, only take first channel');
nChannels = 1;
for k = 1:nChannels
    fprintf('Extracting from channel %d...\n', k);
    t = tic;
    CurChannelEpoch = EarDataEpochs{k, 1};
    CurChannelEpoch=CurChannelEpoch';

    
    %% FOURIER TRANSFORM
    nfft = 2^nextpow2(L); %zero padding

    %% POWER SPECTRAL DENSITY
    nfftWelch = 2^nextpow2(L/3); 
    [psdWelch,fWelch] = pwelch(CurChannelEpoch,hanning(L/3),L/6,nfftWelch, Fs, 'psd');  %[p,f] = pwelch(x,window,noverlap,nfft,fs) , outputs single sided
    
    power = pwelch(CurChannelEpoch,hanning(L/3),L/6, nfftWelch,Fs,'power');  %[p,f] = pwelch(x,window,noverlap,nfft,fs) 

    %% AVERAGE BAND POWER FOR EEG EPOCHS
    %compute average band power for each EEG channel using 3 different methods
    
    %using Pwelch algorithm
    deltaPwelch = bandpower(psdWelch,fWelch,[0.5,4],'psd')';
    thetaPwelch = bandpower(psdWelch,fWelch,[4,8],'psd')';
    alphaPwelch = bandpower(psdWelch,fWelch,[8,12],'psd')';
    betaPwelch = bandpower(psdWelch,fWelch,[12,30],'psd')';
    totalPwelch = bandpower(psdWelch,fWelch,'psd')';
      
    
    %% FEATURES
    
    %FREQUENCY DOMAIN
    %mean frequency(MNF)
    disp('Calculating MNF');
    vector=1:40;
     powerSpectrum = power(1:40, :); %rows is 1Hz, columns is 1 epoch
    for j = 1 : nEpochs
      res( :,j ) = vector' .* powerSpectrum( :, j );
    end
    
    for j = 1 : nEpochs
    MNF(j) = (sum( res(:,j))) ./ sum(powerSpectrum(:,j)); % fix later to work per epoch
    end
    
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
    theta_delta= Ptheta./Pdelta;
    
    alpha_beta =  Palpha ./ Pbeta;
    alpha_delta= Palpha./Pdelta;
    alpha_theta= Palpha./Ptheta;
    
    beta_alpha =  Pbeta ./ Palpha;
    beta_delta= Pbeta./Pdelta;
    beta_theta= Pbeta./Ptheta;
    
    %energy
    Edelta = sum(psdWelch(1:4,:).^2);
    Etheta = sum(psdWelch(4:8,:).^2);
    Ealpha = sum(psdWelch(8:12,:).^2);
    Ebeta  = sum(psdWelch(12:30,:).^2);
    %energy ratios
    Edelta_theta = Edelta ./ Etheta;
    Edelta_alpha = Edelta ./ Ealpha;
    Edelta_beta =  Edelta ./ Ebeta;
    Etheta_alpha = Etheta ./ Ealpha;
    Etheta_beta =  Etheta ./ Ebeta;
    Etheta_delta= Etheta./Edelta;
    Ealpha_beta =  Ealpha ./ Ebeta;
    Ealpha_delta= Ealpha./Edelta;
    Ealpha_theta= Ealpha./Etheta;
    Ebeta_alpha =  Ebeta ./ Ealpha;
    Ebeta_delta= Ebeta./Edelta;
    Ebeta_theta= Ebeta./Etheta;
    
    %spectral entropy
    %totalepochs=totalepochs';
    se=zeros(29,nEpochs);
    for j = 1 : nEpochs
    se(:,j) = pentropy(CurChannelEpoch(:,j),129);
    end
    
    % stdentropy=zeros(1,2673);
    % for j = 1 : 2673
    %stdentropy(j) = std(totalepochs(:,j));
     %end
    % 
    % min=zeros(1,2673);
    % for j = 1 : 2673
    % min(j) = min(totalepochs(:,j));
    % end

    %% label features 
    
fprintf('Labelling features from channel %d...\n', k);
[features, labels] = FeatureLabelsPerEpoch( ...
    deltaPwelch, 'deltaPwelch', thetaPwelch, 'thetaPwelch', alphaPwelch, 'alphaPwelch', betaPwelch, 'betaPwelch', ...
    Edelta, 'Edelta', Etheta, 'Etheta', Ealpha, 'Ealpha', Ebeta, 'Ebeta', ...
    Pdelta, 'Pdelta', Ptheta, 'Ptheta', Palpha, 'Palpha', Pbeta, 'Pbeta', ...
    delta_theta, 'delta_theta', delta_alpha, 'delta_alpha', delta_beta, 'delta_beta', ...
    alpha_theta, 'alpha_theta', alpha_delta, 'alpha_delta', alpha_beta, 'alpha_beta', ...
    beta_theta, 'beta_theta', beta_delta, 'beta_delta', beta_alpha, 'beta_alpha', ...
    theta_alpha, 'theta_alpha', theta_beta, 'theta_beta', theta_delta, 'theta_delta',...
    Edelta_theta, 'Edelta_theta', Edelta_alpha, 'Edelta_alpha', Edelta_beta, 'Edelta_beta', ...
    Ealpha_theta, 'Ealpha_theta', Ealpha_delta, 'Ealpha_delta', Ealpha_beta, 'Ealpha_beta', ...
    Ebeta_theta, 'Ebeta_theta', Ebeta_delta, 'Ebeta_delta', Ebeta_alpha, 'Ebeta_alpha', ...
    Etheta_alpha, 'Etheta_alpha', Etheta_beta, 'Etheta_beta', Etheta_delta, 'Etheta_delta',...
    MNF,'MNF');%, ...
%    epochs, 'epochs');
[TotalFeatures, TotalFeatureLabels] = CombineFeatureLabels(TotalFeatures, TotalFeatureLabels, features, labels);
     fprintf("Done extracting features from channel %d, took %.3f seconds\n", k, toc(t));
end     
disp('Done extracting features');
end


