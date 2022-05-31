%% Show used channels (filtered & unfiltered)
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

[filtered_data, unfiltered_data] = LoadnFilter(path2edf, 'channellist', ChannelsOut.index, 'ASR', 1, ...
                                                    'locutoff', 0.33, 'hicutoff', 30, 'forder', 30);

filsmall_piece = filtered_data(:, 1 : 70000);
unfilsmall_piece = unfiltered_data(:, 1 : 70000);
yunfil = unfilsmall_piece;
Yunfil = fft(unfilsmall_piece);
yfil = filsmall_piece;
%% x axis
N = size(yunfil, 2);
t = linspace(0, N / Fs, N);

%% plot
fig = figure(1);
figsize(fig, 's'); %try 's', 'm', 'b', 'o'/'r'
tiles = tiledlayout(length(ChannelsOut.index), 1);
ChannelString = ChannelsOut.label;

colororder({'black','black'}) %make both y labels black
for k = 1:length(ChannelsOut.index)
    nexttile
    hold on;
    ax(1) = plot(t, yunfil(k, :));
    ax(2) = plot(t, yfil(k, :));
    hold off;
    plotline(ax, [1 2]);
    plotcolor(ax(1), 'red');
    plotcolor(ax(2), 'green');
        
    yyaxis right;
    ylabel(ChannelString{k}, 'Rotation', 0, 'VerticalAlignment','middle', 'HorizontalAlignment','left');
    yticks([])
    
    yyaxis left;
    xlim([t(1) t(end)]); %full signal visible
    ylim([-400 400]); %visual inspection
end

title(tiles, "Segment of EEG data from channels around the ear", 'interpreter', 'latex', 'fontsize', 18); %add title
legend({'Unfiltered data', 'Filtered data'}, ...
                'location', 'none', 'Position', [0.7604,0.05479,0.1432,0.03253]);
xlabel(tiles, 'Time [$s$]', 'interpreter', 'latex', 'fontsize', 18)
yyaxis left;
ylabel(tiles, 'Voltage [$\mu V$]', 'interpreter', 'latex', 'fontsize', 18); %add xlabel
fig.Position = fig.Position + [0 0 0 300]; %stretch figure in height

%% Save image
location = GetPath2Images() + mfilename;
extension = "png";
SaveImage(fig, location, extension);
% close all;
