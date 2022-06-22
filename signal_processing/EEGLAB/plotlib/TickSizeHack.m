%% Uses a 'hack' to increase fontsize of ticks
% warning: increases ALL fontsizes, use this function BEFORE specifiying font sizes of titles, labels etc.

function TickSizeHack(fontsize)
warning('TickSizeHack sets all fontsizes, call this function before specifiying font sizes of titles, labels etc.');

if ~exist('fontsize', 'var')
    fontsize = 14;
end

axis = gca;
axis.TickLabelInterpreter = 'latex';
axis.FontSize = fontsize;
end