function arr = drawArrow(fig, x, y, varargin)
    arr = annotation('textarrow', [1 1], [0 0], varargin{:}, 'interpreter', 'latex');
    arr.Parent = fig.CurrentAxes;
    arr.X = x;
    arr.Y = y;
    arr.HorizontalAlignment = 'center';
end