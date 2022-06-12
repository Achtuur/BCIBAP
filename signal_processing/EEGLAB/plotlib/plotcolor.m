%% Changes color of line using presets
%% inputs:
%   axis: axes with plots to be colored
%   colorset: use string to select which colorset to use, currently supported are:
%           'green', 'purple', 'red', 'blue', 'orange', 'yellow', 'magenta', 'cyan', 'tudelft' and 'black'
%           can also use '0' to '10'
%% optional
%   colordiff: [0 255] difference in RGB value to the next color (includes first color)
%   brightness: [0 255] choose base brightness (adds this value to RGB)


function color = plotcolor(axis, colorset, varargin)
if ~exist('colorset', 'var')
    colorset = 1; %choose which colorset to use
end


if nargin < 3
    g.colordiff = 25; 
    g.brightness = 25;
else
    g = finputcheck( varargin, { ...
        'colordiff' 'integer' [0 255] 25;
        'brightness' 'integer' [0 255] 25;
        }, 'plotcolor');
end

if(~isnumeric(colorset)) %if string as input
   colorset = str2colorset(colorset); 
end

colorsets = [
         58 153 95;    %green
         144 103 167;   %purple
         211 95 96;     %red
         39, 84, 138;   %blue
         201, 149, 71;  %orange
         199, 194, 103; %yellow
         140, 79, 104;   %pink
         70, 122, 120;  %cyan
         110, 187, 213; %tudelft
         0 0 0          %black
         ]/255; %every row is a color, with the for loop below adding up to 7 lighter shades
%clr = zeros(length(axis), 3);
color = colorsets(colorset, :);

if isempty(axis) %no axis input => just return color
    color = clamp(color + g.brightness/255, 0, 1);
else %axis input => recolor axis
    for i = 1:length(axis)
        clr = clamp(color + (i-1)*g.colordiff/255 + g.brightness/255, 0, 1);
        clr(clr > 1) = 1; %set colors above 1 to 1
        type = DetermineGraphType(axis(i));
        if strcmp(type, 'bar') || strcmp(type, 'patch')
            axis(i).FaceColor = clr;
            axis(i).EdgeColor = clamp(clr - min(clr/2, 2*g.brightness/255), 0, 1);
        elseif strcmp(type, 'line')
            axis(i).Color = clr;
        elseif strcmp(type, 'arrow')
           axis(i).Color = clr;
           axis(i).TextColor = clamp(clr - 4*g.brightness/255, 0, 1);
        end
    end
end
end

%makes sure minX <= x <= maxX
function x = clamp(x, minX, maxX)
    x = max(minX, min(x, maxX));  
end



function n = str2colorset(str)
    n = 10; %default to black
    if(strcmp(str, 'green'))
        n = 1;
    elseif(strcmp(str, 'purple'))
        n = 2;
    elseif(strcmp(str, 'red'))
        n = 3;
    elseif(strcmp(str, 'blue'))
        n = 4;
    elseif(strcmp(str, 'orange'))
        n = 5;
    elseif(strcmp(str, 'yellow'))
        n = 6;
    elseif(strcmp(str, 'pink') || strcmp(str, 'magenta'))
        n = 7;
    elseif(strcmp(str, 'cyan'))
        n = 8;
    elseif(strcmp(str, 'tu') || strcmp(str, 'tudelft'))
        n = 9;
    elseif(strcmp(str, 'black'))
        n = 10;
    end
end

