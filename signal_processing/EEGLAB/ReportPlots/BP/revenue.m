clc;
clear;
close all;

money = load('ReportPlots/BP/totalmoney.mat');

expenses = money.expenses_cum;
rev = money.revenue_cum;
ydata = (rev-expenses)/10^6;
xdata = 2022:1:2022+length(expenses)-1;

fig = figure();
hold on;
ax(1) = bar(xdata, ydata);
% ax(2) = plot(xdata, expenses);
hold off;
plotline(ax, 2);
br = 25;
plotcolor(ax(1), 'tudelft', 'brightness', br);
% plotcolor(ax(2), 'green', 'brightness', br);
xdif = 0.075*(xdata(end) - xdata(1));
xlim([xdata(1)-xdif xdata(end)+xdif]);
ylim([min(ydata) max(ydata)]*1.1);
figsize(fig, 'o');
bartext(xdata, ydata); 
addgrid('X', 0, 'Y', 1);
plottext(ax, 'Revenue after Expenses', {'Yearly Net Flow'}, 'Year', 'Euros (Millions)', 'fontsize', 12, 'legendloc', 'northwest');
%% Save image
location = GetPath2Images(mfilename);
extension = "eps";
SaveImage(fig, location, mfilename, extension);
% close all;
