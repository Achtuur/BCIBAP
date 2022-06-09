%%fig 1
clc; clear; close all;
fig = openfig('ReportPlots/figs/loss.fig');

axis = fig.Children;
leg = axis(1);
ax = axis(2).Children;
% % fig1 style
plotline(ax, 2);
br = 25;
plotcolor(ax(1), 'green', 'brightness', br);
plotcolor(ax(2), 'purple', 'brightness', br);
plottext(ax, 'Min objective vs Number of function evaluations',...
    {'Min observed objective', 'Estimated min objective'}, ...
    'Function Evaluations', 'Min Objective', 'fontsize', 10, 'legendloc', 'northeast');
% xdiff = 0%length(x1) * 0;
% xlim([0-xdiff length(x1)+xdiff]);
% ylim([0 0.]);
figsize(fig, 'o');

%% fig 2
clc; clear; close all;
fig = openfig('ReportPlots/figs/Iguess.fig');

axis = fig.Children;
leg = axis(1);
%% fig2 style
plotline(ax, 2);
br = 25;
plotcolor(ax(1), 'green', 'brightness', br);
plotcolor(ax(2), 'purple', 'brightness', br);
% xdiff = 0%length(x1) * 0;
% xlim([0-xdiff length(x1)+xdiff]);
% ylim([0 1.5]);
figsize(fig, 'o');
