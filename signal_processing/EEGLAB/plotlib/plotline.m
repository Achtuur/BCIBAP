%% Do some line styling stuff
%   currently only supports linewidth
%% Inputs
%    axis: axes with plots
%    linewidth: input as array to select linestyle per axis elements
%               can be used to make every nth line a certain width
%               eg: linewidth = [1 2] will make axis(1) have a linewidth of 1, axis(2) a linewidth of 2, axis(3) lw of 1, axis(4) lw of 2 etc..


function plotline(axis, linewidth, varargin)
if ~exist('linewidth', 'var')
    error('No linewidth specified');
end

if nargin < 3
    g.HeadSize = 1; 
%     g.HeadLength = 1;
else
    g = finputcheck( varargin, { ...
        'HeadSize' 'integer' [0 inf] 1;
%         'HeadLength' 'integer' [0 inf] 1;
        }, 'plotcolor');
end

for k = 0:length(axis)-1
    type = DetermineGraphType(axis(k+1));
    if strcmp(type, 'line')
            if(length(linewidth) > 1)
                applied_linewidth = linewidth(1 + mod(k,length(linewidth))); %if linewidth array, take the k-th linewidth
            else
                applied_linewidth = linewidth;
            end

            axis(k+1).LineWidth = applied_linewidth; %change linewidth
    elseif strcmp(type, 'arrow')
        V = sqrt((axis(k+1).Y(2) - axis(k+1).Y(1))^2 + (axis(k+1).X(2) - axis(k+1).X(1))^2); %magnitude of arrow
        axis(k+1).HeadLength = linewidth * V * g.HeadSize;
        axis(k+1).HeadWidth = linewidth * V * g.HeadSize;
        axis(k+1).LineWidth = linewidth;
    end
end
end
