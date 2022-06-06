function PSD(locutoff, hicutoff, downsample, forder)
if ~exist('locutoff', 'var') %snippet in order to run this file separately
    locutoff = 0.5;
    hicutoff = 40;
    downsample = 2;
    forder = 30;
end

%% SIGNAL PARAMETERS 
AddPath();
eegpath = AddPath();
dataset = 'chb10';
path2dataset = eegpath + "sample_data/" + dataset;
FileIndices = 1;
EpochDurationSeconds = 3;
path2summary = path2dataset + "/" + dataset + "-summary.txt";
FileIndicesstr = "01";
path2edf = 'FeatExtract\chb10_01.edf';
                 

% downsample = 2;

[Fs, LabelsOut, ChannelsOut, rounding_err] = Label_extract2(path2summary, EpochDurationSeconds, FileIndices, downsample);
T = 1/Fs;             % Sampling period 
[EarData, unfiltered_data] = LoadnFilter(path2edf, 'channellist', ChannelsOut.index, 'ASR', 0, ...
'locutoff', locutoff, 'hicutoff', hicutoff, 'forder', forder, 'downsample', downsample);

%% MAKE EPOCHS
EpochLengthSec = 3; 
[epochs, L] = DivideInEpochs(EarData, Fs, EpochDurationSeconds);
rowsEpoch= floor(length(EarData)/L);
epochs = epochs{1};

% epochs= zeros(rowsEpoch,L);
% x=0;
% for i=1:rowsEpoch
%     epochs(i,:)= EarData(1,(x*L+1):L*(x+1));
%     x=x+1;
% end
% epoch1= epochs(2,:);
% 
% epoch2= decimate(epoch1,2);
% 
% epochsDec=zeros(2406,384);
% for i=1:2406
%     epochsDec(i,:)=decimate(epochs(i,:),2);
% end
% 
% epoch1= decimate(epoch1,2);


%% TIME DOMAIN SIGNAL
t = (0:L-1)*T;        % Time vector


%% POWER SPECTRAL DENSITY

nfft = 2^nextpow2(L); %zero padding
nfftWelch= 2^nextpow2(L/3);
[psdWelch,fWelch] = pwelch(epochs(2,:),hanning(L/3),L/6,nfftWelch, Fs, 'psd');  %[p,f]= pwelch(x,window,noverlap,nfft,fs) , outputs single sided
% pwelch(epochs(2,:),hanning(L/3), L/6, nfftWelch,Fs,'psd');
  


power= pwelch(epochs(2,:),hanning(L/3),L/6,nfftWelch, Fs,'power');  %[p,f]= pwelch(x,window,noverlap,nfft,fs) 
% pwelch(epochs(2,:),hanning(L/3),L/6, nfftWelch,Fs,'power');
%% PLOT psd
fig=figure();

[psdPerio,fPerio] = periodogram(epochs(2,:), hanning(L), nfft, Fs);

t = tiledlayout(1, 2);
%% Plot in tiles
%plot1
nexttile;
ax(1) = plot(fWelch,10*log10(psdWelch));
title('Welch PSD','interpreter' ,'latex','fontsize', 18,'FontWeight','bold')
legend('PSD estimate', 'interpreter', 'latex', 'fontsize', 8);
xlim([0 Fs/downsample]) 
ylim([-80 20]);
axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = 14;

%plot2
nexttile
ax(2) = plot(fPerio,10*log10(psdPerio));
title('Periodogram PSD','interpreter', 'latex','fontsize', 18,'fontweight','bold')
legend('PSD estimate', 'interpreter', 'latex', 'fontsize', 8);
xlim([0 Fs/downsample])
ylim([-80 20]);
axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = 14;

%% Specify common title, X and Y labels
title(t, 'Power Spectral Density estimates using two methods','interpreter', 'latex','fontsize', 18)
xlabel(t, 'Frequency [Hz]','interpreter', 'latex', 'fontsize',17)
ylabel(t, 'Power [dB/Hz]','interpreter', 'latex','fontsize',17)

plotcolor(ax(1), 'green', 'colordiff', 30);
plotcolor(ax(2), 'green', 'colordiff', 30);
plotline(ax, 2);
figsize(fig, 'o'); %try 's', 'm', 'b', 'o'/'r'
%% Save image
location = GetPath2Images() + mfilename;
extension = "eps";
SaveImage(fig, location, extension);
% close all;