function welchPSD(locutoff, hicutoff, dwnsample, forder)
if ~exist('locutoff', 'var') %snippet in order to run this file separately
    locutoff = 0;
    hicutoff = 30;
    dwnsample = 2;
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
                 

% dwnsample = 2;

[Fs, LabelsOut, ChannelsOut, rounding_err] = Label_extract2(path2summary, EpochDurationSeconds, FileIndices, dwnsample);
T = 1/Fs;             % Sampling period 
[EarData, unfiltered_data] = LoadnFilter(path2edf, 'channellist', ChannelsOut.index, 'ASR', 0, ...
'locutoff', locutoff, 'hicutoff', hicutoff, 'forder', forder, 'downsample', dwnsample);

%% MAKE EPOCHS
EpochLengthSec = 3; 
[epochs, L] = DivideInEpochs(EarData, Fs, EpochDurationSeconds);
rowsEpoch= floor(length(EarData)/L);
epochs = epochs{1};
epoch = epochs(2,:);

t = linspace(0, length(epoch)/Fs, length(epoch));
%% PLOT psd
fig=figure();

ax(1) = plot(t, epoch);
% title('Welch PSD','interpreter' ,'latex','fontsize', 18,'FontWeight','bold')
legend('EEG', 'interpreter', 'latex', 'fontsize', 12);
ylim([-150 150]) 
xlim([0 3]);
axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = 14;


%% Specify common title, X and Y labels
title("Epoch of EEG data",'interpreter', 'latex','fontsize', 18)
xlabel('Time [$s$]','interpreter', 'latex', 'fontsize',17)
ylabel('Voltage [$\mu V$]','interpreter', 'latex','fontsize',17)

plotcolor(ax(1), 'green', 'colordiff', 30);
plotline(ax, 2);
figsize(fig, 's'); %try 's', 'm', 'b', 'o'/'r'
%% Save image
location = GetPath2Images(mfilename);
extension = "png";
SaveImage(fig, location, mfilename, extension);
% close all;