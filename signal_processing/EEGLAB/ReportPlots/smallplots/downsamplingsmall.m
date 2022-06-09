clc;
clear;
close all;
Fs = 256;
N = 1000;
x = triang(N);
dsf = 2; %downsampling factor
x1 = [x; zeros(N * (dsf-1), 1); x]; %not downsampeld
x2 = repmat(x, [dsf+1, 1]) * 1/dsf;%downsampled

fig = figure();
hold on;
ax(1) = plot(x1);
ax(2) = plot(x2);
hold off;
plotline(ax, 2);
br = 25;
plotcolor(ax(1), 'green', 'brightness', br);
plotcolor(ax(2), 'purple', 'brightness', br);
xdiff = length(x1) * 0;
xlim([0-xdiff length(x1)+xdiff]);
ylim([0 1.5]);
xticks([]);
yticks([]);
figsize(fig, 'u');
%% Save image
location = GetPath2Images() + mfilename;
extension = "png";
SaveImage(fig, location, extension);
% close all;
