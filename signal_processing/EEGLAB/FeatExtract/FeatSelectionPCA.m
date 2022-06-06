% PCAselect uses PCA to select featurse until sum(explained_variance(i)) > uplimit
%
% Syntax:
%    [features_out] = PCAselect(features, uplimit)
%
% Inputs:
%    features_norm - matrix containing NORMALISED features
%    uplimit - value to which feature scores are summed. range: [0 100], default 95
%
% Outputs:
%    features_out - best scoring features up to uplimit using PCA
%    i - first i features taken from features_out
%
function [FeatVector] = FeatSelectionPCA(features)
%% pca
    [coeff, score, latent, ~, explained, mu]= pca(features_norm);
    s = 0;
    for i = 1:length(explained)
       s = s + explained(i);
       if s > uplimit
           break;
       end
    end
    features_out = transpose(coeff(:, 1:i)' * features_norm');
end

% idx = find(cumsum(explained)>95,1);
% FeatVector