%% resizes figure for report
%% inputs:
%   fig: figure to be resized
%   size:
%       either a position matrix (looks like [x y width height])
%       or one of these strings ('/' means option between both strings): s/small, m/medium, b/big, f/full/fullscreen or overleaf/o/report/r

function figsize(fig, size)
    if (~isnumeric(size))
       size = str2size(size);
    end
    
    fig.Position = size;
end

function sz = str2size(str)
    %Sets the units of your root object (screen) to pixels
    set(0,'units','pixels');
    %Obtains this pixel information
    Pix_SS = get(0,'screensize'); % = [1 1 Width Height]
    %Sets the units of your root object (screen) to inches
    set(0,'units','inches');
    %Obtains this inch information
    Inch_SS = get(0,'screensize'); % [0 0 Width Height]
    set(0, 'units', 'pixels')

    pixperinch = Pix_SS(3) / Inch_SS(3); %get pixels per inch

    if (strcmp(str, 'small') || strcmp(str, 's'))
        sz = [0 0 8 6] * pixperinch;
    elseif(strcmp(str, 'medium') || strcmp(str, 'm'))
        sz = [0 0 12 9] * pixperinch;
    elseif(strcmp(str, 'big') || strcmp(str, 'b'))
        sz = [0 0 16 12] * pixperinch;
    elseif(strcmp(str, 'overleaf') || strcmp(str, 'report') || strcmp(str, 'r') || strcmp(str, 'o'))
        sz = [0 0 10 6] * pixperinch; %figure this one out later
    elseif(strcmp(str, 'fullscreen') || strcmp(str, 'full') || strcmp(str, 'f'))
        sz = [0 0 Pix_SS(3) Pix_SS(4)];
    else
        sz = [0 0 8 6] * pixperinch;
    end
end