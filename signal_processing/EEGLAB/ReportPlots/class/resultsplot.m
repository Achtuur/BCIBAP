%% 1 channel with 99% PCA where applicable
clc; clear; close all;
s = strrep(mfilename('fullpath'), mfilename, ''); %get path to file this script is run in
NN = load(s + "\data\NN.mat");
SVM = load(s + "\data\SVM.mat");
RF = load(s + "\data\RF.mat");

RF9_FT = RF.RF9_FT;
RF9_wav = RF.RF9_wav;
RF9_both =RF.RF9_both;
SVM9_wav = SVM.SVM9_wav(:, 5:6);
SVM9_FT = SVM.SVM9_FT(:, 3:4);
NN9_wav = NN.NN9_wav(:, 5:6);
NN9_FT = NN.NN9_FT(:, 5:6);

x = ones(9, 7) .* (0:7-1);

AorS = 2; %Set this var to 1 to plot accuracy, 2 to plot sensitivity

if AorS == 1
    tit = ["Comparison of best accuracy results for", "different ML models and features"];
    ylab = "Accuracy in \%";
else
    AorS = 2; %ensure it is 2
    tit = ["Comparison of best sensitivity results for", "different ML models and features"];
    ylab = "Sensitivity in \%";
end

n = 1:9;
n(5) = []; %exclude patient 6

avg = [mean(RF9_wav(n, :)); mean(RF9_FT(n, :)); mean(RF9_both(n, :)); ...
    mean(SVM9_wav(n, :)); mean(SVM9_FT(n, :)); ...
    mean(NN9_wav(n, :)); mean(NN9_FT(n, :))];
avg = avg(:, AorS); %take accuracy or sensitivity


margin = 0.25;

nRf = 3;
nSVM = 2;
nNN = 2;

RFx = [0, nRf-1] + [-margin margin];
SVMx = [nRf, nRf + nSVM - 1] + [-margin margin];
NNx = [nRf + nSVM, nRf + nSVM + nNN - 1] + [-margin margin];

fig = figure();
hold on;
% background color
br = 100;
p(1) = patch([RFx fliplr(RFx)], [200 200 0 0], 'w');
p(2) = patch([SVMx fliplr(SVMx)], [200 200 0 0], 'w');
p(3) = patch([NNx fliplr(NNx)], [200 200 0 0], 'w');

plotcolor(p(1), 'green', 'brightness', br);
plotcolor(p(2), 'red', 'brightness', br);
plotcolor(p(3), 'purple', 'brightness', br);

plax(1) = plot(-100, -100, 'x'); %plotting invisible o and x for legend hack
plax(2) = plot(-100, -100, 'o');
plax(3) = plot(-100, -100, 's');
plax(4) = plot(x(1,:), avg, '-o');

ax(1) = plot(x(:, 1), RF9_wav(:, AorS), 'x');
ax(2) = plot(x(:, 2), RF9_FT(:, AorS), 'o');
ax(3) = plot(x(:, 3), RF9_both(:, AorS), 's');

ax(4) = plot(x(:, 4), SVM9_wav(:, AorS), 'x');
ax(5) = plot(x(:, 5), SVM9_FT(:, AorS), 'o');

ax(6) = plot(x(:, 6), NN9_wav(:, AorS), 'x');
ax(7) = plot(x(:, 7), NN9_FT(:, AorS), 'o');

hold off;

axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = 14;

plotline(plax(4), 2);
br = 50;
plotcolor(plax(1:3), 'black', 'brightness', br);
plotcolor(plax(4), 'orange', 'brightness', 0);

plotcolor(ax(1:3), 'green', 'brightness', -br);
plotcolor(ax(4:5), 'red', 'brightness', -br);
plotcolor(ax(6:7), 'purple', 'brightness', -br);
plottext(plax, tit, {'Patient analysed with wavelet features', 'Patient analysed with FT features', 'Wavelet \& FT features combined', 'Mean of all patients (patient 6 excluded)'}, ...
    'Model', ylab, 'fontsize', 8, 'legendloc', 'northeastoutside');

xlim([0 - margin, nRf + nNN + nSVM - 1 + margin]);
ylim([0 102]);
figsize(fig, 'o');



xticks([mean(RFx), mean(SVMx), mean(NNx)]);
xticklabels(["Random Forest", "SVM", "Neural Network"]);


%% Save image
location = GetPath2Images(mfilename);
extension = "eps";
SaveImage(fig, location, mfilename, extension);
