function SaveImage(fig, location, extension)

if ~contains(extension, '.')
   extension = "." + extension; %add dot
end

if strcmp(extension, ".eps")
   saveas(fig, location + extension, 'epsc'); 
else
   saveas(fig, location + extension); 
end
end