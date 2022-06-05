%% Divides filtered_data into epochs

%% Inputs
%   filtered_data: input data to be divided into epochs
%   Fs: sampling frequency of filtered_data
%   EpochLengthSec: length of epochs in seconds
%   (optional) rounding_err: number of epochs to be removed due to rounding errors from label extraction

%% Outputs
%   epochs: cell containing filtered_data divided into epochs. Every row of epochs is a single channel's data divided into epochs
%   L: sample length of single epoch

%% TODO
% make it so more channels from filtered_data can be used

function [epochs, L] = DivideInEpochs(filtered_data, Fs, EpochLengthSec)
%% test vars
%     filtered_data = load('MLModel/loadeddata/nFiles1Channels3,4,15,16,19,20,21,22,23filtered_data.mat').filtered_data;
%     Fs = 256;
%     EpochLengthSec = 2;

%% MAKE EPOCHS

L = Fs*EpochLengthSec; %sample length of epoch
rowsEpoch = floor(length(filtered_data) / L);
channels = size(filtered_data, 1); %assume channels in rows
epochs = cell(channels, 1); %final epochs with every channel
epochs_chan = zeros(rowsEpoch,floor(L)); %epochs per channel

for k = 1:channels
    x = 0;
    for i = 1:rowsEpoch
        epochs_chan(i,:) = filtered_data(k, (x*L+1) : L*(x+1));
        x = x+1;
    end
    epochs(k,1) = {epochs_chan};
end
end
