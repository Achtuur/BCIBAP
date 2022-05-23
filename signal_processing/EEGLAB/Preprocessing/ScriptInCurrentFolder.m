%% Check if script is in same folder as function caller

function bool = ScriptInCurrentFolder(script, caller)
    bool = exist(replace(which(caller), caller + ".m", '') + script + '.m', 'file');
end