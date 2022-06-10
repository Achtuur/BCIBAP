%% returns path to script + '/Images/'
function path2images = GetPath2Images(filename)
    path2images = fileparts(which(filename)) + "\Images\"; %get path to /Images/ folder
end