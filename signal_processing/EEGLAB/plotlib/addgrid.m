function addgrid(varargin)
if nargin < 1
    g.X = 1; 
    g.Y = 1;
    g.linestyle = '-';
else
    g = finputcheck( varargin, { ...
        'X' 'integer' [0 1] 0;
        'Y' 'integer' [0 1] 0;
        'linestyle' 'string' {} '-';
        }, 'plotcolor');
end
axis = gca;
if g.X
    axis.XGrid = 'on';
end
if g.Y 
    axis.YGrid = 'on';
end

if g.X || g.Y
    axis.GridLineStyle = g.linestyle;
end

end