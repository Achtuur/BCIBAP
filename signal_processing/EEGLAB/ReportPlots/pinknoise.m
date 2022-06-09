%% Show pink noise (1/f noise)
%% init
% clc; clear; close all;

function pinknoise(locutoff, hicutoff, dwnsample, forder)
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
% dwnsample = 1;
[Fs, LabelsOut, ChannelsOut, rounding_err] = Label_extract2(path2summary, EpochDurationSeconds, FileIndices, dwnsample);
% ChannelsOut = ChannelsOut.index;
% locutoff = 0.5;
% hicutoff = 30;
[filtered_data, unfiltered_data] = LoadnFilter(path2edf, 'channellist', ...
    ChannelsOut.index, 'ASR', 0, 'downsample', dwnsample, ...
    'locutoff', locutoff, 'hicutoff', hicutoff, 'forder', forder);
ch = 6;
filtered_data = filtered_data(ch,:); % take one channel
unfiltered_data = unfiltered_data(ch,:);
filsmall_piece = filtered_data(1, 600000/dwnsample : 620000/dwnsample);
unfilsmall_piece = unfiltered_data(1, 600000 : 620000); %relatively clean data
yunfil = unfilsmall_piece;
Yunfil = fft(unfilsmall_piece, 20000*4);
yfil = filsmall_piece;
Yfil = fft(filsmall_piece, 20000*4);
%% x axis
N = size(Yunfil, 2);
t = linspace(0, N / Fs, N);
% f = linspace(0, Fs-(Fs/N), N); %0 to Fs
f = linspace(0, Fs/2, N/2); % -Fs/2 to Fs/2 (use with fftshift)
flog = logspace(0, log10(Fs/2), N/2); %logscale plot
n = 1 : 1 : N/2;

%% plot
c = 5000;
ypink = c./f;

% ypink = ypink(n);
Yfil = Yfil(n);
Yunfil = Yunfil(n);

ypink = mag2db(abs(ypink));
Yfil = mag2db(abs(Yfil));
Yunfil = mag2db(abs(Yunfil));

fig = figure();
hold on;
ax(1) = semilogx(f, Yunfil);
ax(2) = semilogx(f, Yfil);
ax(3) = semilogx(f, ypink);
hold off;
set(gca, 'XScale', 'log')
plotline(ax, [1 1 2]);
plotcolor(ax(1), 'red');
plotcolor(ax(2), 'green');
plotcolor(ax(3), 'purple');

if locutoff == 0 %lowpass
    fildata_legend = sprintf("Lowpass filtered data (cutoff at %.1f Hz)", hicutoff);
else %bandpass
    fildata_legend = sprintf("Bandpass filtered data (cutoffs at %.2f and %.2f Hz)", locutoff, hicutoff);
end

plottext(ax, 'PSD of piece of (relatively clean) EEG data',...
    {'Unfiltered data', fildata_legend, sprintf("Pink noise ($%d/f$)", c)}, ...
    'Frequency [Hz]', 'Amplitude [dB]', 'fontsize', 10, 'legendloc', 'best');
figsize(fig, 'o'); %try 's', 'm', 'b', 'o'/'r'


%% Save image
location = GetPath2Images() + mfilename;
extension = "eps";
SaveImage(fig, location, extension);
% close all;
