clc; clear;
eegpath = AddPath();
dataset = 'chb04';
path2dataset = eegpath + "sample_data\" + dataset + "\";
FileIndices = 5;
EpochLengthSec = 3;
% %% Get labels of data
% disp('Getting labels of data');
% t = tic;

fac_downsample = 2; %downsa5mpling factor
summarypath = path2dataset + dataset + "-summary.txt";
[Fs, labels1, channellist, rounding_err] = Label_extract2(summarypath, EpochLengthSec, FileIndices, fac_downsample); %get labels of where there are seizures
channellist = channellist.index;

%% get filtered data
t = tic;
disp("Loading data...");
filtered_data = LoadData(path2dataset, FileIndices, 'overwrite', 1,...
    'channellist', channellist, 'rounding_err', rounding_err, 'ASR', 0, 'downsample', fac_downsample);
% t = toc(t);
% fprintf("Data loaded, took %.3f seconds\n", t);
% disp('Extracting features...');
% T = 1/Fs;             % Sampling period 
 L = Fs*EpochLengthSec;
% totalepochs = totalepochs{1,1}; %take first channel for testing

%% epochs
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
%% POWER SPECTRAL DENSITY
nfftWelch = 2^nextpow2(L/3); 
[psdWelch,fWelch] = pwelch(totalepochs',hanning(L/3),L/6,nfftWelch, Fs, 'psd');  %[p,f] = pwelch(x,window,noverlap,nfft,fs) , outputs single sided

power = pwelch(totalepochs',hanning(L/3),L/6,nfftWelch, Fs,'power');  %[p,f] = pwelch(x,window,noverlap,nfft,fs) 

%% AVERAGE BAND POWER FOR EEG EPOCHS
%compute average band power for each EEG channel using 3 different methods

%using the time series input 
% deltaTime = bandpower(totalepochs',Fs,[0.5,4])';
% thetaTime = bandpower(totalepochs',Fs,[4,8])';
% alphaTime = bandpower(totalepochs',Fs,[8,12])';
% betaTime = bandpower(totalepochs',Fs,[12,30])';

%using Pwelch algorithm
deltaPwelch = bandpower(psdWelch,fWelch,[1,4],'psd')';
thetaPwelch = bandpower(psdWelch,fWelch,[4,8],'psd')';
alphaPwelch = bandpower(psdWelch,fWelch,[8,12],'psd')';
betaPwelch = bandpower(psdWelch,fWelch,[12,30],'psd')';
totalPwelch = bandpower(psdWelch,fWelch,'psd')';

%using Periodogram algorithm
% [psdPerio,fPerio] = periodogram(totalepochs',hanning(L),nfft,Fs);
% deltaPerio = bandpower(psdPerio,fPerio,[0.5,4],'psd')';
% thetaPerio = bandpower(psdPerio,fPerio,[4,8],'psd')';
% alphaPerio = bandpower(psdPerio,fPerio,[8,12],'psd')';
% betaPerio = bandpower(psdPerio,fPerio,[12,30],'psd')';
    
%% FEATURES
%TIME DOMAIN
%mean value
% mean = sum(epochs') ./ length(epochs(1,:));
% disp('Calculating mean');
% Mean = mean(totalepochs')';

%maximum value
%  posEpoch=epochs;
%  posEpoch(posEpoch < 0) = 0; %take rid of negative values (this is extremely slow and unnecessary)
%  maxValue= max(transpose(posEpoch)); 
%  disp('Calculating max value');
%  maxValue = max(totalepochs')';

% %minimum value
% negEpoch=epochs;
% negEpoch (negEpoch>0) = 0; %take rid of positive values (this is extremely slow and unnecessary)
% minValue = min(transpose(abs(negEpoch)));
% disp('Calculating min value');
% minValue = min(totalepochs')';
% 
% %energy
% disp('Calculating energy');
% energy = sum(abs(transpose(totalepochs).^2));
% %variance
% disp('Calculating variance');
% variance = var(transpose(totalepochs));


%FREQUENCY DOMAIN
%mean frequency(MNF)
disp('Calculating MNF');
vector=1:40;
 powerSpectrum = power(1:40, :); %rows is 1Hz, columns is 1 epoch
for j = 1 : 2673
  res( :,j ) = vector' .* powerSpectrum( :, j );
end

for j = 1 : 2673
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
totalepochs=totalepochs';
se=zeros(29,2673);
for j = 1 : 2673
se(:,j) = pentropy(totalepochs(:,j),129);
end

stdentropy=zeros(1,2673);
for j = 1 : 2673
stdentropy(j) = std(se(:,j));
end

minentropy=zeros(1,2673);
for j = 1 : 2673
minentropy(j) = min(se(:,j));
end

stdepoch=zeros(1,2673);
for j = 1 : 2673
stdepoch(j) = std(totalepochs(:,j));
end

% min=zeros(1,2673);
% for j = 1 : 2673
% min(j) = min(totalepochs(:,j));
% end
disp('labelling features');
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
    MNF,'MNF',stdentropy,'stdentropy',minentropy,'minentropy',stdepoch,'stdepoch');%, ...
%    epochs, 'epochs');
       
disp('Done extracting features');

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

figure(4)
pentropy(totalepochs(:,2000),129);
senonseizure=pentropy(totalepochs(:,2000),129);
figure(5)
pentropy(totalepochs(:,5),129)
seseizure=pentropy(totalepochs(:,5),129);


% figure(6)
% % 
% scatter(stdepoch(1,1:148*9),stdentropy(1,1:148*9));
% %
% hold on
% scatter(stdepoch(1,148*9:2673),stdentropy(1,148*9:2673));
figure(5)
t = tiledlayout('flow');
% % Plot in tiles
nexttile, ax(1)= bar(explained), title('Welch Power Spectral Density Estimate','interpreter' ,'latex','fontsize', 18,'FontWeight','bold'),xlim([0 128]) 
%nexttile, ax(2)=  plot(fPerio,10*log10(psdPerio)),title('Periodogram Power Spectral Density Estimate','interpreter', 'latex','fontsize', 18,'fontweight','bold'), xlim([0 128])
plotcolor(ax,'green', 'colordiff',0);
% % Specify common title, X and Y labels
% title(t, 'Decomposition of epoch signal','interpreter', 'latex','fontsize', 18)
xlabel(t, '$Frequency [Hz]$','interpreter', 'latex', 'fontsize',17)
ylabel(t, '$Power/frequency [dB/Hz]$','interpreter', 'latex','fontsize',17)
%saveas(gcf,'Pwelch_PerioPsd','epsc')

%% Save image
location = GetPath2Images() + mfilename;
extension = "eps";
SaveImage(fig, location, extension);