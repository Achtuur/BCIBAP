function [features_norm, mus, stds] = NormalizeFeat(features)
%NORMALIZEFEAT Summary of this function goes here
%   Detailed explanation goes here
disp('Normalising features...');
t = tic;

matfeat = features;
idx = isnan(matfeat);
NaNrows = unique(rem(find(idx==1),length(features)));
NaNrows(NaNrows == 0) = length(features); %fix bottom column
matfeat(NaNrows,:) = NaN;
for k = NaNrows'
    matfeat(k, :) = mean(matfeat,'omitnan');
end

% makes wrong measurements means
for k = 1:size(matfeat, 2)
    i = isnan(matfeat(:,k));
    j = ~i;
    matfeat(i, k) = mean(matfeat(j,k), 'omitnan');
end

[features_norm, mus, stds] = zscore(matfeat);

t = toc(t);
fprintf("Normalised features, took %.3f seconds\n", t);
end

