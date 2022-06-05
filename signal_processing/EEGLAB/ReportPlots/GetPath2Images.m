function path2images = GetPath2Images()
    path2images = strrep(mfilename('fullpath'), mfilename, '') + "Images\"; %get path to /Images/ folder
end