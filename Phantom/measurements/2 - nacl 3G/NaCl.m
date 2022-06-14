% Constants
R = 0.06;
A = pi*R.^2;
T = 0.008;
e0 =  8.854187817*10.^(-12); % matlab constant
C0 = (A*e0)/T;

F = dataa3000mgn1000mg(:,2); %Frequency
colorshex = ["#0300a6","#fa7029","#00d999","#84f0e1","#c8c942","#a700cf","#fa7029","#ebed5c","#75ffad","#0300a6","#00d999"];

% tudelft-sea-green = (117, 255, 173)
% tudelft-dark-blue = (0, 52, 153)
% tudelft-purple = (3, 0, 166)
% tudelft-turquoise = (42, 235, 185)
% tudelft-sky-blue = (132, 240, 225)
% tudelft-lavender = (130, 190, 237)
% tudelft-orange = (250, 112, 41)
% tudelft-warm-purple = (105, 0, 250)
% tudelft-fuchsia = (167, 0, 207)

%-----conductivity
Reals = [dataa3000mgn500mg(:,3) dataa3000mgn750mg(:,3) dataa3000mgn1000mg(:,3) dataa3000mgn1250mg(:,3) dataa3000mgn1500mg(:,3) dataa3000mgn1750mg(:,3)];

conductivity_d1 = (Reals .^(-1)) * (T/A);

figure
subplot(1,2,1)
hold on
for i = 1:size(conductivity_d1,2)
   p1 = semilogy(F, conductivity_d1(:,i), '-', 'LineWidth', 1.5);  
   p1.Color = colorshex(i);
end
hold off
box on

title("Parallel plate capacitor measurements", 'interpreter',  'latex','fontsize',18);
xlabel("Frequency [Hz]", 'interpreter',  'latex','fontsize',18)
ylabel("Conductivity [S/m]", 'interpreter',  'latex','fontsize',18);

leg = legend('7','8','9', '10','11','12','interpreter',  'latex','fontsize',14,'Location','northwest');
title(leg,'Solution', 'interpreter',  'latex','fontsize',14);

%-----relative permittivitiy

Imags = [dataa3000mgn500mg(:,4) dataa3000mgn750mg(:,4) dataa3000mgn1000mg(:,4) dataa3000mgn1250mg(:,4) dataa3000mgn1500mg(:,4) dataa3000mgn1750mg(:,4)];

F_part = (F .^-1) * (1/(2*pi));

% Serie circuit way
% CS = F_part .* (Imagsd1(:,1) .^ -1);
% T1 = Reals(:,1) .* CS;
% T2 = 2*pi*(T1 .* F);
% lossfactor = tan(T2);
% permittivitytest1 = CS/(C0*(1+lossfactor .^ 2));
% permittivitytest2 = (lossfactor.*CS)/(C0*(1+lossfactor .^ 2));
% mag = sqrt(permittivitytest1.^2 + permittivitytest2.^2);

for j = 1:size(Imags,2)        
    C1 = F_part .* (Imags(:,j) .^ -1);
    permittivity(:,j) = C1 .* (T/(A*e0));
end

subplot(1,2,2)
hold on
for k = 1:size(permittivity,2)
   f1 = semilogy(F, permittivity(:,k), '-', 'LineWidth', 1.5);
   f1.Color = colorshex(k);
end
hold off
box on

leg = legend('7','8','9', '10','11','12', 'interpreter',  'latex','fontsize',14);
title(leg, 'Solution', 'interpreter',  'latex','fontsize',14);

title("Parallel plate capacitor measurements", 'interpreter',  'latex','fontsize',18);
xlabel("Frequency [Hz]", 'interpreter',  'latex','fontsize',18);
ylabel("Permittivity [F/m]", 'interpreter',  'latex','fontsize',18);
