%% Show performance of ASR (no ASR done here for comparison)

% clc; clear; close all;
function showseizure(locutoff, hicutoff, dwnsample, forder)
if ~exist('locutoff', 'var') %snippet in order to run this file separately
    locutoff = 0.5;
    hicutoff = 30;
    dwnsample = 2;
    forder = 30;
end
    showSeizure2(0, forder, locutoff, hicutoff, dwnsample); %no ASR
    showSeizure2(1, forder, locutoff, hicutoff, dwnsample); %yes ASR
end
function showSeizure2(ASR, forder, locutoff, hicutoff, dwnsample)
    %% init
    eegpath = AddPath();
    dataset = 'chb03';
    path2dataset = eegpath + "sample_data/" + dataset;
    FileIndices = 1;
    EpochDurationSeconds = 3;
    path2summary = path2dataset + "/" + dataset + "-summary.txt";
    FileIndicesstr = sprintf("0%d", FileIndices);
    path2edf = path2dataset + "/" + dataset + "_" + FileIndicesstr + ".edf";

    %% get data
    [Fs, LabelsOut, ChannelsOut, ~] = Label_extract2(path2summary, EpochDurationSeconds, FileIndices, dwnsample);
    ChannelsOut = ChannelsOut.index;
    [filtered_data, unfiltered_data] = LoadnFilter(path2edf, 'channellist', ChannelsOut, 'ASR', ASR, ...
    'locutoff', locutoff, 'hicutoff', hicutoff, 'forder', forder, 'downsample', dwnsample);

    ch = 1;
    filtered_data = filtered_data(ch,:); % take one channel
    unfiltered_data = unfiltered_data(ch,:);
    filsmall_piece = filtered_data(:, :);
    unfilsmall_piece = unfiltered_data(:, :); %relatively clean data
    yunfil = unfilsmall_piece;
    yfil = filsmall_piece;

    seizline = -750;
    noseiz = LabelsOut{1,2};
    noseiz(noseiz ~= 0) = NaN;
    noseiz(noseiz == 0) = seizline;
    seiz = LabelsOut{1,2};
    seiz(seiz ~= 1) = NaN;
    seiz(seiz == 1) = seizline;
    for k = 1:length(seiz) % extend epochs to length of time vector
       o = floor(Fs*EpochDurationSeconds);
       temp1((k-1) * o + 1 : k * o) = noseiz(k);
       temp2((k-1) * o + 1 : k * o) = seiz(k);
    end
    noseiz = temp1;
    seiz = temp2;
    clear temp1 temp2;

    %% x axis
    N = size(yunfil, 2);
    t = linspace(0, N / Fs, N);
    mintime = 110;
    maxtime = 680;
    t(t < mintime) = NaN;
    t(t > maxtime) = NaN;
    n = find(~isnan(t)); % get indices
    noseiz = noseiz(n);
    seiz = seiz(n);
    yfil = yfil(n);
    yunfil = yunfil(n);
    t = t(n);

    %% plot

    fig = figure();
    hold on;
    ax(1) = plot(t, yunfil);
    ax(2) = plot(t, yfil);
    ax(3) = plot(t, noseiz);
    ax(4) = plot(t, seiz);
    hold off;
    
    if ASR
       leg = {'Unfiltered data', 'filtered data and performed ASR', 'No seizure', 'Seizure'};
    else
       leg = {'Unfiltered data', "filtered data", 'No seizure', 'Seizure'};
    end
    
    plotline(ax, [1 1 3 3]);
    plotcolor(ax(1), 'red');
    plotcolor(ax(2), 'green');
    plotcolor(ax(3), 'purple');
    plotcolor(ax(4), 'orange');
    plottext(ax, 'EEG data including an epileptic seizure', leg, ...
        'Time [$s$]', 'Voltage [$\mu V$]', 'fontsize', 10, 'legendloc', 'northeast');
    figsize(fig, 'o'); %try 's', 'm', 'b', 'o'/'r'

    perclim = 0.05; %percentage of limit that is taken extra/reduced
    ylim([-abs(seizline) abs(seizline)] * (1 + perclim))
    xlim([mintime maxtime] .* [1+perclim 1-perclim]);

    %% Save image
    if ASR
        fname = mfilename + "ASR";
    else
        fname = mfilename + "noASR";
    end
    location = GetPath2Images(mfilename);
    extension = "eps";
    SaveImage(fig, location, fname, extension);
%     close all;
end
