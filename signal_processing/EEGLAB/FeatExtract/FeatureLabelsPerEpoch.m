%% Transforms multiple data input into single cell array containing all features per epoch
%% Inputs
%   - data/label pairs
%       - data is vector/matrix containing data per epoch representing 1 feature
%       - label is a string containing name for feature
%% Outputs
%   - features is a cell array of size number of epochs by number of features containing all input features per epoch
%   - labels is a cell array of size 1 by number of epochs containing all given input labels

%% Example
% [feat, lab] = FeatureLabelsPerEpoch(data1, 'label1', data2, 'label2', ... datan, 'labeln')
% where size(data1, 1) == size(data2, 1) ... == size(datan, 1)
function [features, labels] = FeatureLabelsPerEpoch(varargin)
    %% Some input checking
    if nargin < 1
        error('Too little inputs')  
    elseif mod(nargin, 2) ~= 0
        error('Input does not consist of name/value pairs')
    end
    
    %% Init
    nEpochs = size(varargin{1}, 1); %amount of epochs is equal to rows of any data element (should have same amount of epochs)
    if nEpochs == 1 && size(varargin{1}, 2) ~= 1
       nEpochs = size(varargin{1}, 2); %use column as epochs if input is 1xNepochs 
    end
    L = nargin/2; %amount of data/label pairs
    features = cell(nEpochs, L);
    labels = cell(1, L);
    
    for i = 1:L %loop through all data/name pairs
        data = varargin{2*i - 1}; %every second element starting from 1
        label = varargin{2*i}; %every second element starting from 2
        if size(data, 1) ~= nEpochs %check number of epochs
            if size(data, 2) == nEpochs % if column length is equal to number of epochs but row length isnt, maybe data wasnt transposed properly
                data = data'; % attempt to fix by transposing data
            else
                sizestr = sprintf("%d x %d", size(data,1), size(data,2));
                error("FeatureLabelingError:NotSameEpochs", ...
                    "Not all data has same amount of epochs \n" + ...
                     "Faulty data '" + label + "'; size " + sizestr);
            end
        end
        col = cell(size(data,2), 1); %col is cells of epochs x 1 which will contain data of columns of data per epoch
        for k = 1:size(data,1) %loop through rows of data
            col{k, 1} = data(k, :); 
        end
        features(:, i) = col;
        labels(1, i) = {label};
    end
end