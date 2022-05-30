function SaveImage(fig, location, extension)
%% create location folder if doesn't exist yet
%imgpath = strrep(mfilename('fullpath'), mfilename, '') + "/Images/"; %remove filename to obtain path to folder where script is run
mkdir(location);

%% save image
if ~contains(extension, '.')
   extension = "." + extension; %add dot
end

if strcmp(extension, ".eps")
   saveas(fig, location + "." + extension, 'epsc'); 
else
   saveas(fig, location + "." + extension); 
end
end