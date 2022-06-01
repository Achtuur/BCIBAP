%% Compare lowpass vs bandpass
%% init
clc; clear; close all;
eegpath = AddPath();
dataset = 'chb03';
path2dataset = eegpath + "sample_data/" + dataset;
FileIndices = 1;
EpochDurationSeconds = 3;
path2summary = path2dataset + "/" + dataset + "-summary.txt";
FileIndicesstr = "01";
path2edf = path2dataset + "/" + dataset + "_" + FileIndicesstr + ".edf";

%% get data
[Fs, LabelsOut, ChannelsOut, rounding_err] = Label_extract2(path2summary, EpochDurationSeconds, FileIndices);
ChannelsOut = ChannelsOut.index;
locutoff = 0;
hicutoff = 30;
[lowpass_filtered_data, lowpass_unfiltered_data] = LoadnFilter(path2edf, 'channellist', ChannelsOut, 'ASR', 0, ...
                                                    'locutoff', locutoff, 'hicutoff', hicutoff, 'forder', 30);
locutoff = 0.25;
[bandpass_filtered_data, bandpass_unfiltered_data] = LoadnFilter(path2edf, 'channellist', ChannelsOut, 'ASR', 0, ...
                                                    'locutoff', locutoff, 'hicutoff', hicutoff, 'forder', 30);

ch = 6;
lowpass_filtered_data = lowpass_filtered_data(ch,:); % take one channel
bandpass_filtered_data = bandpass_filtered_data(ch,:);
lowpass_small_piece = lowpass_filtered_data(1, 600000 : 620000);
bandpass_small_piece = lowpass_unfiltered_data(1, 600000 : 620000); %relatively clean data
y_low = bandpass_small_piece;
y_band = lowpass_small_piece;
%% x axis
N = size(y_low, 2);
t = linspace(0, N / Fs, N);

%% plot
fig = figure(1);
hold on;
ax(1) = plot(t, y_low);
ax(2) = plot(t, y_band);
hold off;
plotline(ax, [1 1]);
plotcolor(ax(1), 'red');
plotcolor(ax(2), 'green');

low_legend = sprintf("Lowpass filtered data (cutoff at %.1f Hz)", hicutoff);
band_legend = sprintf("Bandpass filtered data (cutoffs at %.2f and %.2f Hz)", locutoff, hicutoff);


plottext(ax, 'PSD of piece of (relatively clean) EEG data',...
    {low_legend, band_legend}, ...
    'Time [$s$]', 'Voltage [$\mu V$]', 'fontsize', 10, 'legendloc', 'best');
figsize(fig, 'o'); %try 's', 'm', 'b', 'o'/'r'


%% Save image
location = GetPath2Images() + mfilename;
extension = "eps";
SaveImage(fig, location, extension);
% close all;
