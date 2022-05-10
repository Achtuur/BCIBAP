%Adds necessary folders and subfolders to path
function AddPath()
folders = {'Classification', 'FeatExtract', 'Label-function-CHB-Data', 'MLModel', 'sample_data', 'Preprocessing'};

for k = 1 : size(folders, 2)
    addpath(genpath(folders{k})); %addfolder{k} and all subfolders inside folder{k} to path
end
end
