function [FeatVector] = FeatSelectionPCA(features)
%% normalise features
features=cell2mat(features);
features_norm = zscore(features);

%% pca
[coeff,score,latent,~,explained,mu]= pca(features_norm);
for i=2:35
    if (sum(explained(1:i))<95) %take the principal components with cumulative variance of 95%
        continue;
    else
        FeatVector=coeff(:,1:i)'*features_norm'; 
        break;
    end
end

% idx = find(cumsum(explained)>95,1);
% FeatVector