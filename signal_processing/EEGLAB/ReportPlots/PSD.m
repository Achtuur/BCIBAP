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


epoch1= decimate(epoch1,2);


%% TIME DOMAIN SIGNAL
t = (0:L-1)*T;        % Time vector


%% POWER SPECTRAL DENSITY
figure(4)
nfftWelch= 2^nextpow2(L/3); 
[psdWelch,fWelch] = pwelch(epochs(2,:),hanning(L/3),L/6,nfftWelch, Fs, 'psd');  %[p,f]= pwelch(x,window,noverlap,nfft,fs) , outputs single sided
pwelch(epochs(2,:),hanning(L/3), L/6, nfftWelch,Fs,'psd');
figure(5)
power= pwelch(epochs(2,:),hanning(L/3),L/6,nfftWelch, Fs,'power');  %[p,f]= pwelch(x,window,noverlap,nfft,fs) 
pwelch(epochs(2,:),hanning(L/3),L/6, nfftWelch,Fs,'power');
%% PLOT psd
fig=figure(7)

t = tiledlayout('flow');
% % Plot in tiles
nexttile, ax(1)= plot(fWelch,10*log10(psdWelch)), title('Welch Power Spectral Density Estimate','interpreter' ,'latex','fontsize', 18,'FontWeight','bold'),xlim([0 128]) 
nexttile, ax(2)=  plot(fPerio,10*log10(psdPerio)),title('Periodogram Power Spectral Density Estimate','interpreter', 'latex','fontsize', 18,'fontweight','bold'), xlim([0 128])
plotcolor(ax,'green', 'colordiff',0);
% % Specify common title, X and Y labels
% title(t, 'Decomposition of epoch signal','interpreter', 'latex','fontsize', 18)
xlabel(t, '$Frequency [Hz]$','interpreter', 'latex', 'fontsize',17)
ylabel(t, '$Power/frequency [dB/Hz]$','interpreter', 'latex','fontsize',17)
saveas(gcf,'Pwelch_PerioPsd','epsc')

%% Save image
location = GetPath2Images() + mfilename;
extension = "eps";
SaveImage(fig, location, extension);