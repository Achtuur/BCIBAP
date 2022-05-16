function [epochs, L] = DivideInEpochs(filtered_data, Fs, EpochLengthSec)
%% MAKE EPOCHS

L = Fs*EpochLengthSec; %sample length of epoch
rowsEpoch = floor(length(filtered_data)/L);

epochs = zeros(rowsEpoch,floor(L));
x = 0;
for i = 1:rowsEpoch
    epochs(i,:) = filtered_data(1, (x*L+1) : L*(x+1));
    x = x+1;
end
end