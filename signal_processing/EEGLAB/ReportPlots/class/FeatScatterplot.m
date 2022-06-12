%% example of scatter plot in 2d feature space
clear;
close all;
clc;

fig = openfig('ReportPlots/class/figs/PowerDeltavsPowerTheta.fig');

axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = 14;

axis = fig.Children;
leg = axis(1);
ax = axis(2).Children;
% % fig1 style
ax(1).Marker = '.';
ax(2).Marker = '.';
plotline(ax, 1);
br = 25;
plotcolor(ax(1), 'green', 'brightness', br);
plotcolor(ax(2), 'red', 'brightness', br);
plottext(ax, 'Scatterplot of seizure labels in a 2-D feature space.',...
    {'No seizure', 'Seizure'}, ...
    '$\delta$ Band Power', '$\theta$ Band Power', 'fontsize', 10, 'legendloc', 'northeast');
xlim([0 1]);
ylim([0 1]);
figsize(fig, 'o');
axis = gca;
axis.YAxisLocation = 'left';

%% save image
location = GetPath2Images(mfilename);
extension = "png"; % saved as png since eps is too large?
SaveImage(fig, location, mfilename, extension);