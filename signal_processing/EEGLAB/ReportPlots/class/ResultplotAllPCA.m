clc; clear all; close all;
AorS = 1:2;
pca = 1:3;

% plot acc/sens for 0, 95 and 99% pca

AorS = 1;
pca = 3;

for i = AorS
    for k = pca
        resultsplot(i, k);
    end
end

% close all;