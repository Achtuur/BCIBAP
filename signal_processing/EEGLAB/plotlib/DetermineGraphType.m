
function type = DetermineGraphType(ax)
    
    cls = getAxClass(ax);
    if contains(cls, 'primitive.Bar')
        type = 'bar';
    elseif contains(cls, 'TextArrow')
        type = 'arrow';
    elseif contains(cls, 'primitive.Line') || contains(cls, 'matlab.graphics.chart.decoration.ConstantLine')
        type = 'line';
    elseif contains(cls, 'primitive.Patch')
        type = 'patch';
    else
        type = 'line';
        warning('Axis of unsupported type for coloring, may cause issues'); 
    end
end

function cls = getAxClass(ax)
    w = whos;
    for k = 1:length(w)
        if strcmp(w(k).name, 'ax')
            cls = w(k).class;
            break;
        end
    end
end