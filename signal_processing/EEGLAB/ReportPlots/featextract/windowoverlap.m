clc; clear; close all;

Fs = 128;
N = 1000; %4 epochs
x = rand(1, 4*N) - 0.5;
A = 0.75;

t = linspace(0, 4*N/Fs - 1/Fs, 4*N);
N = N/Fs;
windowX = [0, 0;
    N, N;
    0, N;
    0, N]';
windowY = [-A, A;
    -A, A
    A, A;
    -A, -A]';
nWindows = 4;
overlaps = [1 0.75];

fig = figure();
tiles = tiledlayout(2,1);
% nWindows * N * overlaps(1)
xdiff = N * 0.51;
%xlims = {[0 N*nWindows*overlaps(1)+5/Fs], [0 N*(nWindows+1)*overlaps(2)+5/Fs]};
xlims = {[0 N*nWindows*overlaps(1)+5/Fs], [0 N*nWindows*overlaps(1)+5/Fs]};
for o = 1:length(overlaps)
nexttile;
hold on;
br = 25;
ax(1) = plot(t, x);
ax(2) = line([1000 1000], [1000 1000], 'LineStyle', '--'); %hidden line for legend
plotcolor(ax(2), 'black', 'brightness', br);
drawArrow = @(x,y, varargin) quiver( x(1),y(1),x(2)-x(1),y(2)-y(1),0, varargin{:});
clr = {'purple', 'red', 'orange', 'cyan'};
for n = 0:nWindows-1
    if overlaps(o) ~= 1
%        ypl = 0.1*A * (-1)^n;
    ypl = 0;
    else
        ypl = 0;
    end
    xshift = n*(N*overlaps(o));
    ax(3+4*n : 6 + 4*n) = line(windowX + xshift, windowY + ypl, 'LineStyle', '--');
    text(xshift + N/2 - 0.15*N, A*1.2 * (-1)^n, sprintf("Window %d", n+1));

    cl = plotcolor(ax(3+4*n : 6 + 4*n), clr{n+1}, 'colordiff', 0, 'brightness', br);
    drawArrow([xshift+0.125*N, 0.02*N + xshift], ...
        [1 1]*A*1.2 * (-1)^n, 'Color', cl, 'LineWidth', 2); % arrow pointing left
    drawArrow([xshift+N-0.125*N, -0.02*N + N + xshift], ...
        [1 1]*A*1.2 * (-1)^n, 'Color', cl, 'LineWidth', 2); % arrow pointing right
end

hold off;
plotline(ax(1), 1);
plotline(ax(2:end), 2);
plotcolor(ax(1), 'green', 'brightness', br);

xdiff = N * 0.31;
xlim(xlims{o});
ylim([-1 1]);
axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = 14;
title(sprintf("Window overlap = %.1f\\%%", (1-overlaps(o))*100), 'interpreter', 'latex');
end

title(tiles, 'Example of overlapping windows on an arbitrary signal', 'interpreter', 'latex', 'fontsize', 19);
xlabel(tiles, 'Time [s]', 'interpreter', 'latex', 'fontsize', 19);
ylabel(tiles, 'Amplitude [arbitrary unit]', 'interpreter', 'latex', 'fontsize', 19);
legend({'Arbitrary signal', 'Windows'}, 'location', 'none', 'Position', [0.7324,0.4347,0.1722,0.08281]);
figsize(fig, 'o');
%% Save image
location = GetPath2Images(mfilename);
extension = "png";
SaveImage(fig, location, mfilename, extension);
% close all;