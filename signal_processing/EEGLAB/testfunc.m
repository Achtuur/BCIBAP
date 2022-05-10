clear;
diff = calcTimeDiff('18:35:30', '19:05:30');


function d = calcTimeDiff(startTimeHMS, endTimeHMS)
    %Split HMS time from 'hh:mm:ss' to cell array {'hh', 'mm', 'ss'}
    startTimeHMS = split(startTimeHMS, ':'); endTimeHMS = split(endTimeHMS, ':');
    d = zeros(0, 3);
    for i = 1 : 3
        d(i) = str2double(endTimeHMS{i}) - str2double(startTimeHMS{i}); %calculate 
    end
    d = d(1) * 3600 + d(2) * 60 + d(3);
    
    if d < 0
       error('Time difference negative'); 
    end
end