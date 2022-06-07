clc; clear;

[featuresWavelet,features,labels,featurelabels,featurelabelsWavelet] = getFeatures();

 %% normalise features
featuresWavelet=NormalizeFeat(featuresWavelet);
features=NormalizeFeat(features);

[features_outFourier, iFourier,explainedFourier,latentFourier] = FeatSelectionPCA(features, 100);
[features_outWavelet, iWavelet,explainedWavelet,latentWavelet] = FeatSelectionPCA(featuresWavelet, 100);
fig=figure();
t = tiledlayout(1,2);
nexttile;
% % Plot in tiles
ax(1)= bar(explainedFourier./100);
title('PCA on fourier','interpreter' ,'latex','fontsize', 18,'FontWeight','bold');
xlim([0 28])
ylim([0 1])
legend('Individual explained variance', 'interpreter', 'latex', 'fontsize', 8)
hold on
stairs(cumsum(latentFourier)/sum(latentFourier));
legend('Cumulative explained variance', 'interpreter', 'latex', 'fontsize', 8)
axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = 14;

nexttile;
ax(2)= bar(explainedWavelet./100); 
title('PCA on wavelet','interpreter' ,'latex','fontsize', 18,'FontWeight','bold')
xlim([0 36])
ylim([0 1])
legend('Individual explained variance', 'interpreter', 'latex', 'fontsize', 8)
hold on
stairs(cumsum(latentWavelet)/sum(latentWavelet));
xlim([0 36])
ylim([0 1])
legend('Cumulative explained variance', 'interpreter', 'latex', 'fontsize', 8)
%plotcolor(ax,'green', 'colordiff',0);

% % Specify common title, X and Y labels
% title(t, 'Decomposition of epoch signal','interpreter', 'latex','fontsize', 18)
xlabel(t, 'Explained variance ratio','interpreter', 'latex', 'fontsize',17)
ylabel(t, 'Principal component index', 'latex','fontsize',17)
saveas(gcf,'1ChannelPCA','epsc')

%% Save image
figsize(fig, 'o'); %try 's', 'm', 'b', 'o'/'r'
location = GetPath2Images() + mfilename;
extension = "eps";
SaveImage(fig, location, extension);


% figure(4)
% pentropy(totalepochs(:,2000),129);
% senonseizure=pentropy(totalepochs(:,2000),129);
% figure(5)
% pentropy(totalepochs(:,5),129)
% seseizure=pentropy(totalepochs(:,5),129);

% figure(6)
% % 
% scatter(stdepoch(1,1:148*9),stdentropy(1,1:148*9));
% %
% hold on
% scatter(stdepoch(1,148*9:2673),stdentropy(1,148*9:2673));
