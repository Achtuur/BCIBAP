%Adds necessary folders and subfolders to path
function eegpath = AddPath()
folders = {'Classification', 'FeatExtract', 'Label-function-CHB-Data', 'MLModel', 'sample_data', 'Preprocessing', ...
    'functions/guifunc/', 'PerformanceMeasuring', 'plotlib', 'ReportPlots'};

for k = 1 : size(folders, 2)
    addpath(genpath(folders{k})); %addfolder{k} and all subfolders inside folder{k} to path
end
eegpath = strrep(mfilename('fullpath'), mfilename, ''); %get path to /EEGLAB/ folder
end
