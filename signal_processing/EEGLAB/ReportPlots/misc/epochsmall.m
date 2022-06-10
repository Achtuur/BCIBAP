clc; clear; close all;
Fs = 128;
epochlengthsec = 3;
nep = 7;
N = Fs*epochlengthsec * nep; %4 epochs
x = rand(1, N);
t = linspace(0, N/Fs, N);
ep = epochlengthsec : epochlengthsec : epochlengthsec*nep;

fig = figure();
hold on;
ax(1) = plot(t, x);
ax(2:2+nep-1) = xline(ep, '--');

hold off;
plotline(ax(1), 0.5);
plotline(ax(2:end), 2);
br = 25;
plotcolor(ax(1), 'orange', 'brightness', br);
plotcolor(ax(2), 'black', 'brightness', br);
xdiff = t(end) * 0.2;
xlim([t(500) t(end)-xdiff]);
ylim([-1 2]);
xticks([]);
yticks([]);
figsize(fig, 'u');
%% Save image
location = GetPath2Images(mfilename);
extension = "png";
SaveImage(fig, location, mfilename, extension);
% close all;