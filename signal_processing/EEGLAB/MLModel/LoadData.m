%% Loads and preprocesses data from raw .edf files

%% Inputs
%   path2dataset: path to dataset folder containing .edf files. folder name should be 'chbxx' where xx is number of the patient
%   FileIndices: indices of files in summary.txt to be labeled, starts at 1
% OPTIONAL:
%   overwrite: overwrite .mat file instead of reading it when available (default false)
%   channellist: channels to include in read data, use value 0 to include all channels (default 0)
%   rounding_err: vector containing amount of samples to remove per file when loading. Each entry in vector should correspond to a FileIndex (default 0)
%% Outputs
%   filtered_data: matrix containing preprocessed data from .edf files. (These can become quite long!!)
%   Local storage:
%       -loadeddata folder containing .mat files which store the filtered data so continuous runs dont take as long
%           (note these files can become very large)
%% Todo
%   fix later to select correct channels in LoadnFilter
function filtered_data = LoadData(path2dataset, FileIndices, varargin) 
%% test values
% %   comment out the lines about nargin and varargin
%     eegpath = AddPath();
%     path2dataset = eegpath + "/sample_data/" + "chb04";
%     FileIndices = 5;
%     g.overwrite = false;
%     g.channellist = 0;
%     g.rounding_err = linspace(0,0,max(FileIndices));
%%


path2dataset = convertStringsToChars(path2dataset); % make char array so that path can be indexed
path2dataset = strrep(path2dataset, '/', filesep); %make sure every dash in path works for os
path2dataset = strrep(path2dataset, '\', filesep);
FileIndices = sort(FileIndices);

if nargin > 2
   g = finputcheck( varargin, { ...
            'rounding_err' 'integer' [0 inf] linspace(0,0,length(FileIndices));
            'channellist' 'integer' [0 inf] 0;
            'overwrite' 'integer' [0 Inf] 0;
            }, 'LoadData'); 
else
    g.channellist = 0;
    g.rounding_err = linspace(0,0,length(FileIndices));
    g.overwrite = false;
end

scriptpath = mfilename('fullpath'); %get path to current script
scriptpath = strrep(scriptpath, mfilename, ''); %remove filename to obtain path to folder where script is run
datapath = scriptpath + "loadeddata\";
FileIndicesstr = join(string(FileIndices), ',');
ChannelListstr = join(string(g.channellist), ',');
savestr = "nFiles" + FileIndicesstr + "Channels" + ChannelListstr;
datafilepath = datapath + savestr + "filtered_data.mat";

if ~g.overwrite && isfile(datafilepath)
    disp ("LoadData(): Data already saved as " + savestr + "filtered_data.mat!")
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
j = 1;
for i = FileIndices
    istr = string(i);
    if i < 10
       istr = "0" + istr;
    end
    file = sprintf('%s%s_%s.edf',path2dataset, chb, istr); %path to file of recording
    if isfile(file)
        newData =  LoadnFilter(file, 'channellist', g.channellist);
        lim = size(newData, 2) - floor(g.rounding_err(j)); %discard samples that attribute to rounding error
        newData = newData(:, 1 : lim); 
        j = j + 1;
        filtered_data = [filtered_data, newData];
    else
        error(file + " does not exist");
    end
end
disp("Saving " + savestr + "filtered_data.mat"); %saves files up to now to reduce later load time
save(datafilepath, 'filtered_data');
disp("Done saving data, file stored in " + datapath);
end