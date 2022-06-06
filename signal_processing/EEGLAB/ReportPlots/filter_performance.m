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
forder = 6:12:200;
runs = 3;
time = zeros(runs, length(forder));
[Fs, LabelsOut, ChannelsOut, rounding_err] = Label_extract2(path2summary, EpochDurationSeconds, FileIndices, downsample);
ChannelsOut = ChannelsOut.index;
locutoff = 0.5;
hicutoff = 40;
for i = 1:runs
    fprintf("Run %d", i);
    for j = 1:length(forder)
        t = tic;
        [filtered_data, unfiltered_data, filt_coeff] = LoadnFilter(path2edf, 'channellist', ...
            ChannelsOut, 'ASR', 0, 'downsample', downsample, ...
            'locutoff', locutoff, 'hicutoff', hicutoff, 'forder', forder(j));
        time(i, j) = toc(t);
    end
end
%% Get axis data
x = forder;
y = mean(time);
% y = time;
%% plot
fig = figure(1);
linestyle = '-.';
hold on;
ax = plot(x, y, '+');
hold off;

plotline(ax, 1);
br = 5;
plotcolor(ax, 'green', 'colordiff', br);
% plotcolor(ax(2:4), 'purple', 'colordiff', 0, 'brightness', 25);
plottext(ax, "Computation time for filtering with differing filter orders",...
    {''}, 'Filter order []', 'Computation Time [s]', 'fontsize', 10, 'legendloc', 'best');
figsize(fig, 'o'); %try 's', 'm', 'b', 'o'/'r'
axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = 14;

% ylim([-90 50]);
% xlim([0 75]);
%% Save image
location = GetPath2Images() + mfilename;
extension = "eps";
SaveImage(fig, location, extension);
% close all;
