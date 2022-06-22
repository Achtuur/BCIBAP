%% puts value of bar graph as text above it
%x is x values of bar graph, y is y values of bar graph
function bartext(x, y, varargin)

if nargin < 3
    g.rounding = 2; 
    g.inout = 'out';
else
    g = finputcheck( varargin, { ...
        'rounding' 'integer' [0 inf] 2;
        'inout' 'string' {} 'out';
        }, 'plotcolor');
end
y = round(y, g.rounding);

if strcmp(g.inout, 'out')
    verts = {'bottom', 'top'};
elseif strcmp(g.inout, 'in')
    verts = {'top', 'bottom'};
end

for i = 1:length(y)
   vert = verts{1};
   if y(i) < 0
       vert = verts{2};
   end
   text(x(i), y(i), num2str(y(i)), 'vert', vert, 'horiz', 'center'); 
end
end