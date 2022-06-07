clear;
close all;
clc;

t = linspace(0, 16*pi, 3000);
% y1 = sin(t);
% y2 = cos(t);
% y3 = -sin(t);
% y4 = -cos(t);
% y5 = tan(t);
% y6 = -tan(t);
y = @(phi) 0.8*rand(1, length(t)) + cos(t + phi);

r = 2*rand(1, 6);
y1 = 15 + y(r(1));
y2 = 12 + y(r(2));
y3 = 9 + y(r(3));
y4 = 6 + y(r(4));
y5 = 3 + y(r(5));
y6 = y(r(6));

fig = figure(1);
hold on;
ax(1) = plot(t,y1);
ax(2) = plot(t,y2);
ax(3) = plot(t,y3);
ax(4) = plot(t,y4);
ax(5) = plot(t,y5);
ax(6) = plot(t,y6);
hold off;

plotline(ax, 1.5);
plotcolor(ax(1), 'green', 'colordiff', 0);
plotcolor(ax(2), 'purple');
plotcolor(ax(3), 'red');
plotcolor(ax(4), 'orange');
plotcolor(ax(5), 'cyan');
plotcolor(ax(6), 'magenta');
plottext(ax, 'title', {'legend1', 'legend2', 'legend3', 'legend4', 'legend5', 'legend6'}, ...
    'Time [$s$]', 'Voltage [$V$]', 'fontsize', 10, 'legendloc', 'northeast');
figsize(fig, 'o'); %try 'm', 'b', 'o'/'r'
xlim([t(1) t(end)]);
% ylim([-1 10]);

%% Save image
% location = "./images/exampleimage"; %folder + filename without extension
% extension = ".png";
% SaveImage(fig, location, extension);

