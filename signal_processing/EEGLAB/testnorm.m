clear;
close all;
clc;

%%
feat = [1 2 3;
    0 0 NaN;
    7 8 9;
    NaN NaN 0];
%%

idx = find(isnan(feat));
rows = rem(idx, size(feat, 1));
rows(rows == 0) = size(feat, 1);
rows = unique(rows);
feat(rows, :) = NaN;
for k = rows'
    feat(k, :) = mean(feat, 'omitnan');
end
% feat(rows, :) = mean(feat, 'omitnan');
disp(feat)

%%
[b, mu, sigma] = zscore(feat);