%% Run all scripts with a filter plot in them
clear;
close all;
clc;

% use common filter constants
locutoff = 0;
hicutoff = 30;
dwnsample = 2;
forder = 30;

%% pinknoise
pinknoise(locutoff, hicutoff, dwnsample, forder);

%% showfilters
showfilters(0.5, hicutoff, dwnsample, forder);

%% showseizure
showseizure(locutoff, hicutoff, dwnsample, forder);

%% usedchannelsepochs
UsedChannelsEpochs(locutoff, hicutoff, dwnsample, forder);

%% PSD
PSD(locutoff, hicutoff, dwnsample, forder);

%% PCA
PCAfourier(locutoff, hicutoff, dwnsample, forder);

%% close
close all;