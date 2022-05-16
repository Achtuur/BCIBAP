%% Loads and preprocesses data from raw .edf files

%% Inputs
%   path2dataset: path to dataset folder containing .edf files. folder name should be 'chbxx' where xx is number of the patient
%   FileIndices: indices of files in summary.txt to be labeled, starts at 1
%% Outputs
%   filtered_data: matrix containing preprocessed data from .edf files. (These can become quite long!!)
%   Local storage:
%       -loadeddata folder containing .mat files which store the filtered data so continuous runs dont take as long
%           (note these files can become very large)

%% Todo
%   fix later to select correct channels in LoadnFilter
function filtered_data = LoadData(path2dataset, FileIndices, varargin) 
%% test values
%   comment out the lines about nargin and varargin
%     eegpath = AddPath();
%     path2dataset = eegpath + "/sample_data/" + "chb04";
%     g.overwrite = false;
%     FileIndices = [1 2 3];
%%


path2dataset = convertStringsToChars(path2dataset); % make char array so that path can be indexed
path2dataset = strrep(path2dataset,'/', filesep); %make sure every dash in path works for os
path2dataset = strrep(path2dataset, '\', filesep);
FileIndices = sort(FileIndices);

if nargin > 2
   g = finputcheck( varargin, { ...
            'overwrite' 'integer' [0 Inf] 0;
            }, 'LoadData'); 
else
    g.overwrite = false;
end

scriptpath = mfilename('fullpath'); %get path to current script
scriptpath = strrep(scriptpath, mfilename, ''); %remove filename to obtain path to folder where script is run
datapath = scriptpath + "loadeddata\";
FileIndicesstr = join(string(FileIndices), ',');
datafilepath = datapath + "nFiles" + FileIndicesstr + "filtered_data.mat";

if ~g.overwrite && isfile(datafilepath)
    disp ("LoadData(): Data already saved as " + "nFiles" + FileIndicesstr + "filtered_data.mat!")
    disp('Loading .mat file...');
    filtered_data = load(datafilepath);
    filtered_data = filtered_data.filtered_data; %matlab loads it as a struct :/
    disp('Done loading .mat file');
    return
end

if path2dataset(end) ~= filesep %append additional filesep at end if it doesn't exist yet
    path2dataset = append(path2dataset, filesep);
end

mkdir(datapath); %create path if doesnt exist yet
filtered_data = [];
chb = strsplit(path2dataset, filesep); % split path into separate folders
chb = chb{length(chb)-1}; % take second to last (chb should now be 'chbxx') (last entry is empty due to path ending with filesep)
for i = FileIndices
    istr = string(i);
    if i < 10
       istr = "0" + istr;
    end
    file = sprintf('%s%s_%s.edf',path2dataset, chb, istr); %path to file of recording
    if isfile(file)
        filtered_data = [filtered_data, LoadnFilter(file)];
%         datafilepath = datapath + "nFiles" + string(i) + "filtered_data.mat";
    else
        error(file + " does not exist");
    end
end
disp("Saving " + "nFiles" + FileIndicesstr + "filtered_data.mat"); %saves files up to now to reduce later load time
save(datafilepath, 'filtered_data');
disp("Done saving data, file stored in " + datapath);
end