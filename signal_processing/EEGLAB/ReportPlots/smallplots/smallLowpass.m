function smallLowPass(locutoff, hicutoff, dwnsample, forder)
if ~exist('locutoff', 'var') %snippet in order to run this file separately
    locutoff = 0;
    hicutoff = 30;
    dwnsample = 2;
    forder = 30;
end
eegpath = AddPath();
dataset = 'chb03';
path2dataset = eegpath + "sample_data/" + dataset;
FileIndices = 1;
EpochDurationSeconds = 3;
path2summary = path2dataset + "/" + dataset + "-summary.txt";
FileIndicesstr = "01";
path2edf = path2dataset + "/" + dataset + "_" + FileIndicesstr + ".edf";


%% get data
dwnsample = 1;
[Fs, LabelsOut, ChannelsOut, rounding_err] = Label_extract2(path2summary, EpochDurationSeconds, FileIndices, dwnsample);
ChannelsOut = ChannelsOut.index;
% forder = 30;
% hicutoff = 30;
[filtered_data, unfiltered_data, filt_coeff] = LoadnFilter(path2edf, 'channellist', ...
    ChannelsOut, 'ASR', 0, 'downsample', dwnsample, ...
    'locutoff', 0, 'hicutoff', hicutoff, 'forder', forder);
%% Get axis data
N = 5000;
%x
f = linspace(0, Fs, N);
fshift = linspace(-Fs/2, Fs/2 - Fs/2/N, N);

%y
Z_low = fftshift(fft(filt_coeff, N));
Z_low = mag2db(abs(Z_low));
% take only x > 0 (real valued so symmetrical)
n = find(fshift >= 0);
fshift = fshift(n);
Z_low = Z_low(n);
xmax = find(islocalmin(Z_low), 1, 'first');
% xmax = fshift(xmax);

fshift = fshift(1:xmax);
Z_low = Z_low(1:xmax);
%% plot
fig = figure();
linestyle = '-.';
hold on;
ax(1) = plot(fshift, Z_low);
hold off;
plotline(ax, 2);
br = 25;
plotcolor(ax(1), 'green', 'brightness', br);
%plottext(ax, sprintf("Magnitude reponses of filters (order = $%d$)", forder),...
   % { 'Lowpass filter', 'Bandpass filter', '$-6$ dB cutoffs'}, 'Frequency [Hz]', 'Amplitude [dB]', 'fontsize', 12, 'legendloc', 'best');
figsize(fig, 'u'); %try 's', 'm', 'b', 'o'/'r'
axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = 14;

xticks([]);
yticks([]);

ylim([-90 40]);
xlim([0 fshift(end)*1.05]);
%% Save image
location = GetPath2Images() + mfilename;
extension = "png";
SaveImage(fig, location, extension);
% close all;
