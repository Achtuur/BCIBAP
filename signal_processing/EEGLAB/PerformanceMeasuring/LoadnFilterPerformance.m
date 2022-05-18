clc; clear;
clear; clc;
eegpath = AddPath();
dataset = 'chb03';
path2dataset = eegpath + "sample_data\" + dataset + "\";
FileIndices = 1:1;
indexstr = sprintf("%d", FileIndices);
if length(indexstr) == 1
   indexstr = "0" + indexstr; 
end
path2edf = sprintf("%s%s_%s.edf", path2dataset, dataset, indexstr);

summarypath = path2dataset + dataset + "-summary.txt";
[~, ~, channellist, ~] = Label_extract2(summarypath, 1, FileIndices); %get labels of where there are seizures

forders = 50 : 50 : 50;
times = zeros(length(forders), length(FileIndices));
means = zeros(1, length(forders));
for k = 1 : length(forders)
    j = 1;
    for i = FileIndices
        istr = string(i);
        if i < 10
           istr = "0" + istr;
        end
        file = sprintf('%s%s_%s.edf',path2dataset, dataset, istr); %path to file of recording
        if isfile(file)
            tic;
            fd =  LoadnFilter(file, 'channellist', channellist, 'forder', forders(k));
            times(k, j) = toc;
            j = j+1;
        else
            error(file + " does not exist");
        end
    end
    means(1, k) = mean(times(k,:));
end

