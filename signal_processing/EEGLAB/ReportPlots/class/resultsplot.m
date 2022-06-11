%% 1 channel
clc; clear; close all;
 
RF1_wav = [99.5, 80.0; %random forest wavelet 1 channel
    99.6, 66.7;
    99.2, 38.5;
    99.5, 84.2;
    99.8, 0;
    98.9, 18.2;
    96.2, 32.3;
    99.6, 55.6;
    99.9, 93.8];
x0 = ones(9, 1) * 0;

RF1_FT = [99.5, 73.3; %random forest fourier 1 channel
    99.6, 77.8;
    99.5, 53.8;
    99.3, 78.9;
    99.8, 0;
    99.0, 9.1;
    97.7, 64.5;
    99.7, 66.7;
    99.9, 87.5];
x1 = ones(9, 1) * 1;

SVM1_wav = [99.9, 93.3; %SVM wavelet 1 channel (NUMBERS NOT CORRECT YET)
    99.7, 77.8;
    99.6, 61.5;
    99.7, 94.7;
    99.8, 0.0;
    100, 100;
    97.3, 48.4;
    99.8, 88.9;
    99.8, 87.5];
x2 = ones(9, 1) * 2;

SVM1_FT = [99.9, 93.3; %SVM fourier 1 channel (NUMBERS NOT CORRECT YET)
    99.7, 77.8;
    99.6, 61.5;
    99.7, 94.7;
    99.8, 0.0;
    100, 100;
    97.3, 48.4;
    99.8, 88.9;
    99.8, 87.5];
x3 = ones(9, 1) * 3;

NN1_wav = [99.2, 67.6; %NN wavelet 1 channel 99% PCA
    99.6, 73.1;
    99.0, 6.9;
    99.1, 77.4;
    99.8, 0.0;
    99.1, 35.1;
    96.1, 33.1;
    99.3, 42.3;
    99.9, 90.3];
x4 = ones(9, 1) * 4;

NN1_FT = [99.3, 74.2; %NN fourier 1 channel 99% PCA
    99.7, 29.4;
    99.6, 19.2;
    99.7, 78.4;
    99.8, 0.0;
    100, 21.6;
    97.3, 53.4;
    99.8, 57.7;
    99.8, 89];
x5 = ones(9, 1) * 5;

AorS = 2; %Set this var to 1 to plot accuracy, 2 to plot sensitivity

if AorS == 1
    tit = "Comparison of accuracy results for different ML models and features";
    ylab = "Accuracy in \%";
else
    AorS = 2; %ensure it is 2
    tit = "Comparison of sensitivity results for different ML models and features";
    ylab = "Sensitivity in \%";
end

avg = [mean(RF1_wav); mean(RF1_FT); mean(SVM1_wav); mean(SVM1_FT); mean(NN1_wav); mean(NN1_FT)];
avg = avg(:, AorS); %take accuracy or sensitivity
xavg = 0 : 5;

fig = figure();
hold on;

ax(1) = plot(-100, -100, 'x'); %plotting invisible o and x for legend hack
ax(2) = plot(-100, -100, 'o');
ax(3) = plot(xavg, avg);

ax(4) = plot(x0, RF1_wav(:, AorS), 'x');
ax(5) = plot(x1, RF1_FT(:, AorS), 'o');
ax(6) = plot(x2, SVM1_wav(:, AorS), 'x');
ax(7) = plot(x3, SVM1_FT(:, AorS), 'o');
ax(8) = plot(x4, NN1_wav(:, AorS), 'x');
ax(9) = plot(x5, NN1_FT(:, AorS), 'o');

hold off;

axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = 14;

plotline(ax, 2);
br = 25;
plotcolor(ax(1:2), 'black', 'brightness', br);
plotcolor(ax(3), 'orange', 'brightness', br);

plotcolor(ax(4), 'green', 'brightness', br);
plotcolor(ax(5), 'green', 'brightness', -br);
plotcolor(ax(6), 'red', 'brightness', br);
plotcolor(ax(7), 'red', 'brightness', -br);
plotcolor(ax(8), 'purple', 'brightness', br);
plotcolor(ax(9), 'purple', 'brightness', -br);
plottext(ax, tit, {'Wavelet features', 'FT features', 'Mean'}, 'Model', ylab, 'fontsize', 10, 'legendloc', 'northeastoutside');

xlim([-0.1 5.1]);
ylim([0 102]);
figsize(fig, 'o');



xticks([0.5, 2.5, 4.5]);
xticklabels(["Random Forest", "SVM", "Neural Network"]);


%% Save image
% location = GetPath2Images(mfilename);
% extension = "png";
% SaveImage(fig, location, mfilename, extension);
% close all;

%% all channels

RF_wav = [99.9, 93.3; % Random Forest all channels wavelet
    99.7, 77.8;
    99.6, 61.5;
    99.7, 94.7;
    99.8, 0.0;
    100, 100;
    97.3, 48.4;
    99.8, 88.9;
    99.8, 87.5];
x0 = ones(9, 1) * 0;