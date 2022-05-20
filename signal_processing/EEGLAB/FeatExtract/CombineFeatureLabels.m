%% Combines multiple feature cell arrays using feature labels
% Does so such that same features from different channels are adjacent

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
%        addee_features = l.double_features; adder_features = l.triple_features;
%        addee_labels = l.double_labels; adder_labels = l.triple_labels;
    %% Check addee for empty

    if isempty(addee_labels) || isempty(addee_features) %if addee is empty, then return adder
       features = adder_features;
       labels = adder_labels;
       return;
    end
    
    %% Init for loop
    features = cell(size(addee_features));
    labels = {''};
    unique_adder_labels = unique(adder_labels, 'stable');
    
    %% Loop through labels
    for i = 1:length(unique_adder_labels)
        %% calculate indices
        [first_occ_addee, last_occ_addee] = GetFirstLastMatch(addee_labels, unique_adder_labels{i});
        [first_occ_adder, last_occ_adder] = GetFirstLastMatch(adder_labels, unique_adder_labels{i});
        if isempty(first_occ_addee) && isempty(first_occ_adder)
           error('Labels from adder do not appear in addee'); 
        end
        diff_addee = last_occ_addee - first_occ_addee + 1; % number of times label occurs
        diff_adder = last_occ_adder - first_occ_adder + 1;
        diff_tot = diff_addee + diff_adder;
        
        
        addee_indices = first_occ_addee  : last_occ_addee; %indices for new array from addee
        adder_indices = first_occ_adder  : last_occ_adder; %indices for new array from adder
        new_indices = (i-1) * diff_tot + 1 : i * diff_tot;
        
        %% add adder and addee together
        features(:, new_indices) = [addee_features(:, addee_indices) adder_features(:, adder_indices)];
        labels(:, new_indices) =  [addee_labels(:, addee_indices) adder_labels(:, adder_indices)];
    end
end

function [first, last] = GetFirstLastMatch(labels, str)
    matches = ismember(labels, str);
    first = find(matches, 1, 'first');
    last = find(matches, 1, 'last');
end