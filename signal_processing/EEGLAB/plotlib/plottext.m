%% Configure text objects in a plot
%% inputs:
%   axis: axes with plots on them
%   tit, leg, xlab, ylab: strings for title, legend, xlabel and ylabel respectively
%% optional
%   fontsize: select the SMALLEST fontsize
%   legendloc: override legendlocation, defaults to 'best'

%note: use this AFTER setting xlim and ylim and xticks/yticks since it fucks them up due to making them constant

function plottext(axis, tit, leg, xlab, ylab, varargin)

if nargin < 6
   g.fontsize = 8;
   g.legendloc = 'best';
else
    legendlocs = {'north'; 'south'; 'east'; 'west'; 'northeast'; 'northwest'; 'southeast'; 'southwest'; 'northoutside'; 'southoutside'; 'eastoutside'; 'westoutside'; 'northeastoutside'; 'northwestoutside'; 'southeastoutside'; 'southwestoutside'; 'best'; 'bestoutside'; 'layout'; 'none'};
    g = finputcheck( varargin, { ...
            'fontsize' 'integer' [0 inf] 8;
            'legendloc' 'string' legendlocs 'best'
            }, 'plottext');
end

BIGFONTSIZE = g.fontsize+5; %define some constants for fontsize
MEDIUMFONTSIZE = g.fontsize+3;
SMALLFONTSIZE = g.fontsize;

% if isprop(gca, 'XTickLabel')
%     a = get(gca,'XTickLabel');
%     set(gca,'XTickLabel',a,'FontName','Times','fontsize', SMALLFONTSIZE)
% end

% if isprop(gca, 'YTickLabel')
%     a = get(gca,'YTickLabel');
%     set(gca,'YTickLabel',a,'FontName','Times','fontsize', SMALLFONTSIZE)
% end
    

title(tit, 'interpreter', 'latex', 'fontsize', BIGFONTSIZE); %add title

legend(axis, leg, 'interpreter', 'latex', 'fontsize', MEDIUMFONTSIZE, 'location', g.legendloc); %add legend

if isprop(gca, 'XLabel')
    xlabel(xlab, 'interpreter', 'latex', 'fontsize', BIGFONTSIZE); %add xlabel
end

if isprop(gca, 'YLabel')
    ylabel(ylab, 'interpreter', 'latex', 'fontsize', BIGFONTSIZE) %, 'Rotation',0, 'VerticalAlignment','middle', 'HorizontalAlignment','right'); %add ylabel
end
end

% plottext(axis, 'tit', 'leg', 'xlab', 'ylab', 16);
% plottext(axis, 'tit', {'leg1', 'leg2'}, 'xlab', 'ylab', 16);
% for your copy and pasting pleasure