%% Show artefacts (EMG, 60 Hz power and ECG)
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
[filtered_data, unfiltered_data] = LoadnFilter(path2edf, 'channellist', ChannelsOut);

filtered_data = filtered_data(1,:); % take one channel
unfiltered_data = unfiltered_data(1,:);
filsmall_piece = filtered_data(1, :);
unfilsmall_piece = unfiltered_data(1, :); %relatively clean data
yunfil = unfilsmall_piece;
Yunfil = fft(unfilsmall_piece);
yfil = filsmall_piece;
Yfil = fft(filsmall_piece);
%% x axis
N = size(yunfil, 2);
t = linspace(0, N / Fs, N);
% f = linspace(0, Fs-(Fs/N), N); %0 to Fs
f = linspace(0, Fs/2, N/2); % -Fs/2 to Fs/2 (use with fftshift)
flog = logspace(0, log10(Fs/2), N/2); %logscale plot
n = 1 : 1 : N/2;

%% plot
c = 10000;
ypink = c./f;

% ypink = ypink(n);
Yfil = Yfil(n);
Yunfil = Yunfil(n);

ypink = mag2db(abs(ypink));
Yfil = mag2db(abs(Yfil));
Yunfil = mag2db(abs(Yunfil));

fig = figure(1);
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
plottext(ax, 'PSD of piece of (relatively clean) EEG data',...
    {'Unfiltered data', 'Bandpass filtered data (cutoffs at 0.5 and 50 Hz)', sprintf("$%d/f$ (pink noise)", c)}, ...
    'Frequency [Hz]', 'Amplitude [dB]', 'fontsize', 8, 'legendloc', 'best');
figsize(fig, 'o'); %try 's', 'm', 'b', 'o'/'r'


%% Save image
location = GetPath2Images() + mfilename;
extension = "eps";
SaveImage(fig, location, extension);
% close all;
