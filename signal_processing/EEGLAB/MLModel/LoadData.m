%path: path to chbxx_yy.edf folder. folder name should be 'chbxx' where xx is number of experiment
%nFiles: first n .edf files of certain set

%fix later to have overwrite feature
function filtered_data = LoadData(path, nFiles, varargin) 
    path = convertStringsToChars(path); % make char array so that path can be indexed
    path = strrep(path,'/', filesep); %make sure every dash in path works for os
    path = strrep(path, '\', filesep);
    
    scriptpath = mfilename('fullpath'); %get path to current script
    scriptpath = strrep(scriptpath, mfilename, ''); %remove filename to obtain path to folder where script is run
    datapath = scriptpath + "loadeddata\";
    datafilepath = datapath + "nFiles" + string(nFiles) + "filtered_data.mat";
    if isfile(datafilepath)
        disp ("LoadData(): Data already saved as " + "nFiles" + string(nFiles) + "filtered_data.mat!")
        disp('Loading .mat file...');
        filtered_data = load(datafilepath);
        filtered_data = filtered_data.filtered_data; %matlab loads it as a struct :/
        disp('Done loading .mat file');
        return
    end
        
    if path(end) ~= filesep %append additional filesep at end if it doesn't exist yet
        path = append(path, filesep);
    end
    
    mkdir(datapath); %create path if doesnt exist yet
    filtered_data = [];
    chb = strsplit(path, filesep); % split path into separate folders
    chb = chb{length(chb)-1}; % take second to last (chb should now be 'chbxx') (last entry is empty due to path ending with filesep)
    for i = 1 : nFiles
        istr = string(i);
        if i < 10
           istr = "0" + istr;
        end
        file = sprintf('%s%s_%s.edf',path, chb, istr); %path to file of recording
        filtered_data = [filtered_data, LoadnFilter(file)];
        datafilepath = datapath + "nFiles" + string(i) + "filtered_data.mat";
        
        disp("Saving " + "nFiles" + string(i) + "filtered_data.mat"); %saves files up to now to reduce later load time
        save(datafilepath, 'filtered_data');
        disp("Done saving data, file stored in " + datapath);
    end

end