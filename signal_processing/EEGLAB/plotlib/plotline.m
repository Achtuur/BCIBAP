%% Do some line styling stuff
%   currently only supports linewidth
%% Inputs
%    axis: axes with plots
%    linewidth: input as array to select linestyle per axis elements
%               can be used to make every nth line a certain width
%               eg: linewidth = [1 2] will make axis(1) have a linewidth of 1, axis(2) a linewidth of 2, axis(3) lw of 1, axis(4) lw of 2 etc..


function plotline(axis, linewidth)
    if ~exist('linewidth', 'var')
        error('No linewidth specified');
    end
    
    for k = 0:length(axis)-1
        if(length(linewidth) > 1)
            applied_linewidth = linewidth(1 + mod(k,length(linewidth))); %if linewidth array, take the k-th linewidth
        else
            applied_linewidth = linewidth;
        end

        axis(k+1).LineWidth = applied_linewidth; %change linewidth
    end
end