%% Gives prediction of model for features of epoch

%% Todo
% write the function
function [OutputClass] = Classify(path2model, input_epoch, varargin)
d = load(path2model);
model = d.model; %ML model
mu = d.mu_train; %mean of train data used for model
sigma = d.sigma_train; %std of train data used for model
idx = false;
if exist('d.feature_idx', 'var')
    idx = true;
end
norm = (input_epoch - mu) ./ sigma;
if idx
    norm = norm(d.feature_idx);
end
OutputClass = model.predict(norm);
end