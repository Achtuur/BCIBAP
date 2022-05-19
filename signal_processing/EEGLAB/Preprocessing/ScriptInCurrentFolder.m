function bool = ScriptInCurrentFolder(script, caller)
    bool = exist(replace(which(caller), caller + ".m", '') + script + '.m', 'file');
end