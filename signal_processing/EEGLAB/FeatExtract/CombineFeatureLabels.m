%% Combines multiple feature cell arrays using feature labels
% Does so such that same features from different channels are adjacent
% assume that adder only contains labels once

%% Input
%   addee_features, addee_labels: features and labels to which you want to add features and labels
%   adder_features, adder_labels: features and labels which will be added to the addee

%% Output
%  features, labels: combination of addee and adder features and labels where same label features are adjacent

%% Example
% if addee has labels {'a', 'a', 'b', 'b', 'c', 'c'} and adder has labels {'a', 'b', 'c'}
% then output labels is {'a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'c'} where every third a/b/c is from the adder
% output features follows the same idea

function [features, labels] = CombineFeatureLabels(addee_features, addee_labels, adder_features, adder_labels)
    %% test vars
%        l = load('FeatExtract/testfeatures.mat');
%        addee_features = l.double_features; adder_features = l.features;
%        addee_labels = l.double_labels; adder_labels = l.featurelabels;
    %% combine features

    if isempty(addee_labels) || isempty(addee_features) %if addee is empty, then return adder
       features = adder_features;
       labels = adder_labels;
       return;
    end
    
    features = cell(size(addee_features));
    labels = {''};
    
    for i = 1:length(adder_labels) %loop through labels
        matches = ismember(addee_labels, adder_labels{i}); %get matches between labels
        first_occ = find(matches, 1, 'first');
        last_occ = find(matches, 1, 'last');
        if isempty(first_occ)
           error('Labels from adder do not appear in addee'); 
        end
        diff = last_occ - first_occ; % number of times label occurs in addee
        
        %% calculate indices
        addee_indices_new = first_occ + i - 1 : last_occ + i - 1; %indices for new array from addee
        adder_index_new = last_occ + i; %index for new array from adder
        addee_indices_old = i + (i-1) * diff : i + i*diff ; %index from old array
        adder_index_old = i; %index from old array
        
        %% add addee indices
        features(:, addee_indices_new) = addee_features(:, addee_indices_old);
        labels(:, addee_indices_new) =  addee_labels(:, addee_indices_old);
        %% add adder indices
        features(:, adder_index_new) = adder_features(:, adder_index_old);
        labels(:, adder_index_new) = adder_labels(:, adder_index_old);
    end
end