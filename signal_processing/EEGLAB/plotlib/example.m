t = linspace(0, 2*pi, 1000);
y1 = sin(t);
y2 = cos(t);
y3 = -sin(t);

fig = figure(1);
hold on;
ax(1) = plot(t,y1);
ax(2) = plot(t,y2);
ax(3) = plot(t,y3);
hold off;

plotline(ax, [3 2]);
plotcolor(ax(1:2), 2);
plotcolor(ax(3), 'tudelft');
plottext(ax, 'title', {'legend1', 'legend2', 'legend3'}, 'Time [$s$]', 'Voltage [$V$]', 'fontsize', 10, 'legendloc', 'northeast');
figsize(fig, 'o'); %try 'm', 'b', 'o'/'r'
xlim([0 2*pi]);
ylim([-1 1]);

%% Save image
location = "./images/exampleimage"; %folder + filename without extension
extension = ".png";
SaveImage(fig, location, extension);

