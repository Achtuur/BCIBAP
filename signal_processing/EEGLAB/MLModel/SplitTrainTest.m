%% Get indices for training and testing data based on classes in Y
%   Note these indices are randomly selected

%% Inputs
%   Y: vector containing labels for classes
%   percent_train_split: percentage of data that becomes training data (range is [0, 1]

%% Outputs
%   train_id, test_id: indices of Y that can be used for training data and testing data

function [train_id,test_id]=SplitTrainTest(Y,percent_train_split)

    train_id=[];
    test_id=[];
    num_classes=length(unique(Y));
    classes = unique(Y);

% loop through the classes
    for i=1:num_classes 
        % finding the indices belonging to each class
        ind_i=find(Y==classes(i));
        % shuffling the indice
        ind_i_perm=ind_i(randperm(length(ind_i)));
        % the split point for train test
        ind_split=round(percent_train_split*length(ind_i));
        % adding the train ids to the the previous ids 
        train_id=[train_id;ind_i_perm(1:ind_split)];
        % adding the test ids to the the previous ids 
        test_id=[test_id;ind_i_perm(ind_split+1:end)]; 

    end
end