%% Show performance of ASR (no ASR done here for comparison)

clc; clear; close all;
forder = 10:4:50;
% 
% for k = forder
%    showSeizure(1, k); 
% end

%forder 30 for ASR
showSeizure(0, 30); %no ASR
showSeizure(1, 30); %yes ASR

function showSeizure(ASR, forder)
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
    [Fs, LabelsOut, ChannelsOut, ~] = Label_extract2(path2summary, EpochDurationSeconds, FileIndices);
    ChannelsOut = ChannelsOut.index;
    [filtered_data, unfiltered_data] = LoadnFilter(path2edf, 'channellist', ChannelsOut, 'ASR', ASR, ...
                                                    'locutoff', 0.25, 'hicutoff', 30, 'forder', forder);

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
        'Time [S]', 'Voltage [$\mu V$]', 'fontsize', 8, 'legendloc', 'northeast');
    figsize(fig, 'o'); %try 's', 'm', 'b', 'o'/'r'

    perclim = 0.05; %percentage of limit that is taken extra/reduced
    ylim([-abs(seizline) abs(seizline)] * (1 + perclim))
    xlim([mintime maxtime] .* [1+perclim 1-perclim]);

    %% Save image
    if ASR
        location = GetPath2Images() + mfilename + "ASR";
    else
        location = GetPath2Images() + mfilename + "noASR";
    end
    extension = "eps";
    SaveImage(fig, location, extension);
%     close all;
end
