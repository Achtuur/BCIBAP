%% Show ASR using sine (doesnt really work lol)
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
[filtered_data, unfiltered_data] = LoadnFilter(path2edf, 'channellist', ChannelsOut, 'ASR', 1);
ch = 1;
filtered_data = filtered_data(ch,:); % take one channel
unfiltered_data = unfiltered_data(ch,:);
filsmall_piece = filtered_data(1, :);
unfilsmall_piece = unfiltered_data(1, :); %relatively clean data
yunfil = unfilsmall_piece;
yfil = filsmall_piece;
%% x axis
N = size(yunfil, 2);
t = linspace(0, N / Fs, N);

%% plot

fig = figure(1);
hold on;
ax(1) = plot(t, yunfil);
ax(2) = plot(t, yfil);
hold off;
plotline(ax, [1 1]);
plotcolor(ax(1), 'red');
plotcolor(ax(2), 'green');
plottext(ax, 'PSD of piece of (relatively clean) EEG data',...
    {'Unfiltered data', 'Bandpass filtered data (cutoffs at 0.5 and 50 Hz)'}, ...
    'Frequency [Hz]', 'Amplitude [dB]', 'fontsize', 8, 'legendloc', 'best');
figsize(fig, 'o'); %try 's', 'm', 'b', 'o'/'r'

%% Save image
location = GetPath2Images() + "pinknoiseplot";
extension = "eps";
SaveImage(fig, location, extension);
% close all;
