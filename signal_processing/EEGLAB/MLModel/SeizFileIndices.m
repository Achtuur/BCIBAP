function [FileIndices] = SeizFileIndices(dataset)
%SEIZFILEINDICES Summary of this function goes here
%   Detailed explanation goes here
switch dataset
    case 'chb01'
        FileIndices = [3 4 15 16 18 21 26];
    case 'chb02'
        FileIndices = [16 19];
    case 'chb03'
        %FileIndices = [1 2 3 4]; %34 35 36 perform strangely thererofre kept out
        FileIndices = [1 2 3 4 34 35 36];
    case 'chb04'
        FileIndices = [5 8 28];
    case 'chb05'
        FileIndices = [6 13 16 17 22];
    case 'chb06'
        FileIndices = [1 4 9 10 13 18 24];
    case 'chb07'
        FileIndices = [12 13 19]; %Check if 19 or 18 has seizures
    case 'chb08'
        FileIndices = [2 5 11 13 21];
    case 'chb09'
        FileIndices = [6 8 19];
    case 'chb10'
        FileIndices = [12 20 27 30 31 38 89];
    case 'chb11'
        FileIndices = [82 92 99];
    case 'chb12'
        FileIndices = [6 8 9 10 11 23 27 28 29 33 36 38 42];
    case 'chb13'
        FileIndices = [19 21 40 55 58 59 60 62];
    otherwise
        disp("File Not Found, Empty array returned")
        FileIndices = [];
end
end

