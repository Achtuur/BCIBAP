%% Divides filtered_data into epochs

%% Inputs
%   filtered_data: input data to be divided into epochs
%   Fs: sampling frequency of filtered_data
%   EpochLengthSec: length of epochs in seconds
%   (optional) rounding_err: number of epochs to be removed due to rounding errors from label extraction

%% Outputs
%   epochs: filtered_data divided into epochs
%   L: sample length of single epoch

%% TODO
% make it so more channels from filtered_data can be used

function [epochs, L] = DivideInEpochs(filtered_data, Fs, EpochLengthSec)
%% MAKE EPOCHS

L = Fs*EpochLengthSec; %sample length of epoch
rowsEpoch = floor(length(filtered_data) / L);
epochs = zeros(rowsEpoch,floor(L));
x = 0;
for i = 1:rowsEpoch
    epochs(i,:) = filtered_data(1, (x*L+1) : L*(x+1));
    x = x+1;
end
end