clc; clear;
eegpath = AddPath();
dataset = 'chb03';
path2dataset = eegpath + "sample_data/" + dataset;
FileIndices = SeizFileIndices(dataset);
EpochLengthSec = 3;
path2summary = path2dataset + "/" + dataset + "-summary.txt";
FileIndicesstr = "01";
path2edf = path2dataset + "/" + dataset + "_" + FileIndicesstr + ".edf";

[featuresWavelet, featurelabelsWavelet, features, featurelabels, labels] = getFeatures(dataset, path2dataset, FileIndices, EpochLengthSec);

 %% normalise features
featuresWavelet = NormalizeFeat(featuresWavelet);
features = NormalizeFeat(features);

[features_outFourier, iFourier,explainedFourier, latentFourier] = FeatSelectionPCA(features, 100);
[features_outWavelet, iWavelet,explainedWavelet, latentWavelet] = FeatSelectionPCA(featuresWavelet, 100);

% trick to make it seem like they start at 0
explainedWavelet = [-99; explainedWavelet];
latentWavelet = [0; latentWavelet];

explainedFourier = [-99; explainedFourier];
latentFourier = [0; latentFourier];
leftylim = [0 0.55];
rightylim = [0 1];

fig = figure();
t = tiledlayout(1,2);
axbrightness = -25/255;
nexttile;
% % Plot in tiles
hold on;
yyaxis left;
ax(1) = bar(explainedFourier./100);
ylabel('Explained individual variance ratio [ ]','interpreter', 'latex', 'fontsize',17)
ylim(leftylim)
yyaxis right;
ax(2) = stairs(cumsum(latentFourier)/sum(latentFourier));
ylim(rightylim)
hold off;
xlim([1 length(explainedFourier)]);

title('Fourier Transform features','interpreter' ,'latex','fontsize', 18,'FontWeight','bold');
% legend({'Individual explained variance', 'Cumulative explained variance'}, 'interpreter', 'latex', ...
%     'fontsize', 8, 'location', 'none', 'Position', [0.1347 0.4980 0.2022 0.0523]);
axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = 14;

barcolor = plotcolor(ax(1), 'green');
axis.YAxis(1).Color = barcolor + axbrightness;

cumsumcolor = plotcolor(ax(2), 'red');
axis.YAxis(2).Color = cumsumcolor + axbrightness;
plotline(ax(2), 2);

nexttile;
hold on;
yyaxis left;
ax(1) = bar(explainedWavelet./100);
ylim(leftylim)
yyaxis right;
ylabel('Explained cumulative variance ratio [ ]','interpreter', 'latex', 'fontsize', 17)
ylim(rightylim)
ax(2) = stairs(cumsum(latentWavelet)/sum(latentWavelet));
hold off;

xlim([1 length(explainedWavelet)]);
title('Wavelet features','interpreter' ,'latex','fontsize', 18,'FontWeight','bold');
legend({'Individual explained variance', 'Cumulative explained variance'}, 'interpreter', 'latex', ...
    'fontsize', 8, 'location', 'none', 'Position', [0.7020    0.0180    0.2022    0.0523])
axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = 14;

barcolor = plotcolor(ax(1), 'green');
axis.YAxis(1).Color = barcolor + axbrightness;

cumsumcolor = plotcolor(ax(2), 'red');
axis.YAxis(2).Color = cumsumcolor + axbrightness;
plotline(ax(2), 2);

% % Specify common title, X and Y labels
title(t, 'Explained variance of principal components with two feature extraction methods','interpreter', 'latex','fontsize', 18)
xlabel(t, 'Principal component index [ ]', 'interpreter',  'latex','fontsize',17)

figsize(fig, 'o'); %try 's', 'm', 'b', 'o'/'r'
%% Save image
location = GetPath2Images() + mfilename;
extension = "eps";
SaveImage(fig, location, extension);

