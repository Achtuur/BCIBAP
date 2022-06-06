%% Run all scripts with a filter plot in them
clear;
close all;
clc;

%% use common filter constants
locutoff = 0.5;
hicutoff = 30;
downsample = 2;
forder = 30;

%% pinknoise
pinknoise(locutoff, hicutoff, downsample, forder);

%% showfilters
showfilters(locutoff, hicutoff, downsample, forder);

%% showseizure
showseizure(locutoff, hicutoff, downsample, forder);

%% usedchannelsepochs
UsedChannelsEpochs(locutoff, hicutoff, downsample, forder);

%% PSD
PSD(locutoff, hicutoff, downsample, forder);

%% close
% close all;