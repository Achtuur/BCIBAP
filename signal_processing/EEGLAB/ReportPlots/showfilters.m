%% Show ASR using sine (doesnt really work lol)
%% init
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
downsample = 1;
[Fs, LabelsOut, ChannelsOut, rounding_err] = Label_extract2(path2summary, EpochDurationSeconds, FileIndices, downsample);
ChannelsOut = ChannelsOut.index;
forder = 30;
locutoff = 0;
hicutoff = 40;
[filtered_data, unfiltered_data, lowpassfilt_coeff] = LoadnFilter(path2edf, 'channellist', ...
    ChannelsOut, 'ASR', 0, 'downsample', downsample, ...
    'locutoff', locutoff, 'hicutoff', hicutoff, 'forder', forder);

locutoff = 0.5;
[filtered_data, unfiltered_data, bandpassfilt_coeff] = LoadnFilter(path2edf, 'channellist', ...
    ChannelsOut, 'ASR', 0, 'downsample', downsample, ...
    'locutoff', locutoff, 'hicutoff', hicutoff, 'forder', forder);


%% Get axis data
N = 5000;
%x
f = linspace(0, Fs, N);
fshift = linspace(-Fs/2, Fs/2 - Fs/2/N, N);

%y
Z_low = fftshift(fft(lowpassfilt_coeff, N));
Z_low = mag2db(abs(Z_low));
Z_band = fftshift(fft(bandpassfilt_coeff, N));
Z_band = mag2db(abs(Z_band));
% take only x > 0 (real valued so symmetrical)
n = find(fshift >= 0);
fshift = fshift(n);
Z_low = Z_low(n);
Z_band = Z_band(n);
locut = fshift(find(Z_band > -6, 1));
%% plot
fig = figure(1);
linestyle = '-.';
hold on;
ax(1) = plot(fshift, Z_low);
ax(2) = plot(fshift, Z_band);
ax(3) = line([locut locut], [-1000 -6], 'LineStyle', linestyle); %xline at low cutoff
ax(4) = line([hicutoff hicutoff], [-1000 -6], 'LineStyle', linestyle); %x line at high cutoff
ax(5) = line([locut hicutoff], [-6 -6], 'LineStyle', linestyle); %line between hi and low cutoff
hold off;
textdist = locut - locut*0.88;
text(locut - textdist, -40, sprintf("$f_l = %.1f$ Hz", locut), 'fontsize', 13, 'interpreter', 'latex',...
    'Rotation',90, 'VerticalAlignment','middle', 'HorizontalAlignment','right');
text(hicutoff - textdist, -40, sprintf("$f_h = %.1f$ Hz", hicutoff), 'fontsize', 13, 'interpreter', 'latex',...
    'Rotation',90, 'VerticalAlignment','middle', 'HorizontalAlignment','right');
plotline(ax, [2 2 1.5 1.5 1.5]);
br = 25;
plotcolor(ax(1), 'green', 'colordiff', br);
plotcolor(ax(2), 'red', 'colordiff', br);
plotcolor(ax(3:5), 'purple', 'colordiff', 0, 'brightness', 25);
plottext(ax, sprintf("Magnitude reponses of filters (order = $%d$)", forder),...
    { 'Lowpass filter', 'Bandpass filter', '$-6$ dB cutoffs'}, 'frequency [Hz]', 'Amplitude [dB]', 'fontsize', 10, 'legendloc', 'best');
figsize(fig, 'o'); %try 's', 'm', 'b', 'o'/'r'
axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = 14;

ylim([-90 50]);
xlim([0 75]);
%% Save image
location = GetPath2Images() + mfilename;
extension = "eps";
SaveImage(fig, location, extension);
% close all;
