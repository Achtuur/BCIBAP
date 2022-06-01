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

%% get epochs
[unfil_epochs, L] = DivideInEpochs(unfiltered_data, Fs, EpochDurationSeconds);
[fil_epochs, L] = DivideInEpochs(filtered_data, Fs, EpochDurationSeconds);
N = 4;
i_noseiz = find(LabelsOut{1,2} == 0, N, 'first');
i_seiz = find(LabelsOut{1,2} == 1, N , 'first');

for k = 1:size(fil_epochs,1)
   temp = fil_epochs{k}(i_noseiz, :);
   noseiz_filepoch(k,:) = temp(:)'; %collapse into row vector
   
   temp = fil_epochs{k}(i_seiz, :);
   seiz_filepoch(k,:) = temp(:)'; %collapse into row vector
   
   temp = unfil_epochs{k}(i_noseiz, :);
   noseiz_unfilepoch(k,:) = temp(:)'; %collapse into row vector
   
   temp = unfil_epochs{k}(i_seiz, :);
   seiz_unfilepoch(k,:) = temp(:)'; %collapse into row vector
end

%% x axis
% N = size(yunfil, 2);
t = linspace(0, N*L / Fs, L*N);
t_epoch = EpochDurationSeconds : EpochDurationSeconds : t(end)-1;

%% plot
fig = figure(1);
figsize(fig, 's'); %try 's', 'm', 'b', 'o'/'r'

plotnChannels = 4;
plotnChannels = min(max(plotnChannels, 1), 9); %force 0 < nChannels < 10

tiles = tiledlayout(plotnChannels, 2);
ChannelString = ChannelsOut.label;

colororder({'black','black'}) %make both y labels black
for k = 1:2*plotnChannels
    nexttile
    i = ceil(k/2);
    if mod(k, 2) %odd -> show no seizure
        yunfil(1,:) = noseiz_unfilepoch(i,:);
        yfil(1,:) = noseiz_filepoch(i,:);
        if i == 1
           title("No seizure"); 
        end
    else %even -> show seizure
        yunfil(1,:) = seiz_unfilepoch(i,:);
        yfil(1,:) = seiz_filepoch(i,:);
        if i == 1
           title("Seizure"); 
        end
    end
    hold on;
    ax(1) = plot(t, yunfil(1, :));
    ax(2) = plot(t, yfil(1, :));
    ax(3:3+N-2) = xline(t_epoch, '-.')';
    hold off;
    plotline(ax, 1);
    plotcolor(ax(1), 'red');
    plotcolor(ax(2), 'green');
    plotcolor(ax(3:end), 'black', 'colordiff', 0);
        
    yyaxis right;
    ylabel(ChannelString{i}, 'Rotation', 0, 'VerticalAlignment','middle', 'HorizontalAlignment','left');
    yticks([])
    
    yyaxis left;
    xlim([t(1) t(end)]); %full signal visible
    ylim([-400 400]); %visual inspection
end

title(tiles, "A few epochs of EEG data from some channels around the ear", 'interpreter', 'latex', 'fontsize', 18); %add title
legend({'Unfiltered data', 'Pre-processed data', 'Epoch separator'}, ...
                'location', 'best', 'Position', [0.7333, 0.0289, 0.1731, 0.0548]);
xlabel(tiles, 'Time [$s$]', 'interpreter', 'latex', 'fontsize', 18)
yyaxis left;
ylabel(tiles, 'Voltage [$\mu V$]', 'interpreter', 'latex', 'fontsize', 18); %add xlabel
fig.Position = fig.Position + [0 0 0 100]; %stretch figure in height

%% Save image
location = GetPath2Images() + mfilename;
extension = "eps";
SaveImage(fig, location, extension);
% close all;
