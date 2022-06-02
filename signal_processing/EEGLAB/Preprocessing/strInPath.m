%% check if string exists in the path variable
function bool = strInPath(str)
    f = strsplit(path, pathsep);
    i = find(contains(f, str, 'IgnoreCase', ispc));
    bool = any(contains(f, str, 'IgnoreCase', ispc));
end